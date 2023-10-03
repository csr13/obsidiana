import random
from django.conf import settings


USER_AGENTS_FILE = settings.BASE_DIR / "helpers" / "data" / "user-agents.txt"


def get_random_user_agent():
    with open(USER_AGENTS_FILE, "r") as ts:
        user_agents = ts.readlines()
        user_agent = random.choice(user_agents).strip("\n")
        ts.close()
    return user_agent


