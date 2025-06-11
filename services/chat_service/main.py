import grpc
from concurrent import futures
import time
import threading
from protos import chat_pb2, chat_pb2_grpc

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.messages = []
        self.user_stream = {}
        self.lock = threading.Lock()

    def ReceiveMessages(self, request, context):
        usuario = request.user
        print(f"Usuario {usuario} conectado")
        ultimo_index = 0

        try:
            while context.is_active():
                novas_mensagens = []
                with self.lock:
                    if len(self.messages) > ultimo_index:
                        novas_mensagens = self.messages[ultimo_index:]
                        ultimo_index = len(self.messages)

                for msg in novas_mensagens:
                    yield msg
                time.sleep(0.1)
        except grpc.RpcError:
            print(f"Conexão com o  {usuario} finalizada")

    def SendMessage(self, request, context):
        mensagem = request.message
        print(f"Nova mensagem de {mensagem.user}: {mensagem.content}")

        with self.lock:
            self.messages.append(mensagem)

        return chat_pb2.Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port('[::]:50052')
    print("Servidor rotando da porta 50052...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()