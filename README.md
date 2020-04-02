# jascobin

Parsers for Jasco binary data.

Currently only `*.jws` files.

## Requirements

- Python3.7+ only (uses `dataclass`)

## Installation

```
pip install jascobin
```

## Usage

```python
import jascobin

jws = jascobin.load_jws('spectral.jws')

# OleFileIO object of file data
print(jws.ole)

# Header data 
print(jws.header)

# X/Y data
print(jws.x)
print(jws.y)
```

## Caveats

Currently, `jascobin` is only capable of the following:

- Parsing `*.jws` files
- Parsing a few things from `*.jws` files:
    - X/Y data (with multiple channels)
    - What little of the `DataInfo` metadata I've reverse-engineered
