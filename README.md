firefox-greenlight-tests
========================

[![Build Status](https://travis-ci.org/mozilla/firefox-ui-tests.svg?branch=master)](https://travis-ci.org/mozilla/firefox-ui-tests)

Installation
------------

First make sure you have [pip](http://pip.readthedocs.org/en/latest/installing.html) installed.

It is recommended that [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html#installation) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) be used in conjunction with firefox-ui-tests. Start by installing these.

Then:

    pip install firefox-ui-tests

Alternatively you may want to clone the repo for development:

    git clone https://github.com/mozilla/firefox-ui-tests.git
    python setup.py develop

Usage
-----

To run all tests:

    firefox-ui-tests --binary <path to firefox binary>

To run a specific test or directory of tests:

    firefox-ui-tests --binary <path to firefox binary> <path to test or directory>

For more options run:

    firefox-ui-tests --help

Documentation
-------------

Documentation for the puppeteer libraries are hosted on [readthedocs](http://firefox-puppeteer.readthedocs.org/en/latest/).
