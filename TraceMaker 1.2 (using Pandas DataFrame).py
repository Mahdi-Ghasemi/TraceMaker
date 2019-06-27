#-------------------------------------------------TraceMaker--------------------------------------------
# This tool aims to convert original event logs where each line represents one event to a structured event log where
# each line represents one case beside it's trace. To this end, the trace of activities that each case has experienced
# in the process is extracted from the original log. Each trace is a sequence of events(activities) associated to a case.

#-------------------------------------------------------------------------------------------------------
# the main use of this tool is in goal-oriented process discovery where the event log should be in a particular shape:
# each line consists of the case identifier, the trace of the case and the satisfaction level of different goals.
# Process mining community can use the tool to have perception about traces
#--------------------------------------------------------------------------------------------------------

import pandas as pd
import csv
import os
import time
start_time = time.time()


# 'Original log.csv' is the original log structured as follows:
# The first row: Column header (The title spelling is not restricted)
# Column 1: Case identifier
# Column 2: Event
# Column 3: Timestamp


# opens the original event log for reading
LogInDF=pd.read_csv('Original log.csv')

# creates a csv file as output
LogOutDF=pd.DataFrame(columns=['Case', 'Trace'])


# sorts the input log based on Case identifier and then based on Timestamp
Case=LogInDF.columns[0]
Activity=LogInDF.columns[1]
Time=LogInDF.columns[2]
LogInDF.sort_values(by=[Case, Time], inplace=True)

#resets the row number of sorted log
LogInDF=LogInDF.reset_index(drop=True)



# keeps the number of all events (rows) recorded in the original log
NumberOfEvents=len(LogInDF.index)

# the algorithm begins:

# defines TempTrace as a string that keeps the current trace in each iteration
TempTrace=''

# adds a line to the sorted log (needed for the iteration)
LogInDF.loc[NumberOfEvents]=['End of input log','','']

# the initial value of TempTrace is the first activity of the first case
TempTrace=LogInDF.loc[0, Activity]

# initiates an index for rows of output data log
outindex=0

# the iteration to check all rows of sorted log and concatenate the activities belong to the same case
for index in list(range(1,NumberOfEvents+1)):
        if LogInDF.loc[index, Case]==LogInDF.loc[index - 1, Case]: # checks if the current case is the same as the previous one
            TempTrace= TempTrace +";" + LogInDF.loc[index, Activity]
        else: # the current case is different from previous one
            LogOutDF.loc[outindex]=[LogInDF.loc[index - 1, Case], TempTrace] #the trace of previous case is completed and is stored in output data frame
            TempTrace=LogInDF.loc[index, Activity] # the current trace is reset with the event of current case
            outindex += 1

#Makes the output file from the output data frame
LogOutDF.to_csv('Traces.csv', index=False)

# report the number of all cases and the number of all events and the path of the generated data file
print("\nTraceMaker exctracted the traces of all cases successfully!")
print("\nTraces.csv was made in %s\ \n Number of cases= %d \n Number of original events= %d" % (os.getcwd(), len(LogOutDF.index), NumberOfEvents))

# report the execution time
print("\n\n--- execution time was %s seconds ---" % (time.time() - start_time))

