from setuptools import setup, find_packages
setup(
    name="formify",
    version="0.2.1",
    packages=find_packages(),
	package_data={
        "": ["*.css"],
    },
	install_requires=["pyside2", "matplotlib"]
)