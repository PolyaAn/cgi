# -*- coding: utf-8 -*-

import os, sys, re, codecs, binascii, cgi, cgitb, datetime, pickle
from msg import *

cgitb.enable()
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

class Messenger:
	def __init__(self, q):
		self.q = q
		Message.ClientID = int(q.getvalue('ClientID', 0))
		if Message.ClientID == 0:
			Message.SendMessage(M_BROKER, M_INIT)
		self.MessageText = ''
		self.messages = ''

	def PrintPage(self):
		print(f"""Content-type: text/html; charset=utf-8

<html><head><title>Messages</title></head>
<body style = "display: flex; justify-content: center; font-family: sans-serif;">
<img src="https://psv4.userapi.com/c856236/u135707660/docs/d7/cd11a4b1dba8/IMG_7391.jpg?extra=iJif-dySath4g11pRZD7y1Xi9pZYDDqHc7a5ytUu1zOthqRQN4NBplUWF-HZ_Ex57EGpgNi0bTtU1EeVMZIRisjoX62FbpZhJmwG5OX7qhqLCATSklo7tNezH34l2IwYw406d2QMaANMbTiDfYwKSzs" style="z-index: -12321231; position: absolute"></img>
<form action=/cgi-bin/WebClient.py name=msgform style= "margin-top: 7%;">
<div style =" background-color: white;
    		  width: 100px;
    		  height: 30px;
			  display: flex;
              flex-direction: column;
              justify-content: center;
			  border-radius: 5px;
			  margin-bottom: 20px;
    		  text-align: center;">
			  <span>Ваш ID = {Message.ClientID}</span></div>
<input type=hidden name=type value="send">
<input type=hidden name=ClientID value="{Message.ClientID}">
<input type=text 
	name=message
	value="{self.MessageText}"
	style = 
		"border-radius: 5px;
		width: 800px;
		height: 40px;
		margin-right: 10px;
		border-style: none;"
		placeholder = "Введите сообщение">
<input type = text
       name = id	style = 
		"border-radius: 5px;
		height: 40px;
		width: 200px;
		border-style: none;"
		placeholder = "Введите ID">
<br>
<input type=submit 
	value="Send"
	style= "height: 40px;
		 width: 200px;
		 border-radius: 5px;
		 border-style: none;
		 float: right;
		 margin: 10px;
		 margin-right: 0px;"
		 >
<input type=button 
	value="Get"	
	onclick="document.forms.msgform.type.value='get'; document.forms.msgform.submit();"
	style= "height: 40px;
		 width: 200px;
		 border-radius: 5px;
		 border-style: none;
		 float: right;
		 margin: 10px;
		 margin-right: 5px"
		 >
<div style="margin-top: 80px;
			  background-color: white;
			  display: flex;
              flex-direction: column;
              justify-content: center;
			  border-radius: 5px;
			  margin-bottom: 20px;
    		  text-align: center;"><span>Входящие сообщения: {self.messages}</span></div>
</form>
</body></html>
	""")


	def MsgSend(self):
		id = ''
		try:
			id = int(self.q.getvalue('id'))
		except:
			pass
		Message.SendMessage(M_ALL if id == '' else id, M_DATA, self.q.getvalue('message'))

		
	def MsgGet(self):
		pass

	def getAll(self): 
		m = Message.SendMessage(M_BROKER, M_ALLDATA)
		if m.Header.Type == M_DATA:
			self.messages = ', '.join(m.Data.split(':::::::'))


def main():
	q = cgi.FieldStorage()
	m = Messenger(q)

	MENU = {
		'send':	m.MsgSend,
		'get':  m.MsgGet,
	}
    

	try:
		MENU[q.getvalue('type')]()
		m.getAll()
	except Exception as e:
		pass

	m.PrintPage()
        
main()
