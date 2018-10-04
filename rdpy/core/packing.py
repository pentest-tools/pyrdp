#!/usr/bin/env python2
import struct

class Integer:
    @classmethod
    def unpack(cls, data):
        if isinstance(data, str):
            return struct.unpack(cls.FORMAT, data)[0]
        else:
            length = {"b": 1, "h": 2, "i": 4}[cls.FORMAT[1].lower()]
            return struct.unpack(cls.FORMAT, data.read(length))[0]

    @classmethod
    def pack(cls, data):
        return struct.pack(cls.FORMAT, data)

# 8 bits
class Int8(Integer):
    FORMAT = "<b"

class Uint8(Integer):
    FORMAT = "<B"

# 16 bits
class Int16LE(Integer):
    FORMAT = "<h"

class Int16BE(Integer):
    FORMAT = ">h"

class Uint16LE(Integer):
    FORMAT = "<H"

class Uint16BE(Integer):
    FORMAT = ">H"

# 32 bits
class Int32LE(Integer):
    FORMAT = "<i"

class Int32BE(Integer):
    FORMAT = ">i"

class Uint32LE(Integer):
    FORMAT = "<I"

class Uint32BE(Integer):
    FORMAT = ">I"