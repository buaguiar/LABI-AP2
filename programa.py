import sys
import select
import json
import socket
from termcolor import colored, cprint
import curses

def main():

	# Configurar o meu porto
	chat_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	chat_skt.bind(("0.0.0.0", 0))

	#Ligar ao servidor
	endereco_server = chat_skt.connect( ("37.247.48.69", 1863) )
	msg_lista = []

	while True:

		#msg_select = select([sys.stdin, chat_skt], [], [])

		#for chat_skt in msg_select:

		print "\n"
		print " --------------------------------------------------------------------------"
		print "      				 CHAT - LABI                     "
		print " --------------------------------------------------------------------------"
		print "\n"

		#JSON para os dados

		utilizador = raw_input(colored('Escreva o seu nome de utilizador:  ', 'blue', attrs=['bold']) )
		receptor = raw_input( colored('Enviar mensagem para  ', 'blue', attrs=['bold']))
		mensagem = raw_input( colored('Mensagem:  ', 'blue', attrs=['bold']))
		choose_user = {'from': utilizador}
		data_flow={'from':utilizador, 'to':receptor, 'msg':mensagem}
		print "\n"
		print colored('DE: ', 'cyan') + data_flow['from']
		print colored('PARA: ', 'cyan') + data_flow['to']
		print colored('MENSAGEM: ', 'cyan') + data_flow['msg']
		print "\n"
		str = json.dumps(data_flow) + "\n"

		#mandar mensagem para o servidor
		chat_skt.send(str)
		str = chat_skt.recv(4096)
		d = json.loads(str)
		#str.split(str = "\n", num = string.count(str))
		# print str
		# print d
		if "msg" in d:
			print colored('DE: ', 'green', attrs=['bold']) + d["from"]
			print colored('PARA: ', 'green', attrs=['bold']) + d["to"]
			print colored('MENSAGEM: ', 'green', attrs=['bold']) + d["msg"]
		else:
			print colored('ERRO: Mensagem nao encontrada do(s) destinatario(s). ', 'red', attrs = ['reverse'])
	chat_skt.close()

	for dst_endereco in msg_lista:
		chat_skt.sendto(dst_endereco)
main()

	# FAZER O SELECT E METER A DAR AS MENSAGENS DE ERRO.
