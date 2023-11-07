#! /bin/bash
#
rm db/faldon-data.sqlite
sqlite3 db/faldon-data.sqlite "VACUUM;"
python3 objects-scraper.py
python3 drops-scraper.py
