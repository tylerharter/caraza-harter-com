.PHONY: compile deploy

compile:
	cd tyler/cs544/s25 && python3 compile.py

deploy:
	python3 sync-s3.py
