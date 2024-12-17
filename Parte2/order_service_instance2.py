from flask import Flask, request, jsonify
import sqlite3
import pika
import json
import requests

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    # Garantir que as tabelas estejam criadas
    conn.commit()
    conn.close()

def send_message_to_queue(message, queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
    connection.close()

def register_service(service_name, service_address):
    try:
        response = requests.post('http://localhost:8761/register', json={
            "name": service_name,
            "address": service_address
        })
        if response.status_code == 201:
            print(f"Service {service_name} registered successfully.")
        else:
            print(f"Failed to register service {service_name}. Response: {response.status_code}")
    except Exception as e:
        print(f"Error registering service: {e}")

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    customer_id = data.get('customer_id')
    product_id = data.get('product_id')

    if not customer_id or not product_id:
        return jsonify({"error": "Customer ID and Product ID are required"}), 400

    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # Verifica se o produto está em estoque (envia mensagem para o Inventory Service)
    check_message = {"product_id": product_id}
    send_message_to_queue(check_message, 'inventoryQueue')

    # Por simplicidade, vamos assumir que o produto está disponível
    cursor.execute('INSERT INTO orders (customer_id, product_id, status) VALUES (?, ?, ?)', 
                   (customer_id, product_id, 'pending'))
    conn.commit()
    order_id = cursor.lastrowid
    conn.close()

    # Enviar mensagem para o Notification Service
    notification_message = {
        "order_id": order_id,
        "customer_id": customer_id,
        "product_id": product_id,
        "status": "pending"
    }
    send_message_to_queue(notification_message, 'notificationQueue')

    return jsonify({"order_id": order_id, "status": "pending"}), 201


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    init_db()
    # Registrar o serviço no Eureka Server com a porta 5001 para esta instância
    register_service('OrderService', 'http://localhost:5001')
    app.run(port=5001) 
