flake:
	flake8 *.py
	flake8 examples/*.py

clean:
	find . -type f -name '*.py[co]' -delete
