from setuptools import setup, find_packages

setup(
    name="formify",
    version="1.2.0",
    packages=find_packages(),
	entry_points={
		'console_scripts': ['formify-install=formify.install_ui:main'],
	},
	package_data={
        "": ["*.css", "*.png", "*.ico"],
    },
	install_requires=["pyside6", "matplotlib", "pyinstaller"]
)