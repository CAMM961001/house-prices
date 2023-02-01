pylint scripts/settings.py > assets/pep8_log.txt
flake8 scripts/settings.py >> assets/pep8_log.txt

pylint scripts/eda.py >> assets/pep8_log.txt
flake8 scripts/eda.py >> assets/pep8_log.txt

pylint scripts/preprocess.py >> assets/pep8_log.txt
flake8 scripts/preprocess.py >> assets/pep8_log.txt

pylint scripts/model.py >> assets/pep8_log.txt
flake8 scripts/model.py >> assets/pep8_log.txt