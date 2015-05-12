#!/bin/env python3

import csv
import optparse
import os.path
import string
import sys

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

usage = "usage: %prog [options] outfile"
parser = optparse.OptionParser(usage)
parser.add_option("-a", "--all", help="get all scores, not just the current", action="store_true", default=False)
(options, args) = parser.parse_args()

if len(args) != 1:
    parser.error("incorrect number of arguments")

outfile = args[0]

if os.path.isfile(outfile):
    print("Output file " + outfile + " already exists.")
    sys.exit(1)

browser = webdriver.Chrome()

current_inspection_scores = []

for char in string.ascii_uppercase:

    browser.get("http://www.jcdh.org/EH/FnL/FnL03.aspx?Letter=" + char)

    try:
        table = browser.find_element_by_id("ctl00_BodyContent_gvFoodScores")
    except NoSuchElementException:
        # So why are there no restaurants that start with X?
        break
    rows = table.find_elements_by_tag_name("tr")
    for row in rows[1:]:
        cells = row.find_elements_by_tag_name("td")
        # Retrieve permit number from link URL
        permit_number = cells[1].find_element_by_tag_name("a").get_attribute("href").split("=")[-1]
        # Retrieve inspection number from link URL
        inspection_number = cells[4].find_element_by_tag_name("a").get_attribute("href").split("=")[-1]
        data = {
            "smoke_free": cells[0].text,
            "name": cells[1].text,
            "permit_number": int(permit_number),
            "type": cells[2].text,
            "address": cells[3].text,
            "scores": [{
                "score": int(cells[4].text),
                "date": cells[5].text,
                "inspection_number": int(inspection_number)
            }]
        }
        current_inspection_scores.append(data)

    print("Retrieved all restaurants that start with " + char)

if options.all:

    for data in current_inspection_scores:

        browser.get("http://www.jcdh.org/EH/FnL/FnL05.aspx?PermitNbr=" + str(data["permit_number"]))
        try:
            table = browser.find_element_by_id("ctl00_BodyContent_gvFoodScores")
            data["scores"] = []
            rows = table.find_elements_by_tag_name("tr")
            for row in rows[1:]:
                cells = row.find_elements_by_tag_name("td")
                # Retrieve inspection number from link URL
                inspection_number = cells[2].find_element_by_tag_name("a").get_attribute("href").split("=")[-1]
                data["scores"].append({
                    "date": cells[0].text,
                    "inspection_type": cells[1].text,
                    "score": int(cells[2].text),
                    "inspection_number": int(inspection_number)
                })

            print("Retrieved all scores for restaurant " + data["name"])

        except NoSuchElementException:
            # In case the portal does not return a table, stick with the previous score
            print("Skipped restaurant " + data["name"])

with open(outfile, "w") as csvfile:
    fieldnames = ["permit_number", "name", "address", "type", "smoke_free", "inspection_number", "date", "inspection_type", "score"]
    if not options.all:
        fieldnames.remove("inspection_type")
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC, extrasaction="ignore")
    writer.writeheader()
    for data in current_inspection_scores:
        for row in [dict(data, **score) for score in data["scores"]]:
            writer.writerow(row)

browser.close()
