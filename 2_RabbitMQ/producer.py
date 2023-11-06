import pika
import random
import faker
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
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='task_service', exchange_type='direct')
channel.queue_declare(queue='task_campaing', durable=True)
channel.queue_bind(exchange='task_service', queue='task_campaing')

fake = faker.Faker()


def main():
    for _ in range(100):
        task = Contact(
            num = random.randint(1, 101),
            fullname=fake.name(),
            address = fake.address(),
            job = fake.job(),
            company = fake.company(),
            phone_number = fake.phone_number(),
            email = fake.email()
            )
        task.save()

        channel.basic_publish(
            exchange='task_service',
            routing_key='task_campaing',
            body=str(task.id).encode(),
            # body = json.dumps(task.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(f'Task # {task.num} for ObjectId({task.id}) Sent')

    connection.close()
    
    
if __name__ == '__main__':
    main()