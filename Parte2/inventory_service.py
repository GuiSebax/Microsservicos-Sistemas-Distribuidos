import sqlite3
import json
from flask import jsonify, Flask
import pika


app = Flask(__name__)

# Função para verificar disponibilidade do produto
def check_product_availability(product_id):
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('SELECT stock_quantity FROM products WHERE id = ?', (product_id,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0] > 0:
        return True
    else:
        return False

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

# Função para atualizar o status do pedido no banco de dados
def update_order_status(order_id, status):
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
    conn.commit()
    conn.close()

# Callback para processar mensagens da fila
def callback(ch, method, properties, body):
    data = json.loads(body)
    order_id = data.get('order_id')
    product_id = data.get('product_id')

    if check_product_availability(product_id):
        print(f" [x] Product {product_id} is available. Updating order {order_id} to 'completed'.")
        # Atualiza o pedido para "completed"
        update_order_status(order_id, 'completed')
    else:
        print(f" [x] Product {product_id} is out of stock. Updating order {order_id} to 'failed'.")
        # Atualiza o pedido para "failed"
        update_order_status(order_id, 'failed')

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='inventoryQueue')
    channel.basic_consume(queue='inventoryQueue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for inventory messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()
