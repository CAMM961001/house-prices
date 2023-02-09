pylint scripts/settings.py > logs/pep8_log.txt
flake8 scripts/settings.py >> logs/pep8_log.txt

pylint scripts/eda.py >> logs/pep8_log.txt
flake8 scripts/eda.py >> logs/pep8_log.txt

pylint scripts/preprocess.py >> logs/pep8_log.txt
flake8 scripts/preprocess.py >> logs/pep8_log.txt

pylint scripts/model.py >> logs/pep8_log.txt
flake8 scripts/model.py >> logs/pep8_log.txt