# ModelFileGeneration
"""
This Python class serves as a tool for translating input parameters into various elements of the agent-based model
system. These elements encompass agents, components, systems, and the primary model class itself.
"""
# Imports
import copy

line_array = []
tab_space = "    "
# Stores parameters that will be initialised in the model constructor.
model_parameters = []
# Stores details of parameters that can be tuned during model run time.
flexible_model_parameters = []
# Stores class components that need to be removed form the model during model reset.
agent_class_components = []
# Stores parameters that are needed to re-instantiate the model for the loading model object function.
re_init_parameters = ['size', 'seed']

'''
The generate_base_file function is designed to create a foundational Python file for a customized 
model. The custom model's name is provided as an argument to the 
function (model_name):

    #model_name: A string representing the name of the model for which the base file will be generated.
'''


def generate_base_file(model_name: str):
    # Reset global parameters to prevent data remains from previous runs
    global model_parameters, flexible_model_parameters, agent_class_components, re_init_parameters
    model_parameters = []
    flexible_model_parameters = []
    agent_class_components = []
    re_init_parameters = ['size', 'seed']

    # It opens a new Python file with the name model_name + ".py" in write mode ("w") using a context manager
    # (with open(...)). This file will be used to create the base script for the customized model.
    with open("Saves/Saved Models/Python File/" + model_name + ".py", "w") as python_file:

        # It writes a series of comment markers (e.g., "#ImportRegion," "#TagsRegion," etc.) into the file. These
        # markers are placeholders for different sections of the model code and indicate where specific code sections
        # should be added later during the model development process.
        python_file.write(
            "# ImportRegion\n# TagsRegion\n# Model Parameters\n# Agent Class Components List\n# Model Flexible Parameters\n# Re_init_parameters\n# ModelRegion\n# AgentRegion\n# ComponentRegion\n"
            "# SystemRegion\n# Recorder")

    # It calls a function (presumably read_file_to_array) to read the contents of the newly created file into a list
    # named line_array. The purpose of this step is to prepare the file for further modifications.
    read_file_to_array(model_name)

    # It initializes an empty list called temp_array to store the modified lines of the script.
    temp_array = []

    # It iterates through each line in line_array.
    for line in line_array:

        # It appends the original line to the temp_array, preserving the original content and structure of the script.
        temp_array.append(line + "\n")

        # t checks if the current line matches the comment marker "#ImportRegion," indicating the section where import
        # statements should be added.
        if line == "# ImportRegion":
            # If the marker is found, it appends a series of import statements related to agent-based modeling
            # libraries, such as ECAgent.Core, ECAgent.Tags, ECAgent.Environments, and some utility functions
            # like pickle.
            temp_array.append("import ECAgent.Core as Core")
            temp_array.append("import ECAgent.Tags as Tags")
            temp_array.append("import ECAgent.Collectors as Collectors")
            temp_array.append("from ECAgent.Environments import GridWorld, PositionComponent, discrete_grid_pos_to_id")
            temp_array.append("import time")
            temp_array.append("import random")
            temp_array.append("import numpy\n")

    # After processing all lines and adding the necessary import statements, the function opens the same model_name
    # + ".py" file for writing again in "w" mode, effectively overwriting the original file.
    with open("Saves/Saved Models/Python File/" + model_name + ".py", "w") as python_file:

        # It writes each line from the temp_array to the modified file, including the added import statements,
        # which completes the base script for the customized model.
        for line in temp_array:
            python_file.write(line + "\n")


'''
This write_agen function is designed to facilitate  the addition of customized agent classes to a model by modifying an 
existing Python file. This function takes the following arguments:

    #agent_name: A string representing the name of the custom agent class to be created.
    #parameters: A list of tuples, each containing two elements: the parameter name (string)
     and its data type. These parameters are used to initialize the agent class.
    #fields: A list of tuples, each containing two elements: the field name (string) and 
     its initial value (any valid Python value). These fields values are either taken from the parameters when
     instantiating the class or set by the user.
    #component_list: A list of tuples, each containing two elements: the name of a component to be added to the agent
     (string) and a list of parameters (if any) required for that component.
    #file_name: A string representing the name of the Python script file where the custom agent class will be created.
'''


def write_agent(file_name: str, agent_name: str, parameters: list, fields: list, component_list: list = None):
    # It calls the ReadFileToArray function to read the contents of the specified file_name and stores each line as an
    # element in the global line_array. This is done to prepare the file for modification.
    read_file_to_array(file_name)
    global line_array

    # It initializes a temporary list called temp_array to store the modified lines of the script.
    temp_array = []

    # It iterates through each line in the line_array.
    for line in line_array:

        # It appends the original line to the temp_array, preserving the original content and structure of the script.
        temp_array.append(line + "\n")

        #  It checks if the current line matches the comment "#AgentRegion," which serves as a marker indicating where
        #  the custom agent class should be added.
        if line == "# AgentRegion":
            temp_array.append("\n")

            #  If the marker is found, it opens a template file located at "Syntax/AgentClassSyntax" in read mode.
            #  This template contains the skeleton structure of a Python class.
            with open("Syntax/AgentClassSyntax", "r") as python_file:
                if parameters == [None]:
                    content = python_file.read()
                    to_print = content.replace("AgentGroup", agent_name)
                    to_print2 = to_print.replace("#AnyAttribute", "")
                    to_print3 = to_print2.replace("#SelfAnyAttribute", "")
                    to_print4 = to_print3.replace("AgentTag", agent_name.upper())
                    temp_array.append(to_print4 + "\n\n")

                # It customizes the template by replacing placeholders such as "AgentGroup" with the provided
                # agent_name. Depending on whether parameters are provided or not, it also replaces placeholders for
                # attributes and initializes them accordingly.
                else:
                    content = python_file.read()
                    to_print = content.replace("AgentGroup", agent_name)
                    attribute_string = ""
                    for x in range(len(parameters)):
                        if x != len(parameters) - 1:
                            attribute_string += (parameters[x][0]) + ": " + str(parameters[x][1]) + ","
                        else:
                            attribute_string += (parameters[x][0]) + ": " + str(parameters[x][1])
                    to_print2 = to_print.replace("#AnyAttribute", attribute_string)
                    attribute_string = ""
                    if fields != [None]:
                        for x in range(len(fields)):
                            if fields[x][1].lower == "self":
                                if x != len(fields) - 1:
                                    attribute_string += "self." + str(fields[x][0]) + " = " + str(
                                        fields[x][0]) + "\n" + tab_space + tab_space
                                else:
                                    attribute_string += "self." + str(fields[x][0]) + " = " + str(fields[x][0])
                            else:
                                if x != len(fields) - 1:
                                    attribute_string += "self." + str(fields[x][0]) + " = " + str(
                                        fields[x][1]) + "\n" + tab_space + tab_space
                                else:
                                    attribute_string += "self." + str(fields[x][0]) + " = " + str(fields[x][1])
                        to_print3 = to_print2.replace("#SelfAnyAttribute", attribute_string)
                    else:
                        to_print3 = to_print2.replace("#SelfAnyAttribute", "")
                    to_print4 = to_print3.replace("AgentTag", agent_name.upper())
                    # It creates a string components_to_add to store the code for adding components to the agent.
                    components_to_add = ""

                    # # It iterates through the component_list, replacing placeholders in a component addition template
                    # with the component's name and parameters. This string is then inserted into the agent
                    # class definition.
                    if component_list is not None:
                        for component in component_list:
                            component_parameters = ""

                            # The component variable is a tuple containing two elements: the name of the component
                            # (accessed as component[0]) and a list of parameters for that component
                            # (accessed as component[1]).

                            # Inside the loop, it initializes an empty string component_parameters to build a string
                            # representation of the parameters for the current component.
                            for i in range(len(component[1])):
                                if i != len(component[1]) - 1:
                                    component_parameters += component[1][i][1] + ", "
                                else:
                                    component_parameters += component[1][i][1]

                            # After constructing the component_parameters string, it opens a template file located at
                            # "Syntax/AddComponentSyntax" in read mode using a with statement. This template file contains
                            # the syntax for adding a specific component to an agent.
                            with open("Syntax/AddComponentSyntax", "r") as syntax_file:

                                # It reads the content of the template file into the content variable.
                                content = syntax_file.read()

                                # It replaces placeholders in the template with actual values using the replace method.
                                # Specifically: #Component_name with the name of the current component (component[0]).
                                # Parameters with the component_parameters string, which is the comma-separated list
                                # of parameters for the component.
                                to_print = content.replace("#Component_name", component[0])
                                to_print2 = to_print.replace("#Parameters", component_parameters)

                                # The modified component syntax (to_print2) is then appended to the components_to_add
                                # string. This string will accumulate the code necessary to add all components specified
                                # in the component_list
                                if component_list.index(component) != len(component_list) - 1:
                                    components_to_add += to_print2 + "\n" + tab_space + tab_space
                                else:
                                    components_to_add += to_print2

                    # The final variable is the completed customized agent class format to be added to the model.
                    final = to_print4.replace("#ListOfComponentsToAdd", components_to_add)

                    # It writes the customized class definition to the temp_array.
                    temp_array.append(final + "\n\n")

    # After processing all lines in the original file and creating the custom agent class, the function opens the
    # file_name for writing in "w" mode, effectively overwriting the original file.
    with open("Saves/Saved Models/Python File/" + file_name + ".py", "w") as python_file:

        # It writes each line from the temp_array to the modified file, effectively updating the script with the newly
        # added custom agent class.
        for line in temp_array:
            python_file.write(line)


'''
This write_tags function is designed for adding tags to a base Python file(used for custom model) once the user has
created a new agent class. It takes two arguments: 

    #file_name: A string representing the name of the Python script file where the tags will be added.
    #agent_list: A list of tuples, where each tuple contains two elements: the name of a customized agent class (string)
     and the tags associated with that agent (string or list of strings).
'''


def write_tags(file_name, agent_list: list):
    # It calls a function (presumably read_file_to_array) to read the contents of the specified file_name and stores
    # each line as an element in the global line_array. This is done to prepare the file for modification.
    read_file_to_array(file_name)
    global line_array, agent_class_components
    for agent in agent_list:
        agent_class_components_list = [agent, []]
        agent_class_components.append(agent_class_components_list)
    # It initializes an empty list called temp_array to store the modified lines of the script.
    temp_array = []

    # It iterates through each line in the line_array:
    for line in line_array:

        # It appends the original line to the temp_array, preserving the original content and structure of the script.
        temp_array.append(line + "\n")

        # It checks if the current line matches the comment marker "#TagsRegion," which serves as a placeholder
        # indicating where tag-related code should be added.
        if line == "# TagsRegion":
            temp_array.append("\n")

            # It then iterates through the agents list, which contains information about each customized agent
            # and their associated tags. For each agent, it generates a line of code that uses the Tags.add_tag()
            # function to add the specified tag(s) to the agent. The tag(s) are derived from the agents list.
            for agent in agent_list:
                temp_array.append("Tags.add_tag('" + str(agent.upper()) + "')\n")

        # After processing all lines in the original file and adding the tags to the appropriate region, the function
        # opens the file_name + ".py" file for writing in "w" mode, effectively overwriting the original file.
    with open("Saves/Saved Models/Python File/" + file_name + ".py", "w") as python_file:

        # It writes each line from the temp_array to the modified file, including the added tag-related code,
        # thus updating the script with the newly assigned tags for the custom agent classes.
        for line in temp_array:
            python_file.write(line)


'''
The write_agent_component function is designed for the creation  of custom, distinct components that are linked to
specific agents within a customized model file. This Agent Component class not only generates the index but also
manages the agent IDs and keeps a count of the total number of agents that have been created.
This function takes a single argument:

    #file_name, which is the name of the custom model file where these agent-related components should be written.
'''


def write_agent_component(file_name):
    # It calls a function (presumably read_file_to_array) to read the contents of the specified file_name and stores
    # each line as an element in the global line_array. This is done to prepare the file for modification.
    read_file_to_array(file_name)
    global line_array

    # It initializes an empty list called temp_array to store the modified lines of the script.
    temp_array = []

    # It iterates through each line in the line_array:
    for line in line_array:

        # It appends the original line to the temp_array, preserving the original content and structure of the script.
        temp_array.append(line + "\n")

        # It checks if the current line matches the comment marker "#ComponentRegion," which serves as a placeholder
        # indicating where the agent component class code should be added.
        if line == "# ComponentRegion":
            temp_array.append("\n")

            # When the "#ComponentRegion" marker is found. It opens a template file located at
            # "Syntax/AgentComponentClassSyntax" in read mode ('r'). This template file contains the skeleton structure
            # of an agent component class.
            with open("Syntax/AgentComponentClassSyntax", 'r') as python_file:
                # It reads the content of the template file into the variable content.
                content = python_file.read()

            # It appends the content of the template (i.e., the agent component class structure) to the temp_array.
            temp_array.append(content + "\n")

    # After processing all lines in the original file and adding the agent component code to the appropriate region,
    # the function opens the file_name + ".py" file for writing in "w" mode, effectively overwriting the original file.
    with open("Saves/Saved Models/Python File/" + file_name + ".py", "w") as python_file:

        # It writes each line from the temp_array to the modified file, including the added agent component class
        # structure, thus updating the script with the newly created agent component.
        for line in temp_array:
            python_file.write(line)


'''
The write_component function is designed for creating and generating Python code components that can be assigned to
any agents within a custom model. This function takes the following arguments:

    #component_name: A string representing the name of the custom component class to be created.
    #parameters: A list of tuples, each containing two elements: the parameter name (string) and its default data type.
     These parameters are used to initialize the component class.
    #fields: A list of tuples, each containing two elements: the field name (string) and 
     its initial value (any valid Python value). These fields values are either taken from the parameters when
     instantiating the class or set by the user.
    #file_name: A string representing the name of the Python script file where the custom component class will be added.
'''


def write_component(file_name: str, component_name: str, parameters: list, fields: list):
    # It calls the ReadFileToArray function to read the contents of the specified file_name and stores each line as an
    # element in the global line_array. This is done to prepare the file for modification.
    read_file_to_array(file_name)
    global line_array

    # It initializes a temporary list called temp_array to store the modified lines of the script.
    temp_array = []

    # It iterates through each line in the line_array:
    for line in line_array:

        #  It appends the original line to the temp_array, preserving the original content and structure of the script.
        temp_array.append(line + "\n")

        #  It checks if the current line matches the comment "#ComponentRegion," which serves as a marker indicating
        #  where the custom component class should be added.
        if line == "# ComponentRegion":
            temp_array.append("\n")

            # If the marker is found, it opens a template file located at "Syntax/ComponentClassSyntax" in read mode.
            # This template contains the skeleton structure of a Python class.
            with open("Syntax/ComponentClassSyntax", 'r') as python_file:

                # If the component class does not contain any parameters, it will simply name the component class.
                if parameters == [None]:
                    content = python_file.read()
                    to_print = content.replace("ComponentGroup", component_name)
                    to_print2 = to_print.replace("#AnyAttribute", "")
                    to_print3 = to_print2.replace("#SelfAnyAttribute", "")
                    temp_array.append(to_print3 + "\n")

                # Otherwise, it customizes the template by replacing placeholders such as "ComponentGroup" with the
                # provided component_name. Depending on whether parameters are provided or not, it also replaces
                # placeholders for attributes and initializes them accordingly.
                else:
                    content = python_file.read()
                    to_print = content.replace("ComponentGroup", component_name)
                    attribute_string = ""
                    for x in range(len(parameters)):
                        if x != len(parameters) - 1:
                            attribute_string += (parameters[x][0]) + ": " + str(parameters[x][1]) + ", "
                        else:
                            attribute_string += (parameters[x][0]) + ": " + str(parameters[x][1])
                    to_print2 = to_print.replace("#AnyAttribute", attribute_string)
                    attribute_string = ""

                    # Writing field variables to the component class in the body of the class.
                    # Structure of the variable definition varies.
                    for x in range(len(fields)):
                        if fields[x][1].lower() == "self":
                            if x != len(fields) - 1:
                                attribute_string += "self." + str(fields[x][0]) + " = " + str(
                                    fields[x][0]) + "\n" + tab_space + tab_space
                            else:
                                attribute_string += "self." + str(fields[x][0]) + " = " + str(
                                    fields[x][0])
                        else:
                            if x != len(fields) - 1:
                                attribute_string += "self." + str(fields[x][0]) + " = " + str(
                                    fields[x][1]) + "\n" + tab_space + tab_space
                            else:
                                attribute_string += "self." + str(fields[x][0]) + " = " + str(
                                    fields[x][1])
                    to_print3 = to_print2.replace("#SelfAnyAttribute", attribute_string)

                    # It writes the customized class definition to the temp_array.
                    temp_array.append(to_print3)

    # After processing all lines in the original file and creating the custom component class, the function opens the
    # file_name for writing in "w" mode, effectively overwriting the original file.
    with open("Saves/Saved Models/Python File/" + file_name + ".py", "w") as python_file:

        # It writes each line from the temp_array to the modified file, effectively updating the script with the newly
        # added custom component class.
        for line in temp_array:
            python_file.write(line)


'''
The write_system function is designed to add a system component to a customized model by integrating the system's code
from an external file into the model's script. This function is used to extend the functionality of an agent-based
model by including custom system components. It takes the following arguments:

    #file_name: A string representing the name of the Python script file of the customized model where the system
     component code will be added.
    #system_name: A string representing the name of the system component's Python file to be integrated into the model.
'''


def write_system(file_name: str, system_name: str):
    # The function first calls a function (presumably read_file_to_array) to read the contents of the specified
    # file_name and stores each line as an element in the global line_array. This is done to prepare the model
    # file for modification.
    read_file_to_array(file_name)

    # It opens the external system component file with the name system_name + ".py" in read mode ("r") using the open
    # function and assigns it to the system_file variable.
    system_file = open("Saves/Saved Systems/" + system_name, "r")
    # It reads the entire content of the external system component file into the system variable using the read method.
    system = system_file.read()
    global line_array

    # It initializes an empty list called temp_array to store the modified lines of the script.
    temp_array = []
    for line in line_array:

        # It appends the original line to the temp_array, preserving the original content and structure of the
        # model script.
        temp_array.append(line + "\n")

        # It checks if the current line matches the comment marker "#SystemRegion," which serves as a placeholder
        # indicating where the system component's code should be added.
        if line == "# SystemRegion":
            temp_array.append("\n")

            # When the "#SystemRegion" marker is found. It appends the content of the system variable (the code from
            # the external system component file) to the temp_array. This effectively integrates the system component's
            # code into the model script.
            temp_array.append(system + "\n")

    # The system_file is then closed using the close method to release the system file's resources.
    system_file.close()

    # Finally, the function opens the file_name + ".py" file for writing in "w" mode using a context manager
    # (with open(...) as python_file) and writes each line from the temp_array to the modified file,
    # thus updating the script with the newly added system component code.
    with open("Saves/Saved Models/Python File/" + file_name + ".py", "w") as python_file:
        for line in temp_array:
            python_file.write(line)


'''
The write_model function is designed for initializing a custom model by adding systems 
and initializing agent variables based on the provided parameters. It takes four input arguments:

    #file_name: A string representing the name of the Python script file where the model class and agent initialization
     code will be added.
    #model_name: A string representing the name of the model class to be created.
    #agent_amount: A list of tuples, each containing two elements: the name of an agent class (string) and the number
     of instances of that agent to be created (integer).
    #model_parameters: A list of strings representing the parameters that will be passed to the model class when
     it is instantiated.
'''


def write_model(file_name: str, model_name: str):
    # The function calls a function (presumably read_file_to_array) to read the contents of the specified file_name and
    # stores each line as an element in the global line_array. This is done to prepare the file for modification.
    read_file_to_array(file_name)
    global line_array

    # It initializes an empty list called temp_array to store the modified lines of the script.
    temp_array = []

    # It iterates through each line in the line_array.
    for line in line_array:

        # It appends the original line to the temp_array, preserving the original content and structure of the script.
        temp_array.append(line + "\n")

        # It checks if the current line matches the comment marker "#ModelRegion," which serves as a placeholder
        # indicating where the model class code should be added.
        if line == "# ModelRegion":
            temp_array.append("\n")

            # When the "#ModelRegion" marker is found. It opens a template file located at "Syntax/ModelSyntax" in
            # read mode ('r'). This template file contains the skeleton structure of a Python model class.
            with open("Syntax/ModelSyntax", "r") as python_file:
                # It reads the content of the template file into the variable content.
                content = python_file.read()

                # It replaces placeholders in the template with the provided model_name and parameters to create a
                # customized model class definition.
                to_print = content.replace("ModelName", model_name)

                # It appends the customized model class definition to the temp_array.
                temp_array.append(to_print + "\n")

    # After processing all lines in the original file and adding the model class code, the function opens the
    # file_name + ".py" file for writing in "w" mode, effectively overwriting the original file.
    with open("Saves/Saved Models/Python File/" + file_name + ".py", "w") as python_file:

        # It writes each line from the temp_array to the modified file, including the added model class definition,
        # thus updating the script with the newly created model class.
        for line in temp_array:
            python_file.write(line)

    # This function is responsible for loading the syntax associated with a recorder class. The
    # recorder class is utilized to record data related to agent populations and their locations
    # during the runtime of a model. Once this syntax is loaded, it is integrated into a Python file.
    # The purpose of this integration is to enable the passing of recorded data to a graphical user
    # interface (GUI) once it is loaded as a pickle file.
    with open("Saves/Saved Models/Python File/" + file_name + ".py", "r") as python_file:
        content = python_file.read()
        to_print = content.replace('# Model Name', f"self.model_name = '{file_name}'")
        with open("Syntax/Recorder", 'r') as recorder_file:
            recorder_syntax = recorder_file.read()
        to_print2 = to_print.replace("# Recorder", recorder_syntax)

    with open("Saves/Saved Models/Python File/" + file_name + ".py", "w") as python_file:
        python_file.write(to_print2)


def model_agent_initialisation(file_name: str, agents):
    # The function then calls the read_file_to_array function again to read the contents of the modified
    # script into the line_array for further modifications.
    read_file_to_array(file_name)

    # It initializes a new empty list called new_temp_array to store additional modifications to the script.
    new_temp_array = []

    # It iterates through each line in the line_array.
    for line in line_array:

        # It appends the original line to the new_temp_array, preserving the original content and structure
        # of the script.
        new_temp_array.append(line + "\n")

        # It checks if the current line matches the comment "# Create Agents At Random Locations," which serves as
        # a marker for initializing agents.
        if line == "    # Create Agents At Random Locations":

            # When the marker is found, it opens a template file located at "Syntax/InitialiseAgents" in read mode
            # ('r'). This template file contains code for initializing agents.
            with open("Syntax/InitialiseAgents", "r") as python_file:
                content = python_file.read()
                global model_parameters
                # It replaces placeholders in the template with the names of agent classes and the number of instances
                # of each agent class specified in the agent_amount list.
                for agent in agents:
                    model_parameters.append(["init_" + agent.lower(), "int"])
                    to_print = content.replace("init_agent", "init_" + agent.lower())
                    to_print2 = to_print.replace("Agent", agent)

                    # It appends the customized agent initialization code to the new_temp_array.
                    new_temp_array.append(to_print2 + "\n")

    # Finally, it opens the file_name + ".py" file for writing in "w" mode again and writes each line from
    # the new_temp_array to the modified file, updating the script with the agent initialization code.
    with open("Saves/Saved Models/Python File/" + file_name + ".py", "w") as python_file:
        for line in new_temp_array:
            python_file.write(line)


'''
The insert_model_parameters function is designed to add model parameters to the initialization of a custom model in a
Python script. It serves the purpose of automatically inserting the required model parameters after systems and
components have been added to the model. It takes one argument:

    #file_name: A string representing the name of the Python script file (the custom model file) to which the model
     parameters will be added.
'''


def insert_model_parameters(file_name: str, agents: list):
    # The function calls a function (presumably read_file_to_array) to read the contents of the specified file_name and
    # stores each line as an element in the global line_array. This is done to prepare the file for modification.
    read_file_to_array(file_name)
    global line_array
    global model_parameters, flexible_model_parameters, agent_class_components, re_init_parameters
    # It also initializes an empty string called parameters, which will be used to construct a comma-separated string
    # representation of the model parameters (fixed and flexible) that will be passed to the model class during
    # initialization.
    parameters = ""
    flexible_parameters = ""
    model_parameter_list = ['size']
    for parameter in model_parameters:
        model_parameter_list.append(parameter[0])
    model_parameter_list.append('seed')
    # The function then iterates through the model_parameters (which is assumed to be a global variable) and constructs
    # the parameters string. For each parameter in model_parameters, it appends the parameter name and value to the
    # parameters string. If the current parameter is not the last one in the list, a comma is added to separate it
    # from the next parameter.
    for parameter in model_parameters:
        if model_parameters.index(parameter) != len(model_parameters) - 1:
            parameters += parameter[0] + ": " + parameter[1] + ", "
        else:
            parameters += parameter[0] + ": " + parameter[1]

    for parameter in flexible_model_parameters:
        if flexible_model_parameters.index(parameter) != len(flexible_model_parameters) - 1:
            flexible_parameters += tab_space + tab_space + "self." + parameter[0] + ": " + parameter[0] + "\n"
        else:
            flexible_parameters += tab_space + tab_space + "self." + parameter[0] + ": " + parameter[0]

    # After constructing the parameters string, the function opens the file_name + ".py" file for reading ("r" mode).
    # It reads the content of the file into the content variable.
    with open("Saves/Saved Models/Python File/" + file_name + ".py", "r") as python_file:
        content = python_file.read()

        # It then replaces the placeholder "#ModelParameters" in the script content with the constructed parameters
        # string.This effectively inserts the model parameters into the script.
        to_print = content.replace("#ModelParameters", parameters)
        to_print2 = to_print.replace("# Agent Class Components List",
                                     'agent_class_components = ' + str(agent_class_components))

        to_print3 = to_print2.replace('# Model Flexible Parameters',
                                      'model_flexible_parameters = ' + str(flexible_model_parameters))
        to_print4 = to_print3.replace("# Model Parameters", f'Model_parameters = {str(model_parameter_list)}')
    # Finally, the function opens the file_name + ".py" file for writing ("w" mode) and writes the modified content
    # (with the model parameters inserted) back to the file, effectively updating the script with the required
    # model parameters.
    with open("Saves/Saved Models/Python File/" + file_name + ".py", "w") as python_file:
        python_file.write(to_print4)

    last_id_list = []
    for i in agents:
        last_id_list.append([i, []])
    with open("Saves/Saved Models/Python File/" + file_name + ".py", "r") as python_file:
        content = python_file.read()
        to_print = content.replace("# last IDs", "self.agent_last_id = " + str(last_id_list))

    with open("Saves/Saved Models/Python File/" + file_name + ".py", "w") as python_file:
        python_file.write(to_print)

    re_init_list = f""
    for i in re_init_parameters:
        re_init_list += f"self.{i} = {i}" + "\n" + tab_space + tab_space

    with open("Saves/Saved Models/Python File/" + file_name + ".py", "r") as python_file:
        content = python_file.read()
        to_print = content.replace("# re-initialization parameters", re_init_list)
        to_print2 = to_print.replace("# Re_init_parameters", f'Re_init_parameters = {re_init_parameters}')

    with open("Saves/Saved Models/Python File/" + file_name + ".py", "w") as python_file:
        python_file.write(to_print2)


'''
The ReadFileToArray function is a Python utility designed to read the contents of a 
specified file and convert it into an array. This function takes one argument:

    #file_name, which should be a string representing the name of the file to be read.
'''


def read_file_to_array(file_name: str):
    # It initializes a global variable named line_array as an empty list.
    # This list will be used to store the lines of the file.
    global line_array
    line_array = []

    # It opens the specified file for reading using the open function, assuming that the file has a ".py" extension.
    # The file is opened in read mode ("r").
    with open("Saves/Saved Models/Python File/" + file_name + ".py", "r") as python_file:
        # It enters a loop that iterates through each line in the opened file.
        for line in python_file:
            # For each line in the file, it removes any trailing whitespace or newline characters using the
            # rstrip method and appends the cleaned line to the line_array.
            line_array.append(line.rstrip())

    # After reading all the lines in the file, the function returns the line_array,
    # which now contains each line from the file as a separate element in the array.


'''
The write_add_agent_components function is designed to initialize agent components for each agent in a custom model.
This function is used to modify a Python script file by adding code that initializes agent components with a specific
counter and prefix for agent IDs. This function takes the following arguments:

    #file_name: A string representing the name of the Python script file (the custom model file) to which the agent
     components will be added.
    #agent_name: A string representing the name of the agent class for which components will be initialized.
'''


def write_add_agent_components(file_name: str, agent_names: list):
    # It calls the ReadFileToArray function to read the contents of the specified file_name
    # and store each line as an element in the global line_array. This is done to prepare the
    # file for modification.
    read_file_to_array(file_name)
    global line_array, agent_class_components

    # It initializes a temporary list called temp_array to store the modified lines of the script.
    temp_array = []

    # It iterates through each line in the line_array.
    for line in line_array:

        # It appends the original line to the temp_array, preserving the original content and structure of the script.
        temp_array.append(line + "\n")

        # It checks if the current line matches the comment "# Add Agent Components,"
        # which serves as a marker to indicate where the class component should be added.
        if line == "    # Add Agent Components":
            for agent in agent_names:
                agent_component_line = (
                        tab_space + tab_space + agent + ".add_class_component(AgentComponent(" + agent + ", self, " + "'" + agent.lower() + "'" + "))")
                for agent_class in agent_class_components:
                    if agent_class[0] == agent:
                        agent_class[1].append("AgentComponent")
                temp_array.append(agent_component_line + "\n")

    # After processing all lines in the original file, the function opens the file_name for writing in "w" mode,
    # effectively overwriting the original file.
    with open("Saves/Saved Models/Python File/" + file_name + ".py", "w") as python_file:

        # It writes each line from the temp_array to the modified file,
        # effectively updating the script with the newly added class component.
        for line in temp_array:
            python_file.write(line)


'''
The WriteAddClassComponent function is designed to customize a Python script by adding class components to agents
within a specified model.This function takes the following arguments:

    #file_name: A string representing the name of the Python script file to be modified.
    #agent_name: A string representing the name of the agent to which the class component will be added.
    #component_name: A string representing the name of the class component to be added.
    #parameters: A list of strings representing the parameters to be passed when initializing the class component.
'''


def write_add_class_component(file_name, agent_name: str, component_name: str, parameters: list):
    # It calls the ReadFileToArray function to read the contents of the specified file_name
    # and store each line as an element in the global line_array. This is done to prepare the
    # file for modification.
    read_file_to_array(file_name)
    global line_array, agent_class_components, re_init_parameters
    for agent_class in agent_class_components:
        if agent_class[0] == agent_name:
            agent_class[1].append(component_name)
    # It initializes a temporary list called temp_array to store the modified lines of the script.
    temp_array = []
    para = ""

    # It iterates through each line in the line_array.
    for line in line_array:

        # It appends the original line to the temp_array, preserving the original content and structure of the script.
        temp_array.append(line + "\n")

        # It checks if the current line matches the comment "# Add Class Components,"
        # which serves as a marker to indicate where the class component should be added.
        if line == "    # Add Class Components":

            # If the marker is found, it opens a template file located at "Syntax/AddClassComponentSyntax"
            # in read mode. This template contains the syntax for adding a class component to an agent.
            with open("Syntax/AddClassComponentSyntax", "r") as python_file:
                content = python_file.read()

                # It replaces placeholders in the template with the provided agent_name, component_name,
                #  and parameters to create a customized class component declaration.
                to_print = content.replace("Agent", agent_name)
                to_print2 = to_print.replace("#Component", component_name)
                global model_parameters
                global flexible_model_parameters
                if parameters != [None]:
                    temp_parameters = copy.deepcopy(parameters)

                    for i in range(len(parameters)):
                        temp_parameters[i][0] = agent_name.lower() + "_" + parameters[i][0]
                        re_init_parameters.append(agent_name.lower() + "_" + parameters[i][0])

                    # Temporary array to store parameter details to alter later.
                    temp_flexible_parameters = copy.deepcopy(temp_parameters)
                    for i in range(len(parameters)):
                        temp_flexible_parameters[i].append(parameters[i][0])

                    # Append new index of parameter details to the flexible model parameters array.
                    flexible_model_parameters.append(['agent', [agent_name, component_name], temp_flexible_parameters])

                    for i in range(len(parameters)):
                        model_parameters.append(temp_parameters[i])
                        if i != len(parameters) - 1:
                            para = temp_parameters[i][0] + ", "
                        else:
                            para += temp_parameters[i][0]
                else:
                    pass
                to_print3 = to_print2.replace("#Parameters", para)

                # It appends the customized class component declaration to the temp_array.
                temp_array.append(to_print3 + "\n")

    # After processing all lines in the original file, the function opens the file_name for writing in "w" mode,
    # effectively overwriting the original file.
    with open("Saves/Saved Models/Python File/" + file_name + ".py", "w") as python_file:

        # It writes each line from the temp_array to the modified file,
        # effectively updating the script with the newly added class component.
        for line in temp_array:
            python_file.write(line)


'''
The add_systems function is designed to enable users to add customized systems to a custom model file.
This function takes the following arguments:

        #file_name: A string representing the name of the Python script file (the custom model file) to which the
         user wants to add a system.
        #system_name: A string representing the name of the system to be added.
        #system_id: A string representing the identifier or ID associated with the system.
        #parameter_list: A list of strings representing parameters specific to the system. (Can be none)
'''


def add_systems(file_name: str, system_name: str, system_id: str, parameter_list: list):
    # The function calls a function (presumably read_file_to_array) to read the contents of the specified file_name and
    # stores each line as an element in the global line_array. This is done to prepare the file for modification.
    read_file_to_array(file_name)
    global line_array

    # It initializes an empty list called temp_array to store the modified lines of the script.
    temp_array = []

    for line in line_array:

        # It appends the original line to the temp_array, preserving the original content and structure of the script.
        temp_array.append(line + "\n")

        # It checks if the current line matches the comment " # Add Systems." This comment likely serves as a marker
        # to indicate where the system should be added.
        if line == "    # Add Systems":

            # If the marker is found, it opens a template file located at "Syntax/AddSystemSyntax" in read mode.
            # This template contains the code or syntax for adding a system to the custom model.
            with open("Syntax/AddSystemSyntax", "r") as python_file:
                content = python_file.read()

                #  It customizes the template by replacing placeholders such as "#System_name" with the provided
                #  system_name and "#System_id" with the provided system_id. Additionally, if parameter_list is
                #  provided, it replaces "#IfAnyParameters" with the comma-separated list of parameters.
                to_print = content.replace("#System_name", system_name)
                to_print2 = to_print.replace("#System_id", '"' + system_id + '"')
                if parameter_list == [None]:
                    to_print3 = to_print2.replace(", #IfAnyParameters ", "")
                else:
                    parameters = ""
                    global model_parameters
                    global flexible_model_parameters

                    for parameter in parameter_list:

                        # Temporary array to store parameter details to alter later.
                        temp_parameter_array = ['system', system_name, [parameter]]

                        # Append new index of parameter details to the flexible model parameters array.
                        flexible_model_parameters.append(temp_parameter_array)

                        # Append new parameter to the model parameters array.
                        model_parameters.append(parameter)
                        if parameter_list.index(parameter) != len(parameter_list) - 1:
                            parameters += parameter[0] + ", "
                        else:
                            parameters += parameter[0]
                    to_print3 = to_print2.replace(", #IfAnyParameters ", ", " + parameters)

                #  It appends the customized system addition code to the temp_array.
                temp_array.append(to_print3 + "\n")

    # Finally, it opens the file_name + ".py" file for writing in "w" mode again and writes each line from
    # the new_temp_array to the modified file, updating the script with the agent initialization code.
    with open("Saves/Saved Models/Python File/" + file_name + ".py", "w") as python_file:
        for line in temp_array:
            python_file.write(line)


'''
This write_population_collector_system function is designed to collect live
population data for each agent in a model while it is running and record this data as a list. 
This function takes the following arguments:

    #file_name: A string representing the name of the Python script file (the custom model file) to which the
     user wants to add a system.
    #agent_list: A list of agents that are in the model that will be ran.
'''


def write_population_collector_system(file_name: str, agent_list):
    # The function calls a function (presumably read_file_to_array) to read the contents of the specified file_name and
    # stores each line as an element in the global line_array. This is done to prepare the file for modification.
    read_file_to_array(file_name)
    global line_array

    # It initializes an empty list called temp_array to store the modified lines of the script.
    temp_array = []

    # It prepares a string called agent_list_for_record to hold the agent data in a specific format.
    # This string will be used to record live population data for each agent.
    agent_list_for_record = ""
    for agent in agent_list:
        if agent_list.index(agent) != len(agent_list) - 1:
            agent_list_for_record += "'" + agent.lower() + "'" + ": [], "
        else:
            agent_list_for_record += "'" + agent.lower() + "'" + ": []"

    # The function iterates through each line in the original script, preserving its content and structure.
    for line in line_array:

        # It appends the original line to the temp_array, preserving the original content and structure of the script.
        temp_array.append(line + "\n")

        # When the function encounters a specific line (marked as "# SystemRegion"), it performs the following actions:
        if line == "# SystemRegion":
            temp_array.append("\n")

            # It opens another file, "Syntax/PopulationDataCollectorSystem," in read mode.
            with open("Syntax/PopulationDataCollectorSystem", "r") as python_file:
                content = python_file.read()
                to_print = content.replace("#Agents", agent_list_for_record)
                temp_array.append(to_print)

            temp_array.append("\n")

            # Next, it opens another file, "Syntax/CountAgentSyntax," also in read mode.
            with open("Syntax/CountAgentSyntax", "r") as python_file:
                content = python_file.read()

                # It iterates through the agent_list and replaces placeholders in the content with agent-specific
                # information.
                for agent in agent_list:
                    to_print = content.replace("#agent_name_upper", agent)
                    to_print2 = to_print.replace("#agent_name", "'" + agent.lower() + "'")
                    to_print3 = to_print2.replace("#agent_tag", agent.upper())
                    temp_array.append(to_print3 + "\n")

    # Finally, the function returns the modified script, including the recorded population data for each agent.
    with open("Saves/Saved Models/Python File/" + file_name + ".py", "w") as python_file:
        for line in temp_array:
            python_file.write(line)


"""
The write_main_function_to_model function writes a commented by """ """ main function to the model python file, 
once un-commented, it allows the user to run the model simulation outside the graphical editor, but the user has
to manually change the model parameters, as well as size of x_lim and y_lim for the scatter plot, and the number 
of iterations which the model will run for. It takes only one argument:

    #file_name, which is used  to change the model class name within the main_function syntax, and load the
    parameter lists to the constructor.
    
"""


def write_main_function_to_model(file_name):
    para = ''
    for parameter in model_parameters:
        if model_parameters.index(parameter) != len(model_parameters):
            para += f'{parameter[0]}: {parameter[1]}, '
        else:
            para += f'{parameter[0]}: {parameter[1]}'
    with open('Syntax/RunModelAloneSyntax', 'r') as file:
        content = file.read()
        to_print = content.replace("#ModelName", file_name)
        to_print2 = to_print.replace("#ModelParameters", para)

    with open(f'Saves/Saved Models/Python File/{file_name}.py', 'a') as file:
        file.write(to_print2)

    with open(f'Saves/Saved Models/Python File/{file_name}.py', 'r') as py_file:
        content = py_file.read()

    with open(f'{file_name}.py', 'w') as py_file:
        py_file.write(content)
