import csv
import datetime
import pymongo
import urllib2

from pymongo import MongoClient
from lib.read_decorators import SkipFirst
from lib.read_decorators import ReplaceFirst

client = MongoClient()
db = client["lending_club"]
loans = db["available_loans"]

print "Querying Landing Club at ", datetime.datetime.utcnow()

req = urllib2.Request('https://www.lendingclub.com/fileDownload.action?file=InFundingStats3.csv&type=gen')
response = urllib2.urlopen(req)
details = csv.DictReader(ReplaceFirst(SkipFirst(response)))

count = 0
updated = 0
inserted = 0

for row in details:
  count += 1
  loan = dict(row)
  # Clean up the empty column due to CSV parsing problem???
  if loan.has_key(None):
    del loan[None]
  target = {"id" : loan["id"]}
  existing_loan = loans.find_one(target)
  if existing_loan:
    # TODO: compare the two
    is_updated = False
    for key in loan.keys():
      if existing_loan[key] != loan[key]:
        is_updated = True
    if is_updated:
      updated += 1
      # Use the new info, but keep first_seen
      loan["first_seen"] = existing_loan["first_seen"]
      loan["last_seen"] = datetime.datetime.utcnow()
      loans.update(target, loan)
  else:
    inserted += 1
    loan["first_seen"] = datetime.datetime.utcnow()
    loan["last_seen"] = datetime.datetime.utcnow()
    loans.insert(loan)

print "Got ", count,  "loans. New loans: ", inserted
