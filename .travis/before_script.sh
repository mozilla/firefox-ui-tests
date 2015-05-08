#!/bin/bash
set -ev

if [ "$TRAVIS_BRANCH" == "master" ]; then
    OPTIONS="--type daily --branch mozilla-central"
elif [ "$TRAVIS_BRANCH" == "mozilla-aurora" ]; then
    OPTIONS="--type daily --branch mozilla-aurora"
elif [ "$TRAVIS_BRANCH" == "mozilla-beta" ]; then
    OPTIONS="--type release --version latest-beta"
elif [ "$TRAVIS_BRANCH" == "mozilla-release" ]; then
    OPTIONS="--type release --version latest"
fi

mozdownload $OPTIONS
