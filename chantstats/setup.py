import versioneer

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Read long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="chantstats",
    version=versioneer.get_version(),
    description="",
    long_description=long_description,
    url="https://github.com/maxalbert/chantstats",
    author="Maximilian Albert",
    author_email="maximilian.albert@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Other/Nonlisted Topic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(),
    install_requires=["matplotlib", "music21", "pandas", "scipy", "tqdm", "palettable"],
    extras_require={"dev": [], "test": ["pytest", "pytest-cov"]},
    cmdclass=versioneer.get_cmdclass(),
)
