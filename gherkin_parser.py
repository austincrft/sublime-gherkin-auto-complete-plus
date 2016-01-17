import functools
import glob
import logging
import re


def log_func(func):
    @functools.wraps(log_func)
    def wrap(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.info('Entering {}'.format(func.__name__))
        f_result = func(*args, **kwargs)
        logger.debug('{} result: {}'.format(func.__name__, f_result))
        logger.info('Exiting {}'.format(func.__name__))
        return f_result
    return wrap


@log_func
def get_feature_files(directories):
    """ Gets all *.feature files under the provided directories

    :param [str] directories: a list of directory names
    :rtype: set of (str, str)
    """
    if directories is None:
        directories = []

    files = []
    for path in directories:
        if not path.endswith('/'):
            path += '/'
        files.extend(glob.glob(path + '*.feature'))
    return files


@log_func
def get_steps(files):
    """ Gets all Gherkin steps from provided files

    :param files: feature files
    :rtype: set of (str, str)
    """
    if files is None:
        files = []

    main_words = ['given', 'when', 'then']
    extra_words = ['and', 'but']
    steps = set()

    for file in files:
        close_file = False
        if not hasattr(file, 'read'):
            file = open(file)
            close_file = True

        last_main_word = ''

        for line in file.readlines():
            # Separate keyword from line
            line_split = line.split(maxsplit=1)

            # Skip line if no step body is present
            if len(line_split) < 2:
                continue

            first_word = line_split[0].lower()

            if first_word in main_words:
                last_main_word = first_word.lower()
            elif first_word in extra_words:
                pass
            else:
                continue

            line = line_split[1].strip()
            step = (last_main_word, line)
            steps.add(step)

        if close_file:
            file.close()

    return steps


def format_steps(steps):
    """ Formats steps in a uniform way to avoid duplicate steps in results

    :param steps: Gherkin steps paired with their keywords e.g. (keyword, step)
    :type steps: set of (str, str)
    :rtype: set of (str, str)
    """
    if steps is None:
        steps = []

    formatted_steps = set()

    # SWEET MOTHER OF REGEX!
    # Get values in between single- and double-quotes,
    # values in between greater- and less-than signs,
    # and numbers in 'integer' and 'decimal' format
    regex = r'((?:\".+?\")|(?:\'.+?\')|(?:\<.+?\>)|(?:\d+(?:\.\d*)?|(?:\.\d+)))'

    def _is_int(s):
        try:
            int(s)
        except ValueError:
            return False
        return True

    for step in steps:
        keyword = step[0]
        body = step[1]

        replace_values = re.findall(regex, body)
        for word in replace_values:
            if word:
                if word[0] == '"':
                    body = body.replace(word, '"input"', 1)
                elif word[0] == "'":
                    body = body.replace(word, "'input'", 1)
                elif word[0] == '<':
                    body = body.replace(word, '<input>', 1)
                elif _is_int(word[0]) or word[0] == '.':
                    body = body.replace(word, "[number]", 1)
        formatted_steps.add((keyword, body))

    return formatted_steps


@log_func
def run(directories):
    """ Gets feature files from provided directories, gets steps from files,
        formats steps to avoid duplicates.

    :param [str] directories: collection of directories
    :rtype: set of (str, str)
    """
    filenames = get_feature_files(directories)
    steps = get_steps(filenames)
    formatted_steps = format_steps(steps)
    return formatted_steps
