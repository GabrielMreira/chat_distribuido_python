import grpc
import threading
import datetime
import chat_pb2
import chat_pb2_grpc

def receive_messages(stub, user):
    try:
        conexao_request = chat_pb2.ConnectRequest(user=user)

        for mensagem in stub.ReceiveMessages(conexao_request):
            print(f"[{mensagem.timestamp}] {mensagem.user}: {mensagem.content}")
    except grpc.RpcError as e:
        print(f"Erro ao conectar : {e.details()}")

def run():
    with grpc.insecure_channel('localhost:50051') as canal:
        stub = chat_pb2_grpc.ChatServiceStub(canal)

        usuario = input("Insira seu nome de usuario: ")
        print(f"Bem vindo {usuario}, você está conectado ao chat")

        thread_recebedora = threading.Thread(
            target=receive_messages, args=(stub,usuario), daemon=True
        )
        thread_recebedora.start()

        while True:
            try:
                conteudo = input()
                if conteudo.lower() == 'sair':
                    break

                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                mensagem = chat_pb2.Message(user=usuario, content=conteudo, timestamp=timestamp)
                requisicao = chat_pb2.SendMessageRequest(message=mensagem)

                stub.SendMessage(requisicao)
            except KeyboardInterrupt:
                break
        print("Você foi desconectado")

if __name__ == '__main__':
    run()