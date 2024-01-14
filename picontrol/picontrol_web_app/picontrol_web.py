#!/usr/bin/env python3
"""This is just a simple authentication example.

Please see the `OAuth2 example at FastAPI <https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/>`_  or
use the great `Authlib package <https://docs.authlib.org/en/v0.13/client/starlette.html#using-fastapi>`_ to implement a classing real authentication system.
Here we just demonstrate the NiceGUI integration.
"""
import os
from typing import Optional
from router import Router

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from nicegui import Client, app, ui
from config import Config

config = Config()
user = config.user
# in reality users passwords would obviously need to be hashed
passwords = {user["username"]: user['password']}

unrestricted_page_routes = {'/login'}


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

@ui.page('/')
def main() -> None:
    router = Router()

    @router.add('/')
    def dashboard():
        ui.label('Dashboard').classes('text-2xl')

    @router.add('/dashboard')
    def dashboard():
        ui.label('Dashboard').classes('text-2xl')

    @router.add('/games')
    def games():
        ui.label('Games').classes('text-2xl')

    @router.add('/nfc')
    def nfc():
        ui.label('NFC').classes('text-2xl')

    @router.add('/settings')
    def settings():
        ui.label('Settings').classes('text-2xl')

    @router.add('/profile')
    def profile():
        def change_password() -> None:  # local function to avoid passing username and password as arguments
            if passwords.get(username.value) == password.value:
                app.storage.user.update({'username': username.value, 'password': password.value, 'authenticated': True})
                conf = config.config
                ui.open(app.storage.user.get('referrer_path', '/'))  # go back to where the user wanted to go
            else:
                ui.notify('Wrong username or password', color='negative')
        ui.label('Profile').classes('text-2xl')
        with ui.card():
            username = ui.input(app.storage.user.get('username', '')).on('keydown.enter', change_password)
            password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', change_password)
            ui.button('Save', on_click=change_password).classes('mt-4 ml-auto')

    # adding some navigation buttons to switch between the different pages
    with ui.header().classes('flex justify-between w-full p-4'):
        with ui.card().tight().classes('auto flex'):
            ui.image('/assets/img/logo.svg').classes('w-10 h-10')
            with ui.card_section():
                ui.label('PiControl').classes('font-bold center').props('text-align=center')
        ui.button('Dashboard', on_click=lambda: router.open(dashboard)).classes('auto').props('icon=img:/assets/img/dashboard.svg')
        ui.button('Games', on_click=lambda: router.open(games)).classes('auto').props('icon=img:/assets/img/gamepad.svg')
        ui.button('NFC', on_click=lambda: router.open(nfc)).classes('w-32').props('icon=img:/assets/img/tags.svg')
        ui.button('Settings', on_click=lambda: router.open(settings)).classes('auto').props('icon=img:/assets/img/settings.svg')
        ui.button('Profile', on_click=lambda: router.open(profile)).classes('auto').props('icon=img:/assets/img/user.svg')
        ui.button('Logout', on_click=lambda: app.storage.user.update({'authenticated': False})).classes('w-32 ml-auto')

    # this places the content which should be displayed
    router.frame().classes('w-full p-4 bg-gray-100')


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
        username = ui.input('Username').on('keydown.enter', try_login)
        password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        ui.button('Log in', on_click=try_login)


ui.run(title="PiControl", favicon=f'{os.getcwd()}/picontrol_web_app/assets/img/logo.svg', storage_secret='picontrol')
