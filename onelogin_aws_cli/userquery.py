"""
Interactions with the user through the cli
"""
from typing import Any, Callable, List, Tuple

RolePrincipalPair = Tuple


def user_choice(question: str,
                options: List[Any],
                renderer: Callable[[Any], str] = lambda x: x,
                saved_choice: str = None):
    """
    Prompt a user with a question and a specific set of possible responses
    :param question: Specifying context for the user to select an option
    :param options: A list of options for the user to select from
    """
    if saved_choice:
        for option in options:
            if renderer(option) == saved_choice:
                return option
        print("Ignoring invalid saved choice '{}'".format(saved_choice))

    if len(options) == 1:
        return options[0]

    print(question)
    if len(options) == 0:
        raise Exception("No options found")
    option_list = []
    for i, option in enumerate(options):
        option_list.append("[{}] {}".format(i + 1, renderer(option)))
    selection = None
    while selection is None:
        print("\n".join(option_list))
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


def user_role_prompt(all_roles: List[RolePrincipalPair],
                     saved_choice: str = None) -> RolePrincipalPair:
    """
    Prompt a user with a list of AWS IAM roles to choose from. If only 1 role
    is available, return that.
    """
    return user_choice(
        "Pick a role:",
        all_roles,
        renderer=lambda role: role[0],
        saved_choice=saved_choice,
    )
