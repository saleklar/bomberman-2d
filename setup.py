from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bomberman-2d",
    version="1.0.0",
    author="Bomberman Developer",
    description="A fun 2D Bomberman game with AI and multiplayer modes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bomberman-2d",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Topic :: Games/Entertainment",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pygame>=2.0",
    ],
    entry_points={
        "console_scripts": [
            "bomberman=bomberman_2d.main:main",
        ],
    },
)
