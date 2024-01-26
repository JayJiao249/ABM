PYTHON = python3
VENV_DIR = venv
ACTIVATE = $(VENV_DIR)/bin/activate
SRC_FOLDER = src
VENV_PYTHON = $(VENV_DIR)/bin/python
PIP3 = $(VENV_DIR)/bin/pip3

# Create virtual environment
venv:
	$(PYTHON) -m venv $(VENV_DIR)

# Activate the virtual environment
activate: venv
	. $(ACTIVATE)

# Installs dependencies
install: activate
	$(PIP3) install -r requirements.txt

# Copes the src file to the newly created venv folder
copy-src: venv
	cp -r $(SRC_FOLDER) $(VENV_DIR)

# Runs the GUI for ECAgent
run: activate copy-src
	$(VENV_PYTHON) $(SRC_FOLDER)/UI_for_ECAgent.py
