import subprocess
import sys
import io
import datetime
import unittest
import inspect

def install_package(package):
    """Install Python package with pip executed in subprocess."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def run_unittest_suite(suite):
    """Execute unittest suite and return run output."""
    try:
        import xmlrunner
    except ModuleNotFoundError:
        install_package('unittest-xml-reporting')
        import xmlrunner
    with io.StringIO() as stream_fh:
        with io.BytesIO() as report_fh:
            runner = xmlrunner.XMLTestRunner(output=report_fh, stream=stream_fh, verbosity=2)
            start_time = datetime.datetime.utcnow()
            run_result = runner.run(suite)
            end_time = datetime.datetime.utcnow()
            output_content = stream_fh.getvalue()
            report_content = report_fh.getvalue().decode()
    
    result = {
        'was_successful': run_result.wasSuccessful(),
        'num_errors': len(run_result.errors),
        'num_failures': len(run_result.failures),
        'num_skipped': len(run_result.skipped),
        'num_successes': len(run_result.successes),
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'execution_time': end_time.timestamp() - start_time.timestamp(),
        'run_output': output_content,
        'xml_report': report_content,
    }
    return result


def run_unittest_testcase(test_case:unittest.TestCase):
    """Execute unittest TestCase and return run output."""
    assert inspect.isclass(test_case), "test_case must be a class"
    assert issubclass(test_case, unittest.TestCase), "test_case must be unittest.TestCase"
    suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
    return run_unittest_suite(suite)

def run_unittest(test):
    """Execute unittest TestCase or TestSuite and return run output"""
    if isinstance(test, unittest.TestSuite):
        return run_unittest_suite(test)
    elif inspect.isclass(test) and issubclass(test, unittest.TestCase):
        return run_unittest_testcase(test)
    else:
        raise TypeError("test must be unittest TestCase or TestSuite")

