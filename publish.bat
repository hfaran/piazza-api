REM Building dist package
python setup.py sdist bdist_wheel
REM Uploading to PyPI
twine check dist/*
twine upload dist/*
REM Removing dist/ directory
rd /s /q dist\
