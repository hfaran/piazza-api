# Release
1) Update `__version__` in `piazza_api/__init__.py` to the new version
2) Commit this change as "Release 0.9.0" to master, as an example
3) Create a release on GitHub with the new version (e.g., 0.9.0) targeting master

## Build and Publish

### Automated

4) Ensure the deploy Github Action succeeds, or

### Manual

4) `git pull` locally
5) Run  `publish.bat` (in the correct environment) to create the package to upload
