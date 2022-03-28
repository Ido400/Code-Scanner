import sys
from common.errors.connection_rabbit import FailedConnectRabbit
from common.errors.invalid_data import InvalidData
from common.publish_strategy import PublishStrategy
from common.controller_rabbitmq import Rabbit
from common.enums.datacalss_queue import Queue
from common.enums.dataclass_rabbit import RabbitMQ

class ManageRabbit:
    def __init__(self, rabbit:RabbitMQ, list_queues:list):
        """
        Args:
        -----
            rabbit(RabbitMQ): The data class of rabbit
            list_queue(list): List of object queues
        """
        self.rabbit = Rabbit(**rabbit.__dict__)
        self.list_queues = list_queues
    
    def setup_rabbit(self):
        """
        This method will setup the Rabbit environment and declare the 
        exchange and the queues. 
        """
        for queue in self.list_queues:
            self.rabbit.declare_exchange(queue.exchange.exchange,
                                            queue.exchange.type)
            self.rabbit.declare_queue(queue.queue)
            self.rabbit.bind_queue(queue.exchange.exchange, queue.queue, 
                                   queue.routing_key)
   
    def publish(self, queue:Queue, publish_strategy:PublishStrategy, data):
        """
        This method will send a message into the rabbit queue by a specific 
        strategy.

        Args:
        -----
            queue(Queue): The queue object 
            publish_strategy(PublishStrategy): The publish strategy object
            data: The data that send into the rabbit
        """
        try:
            publish_strategy.send_message(self.rabbit.send_to_queue, queue.routing_key, 
                                queue.exchange.exchange, data)
        except SyntaxError:
            raise InvalidData(f"The queue object is invalid {queue}")
        except FailedConnectRabbit:
            sys.exit() 
    def consume(self, queue:Queue, func:callable):
        """
        This method will consume fromm the rabbit queue.

        Args:
        -----
            queue(Queue): The queue object 
            func(callable): The function that manage the data that consume from
                            the queue
        """
        self.rabbit.receive(queue.queue, func)