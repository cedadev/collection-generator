#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

__author__ = "Richard Smith"
__contact__ = "richard.d.smith@stfc.ac.uk"
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [line.strip() for line in open("requirements.txt")]

dev_requirements = [line.strip() for line in open("requirements_dev.txt")]

test_requirements = ['pytest>=3', ]

docs_requirements = [
    "sphinx",
    "sphinx-rtd-theme",
    "nbsphinx",
    "pandoc",
    "ipython",
    "ipykernel",
    "jupyter_client"
]

setup(
    author=__author__,
    author_email=__contact__,
    python_requires='>=3.6',
    setup_requires = ['setuptools_scm'],
    use_scm_version=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Security',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    description="Generate and update collections based on item-descriptions",
    install_requires=[
        'asset_scanner',
        'elasticsearch'
    ],
    license=__license__,
    long_description=readme,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    keywords='collection_generator',
    name='collection_generator',
    packages=find_packages(include=['collection_generator', 'collection_generator.*']),
    test_suite='tests',
    tests_require=test_requirements,
    extras_require={
        "docs": docs_requirements,
        "dev": dev_requirements,
    },
    url='https://github.com/rsmith013/collection_generator',
    zip_safe=False,
    entry_points={
        'asset_scanner.extractors': [
            'collection_generator = collection_generator:CollectionGenerator',
        ],
        'asset_scanner.input_plugins': [
            'collection_id = collection_generator.plugins.inputs.collection_id:CollectionIDInputPlugin'
        ],
        "collection_generator.processors": [
            "elasticsearch_aggregator = collection_generator.plugins.processors.elasticsearch_aggregator:ElasticsearchAggregator",
            "json_aggregator = collection_generator.plugins.processors.json_aggregator:JSONAggregator"
        ],
    }
)
