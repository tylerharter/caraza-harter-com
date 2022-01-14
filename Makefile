.PHONY: compile deploy

compile:
	cd tyler/cs320/f21 && python3 compile.py
	cd tyler/cs320/s22 && python3 compile.py

deploy:
	python s3-sync.py
