#!/usr/bin/env python3
'''
yZDOOM launcher - YAML configs for zdoom, gzdoom

(c) Vitek Urbanec, 2019

vitek@linuxmail.org

'''


import subprocess
import argparse
import os
import sys
import yaml

DOOM = r"""

=================     ===============     ===============   ========  ========
\\ . . . . . . .\\   //. . . . . . .\\   //. . . . . . .\\  \\. . .\\// . . //
||. . ._____. . .|| ||. . ._____. . .|| ||. . ._____. . .|| || . . .\/ . . .||
|| . .||   ||. . || || . .||   ||. . || || . .||   ||. . || ||. . . . . . . ||
||. . ||   || . .|| ||. . ||   || . .|| ||. . ||   || . .|| || . | . . . . .||
|| . .||   ||. _-|| ||-_ .||   ||. . || || . .||   ||. _-|| ||-_.|\ . . . . ||
||. . ||   ||-'  || ||  `-||   || . .|| ||. . ||   ||-'  || ||  `|\_ . .|. .||
|| . _||   ||    || ||    ||   ||_ . || || . _||   ||    || ||   |\ `-_/| . ||
||_-' ||  .|/    || ||    \|.  || `-_|| ||_-' ||  .|/    || ||   | \  / |-_.||
||    ||_-'      || ||      `-_||    || ||    ||_-'      || ||   | \  / |  `||
||    `'         || ||         `'    || ||    `'         || ||   | \  / |   ||
||            .===' `===.         .==='.`===.         .===' /==. |  \/  |   ||
||         .=='   \_|-_ `===. .==='   _|_   `===. .===' _-|/   `==  \/  |   ||
||      .=='    _-'    `-_  `='    _-'   `-_    `='  _-'   `-_  /|  \/  |   ||
||   .=='    _-'          `-__\._-'         `-_./__-'         `' |. /|  |   ||
||.=='    _-'                                                     `' |  /==.||
=='    _-'                                                            \/   `==
\   _-'                                                                `-_   /
 `''                                                                      ``'

"""

PARSER = argparse.ArgumentParser(description='yZDOOM launcher - YAML configs for zdoom, gzdoom')

PARSER.add_argument('-run',
                    action='store',
                    dest='doom_run_config_file')
PARSER.add_argument('-default',
                    action='store',
                    dest='doom_default_config_file',
                    default=os.path.expanduser('~/.config/yzdoom/defaults.yml'))
PARSER.add_argument('-init',
                    action='store_true',
                    dest='init_mode',
                    default=False)

ARGS = PARSER.parse_args()

DEFAULT_CONFIG_MAP = {
    'yzdoom_defaults': {
        'gzdoom': '/usr/games/gzdoom',
        'iwad_folder': '~/.config/gzdoom',
        'pwad_folder': '~/.config/gzdoom'
        
    }
}

def init_config(config_map):
    print('YZDOOM init creating config folder & default config')
    try:
        os.makedirs(os.path.expanduser('~/.config/yzdoom/'))
    except FileExistsError:
        print('folder already exists')
    try:
        with open(os.path.expanduser('~/.config/yzdoom/defaults.yml'), 'w+') as default_config:
            yaml.safe_dump(config_map, default_config)
    except Exception:
       print('cannot create default config file')

if ARGS.init_mode:
    init_config(DEFAULT_CONFIG_MAP)
    sys.exit()

DOOM_RUN_CONFIG_FILE = ARGS.doom_run_config_file
DOOM_DEFAULT_CONFIG_FILE = ARGS.doom_default_config_file

def load_config_yaml(filename):
    ''' YAML loading function '''
    with open(filename, 'r') as yaml_config:
        config_map = yaml.safe_load(yaml_config)
    return config_map

def assemble_params(config_map):
    ''' assemble config map to parameters list '''
    subprocess_run_list = []

    # add binary

    subprocess_run_list.append(config_map['gzdoom'])

    # add IWAD

    config_map['iwad'] = os.path.join(os.path.expanduser(config_map['iwad_folder']), config_map['iwad'])
    subprocess_run_list += ['-iwad'] + [config_map['iwad']]

    # add PWADs

    subprocess_run_list += ['-file'] + \
        [os.path.join(os.path.expanduser(config_map['pwad_folder']), pwad) for pwad in config_map['pwads']]

    return subprocess_run_list

def display_config_info(config_map):
    ''' print out information about the run'''
    print(DOOM)
    print(50*"=")
    print(
        'YZDOOM running IWAD: %s and PWAD(s): \n - %s' % (config_map['iwad'], "\n - ".join(config_map['pwads']))
    )
    print(50*"=")

DOOM_DEFAULTS = load_config_yaml(DOOM_DEFAULT_CONFIG_FILE)
DOOM_RUN = load_config_yaml(DOOM_RUN_CONFIG_FILE)

DOOM_DEFAULTS['yzdoom_defaults'].update(DOOM_RUN['yzdoom_run'])
DOOM_FINAL_CONFIG = DOOM_DEFAULTS['yzdoom_defaults']

display_config_info(DOOM_FINAL_CONFIG)

SUBPROCESS_RUN_LIST = assemble_params(DOOM_FINAL_CONFIG)
PROCESS = subprocess.run(SUBPROCESS_RUN_LIST, check=True, universal_newlines=True)
