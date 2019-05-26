import numpy as np
import os
import sh
import shutil
from enum import Enum
from .logging import logger

__all__ = ["EnumWithDescription", "remove_file_or_folder_if_exists"]


def is_close_to_zero_or_100(x):
    return np.isclose(x, 0.0) or np.isclose(x, 100.0)


def list_directory_tree(root_dir):
    """
    List contents of `root_dir` in a tree-like format.

    Returns
    -------
    str
    """
    if not os.path.exists(root_dir):
        logger.error(f"Cannot list tree under non-existent directory: '{root_dir}'")
        return
    cwd = os.getcwd()
    os.chdir(root_dir)
    res = sh.tree().stdout.decode("utf-8")
    os.chdir(cwd)
    return res


def remove_file_or_folder_if_exists(path, force=False):
    if os.path.isfile(path):
        file_or_folder = "file"
        func_remove = os.remove
    elif os.path.isdir(path):
        file_or_folder = "folder"
        func_remove = shutil.rmtree
    else:
        raise NotImplementedError(f"Path is neither a file nor a folder: {path}")

    if os.path.exists(path):
        if force:
            logger.warn(f"Removing existing {file_or_folder}: {path}")
            func_remove(path)
        else:
            logger.warning(f"Aborting because {file_or_folder} already exists: {path}")
            return


class EnumWithDescription(str, Enum):
    def __new__(cls, name, desc, **kwargs):
        obj = str.__new__(cls, name)
        obj._value_ = name
        obj._description = desc
        return obj

    @property
    def description(self) -> str:
        """
        Returns
        -------
        str
            Long form description of this enum suitable for use in plot titles etc.
        """
        return self._description
