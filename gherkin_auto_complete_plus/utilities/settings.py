import logging

import sublime


_json_bool_error = (
        'Gherkin Auto-Complete Plus: \n\nError in sublime-settings file.'
        ' Valid values for `ignore_open_directories`:\n\ntrue\nfalse'
        '\n(There should be no quotes around the values)'
)


def _get_package_settings():
    """ Gets settings for package """
    return sublime.load_settings('Gherkin Auto-Complete Plus.sublime-settings')


def get_feature_directories():
    """ Gets list of directories specified under the "feature_file_directories"
        option. Returns an empty list if none are found.
    """
    settings = _get_package_settings()
    feature_directories = settings.get('feature_file_directories', default=[])
    return feature_directories


def ignore_open_directories():
    """ Gets bool value for "ignore_open_directories" option """
    settings = _get_package_settings()
    result = settings.get('ignore_open_directories', default=False)

    if type(result) != bool:
        sublime.error_message(_json_bool_error)
        return

    return result


def get_logging_level():
    """ Gets the logging level specified under the "logging_level" option.
        Returns "error" if a logging level isn't specified.
    """
    default = 'error'
    settings = _get_package_settings()
    level = settings.get('logging_level') or default
    return getattr(logging, level.upper())
