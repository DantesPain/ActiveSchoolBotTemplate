from telebot.handler_backends import State, StatesGroup

# TODO: define all your states here


class UnregisteredStates(StatesGroup):
    started = State()
    get_team_name = State()


class TeamStates(StatesGroup):
    registered = State()


class ManagerStates(StatesGroup):
    registered = State()
    choose_team = State()
    get_add_balance_amount = State()


class AdminStates(StatesGroup):
    registered = State()
