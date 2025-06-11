import grpc
from concurrent import futures
from protos import chat_pb2_grpc

ENDERECO_CHAT='localhost:50052'

class GatewayChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.canal = grpc.insecure_channel(ENDERECO_CHAT)
        self.chat_stub = chat_pb2_grpc.ChatServiceStub(self.canal)
        print(f"Gateway conectado ao servidor no endereço {ENDERECO_CHAT}")

    def SendMessage(self, request, context):
        self.chat_stub.SendMessage(request)

    def ReceiveMessages(self, request, context):
        stream_resposta = self.chat_stub.ReceiveMessages(request)

        try:
            for mensagem in stream_resposta:
                yield mensagem
        except grpc.RpcError as e:
            print(f"Erro ao receber mensagem: {e.details()}")
            context.set_details(e.details())

def serve():
    porta_publica = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(GatewayChatService(), server)
    server.add_insecure_port(f'[::]:{porta_publica}')
    print(f"Rodando na porta {porta_publica}")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()