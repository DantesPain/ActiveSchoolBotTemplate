from logging import Logger

from telebot import TeleBot
from telebot.types import Message

from ...config.models import MessagesConfig
from ...business_logic import check_admin_password

from ..states import UnregisteredStates, AdminStates


def admin_reg_handler(
        message: Message,
        bot: TeleBot,
        messages: MessagesConfig,
        logger: Logger,
        **kwargs):
    logger.debug(f"User {message.from_user.id} @{message.from_user.username} started admin registration")
    if ' ' not in message.text:
        bot.send_message(message.chat.id, messages.invalid_admin_password)
        return
    user_input = message.text.split(' ', maxsplit=1)[1]
    with bot.retrieve_data(bot.user.id) as data:
        admins = data.get('admins', [])
        password_hash = data.get('admin_password_hash', None)
    if check_admin_password(password_hash, user_input):
        admins.append(message.from_user.id)
        bot.add_data(bot.user.id, admins=admins)
        bot.set_state(message.from_user.id, AdminStates.registered, message.chat.id)
        logger.debug(f"User {message.from_user.id} @{message.from_user.username} registered as admin")
        bot.send_message(message.chat.id, messages.admin_registered)
    else:
        bot.send_message(message.chat.id, messages.invalid_admin_password)


def register_handlers(bot: TeleBot):
    bot.register_message_handler(
        admin_reg_handler,
        commands=['admin_reg'],
        state=UnregisteredStates().state_list,
        pass_bot=True
    )
