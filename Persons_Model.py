import uuid
import pickledb

'''
install uuid ==> pip install uuid
install pickledb ==> pip install pickledb
'''


class Persons_Model(object):
	def __init__(self):
		self.db = pickledb.load('persons.db',True)
		#True ==> untuk bisa disimpan
		try:
			self.list()
		except KeyError:
			self.db.dcreate('persondb')
	def add(self,p):
		if not isinstance(p,dict):
			return { "result" : "ERROR" }
		uid = uuid.uuid1()	
		self.db.dadd('persondb',( "{}" .  format(str(uid)) ,  p ))
		return { "uid" : "{}" . format(str(uid)) }
	def list(self):
		return self.db.dgetall('persondb')
	def get(self,id):
		return self.db.dget('persondb',id)
	def empty(self):
		try:
			self.db.drem('persondb')
			self.db.dcreate('persondb')
		except KeyError:
			self.db.dcreate('persondb')
		return True
	def remove(self,id):
		self.db.dpop('persondb',id)
		return True


if __name__ == '__main__':
	p = Persons_Model()
	p.empty()
	print p.list()
	p.add({'nama': 'Royyana', 'alamat': 'Ketintang'})
	p.add({'nama': 'Ananda', 'alamat': 'SMP 6'})
	p.add({'nama': 'Ibrahim', 'alamat': 'TK Perwanida'})
	print p.list()
	#p.empty()
	#print p.list()
	#p.add({'nama': 'Azam', 'alamat': 'SD Alfalah Surabaya'})
	#print p.list()

