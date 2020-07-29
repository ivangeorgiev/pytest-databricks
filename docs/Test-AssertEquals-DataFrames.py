# Databricks notebook source
# Install latest pytest-databricks package
# ============================================
# You can also install the package, using Databricks tools.
#
import sys
import subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "pytest-databricks"])

# COMMAND ----------

import unittest
from pytest_databricks.helper import run_unittest

# COMMAND ----------

class TestAssertEqualsForDataFrames(unittest.TestCase):
  """Python unittest TestCase to demonstrate DataSet how to assert two DataFrames are equal."""
    
  def list_to_data_frame(self, items):
    from pyspark.sql import Row
    row_factory = Row('id')
    return spark.createDataFrame([row_factory(i) for i in items])

  def test_assert_dataframes_are_notequal(self):
    df1 = self.list_to_data_frame([1,2,3,4])
    df2 = self.list_to_data_frame([1,2,3,4])
    self.assertNotEqual(df1, df2)
    
  def test_assert_unsorted_collected_dataframes_are_notequal(self):
    df1 = self.list_to_data_frame([1,2,3,4])
    df2 = self.list_to_data_frame([3,2,1,4])
    self.assertNotEqual(df1.collect(), df2.collect())
    
  def test_assert_sorted_collected_dataframes_are_equal(self):
    df1 = self.list_to_data_frame([1,2,3,4])
    df2 = self.list_to_data_frame([3,2,1,4])
    self.assertEqual(df1.orderBy('id').collect(), df2.orderBy('id').collect())

# COMMAND ----------

test_result = run_unittest(TestAssertEqualsForDataFrames)
print(test_result['run_output'])

# COMMAND ----------

# Exit the notebook and return result as JSON
import json
dbutils.notebook.exit(json.dumps(test_result))

# COMMAND ----------


