# encoding = utf-8

import sys
import select
import json
import socket
from termcolor import colored, cprint

def main():

	# Socket
	chat_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ## Criar socket que que utiliza IPv4 e protocolo TCP
	chat_skt.bind(("0.0.0.0", 0)) # IP e porto do computador do utilizador

	# Ligar ao servidor
	try:
		endereco_server = chat_skt.connect( ("37.247.48.69", 1863) ) # conectar o socket ao IP XX.XX.XX.XX e ao porto XXXX
	except:
		print colored("\nLigacao nao estabelecida! A encerrar programa...\n", 'red', attrs = ['bold'])
		sys.exit()

	# Menu
	print "\n"
	print " --------------------------------------------------------------------------"
	print "      				 CHAT - LABI                     "
	print " --------------------------------------------------------------------------"
	print(colored("\n 				  Conectado!\n", 'green'))

	print " Seleciona uma opcao:\n 1 - Escolher nome de Utilizador\n 2 - Enviar mensagem\n 3 - Ajuda\n 4 - Ver utilizadores ativos e o teu nome\n 5 - Sair\n"

	msg_lista = [] #lista usada para o ciclo for

	while True:

		# Select
		msg_select = select.select([chat_skt, sys.stdin, ] , [], [])[0] #ver argumentos
		for sock in msg_select:
			if sock == chat_skt:
				data = chat_skt.recv(4096).decode() #recebe uma string de dados de ate 4096 bytes
				receber_msg(chat_skt, data) #funcao de receber as strings/mensagens
			elif sock == sys.stdin:
				data = sys.stdin.readline() # le o keyboard (ver melhor)
				kb_input(chat_skt, data) #funcao para escolher opcoes e mandar mensagem etc



	for dst_endereco in msg_lista: #ver ciclo for
		chat_skt.send(dst_endereco) # manda
	chat_skt.close() #fecha socket

def kb_input(chat_skt, data):

	menu = raw_input(colored("Opcao >> ", 'blue', attrs = ['bold']))
	print "\n"

	if menu == "1":
		utilizador = raw_input(colored('ESCOLHER NOME DE UTILIZADOR: ', 'blue', attrs=['bold']) )
		choose_user = {'from': utilizador}
		data = json.dumps(choose_user) + "\n" #le o ficheiro json
		chat_skt.send(data) #enviar resposta

	if menu == "2":
		receptor = raw_input( colored('ENVIAR MENSAGEM PARA: ', 'blue', attrs=['bold']))
		mensagem = raw_input( colored('MENSAGEM: ', 'blue', attrs=['bold']))
		data_flow={'to':receptor, 'msg':mensagem}
		if (not mensagem):
			print colored("ERRO: Nao escreveste uma mensagem\n", 'red', attrs = ['bold']) #caso o user nao escrever msg, da mensagem de erro
		if mensagem == "quit": #CASO O UTILIZADOR META "QUIT" O PROGRAMA TERMINA
			while False:
				continue
		else:
			data = json.dumps(data_flow) + "\n" #le o ficheiro json
			chat_skt.send(data) #enviar resposta
		print "\n"

	#Ajuda
	if menu == "3":
		print colored("                                 	AJUDA:\n >> E' considerado erro quando: nao introduz mensagem ou quando recebem mensagem vazia.\n >> Se o campo 'ENVIAR MENSAGEM PARA' estiver vazio e' considerado que deseja mandar a mensagem para todos os utilizadores.\n", 'grey', attrs = ['bold'])

	#Sair
	if menu == "5":
		sys.exit()

	if menu == "4":
		chat_skt.send("{ }\n")
		data = chat_skt.recv(4096).decode()
		d = dict()
		d = json.loads(data)
		print ""
		print colored("Utilizadores ativos: ", 'green', attrs = ['bold']) + d["to"] + colored("\nTeu nome de utilizador: ",  'green', attrs = ['bold']) + d["from"]
		print "\n"

def receber_msg(chat_skt, data):

	try: #tenta escrever mensagem de ate 4096 bytes
		d = dict()
		d = json.loads(data) #passa o json para python

		if "msg" in d:
			print colored('DE: ', 'green', attrs=['bold']) + d["from"]
			print colored('PARA: ', 'green', attrs=['bold']) + d["to"]
			print colored('MENSAGEM NOVA: ', 'green', attrs=['bold']) + d["msg"]
			print "\n"
		elif "error" in d:
			print colored('ERRO: Mensagem do emissor nao encontrada.\n ', 'red')
	except: #se ultrapassar faz o except
		men = data.split("\n") #faz splits das mensagens ao detectar os "\n"
		try: #tenta escrever a mensagem > 4096 bytes em varias msg's
			for i in range(len(men)):
				d = dict()
				d = json.loads(men[i])
				print ""
				if "msg" in d:
					print colored('DE: ', 'green', attrs=['bold']) + d["from"]
					print colored('PARA: ', 'green', attrs=['bold']) + d["to"]
					print colored('MENSAGEM NOVA: ', 'green', attrs=['bold']) + d["msg"]
				elif "error" in d:
					print colored('ERRO: Mensagem do emissor nao encontrada.\n ', 'red', attrs = ['bold'])
		except:
			while False:
				continue #continua o programa




main()
