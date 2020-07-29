import sys

import sublime


super_fn = None
BLACK_FIXABLES = (
    'E111,E117,E121,E122,E123,E124,E125,E126,E128,E129,'
    'E201,E202,E203,'
    'E221,E222,E225,E226,E227,E231,E241,E251,E261,E262,E265,E271,E272,'
    'E301,E302,E303,E306,'
    'E502,'
    'E701,E702,E703,E704,'
    'W291,W292,W293,W391'.split(',')
)


def dprint(*a, **k):
    # print(*a, **k)
    ...


def plugin_loaded():
    dprint('=<> plugin_loaded')
    try:
        sys.modules['sublack']
    except LookupError:
        flash('black-for-flake: sublack not ready or installed')

    patch_flake8()


def plugin_unloaded():
    dprint('=<> plugin_unloaded')
    unpatch_flake8()


def get_plugin_module():
    try:
        return sys.modules['SublimeLinter-flake8.linter']
    except LookupError:
        flash('black-for-flake: flake8 not ready or installed')
        return


def unpatch_flake8():
    global super_fn

    if super_fn is None:
        return

    plugin = get_plugin_module()
    if not plugin:
        return

    dprint('--> Un-patching')
    plugin.Flake8.find_errors = super_fn
    super_fn = None

    if plugin.plugin_unloaded.__name__ == 'blacked_unload':
        delattr(plugin, 'plugin_unloaded')


def patch_flake8():
    global super_fn

    plugin = get_plugin_module()
    if not plugin:
        return

    if plugin.Flake8.find_errors.__name__ == 'blacked_find_errors':
        flash("black-for-flake: Already patched, how's that? 😕")
        return

    if super_fn is not None:
        flash("black-for-flake: super_fn is not None, how's that? 😕")

    dprint('--> Patching')
    super_fn = plugin.Flake8.find_errors

    def blacked_find_errors(self, output):
        if should_auto_config(self.view):
            return [
                error
                for error in super_fn(self, output)
                if (error.error or error.warning) not in BLACK_FIXABLES
            ]

        return super_fn(self, output)

    def blacked_unload():
        dprint('=<> blacked_unload')
        # When 'plugin_unloaded' is called, we unpatch immediately/sync.
        # After that, Sublime/PC will update/replace the plugin. We have to
        # guess how long this can take here.
        unpatch_flake8()
        sublime.set_timeout_async(patch_flake8, 1000)

    plugin.Flake8.find_errors = blacked_find_errors
    try:
        plugin.plugin_unloaded
    except AttributeError:
        plugin.plugin_unloaded = blacked_unload
    else:
        flash("black-for-flake: Hm, Flake has a 'plugin_unloaded'? 🤔")
        print(plugin.plugin_unloaded)


def should_auto_config(view):
    return any(
        view.settings().get(key)
        for key in sublime.load_settings(
            'SublimeLinter-addon-black-for-flake.sublime-settings'
        ).get('selectors', [])
    )


def flash(message):
    print(message)
    window = sublime.active_window()
    if window:
        window.status_message(message)
