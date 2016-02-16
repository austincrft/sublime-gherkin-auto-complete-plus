import sublime
import sublime_plugin

from ..gherkin_event_listener import steps as catalogued_steps
from ..utilities import log_utilities, settings

_logging_level = settings.get_logging_level()
_logger = log_utilities.get_logger(__name__, _logging_level)


class ListGherkinStepsCommand(sublime_plugin.WindowCommand):
    steps = []

    @log_utilities.log_function(_logging_level)
    def run(self):
        """ Method that is executed when the command is called """
        self.steps = self.get_steps(catalogued_steps)
        self.show_quick_panel(self.steps)

    @log_utilities.log_function(_logging_level)
    def get_steps(self, catalogued_steps):
        """ Formats steps and sorts them alphabetically """
        steps = []
        for step in sorted(catalogued_steps):
            formatted_step = step[0].capitalize() + ' ' + step[1]
            steps.append(formatted_step)
        return steps

    @log_utilities.log_function(_logging_level)
    def on_done(self, index):
        """ Method executed when a quick-panel item is selected """
        _logger.debug('index: {}'.format(index))
        if index == -1:
            _logger.debug('Nothing selected from quick panel')
            return

        target_step = self.steps[index]
        _logger.debug('target step: {}'.format(target_step))

        mapping = {"characters": target_step}
        view = self.window.active_view()
        view.run_command("insert", mapping)

    @log_utilities.log_function(_logging_level)
    def show_quick_panel(self, steps):
        """ Displays quick-panel with the given steps
        :param [str] steps: List of steps to be displayed
        """
        self.window.show_quick_panel(steps, self.on_done)
