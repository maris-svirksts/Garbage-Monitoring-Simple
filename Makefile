setup:
	pip install -r requirements.txt

test:
	python -m unittest

#run:
#    python garbage_monitoring/app.py

clean:
    rm -rf __pycache__