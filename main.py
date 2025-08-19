from termcolor import colored


flags = {
    "-n", "--name"
    "-t", "--tag"
}


def main():
   handle_input()


def handle_input():
    user_choice = input("Type 'help' for a list of all the commands. ")
    lower_user_choice = user_choice.lower()

    if lower_user_choice == "help":
        print("commands")
    elif lower_user_choice.startswith("add"):
        print("add")
            


if __name__ == "__main__":
    main()