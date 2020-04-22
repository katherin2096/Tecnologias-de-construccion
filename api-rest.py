#!C:/Python3.8/python.exe

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_httpauth import HTTPBasicAuth
import json

app = Flask(__name__)
api = Api(app)
#api=Api(app, prefix="/ingresar")
auth=HTTPBasicAuth()


USER_DATA={
    "admin":"Gatitos"
}

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password


class PrivateResource(Resource):
    @auth.login_required
    def get(self):
        return{"Holi bienvenidos al mundo de gatos felices":3}
    
api.add_resource(PrivateResource,'/private')

ambitos = {}

ambitos.setdefault('cocina',["manzana","cuchara","platico","martillo"])
ambitos.setdefault('limpieza',["escoba","trapeador","jabon"])
ambitos.setdefault('taller',["martillo","serrucho","desarmador"])

parser = reqparse.RequestParser()

Claves=ambitos.keys()
Valores=ambitos.values()

@app.route('/productos', methods=['GET'])
def getProducto():
	return ambitos

@app.route('/productos/<categoria>', methods=['GET'])
def getCategoria(categoria):
	return jsonify(ambitos[categoria])

@app.route('/productos/buscar/<valor>', methods=['GET'])
def getBuscar(valor):
	res=[]
	for it1 in ambitos:
		for it2 in ambitos[it1]:
			if it2 == valor:
				res.append(it1)
	if 	len(res)>0:
		return jsonify(res)	
	else:
		return "Not found", 404

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

@app.route('/productos/eliminar/<string:categoria>', methods=['DELETE'])
def eliminar(categoria):
	data = request.get_json()
	item= data['item']
	if categoria in ambitos:
		ambitos [categoria] .remove(item)
		return jsonify({'resultado':'exitoso', 'categoria modificada': categoria,'item borrado':item})
	else:
		return jsonify({'resultado':'fallido'})

@app.route('/productos/modificar/<string:categoria>', methods=['PUT'])
def modificar(categoria):
	data = request.get_json()
	item= data['item']
	nuevo_item=data['nuevo_item']
	if categoria in ambitos:
		for it1 in ambitos:
			cont=0
			for it2 in ambitos[it1]:
				if it2==item:
					ambitos[it1][cont]=nuevo_item
					return jsonify({'resultado':'exitoso', 'categoria modificada': categoria,'item anterior':item, 'item actualizado':nuevo_item})
				cont=cont+1
		return jsonify({'resultado':'fallido', "no existe item":item})
	else:
		return jsonify({'resultado':'fallido', "no existe categoria":categoria})

if __name__ == '__main__':
	app.run(debug=True)