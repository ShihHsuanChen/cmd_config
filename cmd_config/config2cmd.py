import subprocess

from cmd_config.parser import parse


def config2cmd(config_file, run=None):
    cmds = parse(config_file)

    if run is None:
        for k, cmd in cmds.items():
            print(f'{k}:',' '.join(cmd))
    elif run in cmds:
        cmd = cmds[run]
        subprocess.run(cmd, check=True)
    else:
        print(f'Cannot find command "{run}"')
        print('Expect either', ', '.join(cmds.keys()))
