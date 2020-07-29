# pytest-databricks
Pytest plugin for testing Databricks notebooks

To help you getting started, I have created a [Getting Started](docs/getting-started.md) page.

## Helpers

* `run_unittest_suite` - execute unittest TestSuite , capture XML report and testing report and return a dictionary with results, suitable for `dbr_client` fixture.
* `run_unittest_testcase` - creates a TestSuite from a unittest TestCase and calls `run_unittest_suite`
* `run_unittest` - convenience method which calls `run_unittest_suite` or `run_unittest_testcase` based on the type of the argument.



## Fixtures

* `dbr_client`
* `dbr_connection`



### Command line and ini options for pytest

Following command line options are added to pytest:

* `--env-databricks-token`
* `--env-databricks-url`
* `--env-databricks-cluster-id`
* `--databricks-token`
* `--databricks-url`
* `--databricks-cluster-id`

Same options are added also to `pytest.ini`


## Release Notes

### 0.0.9 (in progress)

* added [Getting Started](docs/getting-started.md) page

### 0.0.8

- fixed typo

### 0.0.7
- dbr_connection fixture raises exception of token, url or cluster id not specified
- added run_unittest and run_unittest_testcase helpers
- new test client auto_save and dir_auto_save properties
