# pymtstestlib

This is a Python porting of the WINAPI C MTSTestLib library.
The entry points API are kept identical where possible.
Same approach with documentation.

## Installation

```bash
pip install .
```

## Usage
See the unittests in tests/test_api.py for details.

```python
from pymtstestlib import api

result = api.CommOpen("/dev/ttyUSB0", 9600)
```

## Running Tests

```bash
python -m unittest discover
```

to run a single test (for example GetCnfStr):

```bash
python -m unittest tests.test_api.TestAPI.test_GetCnfStr
```

## Simulator

It is possible to launch the tests communicating on a network socket with a mock server (see test_api.py)
Configure
```python
COM="localhost:5000"
```

and run 
```bash
cd simulator
python simulator.py
```

This is in early stage of development; can't help debugging the serial communication itself, but helps simulating different boards responses without having access to the actual phisical hardware.

