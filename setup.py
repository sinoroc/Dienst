""" Setup script
"""


import setuptools


PROJECT = 'Dienst'

VERSION = '0.0.0'

INSTALL_REQUIREMENTS = [
    'pyramid',
    'PyYAML',
    'venusian',
    'zope.interface',
]

TEST_REQUIREMENTS = [
    'pytest',
    'WebTest',
]

SOURCE_DIRECTORY = 'src'

PACKAGES = setuptools.find_packages(SOURCE_DIRECTORY)

PACKAGE_DIRECTORIES = {
    '': SOURCE_DIRECTORY,
}


setuptools.setup(
    name=PROJECT,
    version=VERSION,
    packages=PACKAGES,
    package_dir=PACKAGE_DIRECTORIES,
    install_requires=INSTALL_REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
)


# EOF
