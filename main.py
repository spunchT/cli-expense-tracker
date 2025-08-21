from termcolor import colored

commands = {"add", "delete", "update"}

args = {
    "-n", "--name",
    "-d", "--description",
}

global arg_value 

def main():
    handle_input()


def handle_input():

    # input variables
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
            
    

    # find arguments and their values
    for i in range(len(parsed_words)):
        command = parsed_words[0]  # first word is the command
        current_word = parsed_words[i]  # current word being checked
        next_word = parsed_words[i + 1] if i + 1 < len(parsed_words) else None  # look ahead safely

        if current_word in args:  # if it's a valid argument
            if next_word not in args and next_word:  # make sure the next word isnt another flag
                arg_value = next_word
                function_to_call = f"handle_{command}"  # build function name
                print(function_to_call)
                if function_to_call in globals():  # if fucntion name exists
                
                    globals()[function_to_call](current_word, arg_value)  # call function
                    
                
                else:
                    print("No function found for command:", command)

            else:  # no value provided
                print(colored(f"Value for {current_word} is missing!", "red"))
                return
        
        elif current_word in commands and not next_word.startswith("-"):                               
            print(colored("No Argument Found For " + current_word, "red"))
            break
        
 
def handle_add(passed_arg, passed_value):
    # Check And Add All Flags And Values
    match passed_arg:
        case "-n" | "--name":
            print(f"{passed_arg} Added With Value {passed_value}")
        case "-d" | "--description":
            print(f"{passed_arg} Added With Value {passed_value}")


def handle_help():
    print("Available commands: add, delete, edit, quit")

if __name__ == "__main__":
    main()