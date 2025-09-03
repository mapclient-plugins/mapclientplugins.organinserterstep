from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import io

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))


# List all of your Python package dependencies in the
# requirements.txt file


def readfile(filename, split=False):
    with io.open(filename, encoding="utf-8") as stream:
        if split:
            return stream.read().split("\n")
        return stream.read()


readme = readfile("README.rst", split=True)[3:]  # skip title
# For requirements not hosted on PyPi place listings
# into the 'requirements.txt' file.
requires = [
    "ssvtools",
    "cmlibs.zinc >= 4.2.1",
    "PySide6",
    "cmlibs.utils >= 0.13.0",
    "scaffoldfitter >= 0.11.2"
]  # minimal requirements listing
source_license = readfile("LICENSE")


class InstallCommand(install):

    def run(self):
        install.run(self)
        # Automatically install requirements from requirements.txt
        import subprocess
        subprocess.call(['pip', 'install', '-r', os.path.join(SETUP_DIR, 'requirements.txt')])


setup(
    name='mapclientplugins.organinserterstep',
    version='0.1.0',
    description='MAP Client plugin for embedding organ system in the scaffold using markers.',
    long_description='\n'.join(readme) + source_license,
    long_description_content_type='text/x-rst',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
    ],
    cmdclass={'install': InstallCommand,},
    author='Elias Soltani',
    author_email='',
    url='https://github.com/mapclient-plugins/mapclientplugins.organinserterstep.git',
    packages=find_packages(exclude=['ez_setup',]),
    namespace_packages=['mapclientplugins'],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
)
