.PHONY: compile deploy

compile:
	cd tyler/cs301/spring19 && python compile.py

deploy:
	python s3-sync.py
