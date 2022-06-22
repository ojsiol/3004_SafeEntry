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
import time #used for setting delays

from datetime import datetime # Used for getting current date and time during checkin



#Person object for main user
class Person:
  def __init__(self, name, NRIC):
    self.name = name
    self.NRIC = NRIC

#function for creating new person
def getUserCredential():
    name = input("Please enter name: \n").lower()   
    NRIC = input("Please enter NRIC: \n").lower()
    user = Person(name,NRIC)
    return user

#function for creating number of people to check in
def gCheckIn(location,currentdate):
    x = int(input("Number of people: "))
    for i in range(x):
        Gname = input(str(i+1)+")Please enter name: ").lower()   
        GNRIC = input(str(i+1)+")Please enter NRIC: ").lower()
        response = safeentry_pb2.Request(name=Gname, NRIC=GNRIC,location=location, type="checkin",datetime=currentdate)
        yield response
        time.sleep(1)
#function for creating number of people to check in
def gCheckOut(user,NRIC,stub):
    users = []
    #Append main user to list of users to be checked out
    users.append([user,NRIC])
    #Get number of users to be checked out
    x = int(input("Number of people excluding yourself: "))
    #Add users to group of users to be checked out using group checkout function
    for i in range(x):
        Gname = input("Please enter name: ").lower()   
        GNRIC = input("Please enter NRIC: ").lower()
        users.append([Gname,GNRIC])
    
    #For each user, individually check thier location history and check them out seperately
    for user in users:
        print("\nCheck out for "+str(user[0])+"\n")
        #Send RPC request using username & NRIC
        #Retrieve stream of RPC response of user location transaction
        historyResponses = stub.History(safeentry_pb2.Request(name=user[0], NRIC=user[1] ))
        #Call function to get pending locations to be checked out
        locationsToBeCheckedOut =checkout(historyResponses)
        #Send a stream of checked out rows(Request) with name,nric,location,type,datetime to server to be written to persistent storage
        serverResponse = stub.Checkout(locationsToBeCheckedOut)
        #print server response
        print(serverResponse.message)
        
def checkout(historyResponses):
    #Stack to hold user checked in location
    checkinLocationStack = []
    #stack to check user checked out location
    checkoutLocationStack =[]
    #get entire transaction of the user
    userHistory=historyResponses

    #Populate stack with current location, by subtracting checked in with checked out status
    for row in userHistory:
        if(row.type=="checkin"):
            checkinLocationStack.append(row)
        else:
            checkinLocationStack.pop()

    # iterrate pending checkout location ordered by latest checked in status
    for row in reversed(checkinLocationStack):
        #Current time of checkin
        date_time = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        userInput = input("checkout of "+row.location+"?(Y/N)").lower()
        #if user wishes to check out, create new checkout transaction and append to checkout stack
        if(userInput == 'y'):
            checkoutLocationStack.append([row.name,row.NRIC,row.location,'checkout',date_time])
            response =safeentry_pb2.Request(name=row.name, NRIC=row.NRIC,location=row.location, type='checkout',datetime=date_time)
            yield response
        #if user cancels checkout, break out of loop 
        elif userInput =="n":
            print("no")
            break

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = safeentry_pb2_grpc.SafeEntryStub(channel)
       
        #Make RPC call to server to check if current user has been exposed to COvid-19
        response = stub.Covid(safeentry_pb2.Request(name=user.name, NRIC=user.NRIC))
        #Print notice of all possible covid-19 exposures upon login
        for i in response:
            print(str(i.message))
        while(1):
            #Get current time to be appended to current transaction
            current_date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            #Display options for current user to perform
            print("1. Check in")
            print("2. History (Past 14 days)")
            print("3. Group Check in")
            print("4. Check out")
            print("5. Group Check out")
            print("6. Test to check that you are in close contact from MOH data")
            print("7. Exit")
            rpc_call = input("Choose an option: \n")
            if rpc_call == "1":
                #RPC call to add safeEntry transaction for current user
                location = input("Please enter location: ").lower()  
                response = stub.Checkin(safeentry_pb2.Request(name=user.name, NRIC=user.NRIC,location=location, type="checkin",datetime=current_date_time))
                print(str(response.message))
            elif rpc_call == "2":
                #Send RPC request using username & NRIC
                #Retrieve stream of RPC response of user location transaction history
                historyResponses = stub.History(safeentry_pb2.Request(name=user.name, NRIC=user.NRIC ))
                for x in historyResponses:
                    print(x.name+"\t"+ x.NRIC+"\t"+x.location+"\t"+ x.type+"\t"+x.datetime)
            elif rpc_call == "3":
                #Obtain location for group checkin
                location = input("Please enter location: ").lower()
                #Check in the main user   
                response = stub.Checkin(safeentry_pb2.Request(name=user.name, NRIC=user.NRIC,location=location, type="checkin",datetime=current_date_time))
                print(str(response.message))
                #Call Group Check In Function to check in remaining members of the group
                responses = stub.GroupCheckin(gCheckIn(location,current_date_time))
                for x in responses:
                    print(str(x.message))

            elif rpc_call == "4":
                #Send RPC request using username & NRIC
                #Retrieve stream of RPC response of user location transaction
                historyResponses = stub.History(safeentry_pb2.Request(name=user.name, NRIC=user.NRIC ))
                print("Location for : "+user.name)
                #Call function to get location to be checked out
                locationsToBeCheckedOut =checkout(historyResponses)
                #Send a stream of checked out rows(Request) with name,nric,location,type,datetime to server to be written to persistent storage
                serverResponse = stub.Checkout(locationsToBeCheckedOut)
                #print server response
                print(serverResponse.message)
            elif rpc_call == "5":
                #Call checkout function for group checkout  
                gCheckOut(user.name,user.NRIC,stub)

            elif rpc_call == "6":
                #RPC call to obtain information on potential exposure to covid-19
                response = stub.Covid(safeentry_pb2.Request(name=user.name, NRIC=user.NRIC,datetime=current_date_time))
                for i in response:
                    print(str(i.message))

            elif rpc_call == "7":
                #Terminate program
                print("Terminating.....")
                time.sleep(1)
                break
            else:
                print("\nWrong entry, please try again.....\n")

if __name__ == '__main__':
    logging.basicConfig()
    #Create new user for current checkin transaction
    user = getUserCredential()
    run()
