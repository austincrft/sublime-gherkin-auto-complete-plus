import os
import re
import sublime
import sublime_plugin

feature_error = ('GherkinAutocompletePlus: \nPlease specify a path to the directory'
                 ' containing your Feature Files. Go to \n\n"Preferences -> '
                 'Package Settings -> GherkinAutocompletePlus -> Settings - User"'
                 '\n\n and create an entry for "feature_file_directory".')

definition_error = ('GherkinAutocompletePlus: \nPlease specify a path to the file '
                    'where you would like to keep the step definitions. Go to \n\n'
                    '"Preferences -> Package Settings -> GherkinAutocompletePlus -> '
                    'Settings - User"\n\n and create an entry for "step_path".')


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class UpdateStepsCommand(sublime_plugin.TextCommand):
    """
    Sublime Text command for updating step definitions
    """

    def run(self, edit):
        settings = sublime.load_settings('gherkin_autocomplete_plus.sublime-settings')
        feature_file_directory = settings.get('feature_file_directory')

        if feature_file_directory == 'path/to/featurefiles/directory':
            sublime.error_message(feature_error)
            return None

        if not feature_file_directory.endswith('/'):
            feature_file_directory += '/'

        step_file_path = settings.get('step_path')

        if step_file_path == 'path/to/steps.txt':
            sublime.error_message()

        main_words = ['given', 'when', 'then']
        extra_words = ['and', 'but']

        lines = set()
        last_main_word = ''

        for file_ in os.listdir(feature_file_directory):
            if file_.endswith('.feature'):
                with open(feature_file_directory + file_) as feature:
                    for line in feature.readlines():
                        # Only separate first word in line
                        line_split = line.split(maxsplit=1)
                        first_word = line_split[0].lower() if line_split else ''

                        if not first_word:
                            continue
                        elif first_word in main_words:
                            last_main_word = first_word.lower()
                        elif first_word in extra_words:
                            pass
                        else:
                            continue

                        # Remove keyword from line
                        line = line_split[1]

                        # SWEET MOTHER OF REGEX!
                        # Get values in between single- and double-quotes,
                        # values in between greater- and less-than signs,
                        # and numbers in 'integer' and 'decimal' format
                        replace_values = re.findall(
                            r'((?:\".+?\")|(?:\'.+?\')|(?:\<.+?\>)|(?:\d+(?:\.\d*)?|(?:\.\d+)))',
                            line)

                        for word in replace_values:
                            if word:
                                if word[0] == '"':
                                    line = line.replace(word, '"input"', 1)
                                elif word[0] == "'":
                                    line = line.replace(word, "'input'", 1)
                                elif word[0] == '<':
                                    line = line.replace(word, '<input>', 1)
                                elif is_int(word[0]) or word[0] == '.':
                                    line = line.replace(word, "[number]", 1)

                        lines.add((last_main_word, line.strip() + '\n'))

        with open(step_file_path, 'w') as csv:
            csv.write("Type,Body\n")
            [csv.write(line[0] + ',' + line[1]) for line in lines]
