from flask import Flask, request, jsonify
import threading
import time
import requests

app = Flask(__name__)

# Dicionário para armazenar os serviços registrados
services = {}

@app.route('/register', methods=['POST'])
def register_service():
    data = request.json
    name = data.get('name')
    address = data.get('address')
    if name and address:
        if name not in services:
            services[name] = []
        if address not in services[name]:
            services[name].append(address)
        return jsonify({"message": f"Service {name} registered."}), 201
    return jsonify({"error": "Invalid data"}), 400

@app.route('/services', methods=['GET'])
def get_all_services():
    return jsonify(services), 200

@app.route('/services/<service_name>', methods=['GET'])
def get_service(service_name):
    service_instances = services.get(service_name)
    if service_instances:
        return jsonify(service_instances), 200
    return jsonify({"error": "Service not found"}), 404

# Função para verificar a saúde dos serviços
def health_check():
    while True:
        for service_name, instances in list(services.items()):
            for instance in list(instances):
                try:
                    response = requests.get(f"{instance}/health", timeout=2)
                    if response.status_code != 200:
                        raise Exception("Unhealthy service")
                except Exception:
                    print(f"Removing unhealthy service: {instance}")
                    instances.remove(instance)
            if not instances:
                del services[service_name]
        time.sleep(10)  # Verificar a cada 10 segundos

if __name__ == '__main__':
    # Inicia a thread de health checks
    threading.Thread(target=health_check, daemon=True).start()
    app.run(port=8761, debug=True)
