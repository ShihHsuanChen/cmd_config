import argparse

from cmd_config.config2cmd import config2cmd


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
    config2cmd(args.target, run=args.run)


if __name__ == '__main__':
    main()
