firefox-greenlight-tests
========================

Installation
------------

First make sure you have [pip](http://pip.readthedocs.org/en/latest/installing.html) installed.
Then:

    pip install firefox-greenlight-tests

Alternatively you may want to clone the repo for development:

    git clone https://github.com/mozilla/firefox-greenlight-tests.git


Usage
-----

To run all tests:

    run-greenlight-tests -b <path to firefox binary>

To run a specific test or directory of tests:

    run-greenlight-tests -b <path to firefox binary> <path to test or directory>

For more options run:

    run-greenlight-tests --help
