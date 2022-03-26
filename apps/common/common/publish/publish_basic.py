from common.publish_strategy import PublishStrategy

class PublishBasic(PublishStrategy):
    def send_message(self, send_to_rabbit: callable, routing_key: str, exchange: str, data: str):
        send_to_rabbit(data,routing_key, exchange)