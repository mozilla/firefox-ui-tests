#!/bin/bash
set -ev

mozdownload --type daily --branch mozilla-central
mozdownload --type daily --branch mozilla-central --locale ru
