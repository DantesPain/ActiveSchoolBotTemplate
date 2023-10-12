from telebot import TeleBot

from ...config.models import ButtonsConfig

from . import (
    basic_commands,
    team_registration,
    manager_registration,
    admin_registration,
    point_registration,
    team_actions,
    manager_actions,
    admin_actions,
    unhandled,
)


def register_handlers(bot: TeleBot, buttons: ButtonsConfig):
    # TODO: register all handlers here
    basic_commands.register_handlers(bot, buttons)

    team_registration.register_handlers(bot)
    manager_registration.register_handlers(bot)
    admin_registration.register_handlers(bot)
    point_registration.register_handlers(bot)
    team_actions.register_handlers(bot)
    manager_actions.register_handlers(bot)
    admin_actions.register_handlers(bot)

    # TODO: register all other handlers before this line
    unhandled.register_handlers(bot)
