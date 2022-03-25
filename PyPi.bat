python -m pip install --upgrade pip
python -m pip install --upgrade build
python -m pip install --upgrade twine

python -m build
python -m twine upload --repository pypi -u tfricke dist/*
