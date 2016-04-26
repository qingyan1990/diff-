from setuptools import setup


setup(
    name='pydiff',
    version='0.1',
    author='Qingyan',
    description=('A structural differencer for Python. '
                 'Parses Python into ASTs, compares them, '
                 'and generates interactive HTML.'),
    packages=['pydiff'],
    package_dir={'pydiff': '.'},
    package_data={'pydiff': ['diff.css', 'nav.js']},
    license='GNU GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved'
        ' :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ]
)
