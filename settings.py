import sublime
import logging

feature_error = ('Gherkin Auto-Complete Plus: \nPlease specify a path to the directory'
                 ' containing your Feature Files. Go to \n\n"Preferences -> '
                 'Package Settings -> Gherkin Auto-Complete Plus -> Settings - User"'
                 '\n\n and create an entry for "feature_file_directories".')


def _get_package_settings():
    """ Gets settings for package """
    return sublime.load_settings('Gherkin Auto-Complete Plus.sublime-settings')


def get_feature_directories():
    settings = _get_package_settings()
    feature_directories = settings.get('feature_file_directories', default=[])
    if not feature_directories:
        sublime.error_message(feature_error)
    return feature_directories


def get_logging_level():
    default = 'error'
    settings = _get_package_settings()
    level = settings.get('logging_level') or default
    return getattr(logging, level.upper())
