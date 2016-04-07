import logging

import sublime


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


def get_logging_level():
    """ Gets the logging level specified under the "logging_level" option.
        Returns "error" if a logging level isn't specified.
    """
    default = 'error'
    settings = _get_package_settings()
    level = settings.get('logging_level') or default
    return getattr(logging, level.upper())
