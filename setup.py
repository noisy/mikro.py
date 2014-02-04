from setuptools import setup

setup(
    name='mikro.py',
    version='0.1.0',
    author='@noisy - Krzysztof Szumny',
    author_email='noisy.pl@gmail.com',
    scripts=['scripts/mikro.py'],
    url='https://github.com/noisy/mikro.py/',
    license='LICENSE.txt',
    description='Command line tool for sending messages for http://wykop.pl/mikroblog/ .',
    long_description=open('README.md').read(),
    install_requires=[
       "wykop-sdk>=0.1.1"
    ],
)
