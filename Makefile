.PHONY: compile deploy

compile:
	cd tyler/cs301/fall18 && python compile.py

deploy:
	python s3-sync.py
