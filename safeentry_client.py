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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging

import grpc
import safeentry_pb2
import safeentry_pb2_grpc
import random #Used for selecting random location for checkin
import csv # used for persistent storage for safe entry logs
import time #used for setting delays

from datetime import datetime # Used for getting current date and time during checkin

#location for checkin
location = ["Bedok", "Tampines", "Pasir ris","Ang Mo Kio","Bishan"]

#Person object
class Person:
  def __init__(self, name, NRIC):
    self.name = name
    self.NRIC = NRIC

#function for creating new person
def getUserCredential():
    name = input("Please enter name: \n")   
    NRIC = input("Please enter NRIC: \n")
    user = Person(name,NRIC)
    return user

#function for creating number of people to check in
def Gcheckin():
    x = int(input("Number of people"))
    current_date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    for i in range(x):
        Gname = input("Please enter name: ")   
        GNRIC = input("Please enter NRIC: ")
        response = safeentry_pb2.Request(name=Gname, NRIC=GNRIC,location=random.choice(location), type="checkin",datetime=current_date_time)
        yield response
        time.sleep(1)

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = safeentry_pb2_grpc.SafeEntryStub(channel)

        #Create new user for current checkin transaction
        user = getUserCredential()
        
        #Display options for current user to perform
        print("1. Check in")
        print("2. History")
        print("3. Group Check in")

        rpc_call = input("Choose 1 option: \n")
        current_date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if rpc_call == "1":
            #RPC call to add safeEntry transaction
            response = stub.Checkin(safeentry_pb2.Request(name=user.name, NRIC=user.NRIC,location=random.choice(location), type="checkin",datetime=current_date_time))
            print(str(response.message))
        elif rpc_call == "2":
            #RPC call to retrieve safeEntry Transaction History as message string
            response = stub.History(safeentry_pb2.Request(name=user.name, NRIC=user.NRIC))
            print(str(response.message))

        elif rpc_call == "3":
            response = stub.Checkin(safeentry_pb2.Request(name=user.name, NRIC=user.NRIC,location=random.choice(location), type="checkin",datetime=current_date_time))
            print(str(response.message))
            #Call Group Check In Function
            responses = stub.GroupCheckin(Gcheckin())
            for x in responses:
                print(str(x.message))


if __name__ == '__main__':
    logging.basicConfig()
    run()
