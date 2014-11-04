# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from functools import wraps
from importlib import import_module

from marionette import HTMLElement


class use_lib_as_property(object):
    """
    This decorator imports a library module and sets an instance
    of the associated class as an attribute on the Puppeteer
    object and returns it.

    Note: return value of the wrapped function is ignored.
    """
    def __init__(self, lib):
        self.mod_name, self.cls_name = lib.rsplit('.', 1)

    def __call__(self, func):
        @property
        @wraps(func)
        def _(cls, *args, **kwargs):
            tag = '_{}_{}'.format(self.mod_name, self.cls_name)
            prop = getattr(cls, tag, None)

            if not prop:
                module = import_module('.{}'.format(self.mod_name), 'greenlight.lib')
                prop = getattr(module, self.cls_name)(cls.client)
                setattr(cls, tag, prop)
            func(cls, *args, **kwargs)
            return prop
        return _


class Puppeteer(object):
    client = None

    def set_client(self, client):
        self.client = client

    # these libs are for UI manipulation

    @use_lib_as_property('l10n.L10n')
    def l10n(self):
        pass

    @use_lib_as_property('menupanel.MenuPanel')
    def menupanel(self):
        pass

    @use_lib_as_property('tabs.Tabs')
    def tabstrip(self):
        pass

    @use_lib_as_property('toolbar.Toolbar')
    def toolbar(self):
        pass

    # these libs wrap gecko APIs

    @use_lib_as_property('api.prefs.DefaultPrefBranch')
    def prefs(self):
        pass


class DOMElement(HTMLElement):

    @classmethod
    def create(cls, element):
        instance = object.__new__(cls)
        instance.__dict__ = element.__dict__.copy()
        return instance
