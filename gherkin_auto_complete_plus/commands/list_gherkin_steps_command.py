import sublime
import sublime_plugin

from ..gherkin_event_listener import steps as catalogued_steps
from ..utilities.log_utilities import log_function, get_logger
from ..utilities import log_utilities, settings


class ListGherkinStepsCommand(sublime_plugin.WindowCommand):
    steps = []

    def run(self):
        """ Method that is executed when the command is called """
        # Set up logging -- must be done here because setting file isn't
        # properly loaded at __init__ time
        self._logging_level = settings.get_logging_level()
        self._logger = get_logger(__name__, self._logging_level)

        # Decorate functions before calling
        self.get_steps = log_function(self._logging_level)(self.get_steps)
        self.on_done = log_function(self._logging_level)(self.on_done)
        self.show_quick_panel = log_function(self._logging_level)(self.show_quick_panel)

        # Call methods
        self.steps = self.get_steps(catalogued_steps)
        self.show_quick_panel(self.steps)

    def get_steps(self, catalogued_steps):
        """ Formats steps and sorts them alphabetically """
        steps = []
        for step in sorted(catalogued_steps):
            formatted_step = step[0].capitalize() + ' ' + step[1]
            steps.append(formatted_step)
        return steps

    def on_done(self, index):
        """ Method executed when a quick-panel item is selected """
        self._logger.debug('index: {}'.format(index))
        if index == -1:
            self._logger.debug('Nothing selected from quick panel')
            return

        target_step = self.steps[index]
        self._logger.debug('target step: {}'.format(target_step))

        mapping = {"characters": target_step}
        view = self.window.active_view()
        view.run_command("insert", mapping)

    def show_quick_panel(self, steps):
        """ Displays quick-panel with the given steps
        :param [str] steps: List of steps to be displayed
        """
        self.window.show_quick_panel(steps, self.on_done)
