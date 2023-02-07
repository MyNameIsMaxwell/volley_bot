from aiogram.dispatcher.filters.state import State, StatesGroup


class GreetingsStates(StatesGroup):
    lets_go = State()
    training_interest = State()
    interest_yes = State()
    expensive = State()

