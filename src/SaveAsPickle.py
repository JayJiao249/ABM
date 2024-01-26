# SaveAsPickle.py
"""
This class facilitates the conversion of active custom model instances into pickle files. Users
can then save these files on their devices to retain simulation data. This allows them to later
reload the model and resume simulations from where they left off.
"""

# Imports
import pickle

"""
Serialize and save a custom model instance to a binary file using the pickle module.

Args:
    model_object: The model to be saved.
    file_path (str): The file path where the model will be saved.

Returns:
    bool: True if the model was successfully saved, False otherwise.

Raises:
    Exception: If any error occurs during the saving process, it will be raised.
"""


def save_model_as_pickle(model_object, file_path):
    try:
        # Converts the model instance to the pickle at the selected path.
        with open(file_path, 'wb') as file:
            pickle.dump(model_object, file)
            return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise


"""
Load and deserialize a custom model instance from a binary file saved using the pickle module.

Args:
    selected_file_name (str): The name of the file containing the serialized model.

Returns:
    object: The deserialized model object.

Raises:
    FileNotFoundError: If the specified file does not exist.
    EOFError: If the specified file is empty or not a valid pickle file.
    Exception: If any other error occurs during the loading process, it will be raised.
"""


def load_pickle_as_model(selected_file_name):
    try:
        # Loads the model instance from the selected pickle file.
        with open(selected_file_name, 'rb') as file:
            loaded_object = pickle.load(file)
            return loaded_object
    except FileNotFoundError:
        return f"Error: File '{selected_file_name}' not found."
    except EOFError:
        return f"Error: File '{selected_file_name}' is empty or not a valid pickle file."
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise
