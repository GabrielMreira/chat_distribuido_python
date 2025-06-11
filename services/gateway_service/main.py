import grpc
from concurrent import futures
from protos import chat_pb2, chat_pb2_grpc

CHAT_SERVICE_ADDRESS = 'localhost:50052'


class GatewayChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.channel = grpc.insecure_channel(CHAT_SERVICE_ADDRESS)
        self.chat_stub = chat_pb2_grpc.ChatServiceStub(self.channel)
        print(f"Gateway conectado ao ChatService em {CHAT_SERVICE_ADDRESS}")

    def SendMessage(self, request, context):
        return self.chat_stub.SendMessage(request)

    def ReceiveMessages(self, request, context):
        response_stream = self.chat_stub.ReceiveMessages(request)

        try:
            for message in response_stream:
                yield message
        except grpc.RpcError as e:
            print(f"Gateway: Erro no stream vindo do ChatService. Status: {e.code().name}, Detalhes: {e.details()}")
            context.set_details(f"Erro de comunicação com o serviço de backend: {e.details()}")
            context.set_code(e.code())


def serve():
    public_port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(GatewayChatService(), server)
    server.add_insecure_port(f'[::]:{public_port}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()