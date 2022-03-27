from common.publish_strategy import PublishStrategy
from common.controller_rabbitmq import Rabbit
from common.enums.datacalss_queue import Queue
from common.enums.dataclass_rabbit import RabbitMQ

class ManageRabbit:
    def __init__(self, rabbit:RabbitMQ, list_queues:list):
        self.rabbit = Rabbit(**rabbit.__dict__)
        self.list_queues = list_queues
    
    def setup_rabbit(self):
        for queue in self.list_queues:
            self.rabbit.declare_exchange(queue.exchange.exchange,
                                            queue.exchange.type)
            self.rabbit.declare_queue(queue.queue)
            self.rabbit.bind_queue(queue.exchange.exchange, queue.queue, 
                                   queue.routing_key)
   
    def publish(self, queue:Queue, publish_strategy:PublishStrategy, data):
        publish_strategy.send_message(self.rabbit.send_to_queue, queue.routing_key, 
                                queue.exchange.exchange, data)
    
    def consume(self, queue:Queue, func:callable):
        self.rabbit.receive(queue.queue, func)