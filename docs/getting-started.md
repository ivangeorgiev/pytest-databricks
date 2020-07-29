# Getting Started with pytest-databricks

In this guide I will show you how to quickly get started with pytest-databricks package:

1. Create test notebooks in Databricks
2. Create pytest script to orchestrate tests
3. Execute tests

All sources for this guide are available in GitHub: https://github.com/ivangeorgiev/pytest-databricks-example.

## Create Test Notebooks in Databricks

Here is an example [Databricks notebook](https://github.com/ivangeorgiev/pytest-databricks-example/blob/master/notebooks/Test-AssertEquals-DataFrames.ipynb) defining Python `unittest.TestCase`. You can import it in your Databricks workspace from [Jupyter Notebook](https://github.com/ivangeorgiev/pytest-databricks-example/blob/master/notebooks/Test-AssertEquals-DataFrames.ipynb) format or [Python source](https://github.com/ivangeorgiev/pytest-databricks-example/blob/master/notebooks/Test-AssertEquals-DataFrames.py) format and start using it as a template.

To make it more clear we will look into each command from the notebook.

### Cell 1: Install `pytest-databricks` package

The first command makes sure you have `pytest-databricks` package installed in Databricks. If you prefer, you can install the package using Databricks tools and remove this command cell completely.

```python
import sys
import subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "pytest-databricks"])
```



### Cell 2: Imports

In this cell we import the Python `unittest` module and the `run_unittest` helper function from `pytest-databricks`. 

```python
import unittest
from pytest_databricks.helper import run_unittest
```

The `run_unittest` function is a convenient method of executing test cases, written for python `unittest`. Under the hood, it executes the test case, collects output and xml report and returns a dictionary, which has necessary elements, expected by the `pytest-unittest` test client.



### Cell 3: The actual test case

The example notebook contains actual test case demonstrating how to assert two Spark DataFrames are equal. Here is an example of very simple test case.

```python
class TestMyApp(unittest.TestCase):
    
  def test_1_notequal_2(self):
    self.assertNotEqual(1, 2)
```

For more information on writing Python `unittest` test cases, refer to [unittest documentation](https://docs.python.org/3/library/unittest.html).

### Cell 4: Execute the test case

This cell executes the test cases, using the `run_unittest` helper function we imported earlier. It also prints the captured `unittest` output so that you have it for reference in the notebook.

```python
test_result = run_unittest(TestAssertEqualsForDataFrames)
print(test_result['run_output'])
```

### Cell 5: Exit the notebook

The last cell in the notebook should call `dbutils.notebook.exit` to finish the execution and return result to Databricks. This result can be accessed by external client applications (e.g. pytest-databricks test client). The result from our test notebook is the result returned from the `run_unittest` function in JSON format.

```python
import json
dbutils.notebook.exit(json.dumps(test_result))
```



## Create pytest Script to Orchestrate Tests

I will assume that you start a python project from scratch on your local machine. I will also assume that:

* you have an empty project directory created
* you have Python 3.7 or newer installed
* you can create a Databricks token
* you can find the Databricks cluster ID

### Step 1: Create and activate a virtual environment

It is always good to work in a virtual environment. Let's create one. Execute following in the command prompt if you are Linux/MacOs user:

```python
python -m venv .venv
source .venv/Scripts/activate
```

For Windows command line users the second command is slightly different:

```
python -m venv .venv
.venv\Scripts\activate.bat
```

For PowerShell users:

```powershell
python -m venv .venv
.venv/Scripts/activate.ps1
```

The first command will create a directory `.venv` which contains python virtual environment. The second line activates the environment for the command line (shell) session.

### Step 2: Create requirements.txt

Inside the project directory create a `requirements.txt` text file:

```
pydbr
pytest-databricks
```

We use this file to install package dependencies in Python.

### Step 3: Install dependencies

At the command line run the following command to install python package dependencies:

```bash
pip install -r requirements.txt
```

### Step 4: Create pytest script

Create a directory `tests` inside the project directory and inside it create a `pytest` script. I will use the name `test_myapp.py`. You can use any name, just keep in mind that by default `pytest` looks for Python files which name begins with `test`.

```python
def test_myapp_case1(dbr_client):
    result = dbr_client.execute('/Test-AssertEquals-DataFrames')
    assert result.was_successful == True
```

The defined function `test_myapp_case1` will be executed by `pytest` (note, the name begins with `test_`).

It takes one argument `dbr_client` which is a `pytest` fixture, provided by the `pytest-databricks` plugin.

Calling the `dbr_client.execute()` method (line 2) will execute the notebook with the specified name and return a result object, containing a lot of information. 

To check if the unittest execution finished successfully, you check the `was_successful` attribute (line 3). In case it is False, `pytest` assertion will fail and the test will be marked as failed.

### Step 5: Configure autosave for test output

Inside `tests` directory create a `conftest.py` file:

```python
import pytest
import os

@pytest.fixture(scope="session", autouse=True)
def _conftest(dbr_client):
    dir_results = os.path.join(os.path.dirname(__file__), '..', 'test-results')
    dbr_client.dir_auto_save = dir_results
    dbr_client.auto_save = True
```

This file will be automatically recognized by `pytest` as plugin. What it does is to enable autosave for all type of output from the unittest execution into `test-results` directory which is a sub-directory to the project directory.

### Execute pytest script

At the command line, at the project directory, execute:

```bash
pytest --databricks-token=<DATABRICKS_TOKEN> --databricks-cluster-id=<DATABRICKS_CLUSTER_ID>
```

This will execute the Databricks notebook, retrieve the result, validate notebook is executed OK and store all the output into the `test-results` directory.

You need to replace the `<DATABRICKS_TOKEN>` and the `<DATABRICKS_CLUSTER_ID>` with appropriate values. Alternatively you can define environment variables to specify these parameters, instead of using command line options:

* `DATABRICKS_BEARER_TOKEN`
* `DATABRICkS_CLUSTER_ID`

Here is an example output from the execution:

```
(.venv) C:\Sandbox\PoC\Databricks\pytest-databricks>pytest tests
============================ test session starts ============================ 
platform win32 -- Python 3.7.6rc1, pytest-5.4.3, py-1.9.0, pluggy-0.13.1      
rootdir: C:\Sandbox\PoC\Databricks\pytest-databricks, inifile: pytest.ini     
plugins: cov-2.10.0, databricks-0.0.8
collected 1 item                                                              

tests\test_basic.py .                                                  [100%] 

============================ 1 passed in 16.35s ============================= 
```

## What is inside the test-results directory?

Each notebook execution will create 4 files in this directory with the name:

```
TEST-<notebook-name>-<yyyymmddHHMMSSnnnnnn>(<run_id>).<extension>
```

Here is the meaning of each element:

* `<notebook-name>` - the name of the notebook, executed, without path

* `<yyyymmddHHMMSSnnnnnn>` - timestamp of the execution including 6-digit milliseconds.

* `<run_id>` - Databricks run ID. Can be used to get information about the run:

  * Using Databricks jobs API

  * Using `pydbr` command line utility:

    ```
    pydbr runs get-output 74 -i 2
    ```

  * Open the run page in a browser, typically in a format like:

    ```
    https://westeurope.azuredatabricks.net/?o=<organization>#job/<run_id>/run/1
    ```

Example:

```
TEST-Test-AssertEquals-DataFrames-20200729170234746326(74).html
TEST-Test-AssertEquals-DataFrames-20200729170234746326(74).json
TEST-Test-AssertEquals-DataFrames-20200729170234746326(74).txt
TEST-Test-AssertEquals-DataFrames-20200729170234746326(74).xml
```

