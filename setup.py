#!/usr/bin/env python3

import os
import sys
import codecs

try:
	from setuptools.core import setup, find_packages
except ImportError:
	from setuptools import setup, find_packages

if sys.version_info < (3, 4):
	raise SystemExit("Python 3.4 or later is required.")

version = description = url = author = ''  # Actually loaded on the next line; be quiet, linter.
exec(open(os.path.join("web", "app", "redirect", "release.py")).read())

here = os.path.abspath(os.path.dirname(__file__))

tests_require = [
		'pytest',  # test collector and extensible runner
		'pytest-cov',  # coverage reporting
		'pytest-flakes',  # syntax validation
		'pytest-catchlog',  # log capture
		'pytest-isort',  # import ordering
	]


setup(
	name = "web.app.redirect",
	version = version,
	description = description,
	long_description = codecs.open(os.path.join(here, 'README.rst'), 'r', 'utf8').read(),
	url = url,
	author = author.name,
	author_email = author.email,
	license = 'MIT',
	keywords = ['CleverCloud', 'webapp', 'sample', 'microservice', 'http', 'redirection', '302'],
	classifiers = [
			"Intended Audience :: Developers",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Programming Language :: Python",
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.4",
			"Programming Language :: Python :: 3.5",
			"Programming Language :: Python :: 3.6",
			"Programming Language :: Python :: Implementation :: CPython",
			"Programming Language :: Python :: Implementation :: PyPy",
			"Topic :: Software Development :: Libraries :: Python Modules",
			"Topic :: Utilities"
		],
	
	packages = find_packages(exclude=['test', 'example', 'benchmark', 'htmlcov']),
	include_package_data = True,
	package_data = {'': ['README.rst', 'LICENSE.txt']},
	namespace_packages = ['web', 'web.app'],
	zip_safe = False,
	
	setup_requires = [
			'pytest-runner',
		] if {'pytest', 'test', 'ptr'}.intersection(sys.argv) else [],
	
	install_requires = [
			'uri>=2.0.0,<3.0.0',  # Generic URI datastructure.
			'marrow.package>=1.1.0,<2.0.0',  # Plugin discovery and loading.
			'marrow.mongo[logger]>=1.1.2,<2.0.0',  # Database Access Object layer.
			'waitress',  # "Production" quality HTTP server for use with reverse proxies.
			'web.dispatch.resource',  # URL to endpoint lookup mechanism.
			'cinje',  # Template engine domain-specific language (DSL).
		],
	
	tests_require = tests_require,
	
	entry_points = {
				'marrow.mongo.document': [  # Document classes registered by name.
						# 'RedirectionDomain = web.app.redirect.model:Domain',
					],
			},
)
