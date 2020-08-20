from setuptools import setup, find_packages

setup(
    name="AGUC8",
    install_requires=["sipyco", "pyserial"],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "aqctl_AGUC8 = AGUC8.aqctl_AGUC8:main",
        ],
    },
)