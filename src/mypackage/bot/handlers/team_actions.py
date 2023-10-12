from logging import Logger

from telebot import TeleBot
from telebot.types import Message

from ...config.models import MessagesConfig

from ..states import TeamStates


def get_balance_handler(
        message: Message,
        bot: TeleBot,
        messages: MessagesConfig,
        logger: Logger,
        **kwargs):
    logger.debug(f"User {message.from_user.id} @{message.from_user.username} requested balance")
    with bot.retrieve_data(bot.user.id) as data:
        teams = data.get('teams', {})
    team = teams.get(message.from_user.id)
    if team:
        bot.send_message(message.chat.id, messages.team_balance.format(team['balance']))


def register_handlers(bot: TeleBot):
    bot.register_message_handler(
        get_balance_handler,
        commands=['get_balance'],
        state=TeamStates().state_list,
        pass_bot=True
    )
