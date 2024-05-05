from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='Pyamp',
    version='1.0.0',
    package_dir={'': 'src/'},
    packages=find_packages(where='src/'),
    install_requires=requirements,
    python_requires=">=3.11",
    author='Ignacio Gonsalves',
    description='Minimal MPD client written in Python using Qt',
    license='GPL-3.0',
    long_description=open('README.md').read(),
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
        ],
    },
)
