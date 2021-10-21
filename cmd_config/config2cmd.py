import os
import subprocess
import platform
from dotenv import load_dotenv

from collections import OrderedDict
from cmd_config.parser import parse


def run_cmd(cmd, env_file=None):
    if env_file is not None:
        load_dotenv(env_file)
    if platform.system() == 'Windows':
        cmd = [os.path.expandvars(c) for c in cmd]
        cmd = ' '.join(cmd)
        subprocess.run(cmd, check=True)
    else:
        cmd = ' '.join(cmd)
        subprocess.run(cmd, check=True, shell=True, env=os.environ)


def config2cmd(config_file, run=None, env_file=None):
    cmds = parse(config_file)

    if isinstance(cmds, OrderedDict): # CmdCollection
        if run is None:
            for k, cmd in cmds.items():
                print(f'{k}:', ' '.join(cmd))
        elif len(run) == 0:
            for cmd in cmds.values():
                run_cmd(cmd, env_file=env_file)
        else:
            for r in run:
                if r in cmds:
                    run_cmd(cmds[r], env_file=env_file)
                else:
                    print(f'Cannot find command "{run}"')

    elif isinstance(cmds, list): # CmdType
        cmd = cmds
        if run is None:
            print(' '.join(cmd))
        else:
            run_cmd(cmd, env_file=env_file)
