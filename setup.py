from setuptools import setup, find_packages


__version__ = 0.1

with open("readme.md", "r") as f:
    long_description = f.read()

setup(
    name="PUtils",
    version=__version__,
    author="Ty Gillespie",
    author_email="tygillespie6@gmail.com",
    description="A huge library of Python functions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/trypolis/putils",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3",
)
