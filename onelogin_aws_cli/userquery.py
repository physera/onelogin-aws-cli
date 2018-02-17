import typing


def user_choice(question: str, options: typing.List[str]) -> str:
    """
    Prompt a user with a question and a specific set of possible responses
    :param question: Specifying context for the user to select an option
    :param options: A list of options for the user to select from
    :return:
    """
    print(question + "\n")
    option_list = ""
    for i, option in enumerate(options):
        option_list += ("{}. {}\n".format(i + 1, option))
    selection = None
    while selection is None:
        print(option_list)
        choice = input("? ")
        try:
            val = int(choice) - 1
            if val in range(0, len(options)):
                selection = options[val]
            else:
                print("Invalid option")
        except ValueError:
            print("Invalid option")
    return selection
