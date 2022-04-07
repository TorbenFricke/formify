#/usr/bin/sh

python3.10 -m pip install --upgrade pip
python3.10 -m pip install --upgrade build
python3.10 -m pip install --upgrade twine

python3.10 -m build
python3.10 -m twine upload --repository pypi -u tfricke dist/*