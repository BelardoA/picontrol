#!/usr/bin/python3
"""Pydantic data model that will create tables for the buttons configuration options in the web app."""
from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel


class ButtonTable(BaseModel):
    column2: Optional[str] = ""
    column3: Optional[str] = ""
    rowVal2: Optional[str] = ""
    rowVal3: Optional[str] = ""
    rowVal4: Optional[str] = ""

    @classmethod
    def create_table(cls, **data) -> Tuple[List[Dict], List[Dict]]:
        """
        Create a table for the buttons configuration options in the web app.

        :param data: Data to populate the table.
        :return: columns and rows for the table.
        :rtype: tuple[list[dict], list[dict]]
        """
        instance = cls(**data)
        columns = [
            {"name": "button", "label": "Button", "field": "button", "align": "center"},
            {"name": "pi_off", "label": "Pi Off", "field": "pi_off", "align": "left"},
            {
                "name": "on_running",
                "label": instance.column2,
                "field": "on_running",
                "align": "left",
            },
            {
                "name": "on_sleeping",
                "label": instance.column3,
                "field": "on_sleeping",
                "align": "left",
            },
        ]
        rows = [
            {
                "button": "Power Button",
                "pi_off": "Press to Turn on PI (If NFC Tag found Boot to Game else Boot to ES)",
                "on_running": instance.rowVal2,
                "on_sleeping": instance.rowVal3,
            },
            {
                "button": "Reset Button",
                "pi_off": "N/A",
                "on_running": "Press to Reset Game; Hold 3 seconds to Write Game to NFC Tag",
                "on_sleeping": instance.rowVal4,
            },
        ]
        return columns, rows
