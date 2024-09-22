import logging
from flask import Flask, request, jsonify
from service import InventoryService

app = Flask(__name__)
service = InventoryService()

@app.route('/define_stuff', methods=['POST'])
def define_stuff():
    data = request.json
    type = data.get('type')
    description = data.get('description')
    result = service.define_stuff(type, description)
    return jsonify({'message': result})

@app.route('/undefine', methods=['POST'])
def undefine():
    data = request.json
    type = data.get('type')
    result = service.undefine(type)
    return jsonify({'message': result})

@app.route('/add', methods=['POST'])
def add():
    data = request.json
    quantity = data.get('quantity')
    type = data.get('type')
    result = service.add(quantity, type)
    return jsonify({'message': result})

@app.route('/remove', methods=['POST'])
def remove():
    data = request.json
    quantity = data.get('quantity')
    type = data.get('type')
    result = service.remove(quantity, type)
    return jsonify({'message': result})

@app.route('/get_count', methods=['GET'])
def get_count():
    type = request.args.get('type')
    count = service.get_count(type)
    return jsonify({'count': count})

#adding the new API calls

@app.route('/save_data', methods=['POST'])
def save_data():
    snapshot_id = service.save_data()
    return jsonify({'id': snapshot_id})

@app.route('/load_data', methods=['POST'])
def load_data():
    data = request.json
    snapshot_id = data.get('id')
    result = service.load_data(snapshot_id)
    return jsonify({'message': 'Success' if result == 0 else 'Failed'})

@app.route('/delete_data', methods=['POST'])
def delete_data():
    data = request.json
    snapshot_id = data.get('id')
    result = service.delete_data(snapshot_id)
    return jsonify({'message': 'Deleted Successfully' if result == 0 else 'Failed'})

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(host='0.0.0.0', port=5000, debug=True)
