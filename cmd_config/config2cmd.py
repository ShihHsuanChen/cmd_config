import os
import subprocess
import platform
from collections import OrderedDict
from typing import Dict, Optional

from dotenv import load_dotenv
from cmd_config.parser import parse


def run_cmd(cmd, env_dict: Dict[str, str], env_file: Optional[str] = None):
    for k, v in env_dict.items():
        os.environ[k] = v
    if env_file is not None:
        load_dotenv(env_file, override=True)
    if platform.system() == 'Windows':
        cmd = [os.path.expandvars(c) for c in cmd]
        cmd = ' '.join(cmd)
        subprocess.run(cmd, check=True)
    else:
        cmd = ' '.join(cmd)
        subprocess.run(cmd, check=True, shell=True, env=os.environ)


def config2cmd(config_file, run=None, env_file=None):
    cmdenvs = parse(config_file)

    if isinstance(cmdenvs, OrderedDict): # CmdEnvCollection
        if run is None:
            for k, (cmd, _) in cmdenvs.items():
                print(f'{k}:', ' '.join(cmd))
        elif len(run) == 0:
            for (cmd, env) in cmdenvs.values():
                run_cmd(cmd, env_dict=env, env_file=env_file)
        else:
            for r in run:
                if r in cmdenvs:
                    cmd, env = cmdenvs[r]
                    run_cmd(cmd, env_dict=env, env_file=env_file)
                else:
                    print(f'Cannot find command "{run}"')

    else: # CmdEnvType
        cmd, env = cmdenvs
        if run is None:
            print(' '.join(cmd))
        else:
            run_cmd(cmd, env_dict=env, env_file=env_file)
