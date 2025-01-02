from setuptools import setup, find_packages # pylint: disable=E0401
from __version__ import __version__


with open('requirements.txt', encoding='UTF-8') as f:
    requirements = f.read().splitlines()

setup(
    name='Pyamp',
    version=__version__,
    package_dir={'': 'src/'},
    packages=find_packages(where='src/'),
    package_data={'resources': ['themes/main/*.css', 'themes/mpipe/*.css', 'themes/metal/*.css']},
    install_requires=requirements,
    python_requires=">=3.13.1",
    author='Ignacio Gonsalves',
    description='Minimal MPD client written in Python using Qt',
    license='GPL-3.0',
    long_description=open('README.md', encoding='UTF-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/themidnightmaniac/pyamp',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
    ],
    entry_points={
        'console_scripts': [
            'pyamp = pyamp.main:main',
        ]
    },
)
