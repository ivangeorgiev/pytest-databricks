import os
from pytest_databricks.pytest.client import DatabricksTestClient

def test_dummy(dbr_connection):
    print("This is a basic test")
    result = dbr_connection.dbfs.ls('/')
    assert isinstance(result, list)

def test_TestClient_execute(dbr_connection):
    dbr_client = DatabricksTestClient(dbr_connection)
    dir_results = os.path.join(os.path.dirname(__file__), '..', 'test-results')
    dbr_client.dir_auto_save = dir_results
    dbr_client.auto_save = True
    # dbr_client.dir_xml_reports = dir_results # os.path.join(dir_results, 'xml-reports')
    # dbr_client.dir_run_outputs = dir_results # os.path.join(dir_results, 'outputs')
    # dbr_client.dir_notebook_outputs = dir_results # os.path.join(dir_results, 'outputs')
    # dbr_client.dir_exit_results = dir_results # os.path.join(dir_results, 'outputs')
    # dbr_client.auto_save_xml_report = True
    # dbr_client.auto_save_notebook_output = True
    # dbr_client.auto_save_run_output = True
    # dbr_client.auto_save_exit_result = True
    result = dbr_client.execute('/pytest-databricks-fixtures/Test_Something')
    assert result.was_successful == True
