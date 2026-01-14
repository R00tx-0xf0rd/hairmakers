from datetime import date, timedelta, timezone

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Group,
    ScrollingGroup,
    Select,
    Calendar,
    CalendarConfig,
    Back,
    Cancel,
)
from aiogram_dialog.widgets.text import Const, Format

from bot.booking.getters import get_all_masters, get_all_services
from bot.booking.handlers import cancel_logic, on_master_selected
from bot.booking.states import BookingState


def get_master_window() -> Window:
    """Окно выбора парикмахера."""
    return Window(
        Const("Выбираем парикмахера:"),
        Format("{text_masters}"),
        Group(
            Select(
                Format("{item[name]}"),
                id="master_select",
                item_id_getter=lambda item: str(item["id"]),
                items="masters",
                on_click=on_master_selected,
            ),
            Cancel(Const("Отмена"), on_click=cancel_logic),
            width=2,
        ),
        getter=get_all_masters,
        state=BookingState.master,
    )


def get_service_window() -> Window:
    """Окно выбора услуги."""
    return Window(
        Format("{text_table}"),
        ScrollingGroup(
            Select(
                Format("Стол №{item[id]} - {item[description]}"),
                id="table_select",
                item_id_getter=lambda item: str(item["id"]),
                items="tables",
                on_click=on_table_selected,
            ),
            id="tables_scrolling",
            width=1,
            height=1,
        ),
        Group(
            Back(Const("Назад")),
            Cancel(Const("Отмена"), on_click=cancel_logic),
            width=2,
        ),
        getter=get_all_services,
        state=BookingState.service,
    )


def get_date_window() -> Window:
    """Окно выбора даты."""
    return Window(
        Const("На какой день бронируем столик?"),
        Calendar(
            id="cal",
            on_click=process_date_selected,
            config=CalendarConfig(
                firstweekday=0,
                timezone=timezone(timedelta(hours=3)),
                min_date=date.today(),
            ),
        ),
        Back(Const("Назад")),
        Cancel(Const("Отмена"), on_click=cancel_logic),
        state=BookingState.booking_date,
    )


def get_slots_window() -> Window:
    """Окно выбора слота."""
    return Window(
        Format("{text_slots}"),
        ScrollingGroup(
            Select(
                Format("{item[start_time]} до {item[end_time]}"),
                id="slotes_select",
                item_id_getter=lambda item: str(item["id"]),
                items="slots",
                on_click=process_slots_selected,
            ),
            id="slotes_scrolling",
            width=2,
            height=3,
        ),
        Back(Const("Назад")),
        Cancel(Const("Отмена"), on_click=cancel_logic),
        getter=get_all_available_slots,
        state=BookingState.booking_time,
    )


def get_confirmed_windows():
    return Window(
        Format("{confirmed_text}"),
        Group(
            Button(Const("Все верно"), id="confirm", on_click=on_confirmation),
            Back(Const("Назад")),
            Cancel(Const("Отмена"), on_click=cancel_logic),
        ),
        state=BookingState.confirmation,
        getter=get_confirmed_data,
    )
