# Chat GRPC

Chat de comunicação feito com grpc implementado através de micro serviços

## Instalação das dependências

Execute o comando:

```
pip install -r requirements.txt
```

## Execução do código

Execute os seguintes comandos no terminal:

Iniciar o servidor:
```
python -m services.chat_service.main
```

Iniciar o gateway:
```
python -m services.gateway_service.main
```

Iniciar o client para troca de mensagens, o client pode ser iniciado em diversos terminais pra a troca de mensagens entre diversos clients:
```
python -m client.main
```