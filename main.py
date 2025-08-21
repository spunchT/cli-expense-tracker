from termcolor import colored
import json
import shlex  # Add this import at the top

commands = {"add", "delete", "edit", "utils", "help", "quit"}  # Added help and quit to commands

# Supported currencies
currencies = {
    "usd": "$",
    "eur": "€",
    "cad": "C$"
}
current_currency = "usd"  # Default currency

args = {
    "-n", "--name",
    "-d", "--description",
    "-p", "--price",  # Added price arguments
}

global arg_value 
entry = {"name": None, "description": None, "price": None}  # Added price field

def main():
    handle_input()


def handle_input():
    global arg_value
    arg_value = None
    user_choice = input(colored("Welcome to the Expense Tracker CLI. For assistance, type 'help'.", "blue"))
    lower_user_choice = user_choice.lower()

    # Use shlex.split to handle quoted strings
    parsed_words = shlex.split(lower_user_choice)

    if not parsed_words:
        print(colored("Error: No command entered. Please try again.", "red"))
        return

    command = parsed_words[0]
    collected_args = {}

    # Collect all arguments
    i = 1
    while i < len(parsed_words):
        if parsed_words[i] in args:
            if i + 1 < len(parsed_words):
                collected_args[parsed_words[i]] = parsed_words[i + 1]
                i += 2
            else:
                print(colored(f"Error: Missing value for argument {parsed_words[i]}.", "red"))
                return
        else:
            i += 1

    if command == "add": 
        handle_add(collected_args)
    elif command == "delete":
        handle_delete(collected_args)
    elif command == "edit":
        handle_edit(collected_args)
    elif command == "utils":
        handle_utils()
    elif command == "help":
        handle_help()
    elif command == "quit":
        print(colored("Exiting Expense Tracker. Goodbye!", "blue"))
        return
    else:
        print(colored("Error: Command not recognized. Please try again.", "red"))


def handle_help():
    print(colored("\nExpense Tracker CLI Help", "cyan"))
    print("Commands:")
    print("  add      - Add a new expense entry.")
    print("            Usage: add -n \"Name\" -p Price [-d \"Description\"]")
    print("  delete   - Delete an entry by name.")
    print("            Usage: delete -n \"Name\"")
    print("  edit     - Edit an entry's name or price.")
    print("            Usage: edit -n \"Current Name\" [--new-name \"New Name\"] [-p NewPrice]")
    print("  utils    - Access settings such as currency change.")
    print("            Usage: utils")
    print("  help     - Show this help message.")
    print("            Usage: help")
    print("  quit     - Exit the application.")
    print("\nNotes:")
    print("  - Use quotes for names or descriptions with spaces, e.g. \"Lunch at cafe\".")
    print("  - Supported currencies: USD ($), EUR (€), CAD (C$).")
    print("  - Price must be a valid number.")
    print("  - Duplicate entries (same name and price) are not allowed.")
    print("  - All data is stored in 'data.json' in the current directory.\n")


def handle_utils():
    global current_currency
    print(colored("Settings Menu:", "cyan"))
    print("1. Change currency")
    choice = input("Select an option by number: ").strip()
    if choice == "1":
        print("Supported currencies:")
        for code in currencies:
            print(f"- {code.upper()} ({currencies[code]})")
        new_currency = input("Enter currency code (usd, eur, cad): ").lower().strip()
        if new_currency in currencies:
            current_currency = new_currency
            print(colored(f"Currency successfully changed to {new_currency.upper()} ({currencies[new_currency]}).", "green"))
        else:
            print(colored("Error: Invalid currency code entered.", "red"))


def handle_add(collected_args): 
    global entry, current_currency

    price_provided = False  # Track if price is given

    # Update entry with all provided flags
    for passed_arg, passed_value in collected_args.items():  
        match passed_arg:
            case "-n" | "--name":
                entry["name"] = passed_value
                print(f"Name set to: {passed_value}")
            case "-d" | "--description":
                entry["description"] = passed_value
                print(f"Description set to: {passed_value}")
            case "-p" | "--price":
                try:
                    entry["price"] = float(passed_value)
                    price_provided = True
                    print(f"Price set to: {passed_value} {currencies[current_currency]}")
                except ValueError:
                    print(colored(f"Error: '{passed_value}' is not a valid price.", "red"))
                    return

    # Require both name and price
    if entry["name"] is None:
        print(colored("Error: Name is required to add an entry.", "red"))
        return
    if not price_provided:
        print(colored("Error: Price is required to add an entry.", "red"))
        return

    # save entry to json
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = []

    # Prevent duplicate entries (same name and price)
    for existing in data:
        if existing.get("name") == entry["name"] and existing.get("price") == entry["price"]:
            print(colored("Error: Duplicate entry detected. Entry was not added.", "red"))
            entry["name"] = None
            entry["description"] = None
            entry["price"] = None
            return

    data.append(entry)

    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

    print(colored("Entry successfully added.", "green"))

    # Reset entry for next command
    entry["name"] = None
    entry["description"] = None
    entry["price"] = None


def handle_delete(collected_args):
    # Collect the name argument
    name_to_delete = None
    for passed_arg, passed_value in collected_args.items():
        match passed_arg:
            case "-n" | "--name":
                name_to_delete = passed_value
                print(f"Target entry for deletion: {passed_value}")

    if not name_to_delete:
        print(colored("Error: Please specify the entry name to delete using -n or --name.", "red"))
        return

    # Load data from JSON
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print(colored("Error: No data found to delete.", "red"))
        return

    # Delete entry by name
    original_len = len(data)
    data = [entry for entry in data if entry.get("name") != name_to_delete]

    if len(data) == original_len:
        print(colored(f"Error: No entry found with the name '{name_to_delete}'.", "red"))
    else:
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)
        print(colored(f"Entry '{name_to_delete}' has been deleted.", "green"))


def handle_edit(collected_args):
    name_to_edit = None
    new_name = None
    new_price = None

    # Parse arguments
    for passed_arg, passed_value in collected_args.items():
        match passed_arg:
            case "-n" | "--name":
                name_to_edit = passed_value
                print(f"Editing entry with name: {passed_value}")
            case "--new-name":
                new_name = passed_value
                print(f"New name will be: {passed_value}")
            case "-p" | "--price":
                try:
                    new_price = float(passed_value)
                    print(f"New price will be: {passed_value}")
                except ValueError:
                    print(colored(f"Error: '{passed_value}' is not a valid price.", "red"))
                    return

    if not name_to_edit:
        print(colored("Error: Please specify the entry name to edit using -n or --name.", "red"))
        return

    # Load data from JSON
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print(colored("Error: No data found to edit.", "red"))
        return

    # Find and edit entry
    found = False
    for entry in data:
        if entry.get("name") == name_to_edit:
            found = True
            if new_name:
                entry["name"] = new_name
            if new_price is not None:
                entry["price"] = new_price
            print(colored(f"Entry '{name_to_edit}' has been updated.", "green"))
            break

    if not found:
        print(colored(f"Error: No entry found with the name '{name_to_edit}'.", "red"))
        return

    # Save updated data
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    main()
