
import datetime
import dataclasses
import os
import json
import pydbr


@dataclasses.dataclass
class TestExecutionResult:
    pydbr_output: pydbr.databricks_data_classes.DatabricksRunOutput = None
    run_id: int = None
    run_page_url: str = None
    num_errors: int = None
    num_failures: int = None
    num_skipped: int = None
    num_successes: int = None
    start_time: str = None
    end_time: str = None
    execution_time: float = None
    was_successful: bool = None
    xml_report: str = None
    run_output: str = None
    exit_result: str = None

    @property
    def notebook_name(self):
        return self.pydbr_output.metadata.notebook_name

    @property
    def run_name(self):
        return self.pydbr_output.metadata.run_name

    @classmethod
    def from_run_output(cls, output: pydbr.databricks_data_classes.DatabricksRunOutput):
        test_result = json.loads(output.notebook_output.result)
        obj = cls(**test_result)
        obj.pydbr_output = output
        obj.run_id = output.metadata.run_id
        obj.run_page_url = output.metadata.run_page_url
        obj.exit_result = output.notebook_output.result
        return obj


class DatabricksTestClient:

    auto_save_xml_report = False
    auto_save_run_output = False
    auto_save_notebook_output = False
    auto_save_exit_result = False

    dir_xml_reports = '.'
    dir_run_outputs = '.'
    dir_notebook_outputs = '.'
    dir_exit_results = '.'

    last_run_result: TestExecutionResult = None

    def __init__(self, dbc):
        self._dbc = dbc

    @property
    def dbc(self):
        return self._dbc

    def log(self, message):
        print(message)
        
    def _write_report(self):
        if self.auto_save_xml_report:
            self._write_xml_report()
        if self.auto_save_notebook_output:
            self._write_notebook_output()
        if self.auto_save_run_output:
            self._write_run_output()
        if self.auto_save_exit_result:
            self._write_exit_result()

    def execute(self, path, run_name_prefix=None) -> TestExecutionResult:
        """Execute test notebook and return execution result."""

        now_ts = datetime.datetime.utcnow().strftime(r'%Y%m%d%H%M%S%f')
        notebook_name = path.split('/')[-1]
        run_name_prefix = run_name_prefix or f'TEST-{notebook_name}-'
        run_name = f'{run_name_prefix}{now_ts}'
        run_id = self.dbc.jobs.runs.submit_notebook(path, run_name=run_name)
        self.log(f'Submitted {path}: {run_name}({run_id})')
        self.dbc.jobs.runs.wait(run_id)
        run_output = self.dbc.jobs.runs.get_output(run_id)
        result = TestExecutionResult.from_run_output(run_output)
        self.log(f'Finished {run_name}({run_id}). Run page url: {result.run_page_url}')
        self.log(result.run_output)
        self.last_run_result = result
        self._write_report()
        return result

    def _make_report_filename(self, prefix='', suffix=''):
        run = self.last_run_result
        filename = f'{prefix}{run.run_name}({run.run_id}){suffix}'
        return filename

    def _write_result(self, content, dir, ext):
        file_name = self._make_report_filename() + ext
        file_path = os.path.join(dir, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as fh:
            fh.write(content)

    def _write_xml_report(self):
        assert self.last_run_result is not None, "last_run_result is not set. Nothing to save."
        content = self.last_run_result.xml_report
        self._write_result(content, self.dir_xml_reports, '.xml')

    def _write_run_output(self):
        assert self.last_run_result is not None, "last_run_result is not set. Nothing to save."
        content = self.last_run_result.run_output
        self._write_result(content, self.dir_run_outputs, '.txt')

    def _write_notebook_output(self):
        assert self.last_run_result is not None, "last_run_result is not set. Nothing to save."
        content = self.dbc.jobs.runs.export(self.last_run_result.run_id).notebooks[0].content
        self._write_result(content, self.dir_notebook_outputs, '.html')

    def _write_exit_result(self):
        assert self.last_run_result is not None, "last_run_result is not set. Nothing to save."
        content = self.last_run_result.exit_result
        content = json.dumps(dataclasses.asdict(self.last_run_result), indent=3)
        self._write_result(content, self.dir_exit_results, '.json')
