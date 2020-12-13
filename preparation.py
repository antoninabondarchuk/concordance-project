import glob
import os
import platform
import sys
from pathvalidate import ValidationError, validate_pathtype


def get_raw_path(path):
    """
    Checks if path is valid and converts it to compatible string.
    Args:
        path (str): absolute path to directory or file.
    Raises:
        ValidationError if path or system is wrong.

    Returns:
        Raw path as String.
    """
    try:
        validate_pathtype(path)
        dir_name_path = os.path.normpath(path)
        if platform.system() == 'Windows':
            dir_name_path = dir_name_path + '\\'
        elif platform.system() in ('Linux', 'Darwin'):
            dir_name_path = dir_name_path + '/'
        return dir_name_path
    except (ValidationError, OSError) as e:
        print(f"{e}\n", file=sys.stderr)


def read_all_txt_from_dir(read_path):
    """
    Reads from dir all files with .txt extensions.
    Args:
        read_path (str): absolute validated path to directory or file.

    Returns:
        List of absolute path of txt files to read from in alphabet order.
    """
    read_files = glob.glob(f'{read_path}*.txt')
    return read_files
