# ImportRegion

import ECAgent.Core as Core
import ECAgent.Tags as Tags
import ECAgent.Collectors as Collectors
from ECAgent.Environments import GridWorld, PositionComponent, discrete_grid_pos_to_id
import time
import random
import numpy

# TagsRegion

Tags.add_tag('SHEEP')
Tags.add_tag('WOLF')

Model_parameters = ['size', 'init_sheep', 'init_wolf', 'regrow_time', 'sheep_gain', 'sheep_reproduce_rate', 'wolf_gain',
                    'wolf_reproduce_rate', 'seed']

agent_class_components = [['Sheep', ['AgentComponent', 'SpeciesComponent']],
                          ['Wolf', ['AgentComponent', 'SpeciesComponent']]]

model_flexible_parameters = [['system', 'food', [['regrow_time', 'int']]], ['agent', ['Sheep', 'SpeciesComponent'],
                                                                            [['sheep_gain', 'int', 'gain'],
                                                                             ['sheep_reproduce_rate', 'float',
                                                                              'reproduce_rate']]],
                             ['agent', ['Wolf', 'SpeciesComponent'],
                              [['wolf_gain', 'int', 'gain'], ['wolf_reproduce_rate', 'float', 'reproduce_rate']]]]

Re_init_parameters = ['size', 'seed', 'sheep_gain', 'sheep_reproduce_rate', 'wolf_gain', 'wolf_reproduce_rate']


# ModelRegion

class PredatorPreyModel(Core.Model):
    def __init__(self, size: int, init_sheep: int, init_wolf: int, regrow_time: int, sheep_gain: int,
                 sheep_reproduce_rate: float, wolf_gain: int, wolf_reproduce_rate: float, seed: int = None):
        super().__init__(seed=seed)
        self.iteration = 0
        self.time_sleep = 0
        self.paused = False
        self.isRunning = False
        self.iteration_index = []
        self.agent_last_id = [['Sheep', []], ['Wolf', []]]

        self.size = size
        self.seed = seed
        self.sheep_gain = sheep_gain
        self.sheep_reproduce_rate = sheep_reproduce_rate
        self.wolf_gain = wolf_gain
        self.wolf_reproduce_rate = wolf_reproduce_rate

        self.model_name = 'PredatorPreyModel'

        # Create Grid World
        self.environment = GridWorld(self, size, size)

        # Add Systems
        self.systems.add_system(Recorder("recorder", self, ))
        self.systems.add_system(BirthSystem("birth", self, ))
        self.systems.add_system(DeathSystem("death", self, ))
        self.systems.add_system(ResourceConsumptionSystem("food", self, regrow_time))
        self.systems.add_system(MovementSystem("move", self, ))

        # Add Agent Components
        Sheep.add_class_component(AgentComponent(Sheep, self, 'sheep'))
        Wolf.add_class_component(AgentComponent(Wolf, self, 'wolf'))

        # Add Class Components
        Wolf.add_class_component(SpeciesComponent(Wolf, self, wolf_gain, wolf_reproduce_rate))
        Sheep.add_class_component(SpeciesComponent(Sheep, self, sheep_gain, sheep_reproduce_rate))

        # Create Agents At Random Locations
        for _ in range(init_sheep):
            self.environment.add_agent(Sheep(self), x_pos=self.random.randint(0, size - 1),
                                       y_pos=self.random.randint(0, size - 1))
        for _ in range(init_wolf):
            self.environment.add_agent(Wolf(self), x_pos=self.random.randint(0, size - 1),
                                       y_pos=self.random.randint(0, size - 1))

    # Clears All Agents All Class Components:
    def clear(self):
        for agent in self.environment.get_agents():
            self.environment.removeAgent(agent.id)
        for agent in agent_class_components:
            for component in agent[1]:
                string_code = f"{agent[0]}.remove_class_component({component})"
                exec(string_code)

    # Method that will execute Model for t time steps
    def run(self, t: int):
        t += self.iteration
        self.isRunning = True
        while self.iteration < t:
            if not self.paused:
                self.execute(1)
                self.iteration += 1
                if self.iteration_index == []:
                    self.iteration_index = [1]
                else:
                    self.iteration_index.append(self.iteration_index[-1] + 1)
                time.sleep(self.time_sleep)
                yield self
            else:
                pass
        self.isRunning = False


# AgentRegion

class Wolf(Core.Agent):
    def __init__(self, model, energy: float = None):

        agent_comp = Wolf[AgentComponent]
        self.agent_id = f'{agent_comp.prefix}{agent_comp.counter}'
        super().__init__(self.agent_id, model, tag=Tags.WOLF)
        self.add_component(EnergyComponent(self, model,energy if energy is not None else model.random.random() * 2 * Wolf[SpeciesComponent].gain))
        agent_comp.counter += 1
        for item in self.model.agent_last_id:
            if item[0] == 'Wolf':
                item[1] = agent_comp.counter


class Sheep(Core.Agent):
    def __init__(self, model, energy: float = None):

        agent_comp = Sheep[AgentComponent]
        self.agent_id = f'{agent_comp.prefix}{agent_comp.counter}'
        super().__init__(self.agent_id, model, tag=Tags.SHEEP)
        self.add_component(EnergyComponent(self, model,
                                           energy if energy is not None else model.random.random() * 2 * Sheep[
                                               SpeciesComponent].gain))
        agent_comp.counter += 1
        for item in self.model.agent_last_id:
            if item[0] == 'Sheep':
                item[1] = agent_comp.counter


# ComponentRegion

# To define the prefix for assigning ID to an agent and the current ID number available
class AgentComponent(Core.Component):
    def __init__(self, agent, model, prefix):
        super().__init__(agent, model)
        self.prefix = prefix
        self.counter = 0


class EnergyComponent(Core.Component):
    def __init__(self, agent, model, energy: float = None):
        super().__init__(agent, model)
        self.energy = energy


class SpeciesComponent(Core.Component):
    def __init__(self, agent, model, gain: int, reproduce_rate: float):
        super().__init__(agent, model)
        self.gain = gain
        self.reproduce_rate = reproduce_rate


# SystemRegion

class Recorder(Core.System):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.agents = []
        for agent in self.model.agent_last_id:
            self.agents.append(agent[0])
        self.agent_population = []
        self.initialise_data()
        self.agent_locations = []
        self.x_vals = []

    def initialise_data(self):
        for agent_name in self.agents:
            self.agent_population.append([agent_name, []])

    def execute(self):
        for population in self.agent_population:
            population[1].append(
                len(self.model.environment.get_agents(tag=Tags.__getattr__(population[0].upper()))))
        self.x_vals.append(self.model.iteration)

        for agent_name in self.agents:
            self.agent_locations.append([agent_name, [], []])

        visited_locations = {}

        for location in self.agent_locations:
            agent_type = location[0]

            # Check if this agent type has been visited before
            if agent_type not in visited_locations:
                visited_locations[agent_type] = set()

            for lone_agent in self.model.environment.get_agents(tag=Tags.__getattr__(agent_type.upper())):
                # Get the agent's position
                x = lone_agent[PositionComponent].x
                y = lone_agent[PositionComponent].y

                # Check if this location has been visited for this agent type
                if (x, y) not in visited_locations[agent_type]:
                    location[1].append(x)
                    location[2].append(y)

                    # Mark this location as visited for this agent type
                    visited_locations[agent_type].add((x, y))


class BirthSystem(Core.System):
    def __init__(self, id, model):
        super().__init__(id, model)

    def execute(self):
        for agent in self.model.environment.get_agents():
            new_agent = None
            if agent.tag == Tags.WOLF and self.model.random.random() < Wolf[SpeciesComponent].reproduce_rate:
                # Birth Wolf
                agent[EnergyComponent].energy /= 2.0
                new_agent = Wolf(self.model,
                                 energy=agent[EnergyComponent].energy
                                 )

            elif self.model.random.random() < Sheep[SpeciesComponent].reproduce_rate:
                # Birth Sheep
                agent[EnergyComponent].energy /= 2.0
                new_agent = Sheep(self.model,
                                  energy=agent[EnergyComponent].energy
                                  )

            # Add agent to environment (at its parent's location)
            if new_agent is not None:
                self.model.environment.add_agent(
                    new_agent, *agent[PositionComponent].xy()
                )


class DeathSystem(Core.System):
    def __init__(self, id, model):
        super().__init__(id, model)

    def execute(self):
        toRem = []
        for agent in self.model.environment:
            if agent[EnergyComponent].energy <= 0:
                toRem.append(agent.id)

        for a in toRem:
            self.model.environment.remove_agent(a)


class ResourceConsumptionSystem(Core.System):
    def __init__(self, id: str, model, regrow_time: int):
        super().__init__(id, model)
        self.regrow_time = regrow_time

        def resource_generator(pos, cells):
            return 1 if model.random.random() < 0.5 else 0

        # Generate the initial resources
        model.environment.add_cell_component('resources',
                                             resource_generator)

        def countdown_generator(pos, cells):
            return int(model.random.random() * regrow_time)

        # Generate the initial resources
        model.environment.add_cell_component('countdown', countdown_generator)

    def execute(self):
        # Get resources data
        cells = self.model.environment.cells
        resource_cells = cells['resources'].to_numpy()
        countdown_cells = cells['countdown'].to_numpy()
        eaten_sheep = []
        targets_at_pos = {}
        environment = self.model.environment
        # Process Sheep and Wolves first

        for agent in environment:
            posID = discrete_grid_pos_to_id(agent[PositionComponent].x, agent[PositionComponent].y,
                                            self.model.environment.width)

            # Is wolf or is sheep
            if agent.tag == Tags.WOLF:
                # Get all agents at position
                if posID not in targets_at_pos:
                    targets_at_pos[posID] = environment.get_agents_at(
                        agent[PositionComponent].x, agent[PositionComponent].y)

                for target in targets_at_pos[posID]:
                    # If sheep
                    if target.tag == Tags.SHEEP and target.id not in eaten_sheep:
                        # Mark Sheep for death
                        eaten_sheep.append(target.id)
                        # Wolf gets energy for eating Sheep
                        agent[EnergyComponent].energy += Wolf[SpeciesComponent].gain
                        break

            elif agent.id not in eaten_sheep:
                # Check is grass is Alive
                if resource_cells[posID] > 0:
                    # Sheep consumes Grass and gains Energy
                    agent[EnergyComponent].energy += Sheep[SpeciesComponent].gain
                    resource_cells[posID] = 0

        # Remove eaten sheep
        for sheep in eaten_sheep:
            environment.remove_agent(sheep)

        # Regrow Grass
        countdown_cells[resource_cells < 1] -= 1
        mask = countdown_cells < 1
        resource_cells[mask] = 1
        countdown_cells = numpy.where(mask, numpy.asarray(
            [
                int(self.model.random.random() * self.regrow_time)
                for _ in range(len(countdown_cells))
            ]), countdown_cells)

        # Update grass levels and countdowns in environment
        self.model.environment.cells.update({
            'resources': resource_cells,
            'countdown': countdown_cells
        })


class MovementSystem(Core.System):
    def __init__(self, id: str, model):
        super().__init__(id, model)

    def execute(self):
        # For each agent in the environment
        for agent in self.model.environment:
            # Move within Moore Neighbourhood [-1, 1]
            x_offset = round(2 * self.model.random.random() - 1)
            y_offset = round(2 * self.model.random.random() - 1)
            self.model.environment.move(agent, x_offset, y_offset)

            # Spend Energy
            agent[EnergyComponent].energy -= 1


