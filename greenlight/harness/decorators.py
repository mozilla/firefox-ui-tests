# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from functools import wraps


class uses_lib(object):
    """
    Convenience decorator that injects the specified
    libraries directly into the test scope.

    E.g:
        @uses_lib('toolbar')
        def test_something(self):
            print self.toolbar.location
    """
    def __init__(self, *libs):
        self.libs = libs

    def __call__(self, func):
        @wraps(func)
        def _inject_libs(cls, *args, **kwargs):
            for name in self.libs:
                lib = getattr(cls.lib, name)
                setattr(cls, name, lib)

            ret = func(cls, *args, **kwargs)

            for name in self.libs:
                delattr(cls, name)
            return ret
        return _inject_libs
