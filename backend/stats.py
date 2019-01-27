import parser
import config
from datetime import date

# Populates the data and locations variables
def loadData():
    parser.parseDataCSV()
    parser.parseLocationCSV()

# Returns a tuple that has (startRow, endRow) from data
# for specified dates
def getRows(startDate, endDate):
    startDateSplit = startDate.split('-')
    endDateSplit = endDate.split('-')
    startDateMod = list(map(lambda x: int(x), startDateSplit))
    endDateMod = list(map(lambda x: int(x), endDateSplit))
    startDateForm = date(startDateMod[2], startDateMod[1], startDateMod[0])
    endDateForm = date(endDateMod[2], endDateMod[1], endDateMod[0]) 
    numDays = (endDateForm-startDateForm).days + 1
    startRow = 0
    endRow = 0
    for x in range(len(config.data[0])):
        if (startDateForm < config.data[0][x]):
            startRow = x - 1
            break
    for x in range(len(config.data[0])):
        if (endDateForm < config.data[0][x]):
            endRow = x - 1
            break
    return (startRow, endRow)

# Assumes populated variables, startDate and endDate
# produces a list of elements (i.e. startDate isn't 
# at the end). Produces average spending per day in that range
def avg(startDate, endDate):
    avg = 0
    rows = getRows(startDate, endDate)


loadData()
avg("02-01-2019", "06-01-2019")