import sys
from yaml import load, dump
from collections import OrderedDict


try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def flags_cmd(flags: list):
    return [f'-{f}' for f in flags]


def args_cmd(args: list):
    return [*args]


def kwargs_cmd(kwargs: dict, equalstr=True, listsep=' '):
    kwargs = {
        k.replace('_','-'):
        listsep.join(v) if isinstance(v, list) else v
        for k, v in kwargs.items()
    }
    if equalstr:
        return [f'--{k}={v}' for k, v in kwargs.items()]
    else:
        cmd = [(f'--{k}',v) for k, v in kwargs.items()]
        return [x for y in cmd for x in y]


def parse_command(config, listsep, equalstr):
    if 'executable' not in config or len(config) == 0:
        return []
    exe = config.get('executable')
    _listsep = config.get('listsep', listsep)
    _equalstr = bool(config.get('equalstr', equalstr))
    flags = config.get('flags', [])
    args = config.get('positional', [])
    kwargs = config.get('optional', {})
    subcommand = config.get('subcommand', {})
    cmd = [
        exe,
        *flags_cmd(flags),
        *kwargs_cmd(
            kwargs,
            equalstr=_equalstr,
            listsep=_listsep,
        ),
        *args_cmd(args),
        *parse_command(subcommand, _listsep, _equalstr)
    ]
    return cmd


def parse(ymlfile):
    with open(ymlfile, 'r') as fp:
        s = fp.read()
        data = load(s, Loader=Loader)
    version = data.pop('version', None)
    listsep = data.pop('listsep', ' ')
    equalstr = bool(data.pop('equalstr', True))
    executable = data.pop('commands', dict())

    cmds = OrderedDict()
    for k, v in executable.items():
        cmds[k] = parse_command(v, listsep, equalstr)
    return cmds
