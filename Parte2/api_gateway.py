from flask import Flask, request, jsonify
import requests
import random

app = Flask(__name__)

def get_service_addresses(service_name):
    try:
        response = requests.get(f'http://localhost:8761/services/{service_name}')
        if response.status_code == 200:
            services = response.json()
            return services  # Retorna todas as instâncias disponíveis
    except Exception as e:
        print(f"Error retrieving services: {e}")
    return []

@app.route('/orders', methods=['POST'])
def proxy_order_service():
    instances = get_service_addresses('OrderService')
    if instances:
        # Escolher uma instância aleatoriamente para balanceamento de carga
        instance = random.choice(instances)
        try:
            response = requests.post(f'{instance}/orders', json=request.json)
            return jsonify(response.json()), response.status_code
        except Exception as e:
            return jsonify({"error": f"Failed to connect to OrderService: {e}"}), 500

    return jsonify({"error": "Order service not available"}), 503

if __name__ == '__main__':
    app.run(port=8000, debug=True)
