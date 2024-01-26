"""
This ReadJsonToModel classes is used by the GUI to convert Json outlines of the custom models to the corresponding
python type file.
"""

# Imports
import json
import ModelFileGeneration

"""
These are the global variables used to store data when reading off selected indexes/keys from the json file.
"""
agents = []
agent_names = []
json_data = None
system_details = []
components = []

'''
The read_json_file function is responsible for loading the selected Json file. It takes one argument:
    
    #file_name, which is the name (including path) of the Json file to be read and used to convert to python.
'''


def read_json_file(file_name: str):
    global json_data

    with open(f'Saves/Saved Models/Json Outline/{file_name}', 'r') as json_file:
        json_data = json.load(json_file)


"""
This function is used to gather names of the agents included in the Json file for the custom model, and appened them
to the agent_names list which will be used by other functions. It takes oen argument:

    #data, which is the loaded json data by read_json_file function.


"""


def gather_agent_names(data: json):
    global agent_names
    agent_names = []
    for item in data:
        for key, value in item.items():
            if key == 'WriteAgent':
                agent_names.append(value['agent_name'])


"""
Generates a base Python file for a custom model when converting from a JSON representation to Python code.

This function takes the name of the model file in JSON format as input and uses the ModelFileGeneration module
to create a Python file that serves as the foundational code for the custom model. The generated Python file
typically includes necessary imports, class definitions, and placeholders for model-specific logic. 
It takes oen argument:
   
#model_file_name: A string specifying the name of the model file in JSON format.

"""


def generate_base_file(model_file_name: str):
    ModelFileGeneration.generate_base_file(model_file_name)


"""
Reads agent class section within the json file and pass these values to the called function 
ModelFileGeneration.write_agent to generate agent classes within the base file. Tt take two arguments:

    #modelName, which is the name of the base file.
    #data: Converted json data from the selected json file.
        
"""


def json_to_agent_class(modelName, data: json):
    for item in data:
        for key, value in item.items():
            if key == 'WriteAgent':
                agent_name = value['agent_name']
                agent_parameters = value['parameters']
                agent_fields = value['fields']
                agent_components = value['components']
                ModelFileGeneration.write_agent(modelName, agent_name, agent_parameters, agent_fields,
                                                agent_components)


"""
Reads component class section within the json file and pass these values to the called function 
ModelFileGeneration.write_component to generate agent classes within the base file. Tt take two arguments:

    #modelName, which is the name of the base file.
    #data: Converted json data from the selected json file.
    
"""


def json_to_component_class(modelName, data: json):
    for item in data:
        for key, value in item.items():
            if key == 'WriteComponent':
                component_name = value['component_name']
                component_parameters = value['parameters']
                component_fields = value['fields']
                ModelFileGeneration.write_component(modelName, component_name, component_parameters,
                                                    component_fields)
    ModelFileGeneration.write_agent_component(modelName)


"""
The requires_agent_names function only calls the functions of ModelFileGeneration that only require agent names as 
parameters. Tt take two arguments:

    #modelName, which is the name of the base file.
    #data: Converted json data from the selected json file.

"""


def requires_agent_names(modelName, data):
    global agent_names

    ModelFileGeneration.write_tags(modelName, agent_names)
    ModelFileGeneration.write_add_agent_components(modelName, agent_names)


"""
The json_to_model function is responsible to generate model class content based on the input from the Json file.
Including, add systems, add class components, add initialisation section for agents, define parameters within the 
constructor of the model class.
It takes two arguments:

    #modelName, which is the name of the base file.
    #data: Converted json data from the selected json file.

"""


def json_to_model(modelName, data: json):
    ModelFileGeneration.write_model(modelName, modelName)
    requires_agent_names(modelName, json_data)
    global system_details, components
    system_details = []
    ModelFileGeneration.model_agent_initialisation(modelName, agent_names)

    systems = None
    for item in data:
        if 'WriteComponent' in item:
            component = item['WriteComponent']
            component_name = component.get('component_name')
            component_parameters = component.get('parameters')
            components.append([component_name, component_parameters])
        if 'WriteSystem' in item:
            systems = item['WriteSystem']

    for system_name, system_data in systems.items():
        parameters = system_data.get('parameters')

        if parameters:
            para = []
            for parameter in parameters:
                para.append(parameter)
            value = [system_name, para]
            system_details.append(value)

        else:
            value = [system_name, []]
            system_details.append(value)

    for system in system_details:
        ModelFileGeneration.write_system(modelName, system[0])

    add_systems = []
    custom_system_names = None
    add_class_components = None
    for item in data:
        for key, value in item.items():
            if key == 'WriteModel':
                add_class_components = value['add_class_component'][0]
                add_systems = value['system']
                custom_system_names = add_systems['custom_name']
                add_systems = add_systems['systems']

    for i in range(len(add_systems)):
        if not system_details[i][1]:
            ModelFileGeneration.add_systems(modelName, add_systems[i], custom_system_names[i], [])
        else:
            ModelFileGeneration.add_systems(modelName, add_systems[i], custom_system_names[i],
                                            system_details[i][1])
            for system in ModelFileGeneration.flexible_model_parameters:
                if system[1] == add_systems[i]:
                    system[1] = custom_system_names[i]

    for entry in add_class_components:
        argument_list = []
        for component in components:
            if component[0] == entry['ComponentName']:
                for parameter in component[1]:
                    argument_list.append([parameter[0], parameter[1]])
                ModelFileGeneration.write_add_class_component(modelName, entry['AgentName'],
                                                              entry['ComponentName'], argument_list)

    ModelFileGeneration.insert_model_parameters(modelName, agent_names)

"""
This readJsonToPy function simply executes a collection of functions based on the model name and Json data file.
"""


def readJsonToPy(modelName: str):
    global agents,agent_names,json_data,system_details,components
    agents = []
    agent_names = []
    json_data = None
    system_details = []
    components = []

    generate_base_file(modelName)

    read_json_file(modelName + '.json')
    gather_agent_names(json_data)

    json_to_agent_class(modelName, json_data)
    json_to_component_class(modelName, json_data)

    json_to_model(modelName, json_data)
    ModelFileGeneration.write_main_function_to_model(modelName)


if __name__ == "__main__":
    readJsonToPy('PredatorPreyModel')