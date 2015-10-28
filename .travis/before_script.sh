#!/bin/bash
set -ev

if [[ $LOCALE = 'en-US' ]]
then
    mozdownload --type candidate --branch mozilla-beta
else
    mozdownload --type candidate --branch mozilla-beta --locale ru
fi
