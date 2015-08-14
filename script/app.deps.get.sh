#!/bin/bash

rm -rf app/lib/torhelp
git clone git@github.com:walkr/torhelp.git tmp/app/lib/torhelp
mv tmp/app/lib/torhelp/torhelp app/lib/torhelp
rm -rf tmp