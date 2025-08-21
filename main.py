from termcolor import colored
import json

commands = {"add", "delete", "update"}

args = {
    "-n", "--name",
    "-d", "--description",
}

global arg_value 
entry = {"name": None, "description": None}  

def main():
    handle_input()


def handle_input():

    global arg_value
    arg_value = None
    user_choice = input("Type 'help' for a list of all the commands. ")
    lower_user_choice = user_choice.lower()
    parsed_words = lower_user_choice.split()

    if lower_user_choice == "quit":
        raise SystemExit(0)

    if parsed_words[0] not in commands:
        print(colored("Error: Please Start With An Appropriate Command, Type 'Help' For All The Commands", "red"))
        return

    command = parsed_words[0]
    collected_args = {}  

    # 1️⃣ Collect all arguments
    for i in range(1, len(parsed_words)):
        current_word = parsed_words[i]
        next_word = parsed_words[i + 1] if i + 1 < len(parsed_words) else None

        if current_word in args and next_word and next_word not in args:
            collected_args[current_word] = next_word
        elif current_word in args and (not next_word or next_word in args):
            print(colored(f"Value for {current_word} is missing!", "red"))
            return

    if command == "add": 
        handle_add(collected_args)


def handle_add(collected_args): 
    global entry

    # Update entry with all provided flags
    for passed_arg, passed_value in collected_args.items():  
        match passed_arg:
            case "-n" | "--name":
                entry["name"] = passed_value
                print(f"{passed_arg} Added With Value {passed_value}")
            case "-d" | "--description":
                entry["description"] = passed_value
                print(f"{passed_arg} Added With Value {passed_value}")

    # save entry to json
    if entry["name"] is not None:  # check required field exists
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = []

        data.append(entry)

        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)

        # Reset entry for next command
        entry["name"] = None
        entry["description"] = None


def handle_help():
    print("Available commands: add, delete, edit, quit")


if __name__ == "__main__":
    main()
