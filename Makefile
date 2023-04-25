SRC_DIR = src

db-generate:
	cd $(SRC_DIR) && alembic revision --autogenerate

db-upgrade:
	cd $(SRC_DIR) && alembic upgrade head
