from logging import Logger

from telebot import TeleBot
from telebot.types import Message

from ...config.models import MessagesConfig
from ...business_logic import check_team_name

from ..states import UnregisteredStates, TeamStates


def reg_handler(
        message: Message,
        bot: TeleBot,
        messages: MessagesConfig,
        logger: Logger,
        **kwargs):
    logger.debug(f"User {message.from_user.id} @{message.from_user.username} started the registration")
    bot.set_state(message.from_user.id, UnregisteredStates.get_team_name, message.chat.id)
    bot.send_message(message.chat.id, messages.get_teamname)


def team_name_handler(
        message: Message,
        bot: TeleBot,
        messages: MessagesConfig,
        logger: Logger,
        **kwargs):
    logger.debug(f"User {message.from_user.id} @{message.from_user.username} entered team name")
    if check_team_name(message.text):
        with bot.retrieve_data(bot.user.id) as data:
            teams = data.get('teams', {})
        if message.text in [team['name'] for team in teams.values()]:
            bot.send_message(message.chat.id, messages.teamname_taken)
            return
        teams[message.from_user.id] = {"name": message.text, "balance": 0, "chat_id": message.chat.id}
        bot.add_data(bot.user.id, teams=teams)
        bot.set_state(message.from_user.id, TeamStates.registered, message.chat.id)
        logger.debug(f"User {message.from_user.id} @{message.from_user.username} registered as team {message.text}")
        bot.send_message(message.chat.id, messages.team_registered)
    else:
        bot.send_message(message.chat.id, messages.invalid_teamname)


def register_handlers(bot: TeleBot):
    bot.register_message_handler(reg_handler, commands=['reg'], state=UnregisteredStates().state_list, pass_bot=True)

    bot.register_message_handler(team_name_handler, state=UnregisteredStates.get_team_name, pass_bot=True)
