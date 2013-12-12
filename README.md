piazza-api
==========

Tiny wrapper around Piazza's Internal REST API


Example:
```
>>> from piazza_api import PiazzaAPI
>>> p = PiazzaAPI("hl5qm84dl4t3x2")
Email: ...
Password: ...
>>> p.get(181)
...
```

Inspired by: https://gist.github.com/alexjlockwood/6797443
