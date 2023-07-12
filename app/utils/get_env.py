"""Module used to get environment variables."""
from os import getenv
from dotenv import load_dotenv

load_dotenv('.env')

def get_env(name, cast_as=str):
    """Get an environment variable."""
    value = getenv(name)
    if value is None:
        raise ValueError(f'Environment variable {name} is not set')

    if cast_as == bool:
        return value.lower() in ['true', '1', 'yes', 'y']

    return cast_as(value)
