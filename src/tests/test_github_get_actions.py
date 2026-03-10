# THIS IS BUSTICATED
from composio import ComposioToolSet, App

toolset = ComposioToolSet()
actions = toolset.get_actions(handle=App.GITHUB)

for action in actions:
    print(f"Name: {action.name}, Slug: {action.slug}")

