from dataclasses import dataclass

from common.enums.dataclass_exchange import Exchange


@dataclass
class Queue:
    queue:str
    exchange:Exchange
    routing_key:str