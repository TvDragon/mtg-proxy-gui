from setuptools import setup, find_packages

setup(
    name="myproject",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "dotenv",
        "flask",
        "fpdf",
        "numpy",
        "matplotlib",
        "requests",
        "tqdm",
    ],
)