from setuptools import setup

setup(
    name='pymoney',
    version='0.2',
    py_modules=['pymoney'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        pymoney=pymoney:cli
    ''',
)