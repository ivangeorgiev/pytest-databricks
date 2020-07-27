import os
import pytest
import pydbr
from .client import DatabricksTestClient


def pytest_addoption(parser):
    """pytest hook to initialize plugin options."""
    parser.addoption("--env-databricks-token",
                     help="Environment varialbe with Databricks bearer token.")
    parser.addoption("--env-databricks-url", 
                     help="Environment varialbe with Databricks URL.")
    parser.addoption("--env-databricks-cluster-id",
                     help="Environment varialbe with Databricks cluster id.")

    parser.addini('env-databricks-token',
                  help="Environment varialbe with Databricks bearer token.")
    parser.addini('env-databricks-url', 
                  help="Environment varialbe with Databricks URL.")
    parser.addini('env-databricks-cluster-id',
                  help="Environment varialbe with Databricks cluster id.")

    parser.addoption("--databricks-token", help="Databricks bearer token.")
    parser.addoption("--databricks-url",  help="Databricks URL.")
    parser.addoption("--databricks-cluster-id", help="Databricks cluster id.")

    parser.addini("databricks-token", help="Databricks bearer token.")
    parser.addini("databricks-url", help="Databricks URL.")
    parser.addini("databricks-cluster-id", help="Databricks cluster id.")


@pytest.fixture(scope="session")
def dbr_connection(pytestconfig):
    """Databricks connection fixture."""
    ENV_VAR_TOKEN = (pytestconfig.getoption('--env-databricks-token') or
                     pytestconfig.getini('env-databricks-token') or
                     'DATABRICKS_BEARER_TOKEN')
    ENV_VAR_URL = (pytestconfig.getoption('--env-databricks-url') or 
                   pytestconfig.getini('env-databricks-url') or
                   'DATABRICKS_URL')
    ENV_VAR_CLUSTER_ID = (pytestconfig.getoption('--env-databricks-cluster-id') or
                          pytestconfig.getini('env-databricks-cluster-id') or
                          'DATABRICkS_CLUSTER_ID')

    databricks_url = (pytestconfig.getoption('--databricks-url') or 
                      pytestconfig.getini('databricks-url') or 
                      os.environ.get(ENV_VAR_URL, None))
    databricks_token = (pytestconfig.getoption('--databricks-token') or 
                        pytestconfig.getini('databricks-token') or 
                        os.environ.get(ENV_VAR_TOKEN, None))
    databricks_cluster_id = (pytestconfig.getoption('--databricks-cluster-id') or 
                             pytestconfig.getini('databricks-cluster-id') or 
                             os.environ.get(ENV_VAR_CLUSTER_ID, None))
    
    connection = pydbr.connect(
        bearer_token=databricks_token,
        url=databricks_url,
        cluster_id=databricks_cluster_id)
    yield connection

@pytest.fixture(scope="session")
def dbr_client(dbr_connection):
    client = DatabricksTestClient(dbr_connection)
    yield client
