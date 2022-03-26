from dataclasses import dataclass


@dataclass
class RabbitMQ:
    host:str
    username:str
    password:str