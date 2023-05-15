# Pipenv Cheat Sheet

# Get the version of Python installed 
python -V 
 
# Get the version of VS Code installed 
code -v 

# List installed packages 
python -m pip list 

# Create virtual environment named myenv
python -m venv myenv

# Change to project folder 
cd myenv
 
# Activate the virtual environment 
.\myenv\Scripts\Activate.ps1 

# Install requirements with pip 
python -m pip freeze > requirements.txt 

# Migrate to another venv 
pip install -r requirements.txt

 # Deactivate the environment 
deactivate 

# Delete virtual environment named myenv 
rm -Recurse myenv

<!-- https://medium.com/@astontechnologies/how-to-setup-a-virtual-development-environment-for-python-with-windows-powershell-4cd34b2f9f9b -->