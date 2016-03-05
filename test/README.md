# About
This is the UnitTest section of the project

# Conventions
There are some conventions to be followed.

1. All files here start with the prefix `test_` that match the name of the file whose classes need to be tested.
2. All unittest methods must start with the string `test_` to be recognized by the unittest class.

# Running Tests
You can run all tests by executing the `_do_all_tests.py` script with the `--directory` flag pointing to this directory. For example:

```
$ _do_all_tests.py --directory /path/to/these/unittests
```

# Mocks
Many of these unittests use Python Mocks. A detailed tutorial on Mocks can be found here: http://www.drdobbs.com/testing/using-mocks-in-python/240168251
