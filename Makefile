# An example Makefile that downloads the staticfetcher.
# It assumes your statics file (see example in README) is called statics.py.
# Extend it to your own project, if you like.

staticfetcher.py:
	wget https://raw.github.com/nh2/staticfetcher/master/staticfetcher.py

.PHONY: statics_fetch statics_fetch_force statics_clean

statics_fetch: staticfetcher.py
	python statics.py fetch

statics_fetch_force: staticfetcher.py
	python statics.py fetch --force

statics_clean: staticfetcher.py
	python statics.py clean
