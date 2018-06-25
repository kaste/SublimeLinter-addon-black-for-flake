import sys

import sublime


super_fn = None
BLACK_FIXABLES = (
    'E111,E121,E122,E123,E124,E125,E126,'
    'E201,E202,E203,'
    'E221,E222,E225,E226,E227,E231,E241,E251,E261,E262,E265,E271,E272,'
    'E302,E303,E502,E701,E702,E703,E704,W291,W292,W293,W391'.split(',')
)


def plugin_loaded():
    try:
        sys.modules['sublack']
    except LookupError:
        flash('black-for-flake: sublack not ready or installed')
    else:
        patch_flake8()


def plugin_unloaded():
    global super_fn

    if super_fn:
        flake8 = get_flake8()
        if flake8:
            flake8.find_errors = super_fn


def get_flake8():
    try:
        return sys.modules['SublimeLinter-flake8.linter'].Flake8
    except LookupError:
        flash('black-for-flake: flake8 not ready or installed')
        return


def patch_flake8():
    global super_fn

    flake8 = get_flake8()
    if not flake8:
        return

    super_fn = flake8.find_errors

    def find_errors(self, output):
        if should_auto_config(self.view):
            return [
                error
                for error in super_fn(self, output)
                if (error.error or error.warning) not in BLACK_FIXABLES
            ]

        return super_fn(self, output)

    flake8.find_errors = find_errors


def should_auto_config(view):
    return any(
        view.settings().get(key)
        for key in sublime.load_settings(
            'SublimeLinter-addon-black-for-flake.sublime-settings'
        ).get('selectors', [])
    )


def flash(message):
    window = sublime.active_window()
    if window:
        window.status_message(message)
