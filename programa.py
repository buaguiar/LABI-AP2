
# encoding = utf-8
import sys
import select
import json
import socket
from termcolor import colored, cprint

def main():

	# Config
	chat_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	chat_skt.bind(("0.0.0.0", 0))

	#Ligar ao servidor
	endereco_server = chat_skt.connect( ("37.247.48.69", 1863) )

	print "\n"
	print " --------------------------------------------------------------------------"
	print "      				 CHAT - LABI                     "
	print " --------------------------------------------------------------------------"
	print(colored("\n 				  Conectado!\n", 'green'))

	msg_lista = []

	while True:

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

	utilizador = raw_input(colored('Escreva o seu nome de utilizador:  ', 'blue', attrs=['bold']) )
	receptor = raw_input( colored('Enviar mensagem para  ', 'blue', attrs=['bold']))
	mensagem = raw_input( colored('Mensagem:  ', 'blue', attrs=['bold']))
	choose_user = {'from': utilizador}
	data_flow={'from':utilizador, 'to':receptor, 'msg':mensagem}
	print "\n"
	print colored('DE: ', 'cyan') + data_flow['from']
	print colored('PARA: ', 'cyan') + data_flow['to']
	if (not mensagem):
		print colored("ERRO: Nao escreveste uma mensagem", 'red', attrs = ['bold'])
	else:
		print colored('MENSAGEM: ', 'cyan') + data_flow['msg']
		print "\n"
	data = json.dumps(data_flow) + "\n"


	chat_skt.send(data) #enviar resposta

def receber_msg(chat_skt, data):

	try:
		d = dict()
		d = json.loads(data)

		if "msg" in d:
			print colored('DE: ', 'green', attrs=['bold']) + d["from"]
			print colored('PARA: ', 'green', attrs=['bold']) + d["to"]
			print colored('MENSAGEM NOVA: ', 'green', attrs=['bold']) + d["msg"]
		else:
			print colored('ERRO: Mensagem do emissor nao encontrada). ', 'red')
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
				else:
					print colored('ERRO: Mensagem do emissor nao encontrada). ', 'red')
		except:
			while True:
				continue




main()
