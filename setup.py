import os
from setuptools import setup, find_packages


def get_requirements(fns):
    reqs = []
    for fn in fns:
        if not os.path.exists(fn):
            raise FileNotFoundError(f'Given file {fn} does not exists.')
        with open(fn, 'r') as f:
            reqs += [line.strip() for line in f.readlines()]
    return reqs


setup(
    name='cmd-config',
    description='Convert config to command line string',
    version_config={
        'template': '{tag}',
        'dev_template': '{tag}.post{ccount}',
        'dirty_template': '{tag}.post{ccount}+dirty',
    },
    entry_points={
        'console_scripts': [
            'config2cmd = cmd_config.config2cmd:main'
        ]
    },
    setup_requires=['setuptools-git-versioning'],
    install_requires=get_requirements(['requirements.txt']),
    packages=find_packages(exclude=['test']),
)
