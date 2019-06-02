pip install virtualenv
py -m venv myvenv
.\myvenv\Scripts\activate
python -m pip install --upgrade pip
pip install -r .\requirements.txt
py .\django\manage.py runserver 0.0.0.0:80