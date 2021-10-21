import sys
from yaml import load, dump
from collections import OrderedDict
from typing import List, Dict, Union

CmdType = List[str]
CmdCollection = 'OrderedDict[str, CmdType]'


try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def flags_cmd(flags: list, global_config=dict()):
    return [f'-{f}' for f in flags]


def args_cmd(args: list, global_config=dict()):
    return [*args]


def kwargs_cmd(kwargs: dict, global_config=dict()):
    equalstr = global_config.get('equalstr', True)
    listsep = global_config.get('listsep', ' ')
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


def parse_global_config(config):
    keymap = {'equalstr': bool, 'listsep': str, 'version': str}
    return {c: keymap[c](v) for c, v in config.items() if c in keymap}


def parse_command(config, global_config=dict()) -> CmdType:

    if 'executable' not in config or len(config) == 0:
        return []
    exe = config.get('executable')
    _global_config = {**global_config, **parse_global_config(config)}
    flags = config.get('flags', [])
    args = config.get('positional', [])
    kwargs = config.get('optional', {})
    subcommand = config.get('subcommand', {})
    cmd = [
        exe,
        *flags_cmd(flags, global_config=_global_config),
        *kwargs_cmd(kwargs, global_config=_global_config),
        *args_cmd(args, global_config=_global_config),
        *parse_command(subcommand, global_config=_global_config)
    ]
    return cmd


def parse_commands(commands, global_config=dict()) -> OrderedDict:
    cmds = OrderedDict()
    for k, v in commands.items():
        cmds[k] = parse_command(v, global_config=global_config)
    return cmds


def parse_environments():
    # TODO
    raise NotImplementedError


def parse(ymlfile) -> Union[CmdCollection, CmdType]:
    with open(ymlfile, 'r') as fp:
        s = fp.read()
        data = load(s, Loader=Loader)
    global_config = parse_global_config(data)
    commands = data.pop('commands', dict())
    if commands:
        return parse_commands(commands, global_config=global_config)
    elif 'executable' in data:
        return parse_command(data)
