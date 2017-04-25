#!/usr/bin/env python
import pika
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('credentials.properties')

rabbitServer=config.get('rabbit', 'server');
rabbitPort=config.get('rabbit', 'port');

rabbitUser=config.get('user1', 'username');
rabbitPassword=config.get('user1', 'password');

credentials = pika.PlainCredentials(rabbitUser, rabbitPassword)

connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitServer,rabbitPort,'/',credentials))
channel = connection.channel()

channel.queue_declare(queue='wasp')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='wasp',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
