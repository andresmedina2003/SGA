from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://andresmedin1:AndMen03$@cluster0.gvzqbpc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
mongo = PyMongo(app)

class Aeropuerto:
    def __init__(self, nombre, ciudad):
        self.nombre = nombre
        self.ciudad = ciudad

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'ciudad': self.ciudad
        }

class Vuelo:
    def __init__(self, numero, origen, destino):
        self.numero = numero
        self.origen = origen
        self.destino = destino

    def to_dict(self):
        return {
            'numero': self.numero,
            'origen': self.origen,
            'destino': self.destino
        }

@app.route('/aeropuertos', methods=['GET'])
def obtener_aeropuertos():
    aeropuertos = mongo.db.aeropuertos.find()
    resultados = [aeropuerto for aeropuerto in aeropuertos]
    return jsonify(resultados)

@app.route('/aeropuertos', methods=['POST'])
def crear_aeropuerto():
    datos = request.get_json()
    nuevo_aeropuerto = Aeropuerto(datos['nombre'], datos['ciudad'])
    mongo.db.aeropuertos.insert_one(nuevo_aeropuerto.to_dict())
    return jsonify({'mensaje': 'Aeropuerto creado exitosamente'})

@app.route('/aeropuertos/<id>', methods=['PUT'])
def modificar_aeropuerto(id):
    datos = request.get_json()
    aeropuerto = mongo.db.aeropuertos.find_one({'_id': ObjectId(id)})
    if aeropuerto is None:
        return jsonify({'error': 'Aeropuerto no encontrado'}), 404
    
    aeropuerto['nombre'] = datos['nombre']
    aeropuerto['ciudad'] = datos['ciudad']
    mongo.db.aeropuertos.update_one({'_id': ObjectId(id)}, {'$set': aeropuerto})
    return jsonify({'mensaje': 'Aeropuerto modificado exitosamente'})

@app.route('/aeropuertos/<id>', methods=['DELETE'])
def eliminar_aeropuerto(id):
    aeropuerto = mongo.db.aeropuertos.find_one({'_id': ObjectId(id)})
    if aeropuerto is None:
        return jsonify({'error': 'Aeropuerto no encontrado'}), 404
    
    mongo.db.aeropuertos.delete_one({'_id': ObjectId(id)})
    return jsonify({'mensaje': 'Aeropuerto eliminado exitosamente'})

@app.route('/vuelos', methods=['GET'])
def obtener_vuelos():
    vuelos = mongo.db.vuelos.find()
    resultados = [vuelo for vuelo in vuelos]
    return jsonify(resultados)

@app.route('/vuelos', methods=['POST'])
def crear_vuelo():
    datos = request.get_json()
    nuevo_vuelo = Vuelo(datos['numero'], datos['origen'], datos['destino'])
    mongo.db.vuelos.insert_one(nuevo_vuelo.to_dict())
    return jsonify({'mensaje': 'Vuelo creado exitosamente'})

@app.route('/vuelos/<id>', methods=['PUT'])
def modificar_vuelo(id):
    datos = request.get_json()
    vuelo = mongo.db.vuelos.find_one({'_id': ObjectId(id)})
    if vuelo is None:
        return jsonify({'error': 'Vuelo no encontrado'}), 404
    
    vuelo['numero'] = datos['numero']
    vuelo['origen'] = datos['origen']
    vuelo['destino'] = datos['destino']
    mongo.db.vuelos.update_one({'_id': ObjectId(id)}, {'$set': vuelo})
    return jsonify({'mensaje': 'Vuelo modificado exitosamente'})

@app.route('/vuelos/<id>', methods=['DELETE'])
def eliminar_vuelo(id):
    vuelo = mongo.db.vuelos.find_one({'_id': ObjectId(id)})
    if vuelo is None:
        return jsonify({'error': 'Vuelo no encontrado'}), 404
    
    mongo.db.vuelos.delete_one({'_id': ObjectId(id)})
    return jsonify({'mensaje': 'Vuelo eliminado exitosamente'})

if __name__ == '__main__':
    app.run()