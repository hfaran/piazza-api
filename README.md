# piazza-api

Tiny wrapper around Piazza's Internal API

## Example
```
>>> p = PiazzaAPI("hl5qm84dl4t3x2")
>>> p.user_auth()
Email: ...
Password: ...
>>> p.get(181)
...
```

## Dependencies

* [requests](http://python-requests.org/)

## "Inspiration"

* https://gist.github.com/alexjlockwood/6797443
