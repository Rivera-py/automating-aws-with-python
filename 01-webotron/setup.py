# -*- coding: utf-8 -*-

"""Turn our code into a wheel."""


from setuptools import setup


setup(
    name='webotron-80',
    version='0.1',
    author='Jack Rivera',
    author_email='Jaluri@outlook.com',
    description='Webotron 80 is a tool to deploy static websties to AWS.',
    license='GPLv3',
    packages=['webotron'],
    url='https://github.com/Rivera-py/automating-aws-with-python',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        webotron=webotron.webotron:cli
    '''
)
