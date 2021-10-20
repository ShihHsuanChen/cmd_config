import cmd_config


def get_data_path(fname):
    import os
    datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    return os.path.join(datadir, fname)


def test_parse():
    fname = get_data_path('config.yml')
    cmds = cmd_config.parser.parse(fname)
    assert {'pyinstaller001', 'celery001', 'list'} == set(cmds.keys())
    assert cmds['pyinstaller001'] == ['pyinstaller', '-i', '-y', '--file-name', 'bbb', '--group-name', 'g1,g2', 'aaa']
    assert cmds['celery001'] == ['celery', '--app=main.celery', 'worker', '--queues=queue1 queue2', '--concurrency=3']
    assert cmds['list'] == ['ls', '-a', '-l']
