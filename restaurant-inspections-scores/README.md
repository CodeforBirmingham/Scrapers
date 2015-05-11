Restaurant Inspection Scores
============================

Scrapes the [Restaurant Inspection Scores](http://www.jcdh.org/EH/FnL/FnL03.aspx) from the [Jefferson County Department of Health](http://www.jcdh.org/) website. A snapshot of the downloaded data is [available on Socrata](https://brigades.opendatanetwork.com/dataset/Birmingham-Restaurant-Inspection-Scores/r7g8-mg98).


Usage
-----

The script is written for Python 3 and depends on [Selenium](http://www.seleniumhq.org/).

To install Selenium, run

    pip install --user selenium

Then run the script:

    ./restaurant-inspection-scores.py output.csv
