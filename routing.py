import asyncio
import pandas as pd
import hashlib
import json
import random

# Constants for the simulation
LONG_RUNNING_TASK_DURATION = 2  # seconds
SHORT_RUNNING_TASK_DURATION = 0.1  # seconds

# Function to generate Fibonacci sequence


def fibonacci(n):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence

# Function to generate colors based on Fibonacci modulo 10


def fibonacci_color(fib_number):
    base_color = fib_number % 10
    color_map = {
        0: '#FF5733', 1: '#DAF7A6', 2: '#C70039', 3: '#900C3F',
        4: '#581845', 5: '#FFC300', 6: '#FF5733', 7: '#C70039',
        8: '#DAF7A6', 9: '#900C3F'
    }
    return color_map.get(base_color, "#FFFFFF")

# Random color generator for privacy


def generate_random_color():
    random_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return random_color

# Function to decrypt messages (simulation)


def decrypt_message(message, key):
    return hashlib.sha256((message + key).encode()).hexdigest()

# Function to simulate actions (placeholder for real actions)


def perform_action(action_type, data):
    print(f"Performing action: {action_type} with {data}")

# Hypothetical SCXML processor for ticketing system


class TicketSCXMLProcessor:
    def __init__(self, state_machine_json):
        self.state_data = json.loads(state_machine_json)
        self.state = self.state_data["initial"]
        self.context = self.state_data["context"]

    def transition(self, event):
        state_config = self.state_data["states"][self.state]
        if "on" in state_config and event in state_config["on"]:
            transition = state_config["on"][event]
            self.state = transition["target"]
            if "actions" in transition:
                for action in transition["actions"]:
                    perform_action(action["type"], self.context)
        return self.state

# Node FSM using TicketSCXMLProcessor


class NodeFSM:
    def __init__(self, state_machine_json):
        self.scxml_processor = TicketSCXMLProcessor(state_machine_json)
        self.color = generate_random_color()

    async def handle_event(self, event):
        self.scxml_processor.transition(event)
        return f"Event {event} handled, new state: {self.scxml_processor.state}"

    def get_state(self):
        return self.scxml_processor.state

    def get_color_based_state(self):
        return hashlib.sha256(self.get_state().encode() + self.color.encode()).hexdigest()

# Async function to route message


async def route_message(node_id, fsm, event):
    decrypted_message = decrypt_message("secret_message", "my_secret_key")

    action_result = await fsm.handle_event(event)
    unique_state = fsm.get_color_based_state()

    print(f"Node Color: {fsm.color}")
    print(f"  Decrypted Message: {decrypted_message}")
    print(f"  Action Result: {action_result}")
    print(f"  Node State: {unique_state}\n")

# Async main function


# Async main function
async def main():
    state_machine_json = '''
    {
      "context": {
        "ticket": "null",
        "customer": "null",
        "seniorAgent": "null",
        "assignedAgent": "null",
        "notifications": []
      },
      "id": "ticket",
      "initial": "New",
      "states": {
        "New": {
          "description": "State when a new support issue is reported and entered into the system.",
          "on": {
            "assignTicket": {
              "target": "New",
              "actions": [
                {
                  "type": "assignTicketToAgent"
                },
                {
                  "type": "notifyCustomerNewTicket"
                }
              ]
            },
            "startWork": {
              "target": "In Progress"
            }
          }
        },
        "In Progress": {
          "description": "State when the assigned agent is reviewing and working on the ticket.",
          "after": {
            "REMINDER_TIMEOUT": {
              "target": "#ticket.Send Reminder",
              "actions": []
            }
          },
          "on": {
            "resolve": {
              "target": "Closed"
            },
            "needsReview": {
              "target": "Needs Review"
            }
          }
        },
        "Closed": {
          "description": "State when a ticket is resolved, closed, and a confirmation is sent to the customer with an optional feedback request.",
          "entry": [
            {
              "type": "notifyCustomerResolved"
            },
            {
              "type": "requestCustomerFeedback"
            }
          ],
          "type": "final"
        },
        "Needs Review": {
          "description": "State when a ticket cannot be resolved due to complexity or missing information and requires escalation.",
          "on": {
            "escalateTicket": {
              "target": "Needs Review",
              "actions": [
                {
                  "type": "escalateToSeniorAgent"
                },
                {
                  "type": "notifyCustomerDelay"
                }
              ]
            }
          }
        },
        "Send Reminder": {
          "description": "State for sending reminders to the responsible agent when a ticket remains inactive for a predefined period.",
          "entry": [
            {
              "type": "sendReminderToAgent"
            },
            {
              "type": "escalateIfNecessary"
            }
          ],
          "on": {
            "resolve": {
              "target": "Closed"
            },
            "escalate": {
              "target": "Needs Review"
            }
          }
        }
      }
    }
    '''
    data = pd.read_csv('a.csv', header=None)

    tasks = []
    for index, row in data.iterrows():
        for node_id in row:
            fsm = NodeFSM(state_machine_json)
            event = "startWork" if node_id % 2 == 0 else "assignTicket"
            task = asyncio.create_task(route_message(node_id, fsm, event))
            tasks.append(task)

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
