
Intro 
-----

This folder stores all unit tests for this Flask application.

Note: pytest is used to run the tests

| File           | Description |
--------------------------------
| .coverage      | Configuration file for the test coverage tool (fab test_cov) |
| conftest.py    | Stores module level test fixtures for pytest |
| test_*.py      | Unit test files (must use the "test_" prefix) |


Install
-------

The command line tool is named 'py.test' (with a dot)

<pre>
pip install pytest
</pre>


Usage
-----

<pre>

cd app
py.test -s tests/ 
py.test -s  --cov redidropper  --cov-config tests/.coveragerc  --cov-report term-missing  tests/

</pre>
