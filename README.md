# Hi :wave:!

This is an addon for SublimeLinter. 

**You need to install [SublimeLinter-flake8](https://github.com/SublimeLinter/SublimeLinter-flake8)!**.  Highly recommended is to install **[sublack](https://github.com/jgirardet/sublack)** as well.

The plugin will configure the flake8 plugin and mute all warnings black can actually fix. 

It does this _only if_ a given view is configured with `"sublack.black_on_save": true` or `"SublimeLinter-addon-black-for-flake.enable": true`. (Which keys it evaluates can itself be configured via the settings, but you probably don't need to.) 

Usually, at least as long as `black` is not the default in the python community, you set such a key in the 'settings' section of your project file. Like so:

```json
{
    "folders": [
        {
            "path": "."
        },
    ],

    "settings": {
        "sublack.black_on_save": true
    }
}
```

`sublack` allows you to switch black on or off temporarily per view, e.g. via the context menu. These views will get selected or deselected automatically as well.

If you ever want this to be enabled by default, you could also set it up in your User Preferences.



[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
