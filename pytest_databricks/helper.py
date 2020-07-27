import subprocess
import sys
import io
import datetime
import unittest

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def run_unittest_suite(suite):
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
