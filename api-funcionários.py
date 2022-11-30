import json
from flask import Flask, jsonify, request

app = Flask(__name__)

funcionários = [
  { 'id': 1, 'nome': 'João' },
  { 'id': 2, 'nome': 'Maria' },
  { 'id': 3, 'nome': 'Francisco' }
]

nextFuncionárioId = 4

@app.route('/funcionário', methods=['GET'])
def get_funcionários():
  return jsonify(funcionários)

@app.route('/funcionários/<int:id>', methods=['GET'])
def get_funcionário_by_id(id: int):
  funcionário = get_funcionário(id)
  if funcionário is None:
    return jsonify({ 'error': 'Funcionário não existe'}), 404
  return jsonify(funcionário)

def get_funcionário(id):
  return next((e for e in funcionários if e['id'] == id), None)

def funcionário_is_valid(funcionário):
  for key in funcionário.keys():
    if key != 'nome':
      return False
  return True

@app.route('/funcionário', methods=['POST'])
def create_funcionário():
  global nextFuncionárioId
  funcionário = json.loads(request.data)
  if not funcionário_is_valid(funcionário):
    return jsonify({ 'error': 'Propriedades de funcionário inválidas.' }), 400

  funcionário['id'] = nextFuncionárioId
  nextFuncionárioId += 1
  funcionários.append(funcionário)

  return '', 201, { 'location': f'/funcionários/{funcionário["id"]}' }

@app.route('/funcionários/<int:id>', methods=['PUT'])
def update_funcionário(id: int):
  funcionário = get_funcionário(id)
  if funcionário is None:
    return jsonify({ 'error': 'Funcionário não existe.' }), 404

  updated_funcionário = json.loads(request.data)
  if not funcionário_is_valid(updated_funcionário):
    return jsonify({ 'error': 'Propriedades de funcionário inválidas.' }), 400

  funcionário.update(updated_funcionário)

  return jsonify(funcionário)

@app.route('/funcionários/<int:id>', methods=['DELETE'])
def delete_funcionário(id: int):
  global funcionários
  funcionário = get_funcionário(id)
  if funcionário is None:
    return jsonify({ 'error': 'Funcionário não existe.' }), 404

  funcionários = [e for e in funcionários if e['id'] != id]
  return jsonify(funcionário), 200


app.run()
