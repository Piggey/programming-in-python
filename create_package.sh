# create new venv
python -m venv venv

# get needed packages 
pip install setuptools wheel

# create package
python setup.py sdist bdist_wheel
