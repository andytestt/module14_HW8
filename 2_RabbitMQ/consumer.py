# конспект
import pika
import json
from models import Contact
from mongoengine import connect
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')


connect(host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@learnprogramming.dzh9u9u.mongodb.net/{db_name}?retryWrites=true&w=majority", ssl=True)

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='task_campaing', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    pk = body.decode()
    # pk = json.loads(body.decode())
    task = Contact.objects(id=pk, completed=False).first()
    if task:
        # task.update(set__completed=True, set__consumer="Reckless")
        task.update(set__completed=True)
        print(f"Task # {task.num} for ObjectId({task.id}) updated")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_campaing', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()