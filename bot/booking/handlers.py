from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bot.user.kbs import main_user_kb


async def cancel_logic(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await callback.answer("Сценарий бронирования отменен!")
    await callback.message.answer(
        "Вы отменили сценарий бронирования.",
        reply_markup=main_user_kb(callback.from_user.id),
    )


async def on_master_selected(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str
):
    """Обработчик выбора стола."""
    session = dialog_manager.middleware_data.get("session_without_commit")
    master_id = int(item_id)
    selected_table = await MasterDAO(session).find_one_or_none_by_id(table_id)
    dialog_manager.dialog_data["selected_table"] = selected_table
    await callback.answer(f"Выбран стол №{table_id} на {selected_table.capacity} мест")
    await dialog_manager.next()
