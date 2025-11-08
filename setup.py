'''
A script to create a pip release of the SkillMetrics package.

Description of the package can be found in the wiki:
https://github.com/PeterRochford/SkillMetrics/wiki

Created on Aug 22, 2023

@author: Peter Rochford
'''
from setuptools import setup, find_packages

setup(
    name='SkillMetrics',
    version='1.2.3',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'numpy',
        'pandas',
        'xlsxwriter'
    ],
    author='Peter Rochford',
    author_email='rochford.peter1@gmail.com',
    description='A Python library for calculating and displaying the skill of model predictions against observations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/PeterRochford/SkillMetrics/tree/master',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.11',
    ],
)
