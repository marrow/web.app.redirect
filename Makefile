PROJECT = web.app.redirect
USE = development

.PHONY: all develop clean veryclean serve shell test release

all: clean develop test

develop: ${PROJECT}.egg-info/PKG-INFO

clean:
	find . -name __pycache__ -exec rm -rfv {} +
	find . -iname \*.pyc -exec rm -fv {} +
	find . -iname \*.pyo -exec rm -fv {} +
	rm -rvf build htmlcov

veryclean: clean
	pip uninstall -y ${PROJECT}
	rm -rvf *.egg-info .packaging/*
	pip freeze | grep '==' | xargs pip uninstall -y

serve: develop
	@clear
	@python -m web.app.redirect

shell: develop
	@clear
	@python -m web.app.redirect -i

test: develop
	@clear
	@pytest

release:
	./setup.py sdist bdist_wheel upload ${RELEASE_OPTIONS}
	@echo -e "\nView online at: https://pypi.python.org/pypi/${PROJECT} or https://pypi.org/project/${PROJECT}/"
	@echo -e "Remember to make a release announcement and upload contents of .packaging/release/ folder as a Release on GitHub.\n"

${PROJECT}.egg-info/PKG-INFO: setup.py setup.cfg
	@mkdir -p ${VIRTUAL_ENV}/lib/pip-cache
	pip install --cache-dir "${VIRTUAL_ENV}/lib/pip-cache" -Ue ".[${USE}]"
