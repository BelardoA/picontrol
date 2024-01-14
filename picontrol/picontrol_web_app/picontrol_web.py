#!/usr/bin/env python3
"""This is just a simple authentication example.

Please see the `OAuth2 example at FastAPI <https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/>`_  or
use the great `Authlib package <https://docs.authlib.org/en/v0.13/client/starlette.html#using-fastapi>`_ to implement a classing real authentication system.
Here we just demonstrate the NiceGUI integration.
"""
import os
from typing import Optional
from dataclasses import dataclass

from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import Client, app, ui
from starlette.middleware.base import BaseHTTPMiddleware

from config import Config

first_config = Config()
user = first_config.user
# in reality users passwords would obviously need to be hashed
passwords = {user["username"]: user['password']}

unrestricted_page_routes = {'/login'}
selected_theme = first_config.site_settings['theme']

class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """
    @staticmethod
    async def dispatch(request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if request.url.path in Client.page_routes.values() and request.url.path not in unrestricted_page_routes:
                app.storage.user['referrer_path'] = request.url.path  # remember where the user wanted to go
                return RedirectResponse('/login')
        return await call_next(request)


app.add_middleware(AuthMiddleware)
app.add_static_files('/assets', f'{os.getcwd()}/picontrol_web_app/assets')


def logout() -> None:
    app.storage.user.update({'authenticated': False})
    ui.open('/login')


def change_user():
    def change_user_and_password() -> None:  # local function to avoid passing username and password as arguments
        conf = Config().get_config()
        if conf["user"]['username'] != username.value or conf["user"]['password'] != password.value:
            updated_config = conf.copy()
            updated_config["user"]['username'] = username.value
            updated_config["user"]['password'] = password.value
            # check what if username and/or password were changed
            first_config.save_config(updated_config)
            app.storage.user.update({'username': username.value, 'password': password.value, 'authenticated': True})
            ui.notify('User information updated.', close_button=True, color='positive')
            # reset the form
            username.value = ''
            password.value = ''

    def save_theme(color: str) -> None:
        ui.colors(primary=color)
        conf = Config().get_config()
        updated_config = conf.copy()
        updated_config["site"]['theme'] = color
        first_config.save_config(updated_config)
        ui.notify('Theme updated.', close_button=True, color='positive')
    with ui.row().classes('border-b-2 p-4 w-full'):
        with ui.card().classes('w-full'):
            ui.label('Change user information').classes('text-xl')
            ui.separator()
            username = ui.input('Username').on('keydown.enter', change_user_and_password)
            password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', change_user_and_password)
            ui.button('Save', on_click=change_user_and_password).classes('mt-4 ml-auto')
        with ui.card().classes('w-full'):
            ui.label('Theme').classes('text-xl')
            ui.separator()
            ui.button('Default', on_click=lambda: ui.colors()).tooltip('Default theme (Blue)')
            ui.button('Orange', on_click=lambda: save_theme('#ff4500')).tooltip('Set theme to orange')
            ui.button('Gray', on_click=lambda: save_theme('#555')).tooltip('Set theme to gray')
            ui.button('Red', on_click=lambda: save_theme('#f00')).tooltip('Set theme to red')
            ui.button('Green', on_click=lambda: save_theme('#3bb143')).tooltip('Set theme to green')
            ui.button('Yellow', on_click=lambda: save_theme('#ffbf00')).tooltip('Set theme to yellow')
            ui.button('Purple', on_click=lambda: save_theme('#f0f')).tooltip('Set theme to purple')
            ui.button('Brown', on_click=lambda: save_theme('#960')).tooltip('Set theme to brown')
            ui.button('Pink', on_click=lambda: save_theme('#FFC0CB')).tooltip('Set theme to pink')


def restart_pi() -> None:
    from asyncio import sleep
    ui.notify('Restarting Pi...', color='warning')
    sleep(1)
    # os.system("sudo reboot")


def shutdown_pi() -> None:
    from asyncio import sleep
    ui.notify('Shutting down Pi...', color='red')
    sleep(2)
    # os.system("sudo shutdown -h now")



@ui.page('/')
def main() -> None:
    config = Config()
    color = config.site_settings['theme']

    def toggle_dark_mode():
        # update the config file
        conf = Config().get_config()
        updated_config = conf.copy()
        updated_config["site"]['dark_mode'] = dark.value
        config.save_config(updated_config)

    dark = ui.dark_mode(value=config.site_settings["dark_mode"], on_change=toggle_dark_mode)
    dark_val = '☀️' if dark.value == False else '🌕'

    ui.colors(primary=color)
    with ui.left_drawer().classes('border p-4 top-0 left-0 absolute h-full').props('width=220'):
        with ui.row():
            ui.image('/assets/img/logo.svg').classes('w-10 h-10 align-middle')
            ui.label('PiControl').classes('text-3xl align-middle')
        ui.separator()
        with ui.tabs().props('vertical inline-label').classes('mr-auto') as tabs:
            ui.tab('Dashboard', icon='img:/assets/img/dashboard.svg').classes('justify-start')
            ui.tab('Games', icon='img:/assets/img/gamepad.svg').classes('justify-start')
            ui.tab('NFC', icon='img:/assets/img/tags.svg').classes('justify-start')
            ui.tab('Settings', icon='img:/assets/img/settings.svg').classes('justify-start')
            ui.toggle(options=['☀️', '🌕'], value=dark_val, on_change=lambda: dark.toggle()).classes('justify-start')
        ui.space().classes('flex-grow')
        ui.separator()
        with ui.row():
            with ui.button(icon='sync', on_click=lambda: restart_pi()).classes('ml-6'):
                ui.tooltip('Restart PI').classes('bg-warning font-bold')
            ui.space()
            ui.space()
            with ui.button(icon='power_off', color="red", on_click=lambda: shutdown_pi()):
                ui.tooltip('Shutdown PI').classes('bg-red-500 font-bold')
    with ui.row().classes('border-b-2 p-4'):
        with ui.button(icon='img:/assets/img/user.svg').classes('border p-4 top-4 right-10 absolute').props('rounded'):
            # make the profile menu appear on the right side of the button
            with ui.menu().classes('origin-top-right right-48 mt-10 w-48 rounded-md shadow-lg py-1'):
                ui.menu_item('Profile', lambda: tabs.set_value('Profile')).classes('justify-start')
                ui.menu_item('Logout', lambda: logout()).classes('justify-start')
    with ui.column().classes('p-4'):
        with ui.tab_panels(tabs, value='Dashboard'):
            with ui.tab_panel('Dashboard').classes('w-full'):
                with ui.card().props('text-align=center'):
                    ui.label('Content of Dashboard')
            with ui.tab_panel('Games'):
                ui.label('Content of Games')
            with ui.tab_panel('NFC'):
                ui.label('Content of NFC')
            with ui.tab_panel('Settings'):
                ui.label('Content of Settings')
            with ui.tab_panel('Profile'):
                change_user()


@ui.page('/login')
def login() -> Optional[RedirectResponse]:
    def try_login() -> None:  # local function to avoid passing username and password as arguments
        if passwords.get(username.value) == password.value:
            app.storage.user.update({'username': username.value, 'authenticated': True})
            ui.open(app.storage.user.get('referrer_path', '/'))  # go back to where the user wanted to go
        else:
            ui.notify('Wrong username or password', color='negative')

    if app.storage.user.get('authenticated', False):
        return RedirectResponse('/')
    with ui.card().classes('absolute-center'):
        with ui.row():
            ui.image('/assets/img/logo.svg').classes('w-10 h-10 align-middle')
            ui.label('PiControl').classes('text-3xl align-middle')
        ui.separator()
        username = ui.input('Username').on('keydown.enter', try_login)
        password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        ui.button('Log in', on_click=try_login)


ui.run(port=5000, title="PiControl", favicon=f'{os.getcwd()}/picontrol_web_app/assets/img/logo.svg', storage_secret='picontrol')
