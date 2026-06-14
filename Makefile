# Variables
PYTHON = ./venv/bin/python3
PIP = ./venv/bin/pip
TEST_PDF = sample.pdf

.PHONY: all install sample run clean

all: install sample run

install:
	$(PIP) install -r requirements.txt

sample:
	$(PYTHON) create_sample_pdf.py

run: sample
	$(PYTHON) main.py $(TEST_PDF)

clean:
	rm -f sample.pdf temp.typ output.pdf final_template.typ
	find . -type d -name "__pycache__" -exec rm -rf {} +
