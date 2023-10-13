from logging import Logger

from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from ...config.models import MessagesConfig

from ..keyboards import teams_inline, empty_inline
from ..states import ManagerStates
from ..utils import dummy_true


def add_balance_handler(
        message: Message,
        bot: TeleBot,
        messages: MessagesConfig,
        logger: Logger,
        **kwargs):
    logger.debug(f"User {message.from_user.id} @{message.from_user.username} tried to add balance")
    with bot.retrieve_data(bot.user.id) as data:
        teams = data.get('teams', {})
    keyboard = teams_inline(teams)
    bot.set_state(message.from_user.id, ManagerStates.choose_team, message.chat.id)
    bot.send_message(message.chat.id, messages.choose_team, reply_markup=keyboard)


def choose_team_handler(
        call: CallbackQuery,
        bot: TeleBot,
        messages: MessagesConfig,
        logger: Logger,
        **kwargs):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=empty_inline())
    logger.debug(f"User {call.from_user.id} @{call.from_user.username} chose team {call.data}")
    bot.add_data(call.from_user.id, call.message.chat.id, team_tg_user_id=call.data)
    bot.set_state(call.from_user.id, ManagerStates.get_add_balance_amount, call.message.chat.id)
    bot.send_message(call.message.chat.id, messages.get_add_balance_amount)


def add_balance_amount_handler(
        message: Message,
        bot: TeleBot,
        messages: MessagesConfig,
        logger: Logger,
        **kwargs):
    logger.debug(f"User {message.from_user.id} @{message.from_user.username} "
                 f"tried to add balance amount {message.text}")
    with bot.retrieve_data(bot.user.id) as data:
        teams = data.get('teams', {})
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        team_tg_user_id = data.get('team_tg_user_id')
    teams[team_tg_user_id]['balance'] += int(message.text)
    bot.add_data(bot.user.id, teams=teams)
    bot.set_state(message.from_user.id, ManagerStates.registered, message.chat.id)
    logger.debug(f"User {message.from_user.id} @{message.from_user.username} "
                 f"added balance {message.text} to team {teams[team_tg_user_id]['name']}")
    bot.send_message(message.chat.id, messages.balance_added)


def register_handlers(bot: TeleBot):
    bot.register_message_handler(
        add_balance_handler,
        commands=['add_balance'],
        state=ManagerStates().state_list,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        choose_team_handler,
        func=dummy_true,
        state=ManagerStates.choose_team,
        pass_bot=True
    )
    bot.register_message_handler(
        add_balance_amount_handler,
        is_digit=True,
        state=ManagerStates.get_add_balance_amount,
        pass_bot=True
    )
