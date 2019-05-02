import os
import sh

from .logging import logger

__all__ = ["list_directory_tree"]


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
