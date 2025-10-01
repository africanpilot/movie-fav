# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json
from concurrent import futures

import grpc
import link_lib.grpc_unary.unary_pb2 as pb2
import link_lib.grpc_unary.unary_pb2_grpc as pb2_grpc
from link_lib.microservice_general import GeneralJSONEncoder
from link_lib.microservice_generic_model import GenericModel


class UnaryService(pb2_grpc.UnaryServicer):

    def __init__(self, register_controller, *args, **kwargs):
        self.gen = GenericModel()
        self.register_controller = register_controller

    def sterilized_message(self, result: dict):
        msg = result.get("message")
        if isinstance(msg, dict):
            msg = json.dumps(msg, cls=GeneralJSONEncoder)
        return dict(message=msg, received=result.get("received"))

    def GetServerResponse(self, request, context):
        message: dict = json.loads(request.message)

        topic = message.get("topic")
        body = message.get("body")

        try:
            result = self.register_controller.handler(topic, body=body)
        except Exception as e:
            self.gen.log.info(f"ERROR resolving {message}: {e}")
            result = dict(message=f"Failed to resolve {topic}", received=False)

        return pb2.MessageResponse(**self.sterilized_message(result))


class UnaryServer:

    @staticmethod
    def run(register_controller, port: int = 50051):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb2_grpc.add_UnaryServicer_to_server(UnaryService(register_controller), server)
        server.add_insecure_port(f"[::]:{port}")
        server.start()
        server.wait_for_termination()
