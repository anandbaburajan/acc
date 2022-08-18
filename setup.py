from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in acc/__init__.py
from acc import __version__ as version

setup(
	name="acc",
	version=version,
	description="Accounting app",
	author="Anand",
	author_email="anand.b@frappe.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
