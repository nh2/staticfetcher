#!/usr/bin/env python
"""
Fetches static files.

Example:

	from staticfetcher import Staticfetcher

	STATICS = {
		'jquery/jquery.js': 'http://code.jquery.com/jquery.min.js',
		'underscore.js':    'http://documentcloud.github.com/underscore/underscore.js',
	}

	Staticfetcher(STATICS, root_dir='js').fetch(force=False)
"""

from __future__ import print_function
import os
import urllib

__author__ = 'Niklas Hambuechen'
__license__ = 'MIT'

__all__ = ['Staticfetcher']


def makedirs(f):
	""" Recursively creates the directory structure leading to file f."""
	target_dir = os.path.dirname(f)
	if not os.path.exists(target_dir):
		os.makedirs(target_dir)


class Staticfetcher(object):

	def __init__(self, statics, root_dir='.'):
		"""
		Creates a Staticfetcher to handle files given in static which shall be located under root_dir.

		Args:
			statics (dict): Dictionary mapping from target file name to the URL from which to get the file.

		Kwargs:
			root_dir (string): The top-level directory under which the static files are placed.
		"""
		self.statics = statics
		self.root_dir = root_dir


	def static_path(self, target):
		return os.path.relpath(os.path.realpath(os.path.join(self.root_dir, target)))


	def fetch(self, force=False):
		"""
		Fetches the content of the staticfetcher.
		The directory hierarchy for the static files will be created automatically.

		Kwargs:
			force (bool): Download files even if they already exist.
		"""
		realstatics = dict( (self.static_path(target), url) for (target, url) in self.statics.items() )

		print("Fetching static files (%s)..." % ("force download all" if force else "only nonexistent ones"))
		for target, source in realstatics.items():
			if force or not os.path.exists(target):
				makedirs(target)
				print("  %s <- %s" % (target, source))
				urllib.urlretrieve(source, target)
			else:
				print("  %s (existing)" % target)


	def clean(self):
		"""
		Removes all files managed by this Staticfetcher.
		Directories will not be deleted.
		"""
		print("Cleaning static files...")
		for target in map(self.static_path, self.statics):
			if os.path.exists(target):
				print("  rm %s" % target)
				os.remove(target)

	def run(self):
		"""
		Convenience sub-program that runs an argument parser and fetch static files.

		Example usage:
			from staticfetcher import Staticfetcher
			Staticfetcher(my_statics, root_dir='.').run()

		Example invocation:
			python statics.py fetch
			python statics.py fetch --force
			python statics.py clean
		"""
		import argparse

		parser = argparse.ArgumentParser(description='Fetches static files')

		subparsers = parser.add_subparsers(dest='subparser_name', help='Action to run')

		fetch_parser = subparsers.add_parser('fetch', help='Fetch static files')
		clean_parser = subparsers.add_parser('clean', help='Deletes static files')

		fetch_parser.add_argument('--force', action='store_true', default=False, help='Fetches even already existing files.')

		args = parser.parse_args()

		if args.subparser_name == 'fetch':
			self.fetch(args.force)
		elif args.subparser_name == 'clean':
			self.clean()
