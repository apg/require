"""This module exports `require` which attempts to locate a 
module to import given a config file of possible places to 
find it in.

An example is necessary.

Given a config file:

[2.6]
MySQLdb = MySQLdb-2.6-i386.egg

[2.5]
MySQLdb = MySQLdb-2.5-i386.egg
multiprocessing = /usr/local/pylib
"""

__ALL__ = ['require', 'CONFIG_FILE']

import os
import sys

from ConfigParser import ConfigParser

CONFIG_FILE = 'require-paths.conf'
_CONFIG_LOCATIONS = ['.', '~/']
_CONFIGS = {}
_ENV_VAR = 'PYREQUIRE_CONFIG'
_GLOBAL_SECTION = 'global'
_GLOBAL_PATH_OPTION = 'path'

PY_VERSION_FULL = '%d.%d.%d' % sys.version_info[0:3]
PY_VERSION = '%d.%d' % sys.version_info[0:2]

def require(modname, names=None, config=None):
    """Imports `mod` and optionally specific names from mod

Example:

# equivalent to `import os`
os = require('os')

# equivalent to `from os import open`
os, open = require('os', names=['open'])
"""
    mod = None
    # already imported?
    if modname in sys.modules:
        mod = sys.modules[modname]
    else:
        mod = _find_module_using_config(modname, config)

    if names:
        return _find_names(mod, names)

    return mod


def _find_config(config_file):
    real_path = None
    if config_file is None:
        config_file = os.environ.get(_ENV_VAR, CONFIG_FILE)
    
    if os.path.isabs(config_file):
        real_path = config_file
    else:
        for d in _CONFIG_LOCATIONS:
            tmp = os.path.expanduser(os.path.join(d, config_file))
            check_path = os.path.realpath(tmp)
            if os.path.exists(check_path):
                real_path = check_path
                break

    if not real_path:
        return None
    elif real_path in _CONFIGS:
        return _CONFIGS[real_path]
    else:
        config = ConfigParser()
        config.read(real_path)
        _CONFIGS[real_path] = config
        return config
    

def _find_module_using_config(mod_name, config_file):
    config = _find_config(config_file)
    if not config:
        raise ImportError('No module named %s' % mod_name)

    # add global paths, if present
    if config.has_section(_GLOBAL_SECTION) and \
            config.has_option(_GLOBAL_SECTION, _GLOBAL_PATH_OPTION):
        for p in config.get(_GLOBAL_SECTION, _GLOBAL_PATH_OPTION)\
                .split(os.pathsep):
            if p not in sys.path:
                sys.path.append(p)

    for v in (PY_VERSION_FULL, PY_VERSION):
        if config.has_section(v) and config.has_option(v, mod_name):
            path = config.get(v, mod_name)
            if path not in sys.path:
                sys.path.append(path)
            try:
                mod = __import__(mod_name)
                return mod
            except ImportError:
                continue
    raise ImportError('No module named %s' % mod_name)


def _find_module(mod_name, config_file):
    try:
        mod = __import__(mod_name)
    except ImportError, e:
        return _find_module_by_config(mod_name, config_file)


def _find_names(mod, names):
    out = [mod]
    for name in names:
        try:
            tmp = getattr(mod, name)
            out.append(tmp)
        except AttributeError:
            raise ImportError('can not import name %s' % name)

    return out
