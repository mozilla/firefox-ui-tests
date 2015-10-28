#!/bin/bash
set -ev

if [[ $LOCALE = 'en-US' ]]
then
    mozdownload --type candidate --branch mozilla-release
else
    mozdownload --type candidate --branch mozilla-release --locale ru
fi
