
from icalendar import Calendar, Event
import copy
import sys
from datetime import date,datetime

# file is string
def getCalObject(fileName):
  cal = Calendar.from_string(open(fileName, 'r').read())
  return cal



# events: list of events
# start: datetime
# end: datetime
def filterEventListForTimePeriod(events, dStart, dEnd):

  result = []

  pattern="%Y%m%dT%H%M%S"
  for event in events:
    event = copy.deepcopy(event)
    dEventStart = datetime.strptime(str(event['DTSTART']), pattern)
    dEventEnd = datetime.strptime(str(event['DTEND']), pattern + "Z")
    # if the current event starts after filter end date, ignore
    if (dEventStart > dEnd):
      continue
    # if I work on a sunday night, when the week rolls over
    # i want to bill first part of the session to last week
    # second part to new week
    # so let's modify the event for "last week"
    modified = False # safeguard
    if (dEventEnd > dEnd):
      event['DTEND'] = dEnd.strftime(pattern)
      modified = True
    # and now for the "next week" case:
    if (dEventEnd <= dEnd and dEventStart < dStart):
      event['DTSTART'] = dStart.strftime(pattern)
      if modified: # we're fucked
        raise Exception("You've got a logic error in your code.")
    result.append(event)
  return result

# returns tuple
# week is int, year is int - or there will be tears. 
def getWeekBoundaries(week, year):
  #%w Weekday as a decimal number [0(Sunday),6].
  # this is somewhat annoying as we need to +1 the week
  pattern = "%Y:%W:%w:%H:%M:%S"
  start = datetime.strptime(str(year) + ":" + str(week) + ":1:0:0:0", pattern)
  end = datetime.strptime(str(year) + ":" + str(week + 1) + ":0:23:59:59", pattern)
  return (start, end)
      

def main():

  week = sys.argv[1]
  year = sys.argv[2]
  fileName = sys.argv[3]

  cal =  getCalObject(fileName)
  events = cal.walk('VEVENT')
  (start, end) = getWeekBoundaries(int(week), int(year))
  filtered = filterEventListForTimePeriod(events, start, end)
  print filtered


if __name__ == "__main__":
  main()


