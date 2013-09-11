SHELL := /bin/bash
TESTS=$(shell find tests/ -name "*.py")
VERSION=$(shell python -c "import trebuchet.lib; print trebuchet.lib.get_version()")

version:
	@echo ${VERSION}

release:
	python setup.py sdist upload -r pypi && git tag ${VERSION} && git push upstream --tags
