import csv
import os
RawLog=csv.reader(open("log.csv","r"))
StructuredLog=open("StructuredLog.csv","w")

# extracting field names through first row
# fields=next(RawLog)
# print(fields)

ListOfInLog=list(RawLog)
ListOfInLog=ListOfInLog[1:]

#ListOfInLog=sorted(ListOfInLog,key= lambda case: (case[0],case[2]) )
ListOfInLog.sort(key= lambda case: (case[0],case[2]) )
print(ListOfInLog)
NumberOfEvents=len(ListOfInLog)


DicOfOutLog={}
TempTrace=ListOfInLog[1][1]
ListOfInLog.append(['End of file',''])

for index in list(range(2,NumberOfEvents+1)):
        if ListOfInLog[index][0]==ListOfInLog[index-1][0]:
            TempTrace=TempTrace+";"+ListOfInLog[index][1]
        else:
            DicOfOutLog[ListOfInLog[index-1][0]]=TempTrace
            TempTrace=ListOfInLog[index][1]

for case, trace in DicOfOutLog.items():
    StructuredLog.write(case+','+trace+'\n')

print(index)
print("StructuredLog.csv was made in %s.\n Number of cases= %d\n Number of events= %d" %(os.getcwd(),len(DicOfOutLog),NumberOfEvents))