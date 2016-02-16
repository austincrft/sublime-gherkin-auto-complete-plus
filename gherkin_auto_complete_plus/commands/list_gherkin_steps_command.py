import sublime
import sublime_plugin

from ..gherkin_event_listener import steps as catalogued_steps
from ..utilities import log_utilities, settings

_logging_level = settings.get_logging_level()
_logger = log_utilities.get_logger(__name__, _logging_level)


class ListGherkinStepsCommand(sublime_plugin.WindowCommand):
    steps_dict = {}

    @log_utilities.log_function(_logging_level)
    def run(self):
        self.steps_dict = self.get_steps_dict(catalogued_steps)
        self.show_quick_panel(sorted(self.steps_dict.values()))

    @log_utilities.log_function(_logging_level)
    def get_steps_dict(self, catalogued_steps):
        steps = {}
        for index, step in enumerate(sorted(catalogued_steps)):
            formatted_step = step[0].capitalize() + ' ' + step[1]
            steps[index] = formatted_step
        return steps

    @log_utilities.log_function(_logging_level)
    def on_done(self, index):
        if index == -1:
            _logger.debug('index -1 (nothing selected from quick panel)')
            return

        target_step = self.steps_dict[index]
        _logger.debug('target step: {}'.format(target_step))

        mapping = {"characters": target_step}
        view = self.window.active_view()
        view.run_command("insert", mapping)

    @log_utilities.log_function(_logging_level)
    def show_quick_panel(self, steps):
        self.window.show_quick_panel(steps, self.on_done)
