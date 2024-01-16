#!/usr/bin/python3
"""Utilities for PiControl web app."""

from nicegui import ui
from .dynamic_objects import DynamicLabel, SliderValue
from .button_tables import ButtonTable


def create_confirmation(title: str, message: str, on_click: callable) -> ui.dialog:
    """
    Function to create a confirmation dialog box.

    :param str title: The title of the dialog box.
    :param str message: The message to be displayed in the dialog box.
    :param callable on_click: The function to be called when the user clicks the yes button.
    :return: Confirmation dialog box.
    :rtype: ui.dialog
    """
    with ui.dialog() as dialog, ui.card():
        ui.label(title).classes("text-xl")
        ui.separator()
        ui.label(message)
        with ui.row().classes('ml-auto'):
            ui.button("Yes", color="red", on_click=lambda: on_click(dialog))
            ui.button("No", on_click=lambda: dialog.close())
    return dialog
