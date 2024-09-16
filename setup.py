from setuptools import setup, find_packages

setup(
    name="gitbase",
    version="0.0.3",
    author="Taireru LLC",
    author_email="tairerullc@gmail.com",
    description="A package to manage player data on GitHub with encryption.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TaireruLLC/gitbase",
    packages=find_packages(),
    install_requires=[
        "requests",
        "cryptography"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
