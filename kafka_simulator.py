import time

def produce(message):
    """Simulate producing a message to Kafka"""
    print(f"Produced: {message}")

def consume():
    """Simulate consuming messages from Kafka"""
    print("Consumed messages")
    time.sleep(0.5)  # simulate delay
