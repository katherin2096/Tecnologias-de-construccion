from flask import Flask, jsonify, request, make_response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import json

app=Flask(__name__)
auth= HTTPBasicAuth()
users = {
    "kathy": generate_password_hash("gatito"),
    "susan": generate_password_hash("bye"),
    "ahidalgog": generate_password_hash("12345678")
}

app.config['SECRET_KEY']='secretkey'

with open('paises.json') as f:
    data = json.load(f)

@auth.verify_password
def verify_password(username,password):
    if username in users and check_password_hash(users.get(username), password):
        return username

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = request.args.get('token')
		if not token:
			return jsonify({'message' : 'Falta colocar el token'}), 403
		try:
			data = jwt.decode(token, app.config['SECRET_KEY'])
		except:
			return jsonify({'message' : 'Este token no es valido'}), 403
		return f(*args, **kwargs)
	return decorated    
@app.route('/unprotected')
def unprotected():
    return jsonify({'message': 'Anyone can view this!'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message' : 'This is only'})
    
@app.route('/login')
def login():
    auth1=request.authorization
    if auth1 and verify_password(auth1.username,auth1.password)==auth1.username:
        token=jwt.encode({'user':auth1.username, 'exp':datetime.datetime.utcnow() +datetime.timedelta(minutes=1) },app.config['SECRET_KEY'])

        return jsonify({'token':token.decode('UTF-8')})
    return make_response('Could not verify!',401,{'WWW-Authenticate':'Basic realm="Login Required"'})

@app.route('/paises', methods=['GET'])
@token_required
def mostrar():       
    return jsonify(data)

@app.route('/agregarPais', methods=['POST'])
@token_required
def agregarPais():
    pais=request.args.get('pais')
    data.update({pais:{}})
    with open('paises.json', 'w') as file:
        json.dump(data, file)
        return jsonify({'resultado':'exitoso', 'pais agregado': pais})

@app.route('/agregarRegion', methods=['POST'])
@token_required
def agregarRegion():
    pais=request.args.get('pais')
    region=request.args.get('region')
    if pais in data:
        data[pais].update({region:{}})
        with open('paises.json', 'w') as file:
            json.dump(data, file)
            return jsonify({'resultado':'exitoso', 'region agregada': region})
    else:
        return jsonify({'resultado':'fallido', 'No existe': pais})

@app.route('/agregarDistrito', methods=['POST'])
@token_required
def agregarDistrito():
    pais=request.args.get('pais')
    region=request.args.get('region')
    distrito=request.args.get('distrito')
    if pais in data and region in data[pais]:
        data[pais][region].update({distrito:{}})
        with open('paises.json', 'w') as file:
            json.dump(data, file)
            return jsonify({'resultado':'exitoso', 'distrito agregado': distrito})
    else:
        return jsonify({'resultado':'fallido', 'Es probable que no exista': pais, "Es probable que no exista":region})


@app.route('/modificarPais', methods=['PUT'])
@token_required
def modificarPais():
    pais=request.args.get('pais')
    nuevo=request.args.get('nuevo')
    if pais in data:
        data[nuevo]=data.pop(pais)
        with open('paises.json', 'w') as file:
            json.dump(data, file)
            return jsonify({'resultado':'exitoso', 'pais modificado': pais,'pais actualizado':nuevo})
    else:
         return jsonify({'resultado':'fallido', 'No existe pais': pais})   

@app.route('/eliminarPais', methods=['DELETE'])
@token_required
def eliminarPais():
    pais=request.args.get('pais')
    if pais in data:
        del data[pais]
        with open('paises.json', 'w') as file:
            json.dump(data, file)
            return jsonify({'resultado':'exitoso', 'pais eliminado': pais})
    else:
         return jsonify({'resultado':'fallido', 'No existe pais': pais})   
        
if __name__ == '__main__':
    app.run(debug=True)