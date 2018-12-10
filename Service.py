from flask import Flask,request,jsonify
from flask_restful import Resource, Api, reqparse
import json
import os
from Persons_Model import *
from Auth_Model import *

p_model = Persons_Model()

app = Flask(__name__)
api = Api(app)



class PersonList(Resource):
        def auth_cek(self):
            self.token = request.headers.get('Authorization') or ''
            self.cek = Auth_Model().cek_token(self.token)
	    if (self.cek is None):
                return {'STATUS' : 'Error Authentication'}
            else:
                return None

        def get(self,id=''):
		return self.auth_cek() or p_model.list()
	def post(self):
                args = request.get_json(force=True)
                data = args
		return self.auth_cek() or p_model.add(data)

class Person(Resource):
        def auth_cek(self):
            self.token = request.headers.get('Authorization') or ''
            self.cek = Auth_Model().cek_token(self.token)
	    if (self.cek is None):
                return {'STATUS' : 'Error Authentication'}
            else:
                return None

	def get(self,id):
		return self.auth_cek() or p_model.get(id)
	def delete(self,id):
		return self.auth_cek() or p_model.remove(id)

class Version(Resource):
	def get(self):
		iplist = os.popen("ifconfig eth0 | grep 'inet addr'").readlines()
		my_ip = "".join(iplist)
                return { 'info' : '0.01', 'ip' : "{}" . format(my_ip) }

class Auth(Resource):
	def post(self):
		data = request.get_json(force=True)
		username = data['username'] 
		password = data['password']
		a_model = Auth_Model()
		auth_result = a_model.login(username,password)
		if (auth_result is not None):
			return jsonify(status='OK',token=auth_result)
		else:
			return jsonify(status='ERROR',token=None)
	def get(self,token=''):
		if (token==''):
			return jsonify(status='ERROR')
		a_model = Auth_Model()
		auth_result = a_model.cek_token(token)
		if (auth_result is not None):
			return jsonify(status='OK',token=auth_result)
		else:
			return jsoninfy(status='ERROR')


#definisi rest api interface
api.add_resource(Version,'/version')
api.add_resource(PersonList,'/personlist')
api.add_resource(Person,'/person/<id>')
api.add_resource(Auth,'/auth')



# menjalankan web server

from gevent.pywsgi import WSGIServer
http_server = WSGIServer(('', 5000),app)
http_server.serve_forever()

		


