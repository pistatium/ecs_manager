VERSION=$(python setup.py  --version)
python setup.py sdist bdist_wheel --universal
twine upload dist/ecs_manager-${VERSION}*
