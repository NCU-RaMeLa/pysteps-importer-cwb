# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

# Add the plugin dependencies here
requirements = []

# Add the packages needed to build the package.
setup_requirements = ['pytest-runner']

test_requirements = ['pytest>=3']

setup(
    author="zouihao",
    author_email='zouihao127@ntu.edu.tw',
    python_requires='>=3.6',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Read CWB composite radar data.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    test_suite='tests',
    tests_require=test_requirements,
    include_package_data=True,
    keywords=['pysteps_importer_cwb', 'pysteps' , 'plugin', 'importer'],
    name='pysteps-importer-cwb',
    packages=find_packages(),
    setup_requires=setup_requirements,
    # Entry points
    # ~~~~~~~~~~~~
    #
    # This is the most important part of the plugin setup script.
    # Entry points are a mechanism for an installed python distribution to advertise
    # some of the components installed (packages, modules, and scripts) to other
    # applications (in our case, pysteps).
    # https://packaging.python.org/specifications/entry-points/
    #
    # An entry point is defined by three properties:
    # - The group that an entry point belongs indicate the kind of functionality that
    #   provides. For the pysteps importers use the "pysteps.plugins.importers" group.
    # - The unique name that is used to identify this entry point in the
    #   "pysteps.plugins.importers" group.
    # - A reference to a Python object. For the pysteps importers, the object should
    #   point to a importer function, and should have the following form:
    #   package_name.module:function.
    # The setup script uses a dictionary mapping the entry point group names to a list
    # of strings defining the importers provided by this package (our plugin).
    # The general form of the entry points dictionary is:
    # entry_points={
    #     "group_name": [
    #         "entry_point_name=package_name.module:function",
    #         "entry_point_name=package_name.module:function2",
    #     ]
    # },
    entry_points={
        'pysteps.plugins.importers': [
            'importer_cwb_compref_xxx=pysteps_importer_cwb.importer_cwb_compref:importer_cwb_compref_xxx',
            # Add additional importers if needed.
        ]
    },
    version='0.1.0',
    zip_safe=False,
)
