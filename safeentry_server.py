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
import logging

import grpc
import safeentry_pb2
import safeentry_pb2_grpc
import csv # used for persistent storage for safe entry logs


#Function enabling data persistence by logging SafeEntry transactions
def writeSafeEntryToLogs(name,NRIC,location,type,datetime):
    # open the file in the write mode
    f = open('safeEntryLogs/checkinLogs.csv', 'a')
    # create the csv writer
    writer = csv.writer(f)
    # Write to csv
    writer.writerow([name,NRIC,location,type,datetime])
    # close the file
    f.close()
    #Return transaction details as string message
    return "Transaction Success:\nName :"+name+"\nNRIC :"+NRIC+"\nLocation :"+location+"\nType :"+type+"\nDate time :"+datetime

#Function to read from persistent storage(csv) and respond list of transaction as string
def readSafeEntryLogs():
    #Initialized empty response string
    response = ""
    # open the file in the write mode
    with open('safeEntryLogs/checkinLogs.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Append rows of safe entry row to response
            response+=str(row)+"\n"
    return response

class Safeentry(safeentry_pb2_grpc.SafeEntryServicer):
    def Checkin(self, request, context):
        #Store request into persistent storage(CSV)
        storeTransactionResponse=writeSafeEntryToLogs(request.name,request.NRIC,request.location,request.type,request.datetime)
        #return transaction result as string
        return safeentry_pb2.Reply(message=storeTransactionResponse)
    def History(self, request, context):
        #reads csv file and respond transaction log as string message
        return safeentry_pb2.Reply(message=readSafeEntryLogs())


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    safeentry_pb2_grpc.add_SafeEntryServicer_to_server(Safeentry(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
