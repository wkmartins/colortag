from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Python library for adding ANSI colors to the terminal output using a simple syntax'

setup(
    name="colortag",
    version=VERSION,
    author="Wagner Kauê",
    author_email="<wkmartinst@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'ansi', 'colors', 'color', 'terminal'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
