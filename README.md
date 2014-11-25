firefox-greenlight-tests
========================

Installation
------------

First make sure you have [pip](http://pip.readthedocs.org/en/latest/installing.html) installed.

It is recommended that [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html#installation) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) be used in conjunction with firefox-greenlight-tests. Start by installing these.

Then:

    pip install firefox-greenlight-tests

Alternatively you may want to clone the repo for development:

    git clone https://github.com/mozilla/firefox-greenlight-tests.git
    python setup.py develop


Usage
-----

To run all tests:

    run-greenlight-tests --binary <path to firefox binary>

To run a specific test or directory of tests:

    run-greenlight-tests --binary <path to firefox binary> <path to test or directory>

For more options run:

    run-greenlight-tests --help

Documentation
-------------

Documentation for the puppeteer libraries are hosted on [readthedocs](http://firefox-puppeteer.readthedocs.org/en/latest/).
