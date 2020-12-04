from setuptools import setup, find_packages
setup(
    name="formify",
    version="0.7.0",
    packages=find_packages(),
	package_data={
        "": ["*.css"],
    },
	install_requires=["pyside2", "matplotlib"]
)