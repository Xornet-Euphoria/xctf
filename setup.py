from setuptools import setup, find_packages


setup(
    name="xctf",
    version="0.1",
    install_requires=[],
    package_dir={"": "src"},
    packages=find_packages("src"),
    scripts=["scripts/make_exploit.py"]
)
