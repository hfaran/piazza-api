# piazza-api

Unofficial Client for Piazza's Internal API

## Example
```
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

## Dependencies

* [requests](http://python-requests.org/)
