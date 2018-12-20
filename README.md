# YieldCurves

This is a simple python script to build a csv of historical treasury yield curves.

The [treasury.gov data](https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData) for historical yields of various treasury maturities should definitely be a csv. The data is perfectly suited for csv form. Yet for some reason, they decided to make an overcomplicated xml file out of it. We may never know why, but we can attack it with Python!

Usage is simple: `python parse_xml.py` will download the file and parse it into a sensible csv format (note: the script is in Python 3).

Even more simply, you can just download `yields.csv` from the repo directly.
