Hi :wave:!

This is an addon for SublimeLinter. 

**You need to install both sublack and SublimeLinter-flake8**.

The plugin will auto configure flake8 and mute all warnings black can actually fix. 

It does this _iff_ a given view is configured with `"sublack.black_on_save": true` or `"SublimeLinter-addon-black-for-flake.enable": true`. Usually you set such a key in the 'settings' section of your project file. Like so:

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

The keys can be configured using the plugin settings.



### TODO
- Detect upgrades of flake8, and reapply the patch. 

