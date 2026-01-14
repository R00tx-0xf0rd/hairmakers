from aiogram_dialog import Dialog

booking_dialog = Dialog(
    get_capacity_window(),
    get_table_window(),
    get_date_window(),
    get_slots_window(),
    get_confirmed_windows(),
)
