.PHONY: compile deploy

compile:
	cd tyler/cs544/s23 && python3 compile.py

deploy:
	python s3-sync.py
