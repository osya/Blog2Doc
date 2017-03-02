# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pip.req import parse_requirements

requirements = parse_requirements("requirements.txt", session="")
setup(
        name='Blog2DocScrapy',
        version='',
        description='',
        author='Valeriy Osipov',
        author_email='info@vosipov.com',
        packages=find_packages(),
        zip_safe=False,
        include_package_data=True,
        install_requires=[str(ir.req) for ir in requirements],
        dependency_links=[str(ir._link) for ir in requirements if ir._link]
)
