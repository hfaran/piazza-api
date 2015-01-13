# piazza-api

[![PyPI version](https://badge.fury.io/py/piazza-api.png)](http://badge.fury.io/py/piazza-api)

Unofficial Client for Piazza's Internal API


## Usage

```python
>>> from piazza_api import Piazza
>>> p = Piazza()
>>> p.user_login()
Email: ...
Password: ...

>>> user_profile = p.get_user_profile()

>>> eece210 = p.network("hl5qm84dl4t3x2")

>>> eece210.get_post(100)
...

>>> posts = eece210.iter_all_posts(limit=10)
>>> for post in posts:
...     do_awesome_thing(post)

>>> users = eece210.get_users(["userid1", "userid2"])
>>> all_users = eece210.get_all_users()
```

Above are some examples to get started; more in the documentation (which is coming soon; 
but the code is all Sphinx-style documented and is fairly readable).

You can also use the "internal" PiazzaRPC class which maps more directly
to Piazza's API itself but is not as nice and as intuitive to use as the
`Piazza` class abstraction.

```python
>>> from piazza_api.rpc import PiazzaRPC
>>> p = PiazzaRPC("hl5qm84dl4t3x2")
>>> p.user_login()
Email: ...
Password: ...
>>> p.content_get(181)
...
>>> p.add_students(["student@example.com", "anotherStudent@example.com"])
...
```


## Installation

You've seen this before and you'll see it again.

```bash
# The easy way
sudo pip install piazza-api
```

```bash
# The developer way
git clone https://github.com/hfaran/piazza-api
cd piazza-api
sudo python setup.py install
```

## Contribute

* [Issue Tracker](https://github.com/hfaran/piazza-api/issues)
* [Source Code](https://github.com/hfaran/piazza-api)

### Commit Message Guidelines

Commit messages should be written with the following style: `%{type}(%{scope}): %{description}`.

* Valid `type`s are
  - `feat`
  - `fix`
  - `docs`
  - `style`
  - `refactor`
  - `perf`
  - `test`
  - `revert`

* Valid `scope`s are
  - `dev` (if the change is irrevelant to the user or otherwise has no impact on the top-level API and only to developers)
  - `user` (if this commit is a change that affects the top-level user-facing interface)

* `description` is the actual commit message 


## License

This project is licensed under the MIT License.


## Disclaimer

This is not an official API. I am not affiliated with Piazza Technologies Inc. 
in any way, and am not responsible for any damage that could be done with it. 
Use it at your own risk.
