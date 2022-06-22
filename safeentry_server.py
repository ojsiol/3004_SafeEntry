# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
from datetime import datetime,date, timedelta
import logging
import grpc
import safeentry_pb2
import safeentry_pb2_grpc
import csv # used for persistent storage for safe entry logs
import asyncio
import functools


#Function enabling data persistence by logging SafeEntry transactions
def writeSafeEntryToLogs(name,NRIC,location,type,datetime):
    # open the file in the append mode
    f = open('safeEntryLogs/checkinLogs.csv', 'a', newline='\n')
    # create the csv writer
    writer = csv.writer(f)
    # Write to csv
    writer.writerow([name,NRIC,location,type,datetime])
    # close the file
    f.close()
    #Return transaction details as string message
    return "Transaction Success:\nName :"+name+"\nNRIC :"+NRIC+"\nLocation :"+location+"\nType :"+type+"\nDate time :"+datetime

#Function to read from persistent storage(csv) and respond list of transaction as string
def readSafeEntryLogs(name,NRIC,timeDelta):
    #Get the date T-14 days
    fourteenDaysAgo = date.today() - timedelta(days=timeDelta)
    #Initialized empty response string
    transactions = []
    # open the file in the write mode
    with open('safeEntryLogs/checkinLogs.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Match name and NRIC found in CSV
            if (name == row[0]) and (NRIC == row[1]):
                #Convert csv Datetime to date for comparison
                csvDate = datetime.strptime(row[4], '%d/%m/%Y %H:%M:%S').date()
                #Compare if csv date is after T-14 days
                if csvDate>fourteenDaysAgo:
                    # Append rows of safe entry row to response
                    transactions.append(row)
    return transactions

#read MOH covid log
def readMOH(timeDelta):
    #Get the date T-14 days
    fourteenDaysAgo = date.today() - timedelta(days=timeDelta)
    covidLocationDate = []
    with open('safeEntryLogs/MOHLog.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            #Convert csv Datetime to date for comparison
            csvDate = datetime.strptime(row[1], '%d/%m/%Y').date()
            #Compare if csv date is after T-14 days
            if csvDate>fourteenDaysAgo:
                # Append rows of safe entry row to response
                covidLocationDate.append(row)
    return covidLocationDate

def CompareLog(userlog,mohlog):
    #compare date then location. #assume moh only has the record of 14days
    potentialExposureList = []
    potentialExposure =False
    for userdetail in userlog:
        userLocation = userdetail[2]
        userdate = datetime.strptime(userdetail[4], '%d/%m/%Y %H:%M:%S').date()
        for mohDetail in mohlog:
            mohCovidLocation= mohDetail[0]
            # mohCovidDate = mohDetail[1]
            mohCovidDate = datetime.strptime(mohDetail[1], '%d/%m/%Y').date()
            # mohdate = datetime.strptime(mohdetail[4], '%d/%m/%Y %H:%M:%S').date()
            #get name and nric of the person who was in close contact
            #user location match with moh location
            if (userLocation == mohCovidLocation) and (mohCovidDate ==userdate):
                potentialExposure=True
                #user date is same as moh covid date
                # records.append([userdetail[0],userdetail[2],userdetail[3],userdetail[4]])
                message = userdetail[0] + " is in close contact with covid positive patient during "+ userdetail[3]+ " at " + userdetail[2]+ " around " + userdetail[4]
                potentialExposureList.append(message)
    if potentialExposure==True:
        potentialExposureList.append("ALERT! Please monitor health. Exposure from locations visited above during the past 14 days!")
        return potentialExposureList
    else:
        potentialExposureList.append("Zero exposure of covid-19")
        return potentialExposureList

#function to input new location and datetime to MOH log
def addCovidLog():
    locationOfCovid = input("Location : ")
    dateOfCovid = input("Date(DD/MM/YYYY) : ")
    f = open('safeEntryLogs/MOHLog.csv', 'a', newline='\n')
    # create the csv writer
    writer = csv.writer(f)
    # Write to csv
    writer.writerow([locationOfCovid,dateOfCovid])
    # close the file
    f.close()
    print("New Record inserted")
    return ("Location "+ locationOfCovid)

#function for moh officer to add covid positive location / date
def MOHRemote(loop):
    #Add location and date of new covid location
    addCovidLog()
    #loop the function in asynchronous mode
    loop.run_in_executor(None, functools.partial(MOHRemote, loop))
    return safeentry_pb2.Reply(message="test")

class Safeentry(safeentry_pb2_grpc.SafeEntryServicer):
    def Checkin(self, request, context):
        #Store request into persistent storage(CSV)
        storeTransactionResponse=writeSafeEntryToLogs(request.name,request.NRIC,request.location,request.type,request.datetime)
        #return transaction result as string
        return safeentry_pb2.Reply(message=storeTransactionResponse)

    def GroupCheckin(self, request_iterator,context):
        for request in request_iterator:   
            #store request into csv
            storeTransactionResponse=writeSafeEntryToLogs(request.name,request.NRIC,request.location,request.type,request.datetime)
            groupcheckin = safeentry_pb2.Reply(message=storeTransactionResponse)
            #return transaction result that can be iterated
            yield groupcheckin

    def Checkout(self,request_iterator,context):
        #counter for number of locations to be checked out for user
        rowCount =0
        for request in request_iterator:
            # print(request.name, request.NRIC, request.location, request.type, request.datetime)
            writeSafeEntryToLogs(request.name,request.NRIC,request.location,request.type,request.datetime)
            rowCount+=1
        #if no locations to be checked out    
        if rowCount==0:
            return safeentry_pb2.Reply(message="Checked out of all locations")
        #if checked out of at least one location
        else:
            return safeentry_pb2.Reply(message="Success, "+str(rowCount)+" rows added!")

    def History(self, request, context):
        #reads csv file and retrieve transaction logs as Array
        transactions = readSafeEntryLogs(request.name,request.NRIC,14)
        #Send stream of location history to client
        for x in transactions:
            yield safeentry_pb2.Response(name= x[0], NRIC = x[1], location = x[2], type = x[3], datetime = x[4])
      
    def Covid(self, request, context):
        #retrieve the past 14days of user log
        past14days = readSafeEntryLogs(request.name,request.NRIC,14)
        #retrieve the past 14 days of MOH log
        mohdata = readMOH(14)
        #with user past 14 days log , used it to compare with MOH Log
        founduser = CompareLog(past14days,mohdata)
        for i in founduser:
            covidPositiveResponse = safeentry_pb2.Reply(message=(i))
            yield covidPositiveResponse

    def GroupCheckout(self, request_iterator, context):
        for request in request_iterator:   
            #store request into csv
            storeTransactionResponse=writeSafeEntryToLogs(request.name,request.NRIC,request.location,request.type,request.datetime)
            groupcheckout = safeentry_pb2.Reply(message=storeTransactionResponse)
            #return transaction result that can be iterated
            yield groupcheckout

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    safeentry_pb2_grpc.add_SafeEntryServicer_to_server(Safeentry(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, functools.partial(MOHRemote, loop))
    loop.run_in_executor(None,serve)
    loop.run_forever()
