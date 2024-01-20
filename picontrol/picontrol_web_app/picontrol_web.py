
#!/usr/bin/python3
"""Picontrol Web Application"""
import asyncio
import multiprocessing
import os
from typing import Optional

from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import Client, app, ui
from starlette.middleware.base import BaseHTTPMiddleware

from config import Config
from fan import Fan
from utils import ButtonTable, DynamicLabel, SliderValue, create_confirmation

first_config = Config()
user = first_config.user
# Create a multiprocessing.Queue
queue = multiprocessing.Queue()

# Create an instance of the Fan class, passing the queue to it
fan = Fan(queue)

passwords = {user["username"]: user["password"]}
unrestricted_page_routes = {"/login"}
selected_theme = first_config.site_settings["theme"]


class AuthMiddleware(BaseHTTPMiddleware):
    """
    This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    @staticmethod
    async def dispatch(request: Request, call_next, **kwargs):
        """
        Function to check if the user is authenticated and will redirect them to the login page.

        :param Request request: Application request for the page.
        :param call_next: The next requested page for the user.
        :return: The requested page or the login page.
        :rtype: RedirectResponse or call_next
        """
        if not app.storage.user.get("authenticated", False):
            if (
                request.url.path in Client.page_routes.values()
                and request.url.path not in unrestricted_page_routes
            ):
                app.storage.user[
                    "referrer_path"
                ] = request.url.path  # remember where the user wanted to go
                return RedirectResponse("/login")
        return await call_next(request)


app.add_middleware(AuthMiddleware)
app.add_static_files("/assets", f"{os.getcwd()}/picontrol_web_app/assets")


def logout() -> None:
    app.storage.user.update({"authenticated": False})
    ui.open("/login")


def settings_page() -> None:
    def update_fan_settings() -> None:
        """
        Function to update the fan settings in the config file.

        :return: None
        """
        conf = Config().get_config()
        updated_config = conf.copy()
        updated_config["fan"]["threshold_on"] = threshold_on.value
        updated_config["fan"]["threshold_off"] = threshold_off.value
        updated_config["fan"]["interval"] = interval.value
        first_config.save_config(updated_config)
        ui.notify("Fan settings updated.", close_button=True, color="positive")

    def update_button_settings(button_option: int) -> None:
        """
        Function to update the button settings in the config file.

        :return: None
        """
        conf = Config().get_config()
        updated_config = conf.copy()
        updated_config["button"]["option"] = button_option
        first_config.save_config(updated_config)
        button_model.update(
            current_settings=f"Button Configuration - Currently {'Classic Buttons' if button_option == 1 else 'Pi Buttons'}"
        )
        ui.notify("Button settings updated.", close_button=True, color="positive")

    button_model = {
        "current_settings": f"Button Configuration - Currently {'Classic Buttons' if Config().button_settings == 1 else 'Pi Buttons'}"
    }
    with ui.card().classes("w-full"):
        ui.label("Fan Configuration").classes("text-xl")
        ui.separator()
        ui.label("Threshold On - Celsius").classes("bold")
        threshold_on = (
            SliderValue(
                min=0, max=100, step=1, value=first_config.fan_settings["threshold_on"]
            )
            .bind_value_to(first_config.fan_settings, "threshold_on")
            .props("label-always")
        )
        ui.label("Threshold Off - Celsius").classes("bold")
        threshold_off = (
            SliderValue(
                min=0, max=50, step=1, value=first_config.fan_settings["threshold_off"]
            )
            .bind_value_to(first_config.fan_settings, "threshold_off")
            .props("label-always")
        )
        ui.label("Interval - Seconds").classes("bold")
        interval = (
            SliderValue(
                min=0, max=100, step=1, value=first_config.fan_settings["interval"]
            )
            .bind_value_to(first_config.fan_settings, "interval")
            .props("label-always")
        )
        with ui.row():
            cpu_temps = ui.label(f'CPU: {fan.cpu_temp}°C / {fan.cpu_temp * 9 / 5 + 32}°F')
            current_fan = ui.label(f"Fan: {'On' if fan.fan_on else 'Off'}")
            # Use ui.timer to periodically check the queue and update the labels

            def update_labels():
                if not queue.empty():
                    cpu_temp, fan_on, fan_interval = queue.get()
                    cpu_temps.set_text(f'CPU: {cpu_temp}°C / {cpu_temp * 9 / 5 + 32}°F')
                    current_fan.set_text(f"Fan: {'On' if fan_on is True else 'Off'}")
            # Update labels every 1 second
            ui.timer(interval=1, callback=update_labels)

            # TODO add current temp in F and C
        ui.separator()
        ui.button("Save", on_click=update_fan_settings).classes("mt-4 ml-auto")
    with ui.card().classes("w-full"):
        DynamicLabel().bind_text_from(button_model, "current_settings").classes(
            "text-xl"
        )
        ui.separator()
        classic_columns, classic_rows = ButtonTable.create_table(
            column2="PI On - Game / Es Running",
            column3="PI On - Simulated Off",
            rowVal2="Press to Exit Game / ES",
            rowVal3="Press to Load Game / ES; PI Shuts Down if idle for 30 seconds",
            rowVal4="N/A",
        )
        nes_columns, nes_rows = ButtonTable.create_table(
            column2="PI On - Game Running",
            column3="PI On - ES Running",
            rowVal2="Press to turn off Raspberry Pi",
            rowVal3="Press to turn off Raspberry Pi",
            rowVal4="Press to Start Game from NFC Tag or last Game played",
        )
        ui.table(title="Classic Buttons", columns=classic_columns, rows=classic_rows, row_key="button").classes(
            "w-full"
        )
        ui.button("Classic Buttons", on_click=lambda: update_button_settings(1))
        ui.table(title="Pi Buttons", columns=nes_columns, rows=nes_rows, row_key="button").classes("w-full border-2")
        ui.button("Pi Buttons", on_click=lambda: update_button_settings(2))


def profile_page() -> None:
    """
    Function to that creates the profile page. Allows the user to change their username
    and password as well as the theme.

    :return: None
    """

    def change_user_and_password() -> (
        None
    ):  # local function to avoid passing username and password as arguments
        """
        Nested function to change the user information in the config file and web app.

        :return: None
        """
        conf = Config().get_config()
        if (
            conf["user"]["username"] != username.value
            or conf["user"]["password"] != password.value
        ):
            updated_config = conf.copy()
            updated_config["user"]["username"] = username.value
            updated_config["user"]["password"] = password.value
            # check what if username and/or password were changed
            first_config.save_config(updated_config)
            app.storage.user.update(
                {
                    "username": username.value,
                    "password": password.value,
                    "authenticated": True,
                }
            )
            ui.notify("User information updated.", close_button=True, color="positive")
            # reset the form
            username.value = ""
            password.value = ""

    def save_theme(color: str) -> None:
        """
        Function to save the theme to the config file which is used to set the theme of the web app.

        :param str color: The hex color to use for the theme.
        :return: None
        """
        ui.colors(primary=color)
        conf = Config().get_config()
        updated_config = conf.copy()
        updated_config["site"]["theme"] = color
        first_config.save_config(updated_config)
        ui.notify("Theme updated.", close_button=True, color="positive")

    with ui.row().classes("border-b-2 p-4 w-full"):
        with ui.card().classes("w-full"):
            ui.label("Change user information").classes("text-xl")
            ui.separator()
            username = ui.input("Username").on(
                "keydown.enter", change_user_and_password
            )
            password = ui.input(
                "Password", password=True, password_toggle_button=True
            ).on("keydown.enter", change_user_and_password)
            ui.button("Save", on_click=change_user_and_password).classes("mt-4 ml-auto")
        with ui.card().classes("w-full"):
            ui.label("Theme").classes("text-xl")
            ui.separator()
            ui.button("Default", on_click=lambda: save_theme("#3bb143")).tooltip(
                "Default theme (Green)"
            )
            ui.button("Orange", on_click=lambda: save_theme("#ff4500")).tooltip(
                "Set theme to Orange"
            )
            ui.button("Gray", on_click=lambda: save_theme("#555")).tooltip(
                "Set theme to Gray"
            )
            ui.button("Red", on_click=lambda: save_theme("#f00")).tooltip(
                "Set theme to Red"
            )
            ui.button("Blue", on_click=lambda: save_theme("#5898d4")).tooltip(
                "Set theme to Blue"
            )
            ui.button("Yellow", on_click=lambda: save_theme("#ffbf00")).tooltip(
                "Set theme to Yellow"
            )
            ui.button("Purple", on_click=lambda: save_theme("#f0f")).tooltip(
                "Set theme to Purple"
            )
            ui.button("Brown", on_click=lambda: save_theme("#960")).tooltip(
                "Set theme to Brown"
            )
            ui.button("Pink", on_click=lambda: save_theme("#FFC0CB")).tooltip(
                "Set theme to Pink"
            )


def restart_pi(dialog: ui.dialog) -> None:
    """
    Function to restart the Raspberry Pi.

    :param ui.dialog dialog: The dialog box to close.
    :return: None
    """
    dialog.close()
    ui.notify("Restarting Pi...", color="warning")
    asyncio.sleep(1)
    os.system("sudo reboot")


def shutdown_pi(dialog: ui.dialog) -> None:
    """
    Function to shut down the Raspberry Pi.

    :param ui.dialog dialog: The dialog box to close.
    :return: None
    """
    dialog.close()
    ui.notify("Shutting down Pi...", color="red")
    asyncio.sleep(2)
    os.system("sudo shutdown -h now")


@ui.page("/")
def main() -> None:
    config = Config()
    color = config.site_settings["theme"]

    def save_dark_mode_settings() -> None:
        """
        Function to toggle the dark mode setting in the config file.

        :return: None
        """
        # update the config file
        conf = Config().get_config()
        updated_config = conf.copy()
        updated_config["site"]["dark_mode"] = dark.value
        config.save_config(updated_config)

    dark = ui.dark_mode(
        value=config.site_settings["dark_mode"], on_change=save_dark_mode_settings
    )
    dark_val = "☀️" if dark.value is False else "🌑"
    ui.colors(primary=color)
    with ui.left_drawer().classes("border p-4 top-0 left-0 absolute h-full").props(
        "width=220"
    ):
        with ui.row():
            ui.image("/assets/img/logo.svg").classes("w-10 h-10 align-middle")
            ui.label("PiControl").classes("text-3xl align-middle")
        ui.separator()
        with ui.tabs().props("vertical inline-label").classes("mr-auto") as tabs:
            ui.tab("Dashboard", icon="img:/assets/img/dashboard.svg").classes(
                "justify-start"
            )
            ui.tab("Games", icon="img:/assets/img/gamepad.svg").classes("justify-start")
            ui.tab("NFC", icon="img:/assets/img/tags.svg").classes("justify-start")
            ui.tab("Settings", icon="img:/assets/img/settings.svg").classes(
                "justify-start"
            )
        ui.space().classes("flex-grow")
        ui.separator()
        shutdown_confirmation = create_confirmation(
            title="Shutdown Pi",
            message="Are you sure you want to shutdown the Raspberry Pi?",
            on_click=shutdown_pi,
        )
        reboot_confirmation = create_confirmation(
            title="Restart Pi",
            message="Are you sure you want to restart the Raspberry Pi?",
            on_click=restart_pi,
        )
        with ui.row():
            with ui.button(icon="sync", on_click=lambda: reboot_confirmation.open()).classes("ml-3"):
                ui.tooltip("Restart PI").classes("bg-warning font-bold")
            ui.space()
            ui.space()
            with ui.button(
                icon="power_off", color="red", on_click=lambda: shutdown_confirmation.open()
            ).classes("mr-3"):
                ui.tooltip("Shutdown PI").classes("bg-red-500 font-bold")
    with ui.card().classes("text-xl w-full"):
        with ui.row():
            ui.label("Dashboard").bind_text_from(tabs, "value")
            ui.space()
            with ui.button(icon="img:/assets/img/user.svg").classes(
                "border p-4 top-0 right-4 absolute"
            ).props("rounded"):
                # make the profile menu appear on the right side of the button
                with ui.menu().classes(
                    "origin-top-right right-48 mt-10 w-48 rounded-md shadow-lg py-1"
                ) as menu:
                    with ui.menu_item("Mode").classes("justify-start"):
                        ui.space().classes("mr-2")
                        ui.toggle(
                            options=["☀️", "🌑"],
                            value=dark_val,
                            on_change=lambda: dark.toggle(),
                        ).classes("justify-start")
                    ui.menu_item("Profile", lambda: tabs.set_value("Profile")).classes(
                        "justify-start"
                    )
                    ui.menu_item("Logout", lambda: logout()).classes("justify-start")
                    ui.separator()
                    ui.menu_item("Close", on_click=menu.close)

    with ui.tab_panels(tabs, value="Dashboard").classes("w-full"):
        with ui.tab_panel("Dashboard").classes("w-full"):
            with ui.card().props("text-align=center"):
                ui.label("Content of Dashboard")
        with ui.tab_panel("Games"):
            ui.label("Content of Games")
        with ui.tab_panel("NFC"):
            ui.label("Content of NFC")
        with ui.tab_panel("Settings"):
            settings_page()
        with ui.tab_panel("Profile"):
            profile_page()


@ui.page("/login")
def login() -> Optional[RedirectResponse]:
    ui.colors(primary="#3bb143")

    def try_login() -> (
        None
    ):  # local function to avoid passing username and password as arguments
        if passwords.get(username.value) == password.value:
            app.storage.user.update({"username": username.value, "authenticated": True})
            ui.open(
                app.storage.user.get("referrer_path", "/")
            )  # go back to where the user wanted to go
        else:
            ui.notify("Wrong username or password", color="negative")

    if app.storage.user.get("authenticated", False):
        return RedirectResponse("/")
    with ui.card().classes("absolute-center"):
        with ui.row():
            ui.image("/assets/img/logo.svg").classes("w-10 h-10 align-middle")
            ui.label("PiControl").classes("text-3xl align-middle")
        ui.separator()
        username = ui.input("Username").on("keydown.enter", try_login)
        password = ui.input("Password", password=True, password_toggle_button=True).on(
            "keydown.enter", try_login
        )
        ui.button("Log in", on_click=try_login)


ui.run(
    port=8080,
    title="PiControl",
    favicon=f"{os.getcwd()}/picontrol_web_app/assets/img/logo.svg",
    storage_secret="picontrol",
)
