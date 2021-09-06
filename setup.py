import os
import codecs
import setuptools


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as file_:
        return file_.read()


def get_version():
    for line in read('mmmm/main.py').splitlines():
        if line.startswith('__version__'):
            return line.split("'")[1]
    raise Exception()


def long_description():
    with open('README.md', 'r') as file_:
        lines = []
        cut = False
        for line in file_.readlines():
            if '<!-- end -->' in line:
                cut = False
                continue
            if '<!-- cut -->' in line:
                cut = True
                continue
            if not cut:
                lines.append(line)
        return ''.join(lines)


setuptools.setup(
    name='mmmm',
    version=get_version(),
    author='igrmk',
    author_email='igrmkx@gmail.com',
    description='Google My Maps to MAPS.ME KML converter',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/igrmk/mmmm',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',
    entry_points={'console_scripts': ['mmmm = mmmm:main']},
    install_requires=['lxml'],
)
