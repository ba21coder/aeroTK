from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aerotk",
    version="0.2.0",
    author="Batuhan",
    description="A lightweight, zero-dependency modern UI library for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KULLANICI_ADIN/AeroTk",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pyserial",  # Herkes pip install aerotk dediğinde otomatik inecek!
    ],
)
