.PHONY: docs tests build upload

tests:
	python setup.py test

docs:
	$(MAKE) -C docs html

build:
	python setup.py sdist bdist_wheel

upload:
	python -m twine upload --username __token__ dist/*$(VERSION)*