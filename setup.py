from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name             = 'Garbage Monitoring Simple',
    version          = '0.1.0',
    description      = 'Collected waste: inventory.',
    long_description = readme,
    author           = 'Maris Svirksts',
    author_email     = 'maris.svirksts@gmail.com',
    url              = 'https://github.com/maris-svirksts',
    license          = license,
    packages         = find_packages(exclude=('tests', 'docs'))
)

