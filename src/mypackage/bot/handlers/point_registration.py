from logging import Logger

from telebot import TeleBot
from telebot.types import Message

from ...config.models import MessagesConfig
from ...business_logic import check_point_name

from ..states import AdminStates


def point_reg_handler(
        message: Message,
        bot: TeleBot,
        messages: MessagesConfig,
        logger: Logger,
        **kwargs):
    logger.debug(f"User {message.from_user.id} @{message.from_user.username} started point registration")
    if ' ' not in message.text:
        bot.send_message(message.chat.id, messages.invalid_point_name)
        return
    point_name = message.text.split(' ', maxsplit=1)[1]
    with bot.retrieve_data(bot.user.id) as data:
        points = data.get('points', [])
    if point_name not in points and check_point_name(point_name):
        points.append(point_name)
        bot.add_data(bot.user.id, points=points)
        logger.debug(f"User {message.from_user.id} @{message.from_user.username} registered point {point_name}")
        bot.send_message(message.chat.id, messages.point_registered)
    else:
        bot.send_message(message.chat.id, messages.invalid_point_name)


def register_handlers(bot: TeleBot):
    bot.register_message_handler(
        point_reg_handler,
        commands=['point_reg'],
        state=AdminStates().state_list,
        pass_bot=True
    )
