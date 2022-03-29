import logging
import pika
from pika.exceptions import AMQPConnectionError, ChannelClosedByBroker

from common.errors.connection_rabbit import FailedConnectRabbit
from common.errors.exchange import ExchangeNotFound
from common.logging_controller import exception

LOGGER = logging.getLogger(__name__)

class Rabbit:
    """
        A class for an easy way to connect publish and consume messages using RabbitMQ.

        Methods
        -------
        def __init__(self, host="localhost", port=5672, username="guest", password="guest"):
            Create a connection to Rabbitmq server.
        def declare_queue(self, queue_name: str, durable=True, auto_delete=False):
            Declare a queue to the server.
        def send_to_queue(self, message: str, queue: str, message_persistent=True):
            Publish a message directly to a queue.
        def receive(self, queue: str, func: callable, prefetch_count=1, acknowledge=True):
            Consume messages from a queue.
    """
    @exception(LOGGER)
    def __init__(self, host: str, 
                        username: str, 
                        password: str):
        """
            Initialize a connection to RabbitMQ server.

        Args:
        -----
            host (str, optional): The ip address of the RabbitMQ server. Defaults to "localhost".
            port (int, optional): The port for connecting to the RabbitMQ server. Defaults to 5672.
            username (str, optional): Username for connection. Defaults to "guest".
            password (str, optional): Password for connection. Defaults to "guest".
        """        
        self.creds = pika.credentials.PlainCredentials(username, password)
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host, credentials=self.creds, heartbeat=0))
        except AMQPConnectionError as e:
            raise FailedConnectRabbit(f"{e}")
 
    @exception(LOGGER)
    def declare_queue(self, queue_name: str, durable=True, auto_delete=False):
        """
            Declare queue, create if needed. This method creates or checks a
            queue. When creating a new queue the client can specify various
            properties that control the durability of the queue.
        Args:
        -----
            queue_name (str): The queue name. If an empty string is given and error will be raised.
            durable (bool, optional): The queue wont be deleted in case the server will be rebooted. Defaults to True.
            auto_delete (bool, optional): Delete the queue after consumer cancels or disconnects. Defaults to False.
        Raises:
        -------
            SyntaxError: you cant have an empty string for the queue name, if you do the queue will
            be created with a random name and you wont have its name.
        """

        if queue_name == "":
            raise SyntaxError(
                "You should not have an empty string as queue if there is no exchange.")

        try:
            with self.connection.channel() as channel:
                channel.queue_declare(
                    queue=queue_name, durable=durable, auto_delete=auto_delete)
            LOGGER.info(f"The queue {queue_name} was decalared")
        except SyntaxError as e:
            raise SyntaxError(f"{e}")
        except AMQPConnectionError as e:
            raise AMQPConnectionError(f"{e}")
    
    @exception(LOGGER)
    def declare_exchange(self, exchange:str, type:str):
        """
        This method will declare a new exchange.

        Args:
        -----
            exchange(str): The name of the exchange
            type(str): The type of the exchange (direct ...)
        """
        try:
            with self.connection.channel() as channel:
                channel.exchange_declare(exchange=exchange,exchange_type=type)
            LOGGER.info(f"The exchange {exchange} was decalared")
        except SyntaxError as e:
            raise SyntaxError(f"{e}")
    
    @exception(LOGGER)
    def bind_queue(self, exchange:str, queue:str, routing_key:str):
        """
        This method will bind the queue and the exchange.

        Args:
        -----
            exchange(str): The name of the exchange
            queue(str): The name of the queue 
            routing_key(str): The name of the routing key
        """
        try:
            with self.connection.channel() as channel:
                channel.queue_bind(exchange=exchange, queue=queue, 
                                    routing_key=routing_key)
            LOGGER.info(f"The queue {queue} was bind to the exchange {exchange} \
                            and the routing key {routing_key}")
        except SyntaxError as e:
            raise SyntaxError(f"{e}")
        except AMQPConnectionError as e:
            raise AMQPConnectionError(f"{e}")

    @exception(LOGGER)
    def send_to_queue(self, message: str, routing_key: str, 
                        exchange:str="", message_persistent=True):
        """
            Publish a message directly to a queue. 

        Args:
        -----
            message (str): The message to be send.
            routing_key (str): The name of the routing key that bund the exchange to the queue
            exchange(str): The name of the exchange 
            message_persistent (bool, optional): Message durability, 
            messages wont be lost even if the server reboots. Defaults to True.
        """

        try:
            with self.connection.channel() as channel:
                channel.basic_publish(
                    exchange=exchange,
                    routing_key=routing_key,
                    body=message,
                    properties=pika.BasicProperties(delivery_mode=2,) if message_persistent else None)
            LOGGER.info(f"The message was sent to the exchange - {exchange} routing key {routing_key}")
        except SyntaxError as e:         
            raise SyntaxError(f"{e}")
        except ChannelClosedByBroker as e:
            raise ExchangeNotFound(f"{e}")
        except AMQPConnectionError as e:
            raise AMQPConnectionError(f"{e}")

    @exception(LOGGER)
    def receive(self, queue: str, func: callable, prefetch_count=1, acknowledge=True):
        """
            This method is used to start consuming messages from the RabbitMQ server.

        Args:
        -----
            queue (str): The queue to which you bind and listen.
            func (callable): A callback function that will be called
                with the message as an argument and executed each time
                a new message is consumed.
            prefetch_count (int, optional): The number of messages each consumer
                has at a time. Defaults to 1.
            acknowledge (bool, optional): message acknowledgement after each
                consumed message. Defaults to True.
        """

        def callback(ch, method, properties, body):
            func(body.decode("utf-8"))
            if acknowledge:
                ch.basic_ack(delivery_tag=method.delivery_tag)
                LOGGER.info(f"Consumed from the queue {queue}")
        try:
            with self.connection.channel() as channel:
                channel.basic_qos(prefetch_count=prefetch_count)
                channel.basic_consume(
                    queue=queue, on_message_callback=callback, auto_ack=False if acknowledge else True)
                channel.start_consuming()
        except SyntaxError as e:
            raise SyntaxError(f"{e}")
        except AMQPConnectionError as e:
            raise AMQPConnectionError(f"{e}")

