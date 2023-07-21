# cmd_config

Convert yaml config to command line string


## Install

```shell=
$ pip install git+http://10.0.4.52:3000/j0018/cmd_config.git@<tag>
```

## Usage

```shell=
usage: config2cmd [-h] [-r RUN] target

positional arguments:
  target             target config file (YAML file)

optional arguments:
  -h, --help         show this help message and exit
  -r RUN, --run RUN  run command from config file
```


## Config format

```yaml
version: <version number (not used)>
equalstr: <True, False (default: True)>
listsep: <string to separate list content of optional argument. (default: " ")>

commands:
    <command name1>:
        executable: <executable>
        equalstr: <True, False (default: True)>
        listsep: <string to separate list content of optional argument. (default: " ")>
        positional:
            - <first positional argument>
            - ...
            - ...
        flags:
            - <optional argument without value>
            - ...
            - ...
        optional:
            <optional argument key1>: <value>
            <optional argument key2>:
                - <optional argument value1>
                - <optional argument value2>
                - ...
        subcommand:
            executable: ...
            equalstr: ...
            listsep: ...
            positional:
                - ...
            flags:
                - ...
            optional:
                ...: ...
            
    <command name2>:
        ...
```


## Config file example

```yaml
equalstr: True

commands:
    pyinstaller001:
        executable: pyinstaller
        listsep: ','
        equalstr: False
        positional:
            - aaa
        flags:
            - i
            - y
        optional:
            file-name: bbb
            group_name:
                - g1
                - g2
    celery001:
        executable: celery
        optional:
            app: main.celery
        subcommand:
            executable: worker
            optional:
                queues:
                    - queue1
                    - queue2
                concurrency: 3
    list:
        executable: ls
        flags:
            - a
            - l
    echo:
        executable: echo
        positional:
            - print
            - "$VAR1"
            - "$VAR2"
        environment:
            VAR1: Hello
            VAR2: World
```
Gives
- pyinstaller001: `pyinstaller -i -y --file-name bbb --group-name g1,g2 aaa`
- celery001: `celery --app=main.celery worker --queues=queue1 queue2 --concurrency=3`
- list: `ls -a -l`
- echo: `print Hello World`
