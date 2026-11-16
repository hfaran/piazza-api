# Release
1) Update `__version__` in `piazza_api/__init__.py` to the new version
2) Commit this change as "Release 0.9.0" to develop, as an example
3) Create a release on GitHub with the new version (e.g., 0.9.0) targeting develop

## Build and Publish

### Automated

4) Ensure the deploy Github Action succeeds, or

The deploy action (`python-publish.yml`) publishes with
[Trusted Publishing](https://docs.pypi.org/trusted-publishers/) from this repo's `pypi`
environment, so no PyPI token is stored in GitHub. If the workflow file or the
environment is renamed, update the publisher in the PyPI project's Settings → Publishing
first.

### Manual

Publishing from your own machine needs a PyPI API token. Only the GitHub Action can
publish without one.

4) `git pull` locally
5) `pip install -r dev-requirements.txt` to get `twine` and `wheel`
6) Create an API token at https://pypi.org/manage/account/token/ with the scope
   "Project: piazza-api". Don't use an all-projects token.
7) Run `publish.bat` (Windows) to build, check and upload the package. On macOS or Linux,
   run its commands by hand:
   ```sh
   python setup.py sdist bdist_wheel
   twine check dist/*
   twine upload dist/*
   rm -rf dist
   ```
   When twine prompts, enter the token as the password, and `__token__` if it asks for a
   username. To skip the prompt, set `TWINE_USERNAME=__token__` and
   `TWINE_PASSWORD=<token>` first.

   Delete the token on PyPI when you no longer need it.
