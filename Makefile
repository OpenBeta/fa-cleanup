init:
	virtualenv venv
	. venv/bin/activate
	pip install -r requirements.txt

activate:
	. venv/bin/activate

jupyter:
	jupyter notebook

