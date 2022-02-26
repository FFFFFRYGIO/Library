create_admin:
	python instructions/create_admin.py

build: instructions/requirements.txt
	py -3 -m venv venv
	venv\Scripts\activate
	pip install -r instructions/requirements.txt
	python instructions/create_db.py

create_user:
	python instructions/create_user.py

run:
	python app.py