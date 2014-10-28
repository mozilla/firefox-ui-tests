# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from functools import wraps
from importlib import import_module


class use_lib_as_property(object):
    """
    This decorator imports a library module and sets an instance
    of the associated class as an attribute on the Puppeteer
    object and returns it.

    Note: return value of the wrapped function is ignored.
    """
    def __init__(self, lib):
        self.lib = lib

    def __call__(self, func):
        @property
        @wraps(func)
        def _(cls, *args, **kwargs):
            tag = '_{}'.format(self.lib)
            prop = getattr(cls, tag, None)

            if not prop:
                module = import_module('.{}'.format(self.lib), 'greenlight.lib')
                prop = getattr(module, 'property_class')(cls.client)
                setattr(cls, tag, prop)
            func(cls, *args, **kwargs)
            return prop
        return _


class Puppeteer(object):
    client = None

    def set_client(self, client):
        self.client = client

    @use_lib_as_property('l10n')
    def l10n(self):
        pass

    @use_lib_as_property('tabs')
    def tabstrip(self):
        pass

    @use_lib_as_property('toolbar')
    def toolbar(self):
        pass
