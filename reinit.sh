#!/bin/bash
set -e

cat json_reinit.json > data.json
cd races_info
rm -rf *
echo "Information about races" >> README.txt
