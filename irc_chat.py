import socket, ssl, re, json, sys

def main(HOST, PORT, NICK, PASS, JOIN):
	JOIN = JOIN.split(';')
	
	irc = IRC(HOST, int(PORT))
	irc.connect(NICK, PASS)

	for channel in JOIN:
		irc.join(channel)
	while True:
		# msg = ircsock.recv(4096).decode("UTF-8").rstrip()
		msg = irc.recv()
		if(msg == 'PING :tmi.twitch.tv'):
			irc.send("PONG :tmi.twitch.tv")
		if('PRIVMSG' in msg):
			msgList = irc.PRIVMSG(msg)
			with open("/opt/irc_PRIVMSG_{}.txt".format(msgList['room-name']), "a") as f:
				f.write(str(msgList) + "\r\n")
		elif('USERNOTICE' in msg):
			msgList = irc.USERNOTICE(msg)
			print(msgList)
			with open("/opt/irc_USERNOTICE_{}.txt".format(msgList['room-name']), "a") as f:
				f.write(str(msgList) + "\r\n")
	irc.send("PART #{channel}".format(channel=channel))

class IRC:
	host = str(None)
	port = str(0)
	sock = None
	conn = None
	def __init__(self, host, port):
		self.host = host
		self.port = port
	def connect(self, username, passwd):
		self.sock = socket.socket(socket.AF_INET)
		context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
		context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
		self.conn = context.wrap_socket(self.sock, server_hostname=self.host)
		self.conn.connect((self.host, self.port))
		self.send("PASS oauth:{oauth}".format(oauth=passwd))
		self.send("NICK {username}".format(username=username))
		self.send("CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands")
	def join(self, channel):
		self.send("JOIN #{channel}".format(channel=channel))
		while True:
			msg = self.recv()
			if("End of /NAMES list" in msg):
				break
	def send(self, msg, charset = "UTF-8"):
		return self.conn.send(bytes(msg + "\r\n", charset))
	def recv(self, bit = 4096, charset = "UTF-8"):
		return self.conn.recv(bit).decode(charset).rstrip()
	def __tagsort(self, tagstr):
		temp = tagstr.split(';')
		returnList = {}
		for i in range(len(temp)):
			temp_i = temp[i].split('=')
			if(temp_i[0] not in ['subscriber', 'turbo', 'user-type', 'mod']):
				if(temp_i[0] in ['badge-info', 'badges']):
					if(temp_i[1] == ''):
						returnList[temp_i[0]] = None
					else:
						temp0 = temp_i[1].split(',')
						temp0List = {}
						for j in range(len(temp0)):
							temp0_j = temp0[j].split('/')
							if(temp0_j[1] == ''):
								temp0List[temp0_j[0]] = None
							else:
								temp0List[temp0_j[0]] = temp0_j[1].replace('\\s', ' ')
						returnList[temp_i[0]] = temp0List
				else:
					if(temp_i[1] == ''):
						returnList[temp_i[0]] = None
					else:
						returnList[temp_i[0]] = temp_i[1].replace('\s', ' ')
		return returnList
	def USERNOTICE(self, msgStr):
		pattern = re.compile(r'@(.*) :tmi.twitch.tv (.*) #(\w*)(.*)?')
		msgList = list(re.findall(pattern, msgStr)[0])
		print(msgList)
		returnList = {
			'room-name': msgList[2],
			'msg-type': msgList[1],
		}
		returnList.update(self.__tagsort(msgList[0]))
		return returnList
		return msgStr
	def PRIVMSG(self, msgStr):
		pattern = re.compile(r'@(.*) :(.*)!(.*)@(.*) (.*) #(\w*) :(.*)?')
		msgList = list(re.findall(pattern, msgStr)[0])
		returnList = {
			'room-name': msgList[5],
			'msg-type': msgList[4],
		}
		returnList.update(self.__tagsort(msgList[0]))
		returnList['msg'] = msgList[6]
		return returnList

if(__name__ == "__main__"):
	s = sys.argv
	print(str(s))
	main( s[1], s[2], s[3], s[4], s[5] )
