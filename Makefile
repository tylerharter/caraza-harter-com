.PHONY: compile deploy

compile:
	cd tyler/cs301/fall19 && python3 compile.py
	cd tyler/cs320/s20 && python3 compile.py

deploy:
	python s3-sync.py
