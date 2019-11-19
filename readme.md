![alt](img/yzdoom.png)

# yaml-powered zdoom launcher for Python 3

Bringing the feeling of DevOps to zdoom :) Made with :godmode:, :heart: and :snake:

## what it does?

**yzdoom** is a launcher for [zdoom](https://https://www.zdoom.org/index) that's utilizing [YAML](https://yaml.org) to easily set up your favourite IWAD and PWAD zdoom configurations.

## how it works?

you'll need ****python3**** to run this

the launcher takes *default config* (mandatory) and *run config* (optional).
if a *run config* is specified, the *default config* will be updated with it at runtime.

the zdoom commandline parameters are generated from the updated config keys and values.

defaults config example:
```
yzdoom_defaults:
  gzdoom: /usr/games/gzdoom
  iwad_folder: ~/.config/gzdoom
  pwad_folder: ~/.config/gzdoom
```



## what's supported?

**yzdoom** should of course work on any platform that runs zdoom, but has been developed & tested primarily for Linux.

What currently works is loading IWAD and PWADs. I might add some additional functionality later.

## how to install & set it up?

1. clone the repository
2. navigate to the folder in your shell & run: `$ cp ./yzdoom.py ./yzdoom && chmod +x ./yzdoom && sudo cp ./yzdoom /usr/games/`
3. install YAML parser and emitter for Python via pip: `$ pip install --upgrade PyYAML`
4. run `$ yzdoom -init` to create `~/.config/yzdoom/defaults.yml`
5. open the `~/.config/yzdoom/defaults.yml` with your favorite text editor and adjust what's needed

## how to use?

6. create your YAML config (`my_first_run_config.yml`) according to the following example:
    ```
    yzdoom_run:
        iwad: doom2.wad
        pwads: 
            - brutalv21.pk3
            - bd21.0.3patch.pk3
            - mapsofchaos-ok.wad
    ```
    ***of course make sure you actually have these PWADs and IWAD!***

7. run your config with `$ yzdoom -run my_first_run_config.yml`
8. RIP and TEAR!

## troubleshooting

This is very hacky early release, very hacky and very early. If you get YAML parsing errors, check your indention. :)