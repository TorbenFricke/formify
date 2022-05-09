from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setup(
	name="formify",
	version="1.3.1",
	author="Torben Fricke",
	author_email="mail@torben.co",
	description="An easy to use UI Framework on top of Qt.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	packages=find_packages(),
	python_requires=">=3.8",
	url="https://github.com/TorbenFricke/formify",
	entry_points={
		'console_scripts': ['formify-install=formify.install_ui:main'],
	},
	include_package_data=True,
	package_data={
		"": ["*.css", "*.png", "*.ico"],
	},
	install_requires=["pyside6", "pyinstaller"]
)
