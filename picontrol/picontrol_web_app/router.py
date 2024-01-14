"""Class to create a router for the web app."""

from typing import Callable, Dict, Union

from nicegui import background_tasks, helpers, ui


class RouterFrame(ui.element, component='router_frame.js'):
    pass


class Router:

    def __init__(self) -> None:
        self.routes: Dict[str, Callable] = {}
        self.content: ui.element = None

    def add(self, path: str) -> Callable:
        """
        Decorator to add a page to the router.

        :param str path: The path to the page.
        :return: The decorated function.
        :rtype: Callable
        """
        def decorator(func: Callable):
            self.routes[path] = func
            return func
        return decorator

    def open(self, target: Union[Callable, str]) -> None:
        """
        Open a page.

        :param Union[Callable, str] target: The page to open.
        return: None
        """
        if isinstance(target, str):
            path = target
            builder = self.routes[target]
        else:
            path = {v: k for k, v in self.routes.items()}[target]
            builder = target

        async def build() -> None:
            """
            Build the page.

            :return: None
            """
            with self.content:
                ui.run_javascript(f'''
                    if (window.location.pathname !== "{path}") {{
                        history.pushState({{page: "{path}"}}, "", "{path}");
                    }}
                ''')
                result = builder()
                if helpers.is_coroutine_function(builder):
                    await result
        self.content.clear()
        background_tasks.create(build())

    def frame(self) -> ui.element:
        """
        Create the router frame.

        :return: The router frame.
        :rtype: ui.element
        """
        self.content = RouterFrame().on('open', lambda e: self.open(e.args))
        return self.content
