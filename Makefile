clean:
	@find . -iname '*.orig' -delete 
	@find . -iname '*.pyc' -delete
	@find . -iname '*~' -delete
	@rm -rf dist
	@rm -rf python-wtf.egg-info

#publish:
#	@ipython register.py
