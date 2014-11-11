# piazza-api

Unofficial Client for Piazza's Internal API

## Setup

```bash
git clone https://github.com/hfaran/piazza-api
cd piazza-api
sudo python setup.py install
```

## Examples

Some examples to get started; more in the documentation (which is coming soon; 
but the code is all Sphinx style documented and is fairly readable).

```python
>>> from piazza_api import Piazza
>>> p = Piazza()
>>> p.user_login()
Email: ...
Password: ...
>>> eece210 = p.network("hl5qm84dl4t3x2")
>>> eece210.get_post(100)
...
>>> posts = eece210.iter_all_posts(limit=10)
>>> for post in posts:
...     do_awesome_thing(post)
>>> users = eece210.get_users(["userid1", "userid2"])
>>> all_users = eece210.get_all_users()
```

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
