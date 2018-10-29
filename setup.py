import os
from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='SomfyOpenAPI',
    version='0.1',
    description='A Somfy Open API library',
    long_description=os.path.join(here, 'README.md'),
    author='ETIENNE Thibaut',
    url='https://github.com/tetienne/somfy-open-api',
    license='GNU General Public License v3.0',
    python_requires='>=3.4',
    install_requires=['requests-oauthlib', 'typing']
)
