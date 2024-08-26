.PHONY: compile deploy

compile:
	cd tyler/cs544/f24 && python3 compile.py

deploy:
	python3 sync-s3.py
