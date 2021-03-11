project = abjadext
formatPaths = ${project}/ tests/ *.py

black-check:
	black --check --diff --target-version=py38 .

black-reformat:
	black --target-version=py38 .

build:
	python setup.py sdist

clean:
	find . -name '*.pyc' | xargs rm
	find . -name __pycache__ | xargs rm -Rf
	rm -Rif *.egg-info/
	rm -Rif .cache/
	rm -Rif .tox/
	rm -Rif build/
	rm -Rif dist/
	rm -Rif htmlcov/
	rm -Rif prof/

flake_ignore = --ignore=E203,E266,E501,W503
flake_options = --isolated --max-line-length=88
flake8-check:
	flake8 ${flake_ignore} ${flake_options}

isort-check:
	isort \
	--case-sensitive \
	--check-only \
	--diff \
	--line-width=88 \
	--multi-line=3 \
	--project=abjad \
	--thirdparty=uqbar \
	--trailing-comma \
	--use-parentheses \
	${formatPaths}

isort-reformat:
	isort \
	--case-sensitive \
	--line-width=88 \
	--multi-line=3 \
	--project=abjad \
	--thirdparty=uqbar \
	--trailing-comma \
	--use-parentheses \
	${formatPaths}

jupyter-test:
	jupyter nbconvert --to=html --ExecutePreprocessor.enabled=True tests/test.ipynb

mypy:
	mypy ${project}/

reformat:
	black-reformat
	isort-reformat

release: docs clean build
	pip install -U twine
	twine upload dist/*.tar.gz
	make gh-pages

check:
	make black-check
	make flake8-check
	make isort-check
	make mypy

test:
	make check
	make jupyter-test
