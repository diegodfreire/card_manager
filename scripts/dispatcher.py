import argparse
import json
import os
from nameko.standalone.events import event_dispatcher


RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD", "guest")
CONFIG = {'AMQP_URI': f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}"} # noqa: E501


def dispatch_event(event_type, service_name="scheduler_service", event_data=""): # noqa: E501
    dispatch = event_dispatcher(CONFIG)
    dispatch(service_name, event_type, event_data)


parser = argparse.ArgumentParser()
parser.add_argument("-e", "--events", nargs='+', help="Nome do(s) evento(s) que você deseja chamar") # noqa: E501

args = parser.parse_args()

events = []
if args.events[0] == 'all':
    with open('./scripts/events.json') as json_file:
        data = json.load(json_file)
        events = data['events']
else:
    events = args.events

for event in events:
    print(f"Disparando evento {event}")
    dispatch_event(event)

print("Eventos disparados com sucesso!")
