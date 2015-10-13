import sublime
import sublime_plugin
import re
import gherkin_auto_complete_plus.update_steps as update_steps

settings = sublime.load_settings('gherkin_autocomplete_plus.sublime-settings')
filepath = settings.get('step_path')
keywords = ['given', 'when', 'then']
completions = {}
steps = []


class GherkinEventListener(sublime_plugin.EventListener):
    """
    Sublime Text Event Listener
    """

    def __init__(self):
        self.first_modify = True

    def on_modified(self, view):
        """ Triggers when a sublime.View is modified. If in Gherkin syntax,
            opens AutoComplete menu and fills with completions.

        :param view: sublime.View object
        :type view: sublime.View
        """
        view_sel = view.sel()
        if not view_sel:
            return

        if not self._is_gherkin_scope(view):
            return

        if self.first_modify:
            self._update_steps()
            self.first_modify = False

        view.settings().set('auto_complete', False)

        pos = view_sel[0].end()
        next_char = view.substr(sublime.Region(pos - 1, pos))

        if next_char in (' ', '\n'):
            view.run_command('hide_auto_complete')
            return

        view.run_command('hide_auto_complete')
        self._show_auto_complete(view)
        self._fill_completions(view, pos)

    def on_query_completions(self, view, prefix, locations):
        """ Sublime Text AutoComplete event handler

        Takes the completions that were set in the 'fill_completions' method
        and returns them to the AutoComplete list.

        :param view: `sublime.View` object
        :type view: sublime.View
        :param prefix: last word to the left of the cursor
        :type prefix: str
        :param locations: offset from beginning of line
        :type locations: list(int)

        ^^ None of which are used, but have some documentation anyway.
        """
        _completions = [sug for key, sug in completions.items()]
        completions.clear()

        return sorted(_completions)

    def on_post_save_async(self, view):
        """ Sublime Text 'On File Save' event handler

        Updates the step catolog after file save in Gherkin syntax

        :param view: `sublime.View` object
        :type view: sublime.View
        """
        if self._is_gherkin_scope(view):
            self._update_steps()

    def _update_steps(self):
        """ Executes the 'run' method of the 'update_steps' module
            and stores the results in the 'steps' variable
        """
        steps.clear()
        [steps.append(step) for step in update_steps.run()]

    def _is_gherkin_scope(self, view):
        """ Validates that user is in Gherkin Syntax

        :param view: `sublime.View` object
        :type view: sublime.View

        :return: bool
        """
        location = view.sel()[0].end()
        return view.match_selector(location, "text.gherkin.feature - comment")

    def _step_matches_line(self, step_words, line_words):
        """ Validates that words in step match words in line

        :param step_words: words in step definition
        :type step_words: list(str)
        :param line_words: words in current line
        :type line_words: list(str)

        :return: bool
        """
        # Skip first word in line because it is a keyword
        line_text = ' '.join(line_words[1:])
        step_text = ' '.join(step_words)

        if len(step_text) >= len(line_text):
            match = True
            for index, char in enumerate(line_text):
                if step_text[index] != char:
                    match = False
            return match
        else:
            return False

    def _format_step(self, step, line_words=[]):
        """ Returns step formatted in snippet notation

        :param step: step definition
        :type step: str
        :param line_words: words in step definition
        :type line_words: list(str)

        :return: str
        """
        # Skip first word in line because it is a keyword
        # Skip last word in line so it'll be included in output
        line_text = ' '.join(line_words[1:-1])

        for i in range(len(line_text)):
            step = step.replace(line_text[i], '', 1)
        index = 1
        regex = r'((?:\".+?\")|(?:\'.+?\')|(?:\<.+?\>)|(?:\[number\]))'
        replace_values = re.findall(regex, step)
        for word in replace_values:
            if word[0] == '"':
                step = step.replace(word, '"${' + str(index) + ':input}"', 1)
                index += 1
            elif word[0] == "'":
                step = step.replace(word, "'${" + str(index) + ":input}'", 1)
                index += 1
            elif word[0] == '<':
                step = step.replace(word, '<${' + str(index) + ':input}>', 1)
                index += 1
            elif word[0] == '[':
                step = step.replace(word, '${' + str(index) + ':[number]}', 1)
                index += 1

        return step.strip()

    def _show_auto_complete(self, view):
        """ Opens AutoComplete manually

        :param view: the view containing the cursor
        :type view: sublime.View
        """
        def _show_auto_complete():
            view.run_command('auto_complete', {
                'disable_auto_insert': True,
                'api_completions_only': True,
                'next_completion_if_showing': False,
                'auto_complete_commit_on_tab': True,
            })
        # Have to set a timeout for some reason
        sublime.set_timeout(_show_auto_complete, 0)

    def _fill_completions(self, view, location):
        """ Prepares completions for auto-complete list

        :param view: `sublime.View` object
        :type view: sublime.View
        :param location: position of cursor in line
        :type locations: int
        """
        last_keyword = ''
        current_region = view.line(location)
        current_line_text = view.substr(current_region).strip()
        current_line_words = current_line_text.split()

        # Don't fill completions until after first space is typed
        if ' ' not in current_line_text:
            return

        # If first word is keyword, take that one
        if current_line_words and current_line_words[0].lower() in keywords:
            last_keyword = current_line_words[0].lower()
        # Otherwise, reverse iterate through lines until keyword is found
        else:
            all_lines = view.split_by_newlines(sublime.Region(0, view.size()))
            current_index = all_lines.index(current_region)
            for region in reversed(all_lines[0:current_index]):
                region_text = view.substr(region).lstrip()
                split_line = region_text.split(' ', 1)
                if split_line and split_line[0].lower() in keywords:
                    last_keyword = split_line[0].lower()
                    break

        if not last_keyword:
            print("GherkinAutocompletePlus: Could not find 'Given', 'When', "
                  "or 'Then' in text.")
            return

        for step_type, step in steps:
            if step_type == last_keyword:
                # If only keyword is typed, provide all steps for keyword
                if len(current_line_words) == 1:
                    step_format = self._format_step(step)
                    suggestion = (step + '\t' + step_type, step_format)
                    completions[step] = suggestion

                # If more words typed, check for match
                elif len(current_line_words) > 1:
                    if self._step_matches_line(step.split(), current_line_words):
                        step_format = self._format_step(step, current_line_words)
                        suggestion = (step + '\t' + step_type, step_format)
                        completions[step] = suggestion
