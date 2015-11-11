#!/bin/bash
set -ev

if [[ $LOCALE = 'en-US' ]]
then
    mozdownload --type daily --branch mozilla-aurora
else
    mozdownload --type daily --branch mozilla-aurora --locale ru
fi
