import subprocess
import zlib
from pympower.common.session import MSESSION
from pympower.common.statuscode import StatusCode
from pympower.common.global_val import global_val
from pympower.classes.mbase import *
import pympower_ext._mcrypt as _mcrypt
global_val = global_val.load_global_val();

if global_val.MOCOCRYPTO_DLL:
    _mcrypt.load_mococrypto(os.path.normpath(global_val.MOCOCRYPTO_DLL))

class MEncryptor:
    def __init__(self, encMode:int, zipMode:int, MRK:str):
        if 0 == encMode:
            self.encryptor = None
        else:
            try:
                self.encryptor = _mcrypt._MCrypt(1, encMode, bytes(MRK, encoding='ascii'), False)
            except Exception as e:
                raise MpowerException(
                    f'failed to create encryptor. encMode:{encMode}, zipMode:{zipMode}',
                    StatusCode.ERR_ENCRYPT.value, -1,  StatusCode.ERR_ENCRYPT.name,
                    ', '.join(str(arg) for arg in e.args)
                )

        if 0 == zipMode:
            self.compressor = None
        elif 3 == zipMode:
            self.compressor = zlib.compressobj(wbits=zlib.MAX_WBITS + 16)
        else:
            raise MpowerException(
                f'mpower encrypt zip mode error. zipMode: {zipMode}',
                StatusCode.ERR_ENCRYPT.value, -1,  StatusCode.ERR_ENCRYPT.name
            )

    def update(self, data:bytes) -> bytes:
        if None != self.compressor:
            data = self.compressor.compress(data)
        if None != self.encryptor:
            data = self.encryptor.update(data)
        return data

    def final(self) -> bytes:
        data = b''
        if None != self.compressor:
            data = self.compressor.flush()
        if None != self.encryptor:
            if data:
                data = self.encryptor.update(data)
            data += self.encryptor.final()
        return data

class MDecryptor:
    def __init__(self, encMode:int, zipMode:int, MRK:str):
        if 0 == encMode:
            self.decryptor = None
        else:
            try:
                self.decryptor = _mcrypt._MCrypt(2, encMode, bytes(MRK, encoding='ascii'), False)
            except Exception as e:
                raise MpowerException(
                    f'failed to create decryptor. encMode:{encMode}, zipMode:{zipMode}',
                    StatusCode.ERR_ENCRYPT.value, -1,  StatusCode.ERR_ENCRYPT.name,
                    ', '.join(str(arg) for arg in e.args)
                )

        if 0 == zipMode:
            self.decompressor = None
        elif 3 == zipMode:
            self.decompressor = zlib.decompressobj(wbits=zlib.MAX_WBITS + 32)
        else:
            raise MpowerException(
                f'mpower encrypt zip mode error. zipMode: {zipMode}',
                StatusCode.ERR_ENCRYPT.value, -1,  StatusCode.ERR_ENCRYPT.name
            )

    def update(self, data:bytes) -> bytes:
        if None != self.decryptor:
            data = self.decryptor.update(data)
        if None != self.decompressor:
            if data:
                data = self.decompressor.decompress(data)
        return data

    def final(self) -> bytes:
        data = b''
        if None != self.decryptor:
            data = self.decryptor.final()
        if None != self.decompressor:
            if data:
                data = self.decompressor.decompress(data)
            data += self.decompressor.flush()
            if False == self.decompressor.eof:
                raise MpowerException(
                    'mpower decrypt decompression error', 
                    StatusCode.ERR_DECRYPT.value, -1, StatusCode.ERR_DECRYPT.name
                )
        return data

class MCrypt(MBase):
    def __init__(self, powerdb_con:MpowerDB2=None):
        super().__init__(powerdb_con)

    def close(self):
        pass

    def mpowerDecrypt(self, srcPath:str, tgtPath:str, encMode:int, zipMode:int, MRK:str, lFileSize:int = -1):
        decryptor = MDecryptor(encMode, zipMode, MRK)
        lFileSizeToCheck = 0
        with open(srcPath, 'rb') as src:
            with open(tgtPath, 'wb') as tgt:
                while True:
                    data = src.read(4096)
                    if data:
                        data = decryptor.update(data)
                        lFileSizeToCheck += len(data)
                        tgt.write(data)
                    else:
                        data = decryptor.final()
                        tgt.write(data)
                        lFileSizeToCheck += len(data)
                        break

        if -1 != lFileSize:
            if lFileSizeToCheck != lFileSize:
                os.remove(tgtPath)
                raise MpowerException(
                        'mpower decrypt size error. src:%s, tgt:%s, size:%d, expected:%d' \
                            % (srcPath, tgtPath, lFileSizeToCheck, lFileSize), 
                        StatusCode.ERR_DECRYPT.value, -1, 
                        StatusCode.ERR_DECRYPT.name)

    def mpowerEncrypt(self, srcPath:str, tgtPath:str, encMode:int, zipMode:int, MRK:str):
        try:
            encryptor = _mcrypt._MCrypt(1, encMode, MRK, False)
        except Exception as e:
            raise MpowerException(
                'failed to create encryptor. src:%s, tgt:%s, encMode: %d' \
                    % (srcPath, tgtPath, encMode), 
                StatusCode.ERR_ENCRYPT.value, -1, 
                StatusCode.ERR_ENCRYPT.name,
                ', '.join(str(arg) for arg in e.args)
            )

        if 0 == zipMode:
            compressor = None
        elif 3 == zipMode:
            compressor = zlib.compressobj(wbits=zlib.MAX_WBITS + 16)
        else:
            raise MpowerException(
                'mpower encrypt zip mode error. src:%s, tgt:%s, zipMode: %d' \
                    % (srcPath, tgtPath, zipMode), 
                StatusCode.ERR_ENCRYPT.value, -1, 
                StatusCode.ERR_ENCRYPT.name)

        with open(srcPath, 'rb') as src:
            with open(tgtPath, 'wb') as tgt:
                while True:
                    data = src.read(4096)
                    if data:
                        if None != compressor:
                            data = compressor.compress(data)
                        data = encryptor.update(data)
                        tgt.write(data)
                    else:
                        if None != compressor:
                            data += compressor.flush()
                        if data:
                            data = encryptor.update(data)
                        data += encryptor.final()
                        tgt.write(data)
                        break
