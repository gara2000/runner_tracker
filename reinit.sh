#!/bin/bash
set -e

cat json_reinit.json > data.json
cd images
rm -rf *
