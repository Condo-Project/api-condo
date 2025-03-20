# ----------------------------------------------------------------------
# Created by - Jonathan Mandombe
# ----------------------------------------------------------------------

start: 
	python main.py
docker-compose:
	docker-compose up --build -d

dev: 
#	Running fastapi dev initiates development mode.
	fastapi dev main.py

run: 
#	Executing fastapi run starts FastAPI in production mode by default.
	fastapi run main.py

table:
#	docker-compose up migrate
	python scripts/create_tables.py

install:
	pip install -r requirements.txt
