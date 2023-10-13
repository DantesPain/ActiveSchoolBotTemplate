from logging import Logger

from telebot import TeleBot
from telebot.types import Message

from ...config.models import MessagesConfig, ButtonsConfig

from .. import keyboards
from ..states import UnregisteredStates


# Basic commands

# 1. start - send a welcome message with help reply keyboard
# 2. help - send a help message


def start_handler(
        message: Message,
        bot: TeleBot,
        messages: MessagesConfig,
        buttons: ButtonsConfig,
        logger: Logger,
        **kwargs):
    logger.debug(f"User {message.from_user.id} @{message.from_user.username} started the bot")
    bot.set_state(message.from_user.id, UnregisteredStates.started, message.chat.id)
    bot.send_message(message.chat.id, messages.welcome, reply_markup=keyboards.help_reply_keyboard(buttons.help))


def help_handler(
        message: Message,
        bot: TeleBot,
        messages: MessagesConfig,
        logger: Logger,
        **kwargs):
    logger.debug(f"User {message.from_user.id} @{message.from_user.username} requested help")
    bot.send_message(message.chat.id, messages.help)


def reset_handler(
        message: Message,
        bot: TeleBot,
        messages: MessagesConfig,
        logger: Logger,
        **kwargs):
    logger.debug(f"User {message.from_user.id} @{message.from_user.username} requested reset")
    bot.set_state(message.from_user.id, UnregisteredStates.started, message.chat.id)
    with bot.retrieve_data(bot.user.id) as data:
        teams = data.get('teams', {})
        managers = data.get('managers', [])
        admins = data.get('admins', [])
    if str(message.from_user.id) in teams:
        teams.pop(str(message.from_user.id))
        bot.add_data(bot.user.id, teams=teams)
        bot.send_message(message.chat.id, "Team deleted")
    elif message.from_user.id in managers:
        managers.remove(message.from_user.id)
        bot.add_data(bot.user.id, managers=managers)
        bot.send_message(message.chat.id, "Manager deleted")
    elif message.from_user.id in admins:
        admins.remove(message.from_user.id)
        bot.add_data(bot.user.id, admins=admins)
        bot.send_message(message.chat.id, "Admin deleted")
    else:
        bot.send_message(message.chat.id, "Reset with no actions")


def register_handlers(bot: TeleBot, buttons: ButtonsConfig):
    bot.register_message_handler(start_handler, commands=['start'], state=[None], pass_bot=True)

    bot.register_message_handler(help_handler, commands=['help'], pass_bot=True)
    bot.register_message_handler(help_handler, text_equals=buttons.help, pass_bot=True)

    bot.register_message_handler(reset_handler, commands=['reset'], pass_bot=True)
