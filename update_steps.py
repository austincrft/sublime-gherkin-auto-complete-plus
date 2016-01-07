import glob
import re
import sublime
import sublime_plugin

feature_error = ('Gherkin Auto-Complete Plus: \nPlease specify a path to the directory'
                 ' containing your Feature Files. Go to \n\n"Preferences -> '
                 'Package Settings -> Gherkin Auto-Complete Plus -> Settings - User"'
                 '\n\n and create an entry for "feature_file_directories".')


def _is_int(s):
    """ Evaluates whether provided string is an integer

    :param s: input string
    :type s: str
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def _format_step(step):
    """ Formats Gherkin step in snippet notation

    :param str step: Gherkin step
    :return: formateted Gherkin step
    :rtype: str
    """
    # SWEET MOTHER OF REGEX!
    # Get values in between single- and double-quotes,
    # values in between greater- and less-than signs,
    # and numbers in 'integer' and 'decimal' format
    replace_values = re.findall(
        r'((?:\".+?\")|(?:\'.+?\')|(?:\<.+?\>)|(?:\d+(?:\.\d*)?|(?:\.\d+)))',
        step)

    for word in replace_values:
        if word:
            if word[0] == '"':
                step = step.replace(word, '"input"', 1)
            elif word[0] == "'":
                step = step.replace(word, "'input'", 1)
            elif word[0] == '<':
                step = step.replace(word, '<input>', 1)
            elif _is_int(word[0]) or word[0] == '.':
                step = step.replace(word, "[number]", 1)

    return step

def _get_steps_from_files(files=None):
    if not files:
        files = []

    with open(file_) as feature:
        for line in feature.readlines():
            # Separate keyword from line
            line_split = line.split(maxsplit=1)

            # Skip line if no step body is present
            if len(line_split) < 2:
                continue

            first_word = line_split[0].lower()

            elif first_word in main_words:
                last_main_word = first_word.lower()
            elif first_word in extra_words:
                pass
            else:
                continue

            # Remove keyword from line and format step
            line = _format_step(line_split[1])
            lines.add((last_main_word, line.strip() + '\n'))


def run():
    """ Main method of the module, iterates through directories provided
        in the settings to store and format the Gherkin steps.

    :rtype: list(tuple(str, str))
    """
    settings = sublime.load_settings('Gherkin Auto-Complete Plus.sublime-settings')
    feature_file_directories = settings.get('feature_file_directories')

    if not feature_file_directories:
        sublime.error_message(feature_error)
        return None

    main_words = ['given', 'when', 'then']
    extra_words = ['and', 'but']

    lines = set()
    last_main_word = ''

    for path in feature_file_directories:
        if not path.endswith('/'):
            path += '/'
        for file_ in glob.glob(path + '*.feature'):

    return lines
