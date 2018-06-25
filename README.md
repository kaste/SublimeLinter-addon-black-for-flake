Hi :wave:!

This is an addon for SublimeLinter. 

**You need to install both sublack and SublimeLinter-flake8**.

The plugin will auto configure flake8 and thus mute all warning black can actually fix. 

It does this **iff** a given view is configured with `"sublack.black_on_save": true` or `"SublimeLinter-addon-black-for-flake.enable": true`. Usually you set such a key in the 'settings' section of your project file. (These keys can itself be configured using the plugin settings.)



### TODO
- Detect upgrades of flake8, and reapply the patch