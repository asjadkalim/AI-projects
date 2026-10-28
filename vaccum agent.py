
import random

class VacuumEnvironment:
    """Two-square world: A and B."""
    def __init__(self):
        self.status = {'A': random.randint(0, 1),
                       'B': random.randint(0, 1)}
        self.agent_location = random.choice(['A', 'B'])

    def percept(self):
        return (self.agent_location,
                self.status[self.agent_location])

    def execute(self, action):
        if action == 'Suck':
            self.status[self.agent_location] = 0
        elif action == 'Right':
            self.agent_location = 'B'
        elif action == 'Left':
            self.agent_location = 'A'


def model_based_vacuum_agent(percept):
    """Agent remembers the history of both locations."""

    location, dirty = percept

    # Internal model: remembers the status of locations
    if not hasattr(model_based_vacuum_agent, "history"):
        model_based_vacuum_agent.history = {
            'A': None, 'B': None
        }

    history = model_based_vacuum_agent.history

    # Update memory using the current percept
    history[location] = dirty

    # Clean the current location if it is dirty
    if dirty == 1:
        return 'Suck'

    # If A is clean but B is not confirmed clean, go to B
    if location == 'A' and history['B'] != 0:
        return 'Right'

    # If B is clean but A is not confirmed clean, go to A
    if location == 'B' and history['A'] != 0:
        return 'Left'

    # Both locations are known to be clean
    return 'NoOp'


random.seed(7)
env = VacuumEnvironment()
env.status = {'A': 1, 'B': 1}
env.agent_location = 'B'

# Reset memory for a fresh run
model_based_vacuum_agent.history = {'A': None, 'B': None}

print("Initial state:", env.status,
      "| Agent at", env.agent_location)

score = 0

for step in range(1, 6):
    p = env.percept()
    action = model_based_vacuum_agent(p)

    if action == 'NoOp':
        print(f"Step {step}: Both locations are clean.")
        break

    env.execute(action)

    if action == 'Suck':
        score += 10
    else:
        score -= 1

    print(f"Step {step}: percept={p} -> action={action:5s}"
          f" | world={env.status}"
          f" | memory={model_based_vacuum_agent.history}")

print("Final state:", env.status)
print("Performance score:", score)
