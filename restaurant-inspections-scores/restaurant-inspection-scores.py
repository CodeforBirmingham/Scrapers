#!/bin/env python3

import csv
import os.path
import string
import sys

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

outfile = sys.argv[1]

if os.path.isfile(outfile):
    print("Output file " + outfile + " already exists.")
    sys.exit(1)

browser = webdriver.Chrome()

with open(outfile, "w") as csvfile:
    fieldnames = ["permit_number", "name", "address", "type", "smoke_free", "score", "date"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)

    for char in string.ascii_uppercase:

        browser.get("http://www.jcdh.org/EH/FnL/FnL03.aspx?Letter=" + char)

        try:
            table = browser.find_element_by_id("ctl00_BodyContent_gvFoodScores")
        except NoSuchElementException:
            break
        inspections = table.find_elements_by_tag_name("tr")
        for inspection in inspections[1:]:
            row = inspection.find_elements_by_tag_name("td")
            data = {
                "smoke_free": row[0].text,
                "name": row[1].text,
                "type": row[2].text,
                "address": row[3].text,
                "score": int(row[4].text),
                "date": row[5].text
            }
            # Retrieve permit number from link URL
            permit_number = row[1].find_element_by_tag_name("a").get_attribute("href").split("=")[1]
            data["permit_number"] = int(permit_number)
            writer.writerow(data)

        print("Done with " + char)
