#enconding = utf-8

import pytest
from programa import kb_input

def test1():

    chat_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ## Criar socket que que utiliza IPv4 e protocolo TCP
    data = json.dumps(choose_user) + "\n"
    chat_skt.send(data)
    assert programa.kb_input(chat_skt, data) == "funca"
    chat_skt.close()
