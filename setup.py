import os
from pathlib import Path

from setuptools import setup, find_packages

HERE = Path(__file__).resolve().parent

version_re = re.compile(r"^__version__\s*=\s*'(?P<version>.*)'$", re.M)
def version():
    match = version_re.search(Path('larc/__init__.py').read_text())
    if match:
        return match.groupdict()['version'].strip()
    return '0.0.1'

# long_description = Path(HERE,'README.rst').resolve().read_text()
long_description = Path(HERE,'README.md').resolve().read_text()

def all_ext(path, ext):
    for root, dirs, files in os.walk(path):
        if any(n.endswith('.coco') for n in files):
            yield str(Path(root, '*.coco'))

setup(
    name='jascobin',
    packages=find_packages(
        exclude=['config', 'tests'],
    ),
    package_dir={
        'jascobin': 'jascobin',
    },

    # package_data={
    #     'jascobin': [
    #     ],
    # },
    # include_package_data=True,

    install_requires=[
        'toolz',
        'multipledispatch',
        'olefile',
        'click',
    ]

    version=version(),
    description='Jasco binary data parsing',
    long_description=long_description,

    url='https://bitbucket.org/lowloandresearch/jascobin',

    author='Lowland Applied Research Company (LARC)',
    author_email='dogwynn@lowlandresearch.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.7',
    ],

    zip_safe=False,

    keywords=('jasco jws dichroism spectroscopy'),

    scripts=[
    ],

    entry_points={
        'console_scripts': [
            'jascobin=jascobin.command:main'
        ],
    },
)
