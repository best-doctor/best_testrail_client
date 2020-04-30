check:
	flake8 .
	mypy .
	PYTHONPATH=./best_testrail_client:$PYTHONPATH python -m pytest --cov=best_testrail_client --cov-report=xml -p no:warnings --disable-socket
