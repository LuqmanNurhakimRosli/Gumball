from setuptools import setup, find_packages

setup(
    name="talent-acquisition",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "python-multipart",
        "python-dotenv",
        "google-generativeai",
        "numpy",
    ],
) 