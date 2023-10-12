from telebot import TeleBot
from telebot.util import antiflood
from telebot.apihelper import ApiException


def send_text(bot: TeleBot, chat_id: int, text: str) -> bool:
    result = True
    # Send text to chat_id
    try:
        antiflood(bot.send_message, chat_id, text)
    except ApiException:
        result = False
    return result


# _______________________________________________________________

def check_team_name(name: str) -> bool:
    result = True
    # Check the team name, e.g. length, symbols, etc.
    return result


def check_point_name(name: str) -> bool:
    result = True
    # Check the point name, e.g. length, symbols, etc.
    return result


def get_hash(user_input: str) -> str:
    result = ""
    # Get the hash of the input
    return result


def check_admin_password(password_hash: str, user_input: str) -> bool:
    result = True
    # Get the sha_256 hash of the input and compare it with the password_hash
    return result


def check_manager_password(password_hash: str, user_input: str) -> bool:
    result = True
    # Get the sha_256 hash of the input and compare it with the password_hash
    return result


def assign_starting_point_messages(teams: dict[int, dict], points: list[str], base_message: str) -> dict[int, str]:
    """

    :param teams: Dictionary of teams: {user_id: {name: str, balance: int, chat_id: int}}
    :param points: List of point names
    :param base_message: Base message to be formatted with point name via str.format()
    :return: Dictionary of starting point messages: {chat_id: message}
    """
    result = {}
    # Assign starting points to teams
    for i, user_id in enumerate(teams):
        point_name = points[i % len(points)]
        message = base_message.format(point_name)
        result[teams[user_id]['chat_id']] = message
    return result


def broadcast_starting_points(bot: TeleBot, messages: dict[int, str]) -> dict[int, bool]:
    """

    :param bot: TeleBot instance
    :param messages: Dictionary of messages: {chat_id: message}
    :return: Dictionary of results: {chat_id: result}
    """
    result = {}
    for chat_id, message in messages.items():
        result[chat_id] = send_text(bot, chat_id, message)
    # Broadcast starting points to teams, using send_text function
    return result
