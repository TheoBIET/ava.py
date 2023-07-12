"""Shared configuration file."""
from app.utils.get_env import get_env

SHARED = {
    "IS_DEV": get_env("IS_DEV", bool),
}
