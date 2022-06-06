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




def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        #TODO: initiate the stub
        stub = safeentry_pb2_grpc.SafeEntryStub(channel)

        current_time = datetime.now().strftime("%H:%M:%S")
        print("1. Check in")
        print("2. History")

        rpc_call = input("Choose 1 option: \n")
        if rpc_call == "1":
            response = stub.Checkin(safeentry_pb2.Request(name="hi", NRIC="S123567S",location="tampines", type="checkin",datetime=current_time))
            print("Name, NRIC: " + str(response.message))
        if rpc_call == "2":
            print("History")



if __name__ == '__main__':
    logging.basicConfig()
    run()
