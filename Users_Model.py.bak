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
	def add(self,username='',password='',detail={}):
		id = uuid.uuid1()	
		p = { 'username' : username, 'password': password, 'detail' : detail}
		self.db.dadd('userdb',( "{}" .  format(str(id)) ,  p ))
		return self.db.get(id)
	def list(self):
		return self.db.dgetall('userdb')
	def get(self,id):
		return self.db.dget('userdb',id)
	def find(self,username=''):
		for x in self.list():
			data = self.get(x)
			if (data['username']==username):
				return data	
		return None
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
	users.empty()
	users.add('royyana','kaoskakibiru',{ 'nama' : 'Royyana Muslim Ijtihadie', 'alamat': 'Ketintang' })
	users.add('slamet', 'kaoskakimerah',{'nama' : 'Slamet Raharjo', 'alamat': 'Menteng' })
	users.add('mertens','kanankiriatas',{ 'nama' : 'Dries Mertens', 'alamat': 'Belgia' })
	users.add('pulisic','kaoskakihijau',{ 'nama' : 'Christian Pulisic', 'alamat': 'Washington' })
	#print users.find('notfound')
	print users.find('slamet')

