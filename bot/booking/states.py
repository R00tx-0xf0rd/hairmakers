from aiogram.fsm.state import State, StatesGroup


class BookingState(StatesGroup):
    master = State()
    service = State()
    booking_date = State()
    booking_time = State()
    confirmation = State()
    success = State()
