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

from datetime import datetime

# class Person:
#   def __init__(self, name, NRIC):
#     self.name = name
#     self.NRIC = NRIC

# def getUserCredential():
#     name = input("Please enter name: \n")   
#     NRIC = input("Please enter NRIC: \n")
#     user = Person(name,NRIC)
#     return user


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        #TODO: initiate the stub
        stub = safeentry_pb2_grpc.SafeEntryStub(channel)
        inputName = input("Please enter name: \n")   
        inputNRIC = input("Please enter NRIC: \n")
        current_time = datetime.now().strftime("%H:%M:%S")
        print("1. Check in")
        print("2. History")

        rpc_call = input("Choose 1 option: \n")
        if rpc_call == "1":
            inputlocation = input("Enter current location: ")
            response = stub.Checkin(safeentry_pb2.Request(name=inputName, NRIC=inputNRIC,location=inputlocation, type="checkin",datetime=current_time))
            print("Name, NRIC , Location, Type \n" + str(response.message))
        if rpc_call == "2":
            print("History")



if __name__ == '__main__':
    logging.basicConfig()
    
    run()
