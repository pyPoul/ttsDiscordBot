from dotenv import load_dotenv
from os import getenv


load_dotenv()


AUTH_USERS: list[int] = [
    # authorized users (by discord id)
]

BOT_TOKEN: str = getenv('BOT_TOKEN')
