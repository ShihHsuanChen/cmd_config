import argparse
import subprocess

from cmd_config.parser import parse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'target',
        help='target config file (YAML file)'
    )
    parser.add_argument(
        '-r', '--run',
        type=str,
        default=None,
        help='run command from config file'
    )
    args = parser.parse_args()
    config_file = args.target
    cmds = parse(config_file)

    if args.run is None:
        for k, cmd in cmds.items():
            print(f'{k}:',' '.join(cmd))
    elif args.run in cmds:
        cmd = cmds[args.run]
        subprocess.run(cmd, check=True)
    else:
        print(f'Cannot find command "{args.run}"')
        print('Expect either', ', '.join(cmds.keys()))


if __name__ == '__main__':
    main()
