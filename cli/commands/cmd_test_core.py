import os
import subprocess

import click


@click.command()
@click.argument('path', default=os.path.join('app', 'tests'))
def cli(path):
    """
    Run tests.

    :param path: Test path
    :return: Subprocess call result
    """
    cmd = f'test_core.py {path}'
    return subprocess.call(cmd, shell=True)
