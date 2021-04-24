from setuptools import setup, find_packages

setup(
    name="AGUC8",
    version="0.1",
    description="ARTIQ support for Newport AGUC8 piez motor controller",
    author="OregonIons",
    url="https://github.com/OregonIons/AGUC8",
    download_url="https://github.com/OregonIons/AGUC8",
    install_requires=["sipyco", "pyserial"],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "aqctl_AGUC8 = AGUC8.aqctl_AGUC8:main",
        ],
    },
)
