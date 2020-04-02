import struct
from dataclasses import dataclass
from typing import Tuple, Union, Optional
from pathlib import Path

import olefile

from toolz import pipe, curry
from toolz.curried import partition
from multipledispatch import dispatch

@curry
def unpack(format: str, data: bytes):
    return struct.unpack(format, data[:struct.calcsize(format)])

unpack_data_info = unpack('<LLLLLLddd')

@dataclass(frozen=True)
class Header:
    a: int
    b: int
    c: int
    channels: int
    e: int
    N: int
    start_x: float
    end_x: float
    increment: float

@dataclass(frozen=True)
class Jws:
    ole: olefile.OleFileIO
    header: Header
    ydata: bytes
    y: Tuple[float]
    xdata: bytes
    x: Tuple[float]

    @classmethod
    def from_path(cls, path):
        return cls.from_bytes(Path(path).read_bytes())
    
    @classmethod
    def from_bytes(cls, data: bytes):
        ole = olefile.OleFileIO(data)
        header = get_header(ole)
        ydata = get_ydata(ole, header)
        yvalues = get_yvalues(ole, ydata, header)
        xdata = get_xdata(ole, header)
        xvalues = get_xvalues(ole, xdata, header)
        return cls(ole, header, ydata, yvalues, xdata, xvalues)

    @property
    def columns(self):
        return ('x',) + tuple(f'y{i}' for i in range(self.header.channels))

    def to_rows(self):
        return tuple(zip(self.x, *self.y))
        
def get_header(ole: olefile.OleFileIO) -> Header:
    data_info = ole.openstream('DataInfo').read()
    return Header(*unpack_data_info(data_info))
    
def get_ydata(ole: olefile.OleFileIO, header: Header) -> Optional[bytes]:
    return ole.openstream('Y-Data').read()

def get_yvalues(ole: olefile.OleFileIO, ydata: tuple,
                header: tuple) -> tuple:
    return pipe(
        unpack('f' * header.N * header.channels, ydata) if ydata else (),
        partition(header.N),
        tuple,
    )

def get_xdata(ole: olefile.OleFileIO, header: Header) -> Optional[bytes]:
    return ole.openstream('X-Data').read() if ole.exists('X-Data') else None

def get_xvalues_from_header(xdata: tuple, header: Header):
    x = header.start_x
    while x <= header.end_x:
        yield x
        x += header.increment
        
def get_xvalues(ole: olefile.OleFileIO, xdata: tuple,
                header: Header) -> tuple:
    if xdata:
        return unpack('f' * header.N, xdata)
    return tuple(get_xvalues_from_header(xdata, header))

@dispatch(bytes)
def load_jws(data):
    return Jws.from_bytes(data)
    
@dispatch((str, Path))          # noqa
def load_jws(path) -> Jws:
    return Jws.from_path(path)
