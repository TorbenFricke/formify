import pathlib

stylesheet_path = str(pathlib.Path(__file__).parent / "style.css")

def stylesheet() -> str:
	with open(stylesheet_path, "r") as f:
		return f.read()