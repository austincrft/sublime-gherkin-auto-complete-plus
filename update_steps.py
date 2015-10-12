import glob
import re
import sublime
import sublime_plugin

feature_error = ('GherkinAutocompletePlus: \nPlease specify a path to the directory'
                 ' containing your Feature Files. Go to \n\n"Preferences -> '
                 'Package Settings -> GherkinAutocompletePlus -> Settings - User"'
                 '\n\n and create an entry for "feature_file_directories".')


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def format_step(line):
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

    return line


def run():
    settings = sublime.load_settings('gherkin_autocomplete_plus.sublime-settings')
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
            with open(file_) as feature:
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

                    # Remove keyword from line and format step
                    line = format_step(line_split[1])
                    lines.add((last_main_word, line.strip() + '\n'))

    return lines
