import logging
from flask import Flask, request, jsonify
from service import InventoryService

app = Flask(__name__)
service = InventoryService()
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200
@app.route('/define_stuff', methods=['POST'])
def define_stuff():
    data = request.json
    item_type = data.get('type')
    description = data.get('description')
    result = service.define_stuff(item_type, description)
    return jsonify({'message': result})

@app.route('/undefine', methods=['POST'])
def undefine():
    data = request.json
    item_type = data.get('type')
    result = service.undefine(item_type)
    return jsonify({'message': result})

@app.route('/add', methods=['POST'])
def add():
    data = request.json
    quantity = data.get('quantity')
    item_type = data.get('type')
    result = service.add(quantity, item_type)
    return jsonify({'message': result})

@app.route('/remove', methods=['POST'])
def remove():
    data = request.json
    quantity = data.get('quantity')
    item_type = data.get('type')
    result = service.remove(quantity, item_type)
    return jsonify({'message': result})

@app.route('/get_count', methods=['GET'])
def get_count():
    item_type = request.args.get('type')
    count = service.get_count(item_type)
    return jsonify({'count': count})

@app.route('/save_data', methods=['POST'])
def save_data():
    result = service.save_data()
    return jsonify(result)

@app.route('/load_data', methods=['POST'])
def load_data():
    data = request.json
    snapshot_id = data.get('snapshot_id')
    
    result = service.load_data(snapshot_id)
    
    if result is not None: 
        return jsonify({'message': 'Data loaded successfully.'}), 200
    else:
        return jsonify({'error': 'Snapshot not found.'}), 404

@app.route('/delete_data', methods=['POST'])
def delete_data():
    data = request.json
    snapshot_id = data.get('snapshot_id')
    result = service.delete_data(snapshot_id)
    if result == 0:
        return jsonify({'message': 'Snapshot deleted successfully.'})
    else:
        return jsonify({'error': 'Snapshot not found.'}), 404

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(host='0.0.0.0', port=5000, debug=True)
