# make sure virtual environment is setup for python
pip install virtualenv
py -m venv myvenv
.\myvenv\Scripts\activate
python -m pip install --upgrade pip
pip install -r .\requirements.txt

# run server
py .\django\manage.py runserver 0.0.0.0:8000