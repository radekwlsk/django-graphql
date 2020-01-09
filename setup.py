import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-tenc-graphene',
    version='0.5',
    license='BSD 3-Clause License',
    description='Django app adding Django-Graphene with some initial work and easy configuration.',
    long_description=README,
    author='10Clouds - Dream Team',
    author_email='radoslaw.kowalski@10clouds.com',
    install_requires=[
        'django',
        'graphene_django',
    ],
    packages=find_packages(exclude=['tests', 'tests.py', 'requirements']),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD 3-Clause License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: GraphQL',
    ],
)
