#!/usr/bin/env python
"""
Fetches static files.

Example:

	import staticfetcher

	STATICS = {
		'jquery/jquery.js': 'http://code.jquery.com/jquery.min.js',
		'underscore.js':    'http://documentcloud.github.com/underscore/underscore.js',
	}

	staticfetcher.fetch(STATICS, root_dir='js', force=False)
"""

from __future__ import print_function
import os
import urllib

__author__ = 'Niklas Hambuechen'
__license__ = 'MIT'

__all__ = ['fetch', 'clean']


def makedirs(f):
	""" Recursively creates the directory structure leading to file f."""
	target_dir = os.path.dirname(f)
	if not os.path.exists(target_dir):
		os.makedirs(target_dir)


def static_path(root_dir, target):
	return os.path.relpath(os.path.realpath(os.path.join(root_dir, target)))


def fetch(statics, root_dir='.', force=False):
	"""
	Fetches the given dictionary of static files and puts them into root_dir.
	The directory hierarchy for the static files will be created automatically.

	Args:
		statics (dict): Dictionary mapping from target file name to the URL from which to get the file.

	Kwargs:
		root_dir (string): The top-level directory under which to put the static files.
		force (bool): Download files even if they already exist.
	"""

	realstatics = dict( (static_path(root_dir, target), url) for (target, url) in statics.items() )

	print("Fetching static files (%s)..." % ("force download all" if force else "only nonexistent ones"))
	for target, source in realstatics.items():
		if force or not os.path.exists(target):
			makedirs(target)
			print("  %s <- %s" % (target, source))
			urllib.urlretrieve(source, target)


def clean(statics, root_dir='.'):
	"""
	Removes the files in the the given iterable.
	Directories will not be deleted.

	Args:
		statics: Iterable (e.g. list or dict) mapping from target file name to the URL from which to get the file.

	Kwargs:
		root_dir (string): The top-level directory under which to put the static files.
	"""
	print("Cleaning static files...")
	for target in ( static_path(root_dir, t) for t in statics ):
		if os.path.exists(target):
			print("  rm %s" % target)
			os.remove(target)
