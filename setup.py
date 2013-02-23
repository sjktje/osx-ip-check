from distutils.core import setup

setup(
    name='osx-ip-check',
    version='0.1.0',
    author='Svante J. Kvarnström',
    author_email='sjk@ankeborg.nu',
    packages=['ipcheck'],
    scripts=['bin/ipcheck'],
    description='Check if IP has updated and e-mail changes',
)
