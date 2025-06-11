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

## Execução com docker:

Com o docker desktop instalado na maquina, rode o seguinte comando:

```
docker-compose up
```

Apos os containers estarem online, rode o seguinte comando para iniciar o ou os clientes:
```
python -m client.main
```

Para finalizar o docker aperte ```Ctrl + C``` e execute o seguinte comando:
```
docker-compose down
```