
rs:
	@uvicorn app.main:app --reload


isort:
	@isort ./app


black:
	@black ./app


flake8:
	@flake8 ./app

