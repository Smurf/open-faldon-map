#! /bin/bash
#
rm db/objects.sqlite
sqlite3 db/objects.sqlite "VACUUM;"
python3 objects-scraper.py
python3 drops-scraper.py
