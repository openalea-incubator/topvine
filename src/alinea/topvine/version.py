
major = 0
"""(int) Version major component."""

minor = 9
"""(int) Version minor component."""

post = 0
"""(int) Version post or bugfix component."""

__version__ = ".".join([str(s) for s in (major, minor, post)])
# #}
