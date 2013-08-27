#!/usr/bin/env python
import csv
import sys

from lib.read_decorators import SkipFirst

if __name__ == "__main__":
  fname = sys.argv[1]
  columns = sys.argv[2].split(",")
  with open(fname) as f:
    details = csv.DictReader(SkipFirst(f))
    row = details.next() # consume the first row
    while True:
      try:
        row = details.next()
	for col in columns:
          print row[col],
        print
      except StopIteration:
        exit(-1)
