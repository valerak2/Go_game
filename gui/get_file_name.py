import pathlib
from pathlib import Path

def click_sound_path():
    dir_path = pathlib.Path.cwd()
    path = Path(dir_path, 'audio', 'click.wav')
    return path


def no_click_sound_path():
    dir_path = pathlib.Path.cwd()
    path = Path(dir_path, 'audio', 'no_click.wav')
    return path


def party_log_path():
    dir_path = pathlib.Path.cwd()
    path = Path(dir_path, 'party_log.txt')
    return path


def table_record_path():
    dir_path = pathlib.Path.cwd()
    path = Path(dir_path, 'table_record.txt')
    return path
