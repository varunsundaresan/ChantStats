import matplotlib.pyplot as plt
import numpy as np
import os
import sh
import shutil
from enum import Enum
from .logging import logger

__all__ = ["EnumWithDescription", "remove_file_or_folder_if_exists", "plot_empty_figure"]


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
    res = sh.tree(_env={}).stdout.decode("utf-8")
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
            # logger.warning(f"Aborting because {file_or_folder} already exists: {path}")
            raise IOError(
                f"Aborting because {file_or_folder} already exists: {path} (use `force=True` to remove anyway)"
            )


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


def get_subsample(values, fraction, seed, sort_key=None):
    """
    Return a sub-sample of the given input values.
    """
    assert 0.0 <= fraction <= 1.0
    if fraction == 1.0:
        logger.info("Not doing any sub-sampling.")
        return values
    else:
        if seed is None:
            raise ValueError("Must provide a sampling seed.")

        np.random.seed(seed)
        num_values = len(values)
        sample_size = int(len(values) * fraction)
        logger.info(f"Extracting sub-sample using {sample_size} out of {num_values} values (seed={seed}).")
        perm = np.random.permutation(num_values)
        sample_indices = sorted(perm[:sample_size])
        return sorted(np.take(values, sample_indices), key=sort_key)


def plot_empty_figure(msg_text, fontsize=20, figsize=(20, 4)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.text(0.5, 0.5, msg_text, fontsize=fontsize, color="gray", ha="center", va="center", alpha=1.0)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.close(fig)
    return fig
