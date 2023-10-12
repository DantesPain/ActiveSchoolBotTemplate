from logging import Logger

from telebot import TeleBot
from telebot.types import Message

from ...config.models import MessagesConfig
from ...business_logic import get_hash, assign_starting_point_messages, broadcast_starting_points

from ..states import AdminStates


def rating_handler(
        message: Message,
        bot: TeleBot,
        messages: MessagesConfig,
        logger: Logger,
        **kwargs):
    logger.debug(f"User {message.from_user.id} @{message.from_user.username} added balance")
    with bot.retrieve_data(bot.user.id) as data:
        teams = data.get('teams', {})
    teams_sorted = sorted(teams.values(), key=lambda x: x['balance'], reverse=True)
    rating = "\n".join(f"{team['name']}: {team['balance']}" for team in teams_sorted)
    bot.send_message(message.chat.id, messages.rating.format(rating))


def begin_handler(
        message: Message,
        bot: TeleBot,
        messages: MessagesConfig,
        logger: Logger,
        **kwargs):
    logger.debug(f"User {message.from_user.id} @{message.from_user.username} tried to begin the game")
    with bot.retrieve_data(bot.user.id) as data:
        teams = data.get('teams', {})
        points = data.get('points', {})
    if len(teams) < 2:
        bot.send_message(message.chat.id, messages.not_enough_teams)
    elif len(points) < 1:
        bot.send_message(message.chat.id, messages.not_enough_points)
    else:
        starting_point_messages = assign_starting_point_messages(teams, points, messages.starting_point)
        last_result = {}
        for i in range(3):
            last_result = broadcast_starting_points(bot, starting_point_messages)
            if all(last_result.values()):
                break
        if not all(last_result.values()):
            failures = "\n".join(team['name'] for team in teams.values() if not last_result[team['chat_id']])
            bot.send_message(message.chat.id, messages.broadcast_failures.format(failures))
        else:
            bot.send_message(message.chat.id, messages.broadcast_success)
        logger.debug(f"User {message.from_user.id} @{message.from_user.username} began the game")
        bot.send_message(message.chat.id, messages.game_started)


def set_manager_password_handler(
        message: Message,
        bot: TeleBot,
        messages: MessagesConfig,
        logger: Logger,
        **kwargs):
    logger.debug(f"User {message.from_user.id} @{message.from_user.username} set manager password")
    if ' ' not in message.text:
        bot.send_message(message.chat.id, messages.invalid_manager_password)
        return
    user_input = message.text.split(' ', maxsplit=1)[1]
    bot.add_data(bot.user.id, manager_password_hash=get_hash(user_input))
    bot.send_message(message.chat.id, messages.manager_password_set)


def set_admin_password_handler(
        message: Message,
        bot: TeleBot,
        messages: MessagesConfig,
        logger: Logger,
        **kwargs):
    logger.debug(f"User {message.from_user.id} @{message.from_user.username} set admin password")
    if ' ' not in message.text:
        bot.send_message(message.chat.id, messages.invalid_admin_password)
        return
    user_input = message.text.split(' ', maxsplit=1)[1]
    bot.add_data(bot.user.id, admin_password_hash=get_hash(user_input))
    bot.send_message(message.chat.id, messages.admin_password_set)


def register_handlers(bot: TeleBot):
    bot.register_message_handler(rating_handler, commands=['rating'], state=AdminStates().state_list, pass_bot=True)
    bot.register_message_handler(begin_handler, commands=['begin'], state=AdminStates().state_list, pass_bot=True)
    bot.register_message_handler(
        set_manager_password_handler,
        commands=['set_manager_password'],
        state=AdminStates().state_list,
        pass_bot=True
    )
    bot.register_message_handler(
        set_admin_password_handler,
        commands=['set_admin_password'],
        state=AdminStates().state_list,
        pass_bot=True
    )
