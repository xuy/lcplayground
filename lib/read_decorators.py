class SkipFirst:
  def __init__(self, source):
    self._source = source
    self._at_first = True 

  def __iter__(self):
    return self

  def next(self):
    if self._at_first:
      self._source.next()
      self._at_first = False
    return self._source.next()

# The header line of the CSV file is not quite human readable.
# Here we yield a new line instead of the old one.
from name_translation import new_name
class ReplaceFirst:
  def __init__(self, source):
    self._source = source
    self._at_first = True 

  def __iter__(self):
    return self

  def next(self):
    if self._at_first:
      self._at_first = False 
      # Header, sans "\n"
      row = self._source.next()[:-1]
      new_row = []
      for i in row.split(","):
        new_row.append(new_name[i])
      return ",".join(new_row)
    else: 
      return self._source.next()


