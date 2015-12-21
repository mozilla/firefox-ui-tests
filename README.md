firefox-ui-tests
================

[![Build Status](https://travis-ci.org/mozilla/firefox-ui-tests.svg?branch=mozilla-central)](https://travis-ci.org/mozilla/firefox-ui-tests)

Installation
------------

First make sure you have [pip](http://pip.readthedocs.org/en/latest/installing.html) installed.

It is recommended that [virtualenv](http://virtualenv.readthedocs.org/en/latest/installation.html) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) be used in conjunction with firefox-ui-tests. Start by installing these.

Then:

    git clone https://github.com/mozilla/firefox-ui-tests.git
    cd firefox-ui-tests
    python setup.py develop

If you want to install everything including fixed versions of dependencies (e.g. for mozbase and marionette packages) as we do in our CI system run the following command:

    pip install -r requirements.txt

There is also a `requirements_optional.txt` file, which will install some optional packages like pep8 and mozdownload.

Usage
-----

To run all tests:

    firefox-ui-tests --binary <path to firefox binary>

To run the update tests:

    firefox-ui-update --binary <path to firefox binary>

To run a specific test or directory of tests:

    firefox-ui-tests --binary <path to firefox binary> <path to test or directory>

For more options run:

    firefox-ui-tests --help

Documentation
-------------

Documentation for the puppeteer libraries are hosted on [readthedocs](http://firefox-puppeteer.readthedocs.org/en/latest/).
