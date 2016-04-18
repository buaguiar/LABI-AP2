# encoding = utf-8

import sys
import select
import json
import socket
from termcolor import colored, cprint

def main():

	# Socket
	chat_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	chat_skt.bind(("0.0.0.0", 0))

	# Ligar ao servidor
	endereco_server = chat_skt.connect( ("37.247.48.69", 1863) )

	# Menu
	print "\n"
	print " --------------------------------------------------------------------------"
	print "      				 CHAT - LABI                     "
	print " --------------------------------------------------------------------------"
	print(colored("\n 				  Conectado!\n", 'green'))

	print " Seleciona uma opcao:\n 1 - Enviar mensagem\n 2 - Ajuda\n 3 - Sair\n"

	msg_lista = []

	while True:

		# Select
		msg_select = select.select([chat_skt, sys.stdin, ] , [], [])[0]
		for sock in msg_select:
			if sock == chat_skt:
				data = chat_skt.recv(4096).decode()
				receber_msg(chat_skt, data)
			elif sock == sys.stdin:
				data = sys.stdin.readline()
				mandar_msg(chat_skt, data)



	for dst_endereco in msg_lista:
		chat_skt.send(dst_endereco)
	chat_skt.close()

def mandar_msg(chat_skt, data):

	menu = raw_input(colored("Opcao >> ", 'blue', attrs = ['bold']))
	print "\n"

	if menu == "1":

		utilizador = raw_input(colored('ESCOLHER NOME DE UTILIZADOR: ', 'blue', attrs=['bold']) )
		receptor = raw_input( colored('ENVIAR MENSAGEM PARA: ', 'blue', attrs=['bold']))
		mensagem = raw_input( colored('MENSAGEM: ', 'blue', attrs=['bold']))
		choose_user = {'from': utilizador}
		data_flow={'from':utilizador, 'to':receptor, 'msg':mensagem}
		if (not mensagem):
			print colored("ERRO: Nao escreveste uma mensagem\n", 'red', attrs = ['bold'])
		else:
			data = json.dumps(data_flow) + "\n"
			chat_skt.send(data) #enviar resposta
		print "\n"

	if menu == "2":
		print colored("                                 	AJUDA:\n >> E' considerado erro quando: nao introduz mensagem ou quando recebem mensagem vazia.\n >> Se o campo 'ENVIAR MENSAGEM PARA' estiver vazio e' considerado que deseja mandar a mensagem para todos os utilizadores.\n", 'grey', attrs = ['bold'])

	if menu == "3":
		sys.exit()

def receber_msg(chat_skt, data):

	try:
		d = dict()
		d = json.loads(data)

		if "msg" in d:
			print colored('DE: ', 'green', attrs=['bold']) + d["from"]
			print colored('PARA: ', 'green', attrs=['bold']) + d["to"]
			print colored('MENSAGEM NOVA: ', 'green', attrs=['bold']) + d["msg"]
			print "\n"
		elif "error" in d:
			print colored('ERRO: Mensagem do emissor nao encontrada.\n ', 'red')
	except:
		men = data.split("\n")
		try:
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
				continue




main()
