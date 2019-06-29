#-------------------------------------------------TraceMaker--------------------------------------------
# This tool aims to convert original event logs where each line represents one event to a structured event log where
# each line represents one case beside it's trace. To this end, the trace of activities that each case has experienced
# in the process is extracted from the original log. Each trace is a sequence of events(activities) associated to a case.

#-------------------------------------------------------------------------------------------------------
# the main use of this tool is in goal-oriented process discovery where the event log should be in a particular shape:
# each line consists of the case identifier, the trace of the case and the satisfaction level of different goals.
# Process mining community can use the tool to have perception about traces
#--------------------------------------------------------------------------------------------------------

import csv
import os
import time
start_time = time.time()

# 'Original log.csv' is the original log must be in this shape:
# The first row: Column header (The titles are not restricted)
# Column 1: Case identifier
# Column 2: Event
# Column 3: Timestamp

# opens the original event log for reading
OriginalLog=csv.reader(open("Original log.csv", "r"))

# creates a csv file as output
TracesOut=open("Traces.csv", "w")

# extracting field names through first row
# fields=next(OriginalLog)
# print(fields)

# constructs a list from the original log
ListOfLogIn=list(OriginalLog)

# gets rid of the header (first row of original log)
ListOfLogIn= ListOfLogIn[1:]

# sorts the input log based on Case identifier and then based on Timestamp
ListOfLogIn.sort(key= lambda case: (case[0], case[2]))

# keeps the number of all events recorded in original log
NumberOfEvents=len(ListOfLogIn)

# defines a dictionary whose key will be Case identifier and value will be the trace of that case
DicOfLogOut={}

# the algorithm begins:

# defines TempTrace as a string that keeps the current trace in each iteration
TempTrace=''

# the initial value of TempTrace is the first event of the first case
TempTrace=ListOfLogIn[1][1]

# adds a line to the list of sorted input log
ListOfLogIn.append(['End of file', ''])

# the iteration to check stored log lines and concatenate the events of the same case
for index in list(range(2,NumberOfEvents+1)):
        if ListOfLogIn[index][0]==ListOfLogIn[index - 1][0]: # checks if the current case is the same as the previous one
            TempTrace= TempTrace +";" + ListOfLogIn[index][1]
        else: # the current case is different from previous one
            DicOfLogOut[ListOfLogIn[index - 1][0]]=TempTrace #the trace of previous case is completed and is stored in disctionary
            TempTrace=ListOfLogIn[index][1] # the current trace is replaced with the event of current case

for case, trace in DicOfLogOut.items(): # all the traces are made and the resulting dictionary should be stored in a output file TracesOut.csv
    TracesOut.write(case + ',' + trace + '\n')

# report the number of all cases and the number of all events that was fed and the path of the generated file
print("\n\nTracesOut.csv was made in %s\ \n Number of cases= %d\n Number of used events= %d" % (os.getcwd(), len(DicOfLogOut), NumberOfEvents))


print("\n\n--- execution time was %s seconds ---" % (time.time() - start_time))
