import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytest-databricks",
    version="0.0.8",
    author="Ivan Georgiev",
    #author_email="ivan.georgiev",
    description="Pytest plugin for remote Databricks notebooks testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ivangeorgiev/pytest-databricks",
    packages=setuptools.find_packages(),
    install_requires=[
        'pydbr',
        'pytest'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Pytest",
    ],
    entry_points={
        'pytest11': [
            'databricks = pytest_databricks.pytest.plugin',
        ]
    },
    python_requires='>=3.6',
)
