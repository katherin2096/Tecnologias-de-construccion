#!C:/Python3.8/python.exe

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
import json

app = Flask(__name__)
api = Api(app)

ambitos = {}

ambitos.setdefault('cocina',["manzana","cuchara","platico","martillo"])
ambitos.setdefault('limpieza',["escoba","trapeador","jabon"])
ambitos.setdefault('taller',["martillo","serrucho","desarmador"])

parser = reqparse.RequestParser()

class tipoProducto(Resource):
	def get(self):
		return ambitos
	
	Claves=ambitos.keys()
	Valores=ambitos.values()
	
#get_values_if_any(d1, somekey)
class find(Resource):
	def get(self,valor):
		res=[]
		for it1 in ambitos:
			for it2 in ambitos[it1]:
				if it2 == valor:
					res.append(it1)
		if 	len(res)>0:
			return json.dumps(res)	
		else:
			return "Not found", 404
	

class cocina(Resource):
	def get(self):
		return ambitos['cocina']
class taller(Resource):
	def get(self):
		return ambitos['taller']
class limpieza(Resource):
	def get(self):
		return ambitos['limpieza']

@app.route('/productos/registro', methods=['POST'])
def registroJson():
	data = request.get_json()
	categoria= data['categoria']
	item= data['item']
	for it1 in ambitos:
		if(it1==categoria):
			ambitos.setdefault(categoria, []).append(item)
			return jsonify({'resultado':'exitoso', 'categoria modificada': categoria,'item agregado':item})
	
	return jsonify({'resultado':'fallido','no existe categoria':categoria})

@app.route('/productos/registro/categoria', methods=['POST'])
def registroCategoriaJson():
	data = request.get_json()
	categoria= data['categoria']
	item= data['item']
	ambitos.setdefault(categoria, []).append(item)
	return jsonify({'resultado':'exitoso','categoria nueva':categoria,'item cargado':item})


api.add_resource(tipoProducto, '/productos')
api.add_resource(cocina, '/productos/cocina')
api.add_resource(taller, '/productos/taller')
api.add_resource(limpieza, '/productos/limpieza')
api.add_resource(find, '/productos/busqueda/<valor>')

if __name__ == '__main__':

	app.run(debug=True)
