#!/usr/bin/python3
"""Custom class to allow for dynamic header labels in PiControl web app."""
from nicegui import ui


class DynamicLabel(ui.label):
    """
    This class is a subclass of NiceGUI's label class. It is used to display the header of the page.

    :param ui.label: The label class from NiceGUI.
    """

    def _handle_text_change(self, text: str) -> None:
        """
        This function is used to change the text of the header label.

        :param str text: The text to be displayed in the header label.
        :return: None
        """
        super()._handle_text_change(text)


class SliderValue(ui.slider):
    """
    This class is a subclass of NiceGUI's label class. It is used to display the header of the page.

    :param ui.label: The label class from NiceGUI.
    """

    def _handle_value_change(self, value: int) -> None:
        """
        This function is used to change the text of the header label.

        :param str text: The text to be displayed in the header label.
        :return: None
        """
        super()._handle_value_change(value)
