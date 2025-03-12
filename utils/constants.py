from dotenv import load_dotenv
from os import getenv


load_dotenv()


AUTH_USERS: list[int] = [
    # authorized users (by discord id)
    307528338744803328,
]

BOT_TOKEN: str = getenv('BOT_TOKEN')
