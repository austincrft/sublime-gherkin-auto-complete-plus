import logging

import sublime
import sublime_plugin

from .gherkin_event_listener import steps as catalogued_steps
from .log_utilities import log_func
from .settings import get_logging_level

logging_level = get_logging_level()


class ListGherkinStepsCommand(sublime_plugin.WindowCommand):
    steps_dict = {}

    @log_func(logging_level)
    def run(self):
        self.steps_dict = self.get_steps_dict(catalogued_steps)
        self.show_quick_panel(sorted(self.steps_dict.values()))

    @log_func(logging_level)
    def get_steps_dict(self, catalogued_steps):
        steps = {}
        for index, step in enumerate(sorted(catalogued_steps)):
            formatted_step = step[0].capitalize() + ' ' + step[1]
            steps[index] = formatted_step
        return steps

    @log_func(logging_level)
    def on_done(self, index):
        if index == -1:
            return
        target_step = self.steps_dict[index]
        view = self.window.active_view()
        mapping = {"characters": target_step}
        view.run_command("insert", mapping)

    @log_func(logging_level)
    def show_quick_panel(self, steps):
        self.window.show_quick_panel(steps, self.on_done)
