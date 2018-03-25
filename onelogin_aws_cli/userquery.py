"""
Interactions with the user through the cli
"""
from typing import List, Tuple

RolePrincipalPair = Tuple


def user_choice(question: str, options: List[str]) -> str:
    """
    Prompt a user with a question and a specific set of possible responses
    :param question: Specifying context for the user to select an option
    :param options: A list of options for the user to select from
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


def user_role_prompt(all_roles: List[RolePrincipalPair]) -> RolePrincipalPair:
    """
    Prompt a user with a list of AWS IAM roles to choose from. If only 1 role
    is available, return that.
    """
    selected_role = None

    if len(all_roles) > 1:
        ind = 0
        for role, principal in all_roles:
            print("[{}] {}".format(ind + 1, role))
            ind += 1
        while selected_role is None:
            choice = int(input("Role Number: ")) - 1
            if choice in range(len(all_roles)):
                selected_role = choice
            else:
                print("Invalid role index, please try again")
    else:
        selected_role = 0

    return all_roles[selected_role]
