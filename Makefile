clean:
	@find . -iname '*.orig' -delete 
	@find . -iname '*.pyc' -delete
	@find . -iname '*~' -delete
	@rm -rf dist
	@rm -rf python-wtf.egg-info

test:
	@for testfile in *_test.py; do \
		echo Running tests in $$testfile...; \
		python ./$$testfile; done

#publish:
#	@ipython register.py
