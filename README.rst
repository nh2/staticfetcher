staticfetcher
=============

Fetches static files.

Example
-------

::

    STATICS = {
        'jquery/jquery.js': 'http://code.jquery.com/jquery.min.js',
        'underscore.js':    'http://documentcloud.github.com/underscore/underscore.js',
    }

    from staticfetcher import Staticfetcher

    Staticfetcher(STATICS, root_dir='js').fetch(force=False)

License
-------

staticfetcher is MIT licensed.
