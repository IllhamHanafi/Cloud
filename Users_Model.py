import uuid
import pickledb

'''
install uuid ==> pip install uuid
install pickledb ==> pip install pickledb
'''


class Users_Model(object):
	def __init__(self):
		self.db = pickledb.load('users.db',True)
		#True ==> untuk bisa disimpan
		try:
			self.list()
		except KeyError:
			self.db.dcreate('userdb')
	def add(self,username='',password=''):
		for x in self.list():
			data = self.get(x)
			if (data['username']==username):
					return False
		id = uuid.uuid4()
		p = {'username': username, 'password': password}
		self.db.dadd('userdb', ("{}".format(str(id)), p))
		return True
	def list(self):
		return self.db.dgetall('userdb')
	def get(self,id):
		return self.db.dget('userdb',id)
	def find(self, username=''):
		for x in self.list():
			data = self.get(x)
			if (data['username'] == username):
				return data
		return None
	def login (self,username='', password=''):
		for x in self.list():
			data = self.get(x)
			if (data['username']==username):
				if (data['password']==password):
					print 'Login Success !'
					return True
				else:
					print 'Login Failed !'
					return False
		return False
	def empty(self):
		try:
			self.db.drem('userdb')
			self.db.dcreate('userdb')
		except KeyError:
			self.db.dcreate('userdb')
		return True
	def remove(self,id):
		self.db.dpop('userdb',id)
		return True


if __name__ == '__main__':
	users = Users_Model()
#	users.empty()
	# users.add('azka','yasin')
	# users.add('via', 'valen')
	# users.add('adam','alfian')
	# users.add('nella','kharisma')
	# users.add('admin', 'admin')
	#print users.find('slamet')

