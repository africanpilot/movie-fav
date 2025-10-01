import json

import grpc
import link_lib.grpc_unary.unary_pb2 as pb2
import link_lib.grpc_unary.unary_pb2_grpc as pb2_grpc
from link_lib.microservice_general import GeneralJSONEncoder
from link_lib.microservice_response import LinkResponse


class UnaryClient(object):
    """
    Client for accessing the gRPC functionality
    """

    def __init__(self, message: dict, host: str, port: int = 50051):
        self.host = host
        self.server_port = port
        self.message = message

        # instantiate a communication channel
        self.channel = grpc.insecure_channel(f"{self.host}:{self.server_port}")

        # bind the client to the server channel
        self.stub = pb2_grpc.UnaryStub(self.channel)

    @property
    def sterilized_message(self):
        return json.dumps(self.message, cls=GeneralJSONEncoder)

    def execute(self):
        """
        Client function to call the rpc for GetServerResponse
        """
        try:
            response = self.stub.GetServerResponse(pb2.Message(message=self.sterilized_message))
        except grpc.RpcError as e:
            LinkResponse().http_404_not_found_response(f"Unavailable rpc client - {e}")
        else:
            return response
