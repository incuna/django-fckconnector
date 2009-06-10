# XXX license header here

from setuptools import setup, find_packages

setup(
    name = "fckeditor.connector",
    version = "0.1",
    packages = find_packages('src'),
    package_dir = {'':'src'},

    # scripts and dependencies
    include_package_data = True,
    namespace_packages = ['fckeditor'],
    zip_safe = True,

    # author metadata
    author = 'Nathan R. Yergler',
    author_email = 'nathan@yergler.net',
    description = '.',
    license = 'GNU LGPL',
    url = 'http://code.google.com/p/django-fckconnector/',

    )