import jwt
import datetime
import time
from Users_Model import *

class Token_Model(object):
	def __init__(self,data={}):
		self.key='kaoskakibiru12345'
		self.data = data
	def get_encoded(self):
		encoded = jwt.encode(self.data,self.key,'HS256')
		return encoded
	def get_decoded(self):
		decoded = jwt.decode(self.data,self.key,'HS256')
		return decoded

class Auth_Model(object):
	def __init__(self):
		self.username = ''
		self.password = ''
	def login(self,username,password):
		self.username = username
		self.password = password
		users = Users_Model()
		user_detail = users.find(self.username)
		token_expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
		user_detail['exp']=token_expiration
		if (user_detail is not None):
			return Token_Model(user_detail).get_encoded()
		else:
			return None
	def cek_token(self,data):
                if data=='':
                    return None
		try:
			return Token_Model(data).get_decoded()
		except jwt.ExpiredSignatureError:
			return None


if __name__ == '__main__':
	auth = Auth_Model()
	token = auth.login('slamet','kaoskakimerah')
	print token
	#time.sleep(2)
	cek = auth.cek_token(token)
	print cek
	#cek will be None if token is expired

