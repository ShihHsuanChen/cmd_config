import os
import subprocess
from dotenv import load_dotenv

from cmd_config.parser import parse


def config2cmd(config_file, run=None, envfile=None):
    cmds = parse(config_file)
    if envfile is not None:
        load_dotenv(envfile)

    if run is None:
        for k, cmd in cmds.items():
            print(f'{k}:',' '.join(cmd))
    elif run in cmds:
        cmd = ' '.join(cmds[run])
        subprocess.run(cmd, check=True, shell=True, env=os.environ)
    else:
        print(f'Cannot find command "{run}"')
        print('Expect either', ', '.join(cmds.keys()))
