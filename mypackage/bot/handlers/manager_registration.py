from logging import Logger

from telebot import TeleBot
from telebot.types import Message

from ...config.models import MessagesConfig
from ...business_logic import check_manager_password

from ..states import UnregisteredStates, ManagerStates


def manager_reg_handler(
        message: Message,
        bot: TeleBot,
        messages: MessagesConfig,
        logger: Logger,
        **kwargs):
    logger.debug(f"User {message.from_user.id} @{message.from_user.username} started manager registration")
    if ' ' not in message.text:
        bot.send_message(message.chat.id, messages.invalid_manager_password)
        return
    user_input = message.text.split(' ', maxsplit=1)[1]
    with bot.retrieve_data(bot.user.id) as data:
        managers = data.get('managers', [])
        password_hash = data.get('manager_password_hash', None)
    if check_manager_password(password_hash, user_input):
        managers.append(message.from_user.id)
        bot.add_data(bot.user.id, managers=managers)
        bot.set_state(message.from_user.id, ManagerStates.registered, message.chat.id)
        logger.debug(f"User {message.from_user.id} @{message.from_user.username} registered as manager")
        bot.send_message(message.chat.id, messages.manager_registered)
    else:
        bot.send_message(message.chat.id, messages.invalid_manager_password)


def register_handlers(bot: TeleBot):
    bot.register_message_handler(
        manager_reg_handler,
        commands=['manager_reg'],
        state=UnregisteredStates().state_list,
        pass_bot=True
    )
