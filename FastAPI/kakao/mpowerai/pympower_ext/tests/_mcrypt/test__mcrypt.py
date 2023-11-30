import os
import unittest

from pympower_ext._mcrypt import _MCrypt, load_mococrypto

if 'nt' == os.name:
	load_mococrypto(r'MocoCrypto64.dll')
else:
	load_mococrypto(r'MocoCrypto.so')

class _TestData:
	def __init__(self, enc_mode:int, lfile:bytes, rfile:bytes, mrk:bytes, key_bits:int, key_bytes:int, block_bits:int, block_bytes:int, mode:int, padding_type:int, random_access:bool, partial_final:bool):
		data_dir = os.path.dirname(__file__)

		self.enc_mode = enc_mode
		with open(os.path.join(data_dir, lfile), 'rb') as f: self.lfile = f.read()
		with open(os.path.join(data_dir, rfile), 'rb') as f: self.rfile = f.read()
		with open(os.path.join(data_dir, mrk), 'rb') as f: self.mrk = f.read()
		self.key_bits = key_bits
		self.key_bytes = key_bytes
		self.block_bits = block_bits
		self.block_bytes = block_bytes
		self.mode = mode
		self.padding_type = padding_type
		self.random_access = random_access
		self.partial_final = partial_final

class _TestDataSet:
	dataset = [
		_TestData(enc_mode=1, lfile='LFILE.TXT', rfile='F_1_SEED_128_CBC.SMF', mrk='F_1_SEED_128_CBC.MRK', key_bits=128, key_bytes=16, block_bits=128, block_bytes=16, mode=2, padding_type=2, random_access=False, partial_final=False),
		_TestData(enc_mode=2, lfile='LFILE.TXT', rfile='F_2_SEED_128_ECB.SMF', mrk='F_2_SEED_128_ECB.MRK', key_bits=128, key_bytes=16, block_bits=128, block_bytes=16, mode=1, padding_type=2, random_access=True, partial_final=False),
		_TestData(enc_mode=3, lfile='LFILE.TXT', rfile='F_3_SEED_128_CTR.SMF', mrk='F_3_SEED_128_CTR.MRK', key_bits=128, key_bytes=16, block_bits=128, block_bytes=16, mode=5, padding_type=2, random_access=True, partial_final=True),
		_TestData(enc_mode=4, lfile='LFILE.TXT', rfile='F_4_ARIA_128_CBC.SMF', mrk='F_4_ARIA_128_CBC.MRK', key_bits=128, key_bytes=16, block_bits=128, block_bytes=16, mode=2, padding_type=2, random_access=False, partial_final=False),
		_TestData(enc_mode=5, lfile='LFILE.TXT', rfile='F_5_ARIA_128_CTR.SMF', mrk='F_5_ARIA_128_CTR.MRK', key_bits=128, key_bytes=16, block_bits=128, block_bytes=16, mode=5, padding_type=2, random_access=True, partial_final=True),
		_TestData(enc_mode=6, lfile='LFILE.TXT', rfile='F_6_ARIA_192_CBC.SMF', mrk='F_6_ARIA_192_CBC.MRK', key_bits=192, key_bytes=24, block_bits=128, block_bytes=16, mode=2, padding_type=2, random_access=False, partial_final=False),
		_TestData(enc_mode=7, lfile='LFILE.TXT', rfile='F_7_ARIA_192_CTR.SMF', mrk='F_7_ARIA_192_CTR.MRK', key_bits=192, key_bytes=24, block_bits=128, block_bytes=16, mode=5, padding_type=2, random_access=True, partial_final=True),
		_TestData(enc_mode=8, lfile='LFILE.TXT', rfile='F_8_ARIA_256_CBC.SMF', mrk='F_8_ARIA_256_CBC.MRK', key_bits=256, key_bytes=32, block_bits=128, block_bytes=16, mode=2, padding_type=2, random_access=False, partial_final=False),
		_TestData(enc_mode=9, lfile='LFILE.TXT', rfile='F_9_ARIA_256_CTR.SMF', mrk='F_9_ARIA_256_CTR.MRK', key_bits=256, key_bytes=32, block_bits=128, block_bytes=16, mode=5, padding_type=2, random_access=True, partial_final=True),
		_TestData(enc_mode=11, lfile='LFILE.TXT', rfile='F_11_SEED_128_CBC.SMF', mrk='F_11_SEED_128_CBC.MRK', key_bits=128, key_bytes=16, block_bits=128, block_bytes=16, mode=2, padding_type=2, random_access=False, partial_final=False),
		_TestData(enc_mode=13, lfile='LFILE.TXT', rfile='F_13_SEED_128_CTR.SMF', mrk='F_13_SEED_128_CTR.MRK', key_bits=128, key_bytes=16, block_bits=128, block_bytes=16, mode=5, padding_type=2, random_access=True, partial_final=True),
		_TestData(enc_mode=18, lfile='LFILE.TXT', rfile='F_18_ARIA_256_CBC.SMF', mrk='F_18_ARIA_256_CBC.MRK', key_bits=256, key_bytes=32, block_bits=128, block_bytes=16, mode=2, padding_type=2, random_access=False, partial_final=False),
		_TestData(enc_mode=19, lfile='LFILE.TXT', rfile='F_19_ARIA_256_CTR.SMF', mrk='F_19_ARIA_256_CTR.MRK', key_bits=256, key_bytes=32, block_bits=128, block_bytes=16, mode=5, padding_type=2, random_access=True, partial_final=True),
	]

	def get_data(enc_mode:int) -> _TestData:
		for data in _TestDataSet.dataset:
			if data.enc_mode == enc_mode:
				return data
		raise Exception(f'test data not found: enc_mode={enc_mode}')

class _Test_MCryptTestBase(unittest.TestCase):
	def _test_forward(self, crypt:_MCrypt, data:_TestData, src_text:bytes, dst_text:bytes, chunk_size:int):
		self.assertFalse(crypt.finished)
		self.assertEqual(crypt.enc_mode, data.enc_mode)
		self.assertEqual(crypt.key_bits, data.key_bits)
		self.assertEqual(crypt.key_bytes, data.key_bytes)
		self.assertEqual(crypt.block_bits, data.block_bits)
		self.assertEqual(crypt.block_bytes, data.block_bytes)
		self.assertEqual(crypt.mode, data.mode)
		self.assertEqual(crypt.padding_type, data.padding_type)
		self.assertEqual(crypt.random_access, data.random_access)
		encrypted_text = b''
		for i in range(0, len(src_text), chunk_size):
			chunk = src_text[i:i+chunk_size]
			encrypted_text += crypt.update(chunk)
			self.assertFalse(crypt.finished)
		encrypted_text += crypt.final()
		if data.random_access:
			self.assertFalse(crypt.finished)
		else:
			self.assertTrue(crypt.finished)
		self.assertEqual(encrypted_text, dst_text)

	def _test_enc_forward(self, data:_TestData, chunk_size:int):
		crypt = _MCrypt(1, data.enc_mode, data.mrk, data.random_access)
		self.assertEqual(crypt.enc_or_dec, 1)
		self._test_forward(crypt, data, data.lfile, data.rfile, chunk_size)

	def _test_dec_forward(self, data:_TestData, chunk_size:int):
		crypt = _MCrypt(2, data.enc_mode, data.mrk, data.random_access)
		self.assertEqual(crypt.enc_or_dec, 2)
		self._test_forward(crypt, data, data.rfile, data.lfile, chunk_size)

	def _test_forward_ctr(self, crypt:_MCrypt, data:_TestData, src_text:bytes, dst_text:bytes, chunk_size:int):
		'''
		CTR 모드의 counter를 설정하며 순차 암/복호화 테스트
		'''
		self.assertFalse(crypt.finished)
		self.assertEqual(crypt.enc_mode, data.enc_mode)
		self.assertEqual(crypt.key_bits, data.key_bits)
		self.assertEqual(crypt.key_bytes, data.key_bytes)
		self.assertEqual(crypt.block_bits, data.block_bits)
		self.assertEqual(crypt.block_bytes, data.block_bytes)
		self.assertEqual(crypt.mode, data.mode)
		self.assertEqual(crypt.padding_type, data.padding_type)
		self.assertEqual(crypt.random_access, data.random_access)
		encrypted_text = b''
		for i in range(0, len(src_text), chunk_size):
			counter = int(i / data.block_bytes)
			if data.random_access:
				crypt.set_counter(counter)
				self.assertEqual(crypt.get_counter(), counter)
			else:
				with self.assertRaises(Exception):
					crypt.set_counter(counter)
				return
			chunk = src_text[counter * data.block_bytes:i+chunk_size]
			encrypted_chunk = crypt.update(chunk)
			encrypted_chunk += crypt.final()
			self.assertFalse(crypt.finished)
			encrypted_chunk = encrypted_chunk[i - counter * data.block_bytes:]
			encrypted_text += encrypted_chunk
		self.assertEqual(encrypted_text, dst_text)

	def _test_enc_forward_ctr(self, data:_TestData, chunk_size:int):
		crypt = _MCrypt(1, data.enc_mode, data.mrk, data.random_access)
		self.assertEqual(crypt.enc_or_dec, 1)
		self._test_forward_ctr(crypt, data, data.lfile, data.rfile, chunk_size)

	def _test_dec_forward_ctr(self, data:_TestData, chunk_size:int):
		crypt = _MCrypt(2, data.enc_mode, data.mrk, data.random_access)
		self.assertEqual(crypt.enc_or_dec, 2)
		self._test_forward_ctr(crypt, data, data.rfile, data.lfile, chunk_size)

	def _test_ctr_rev(self, crypt:_MCrypt, data:_TestData, src_text:bytes, dst_text:bytes, block_bytes:int, chunk_size:int):
		'''
		CTR 모드의 counter를 설정하며 역순 암/복호화 테스트
		'''
		self.assertFalse(crypt.finished)
		self.assertEqual(crypt.enc_mode, data.enc_mode)
		self.assertEqual(crypt.key_bits, data.key_bits)
		self.assertEqual(crypt.key_bytes, data.key_bytes)
		self.assertEqual(crypt.block_bits, data.block_bits)
		self.assertEqual(crypt.block_bytes, data.block_bytes)
		self.assertEqual(crypt.mode, data.mode)
		self.assertEqual(crypt.padding_type, data.padding_type)
		self.assertEqual(crypt.random_access, data.random_access)
		encrypted_text = b''
		for i in reversed(list(range(0, len(src_text), chunk_size))):
			counter = int(i / block_bytes)
			if data.random_access:
				crypt.set_counter(counter)
				self.assertEqual(crypt.get_counter(), counter)
			else:
				with self.assertRaises(Exception):
					crypt.set_counter(counter)
				return
			chunk = src_text[counter * block_bytes:i+chunk_size]
			encrypted_chunk = crypt.update(chunk)
			encrypted_chunk += crypt.final()
			encrypted_chunk = encrypted_chunk[i - counter * block_bytes:]
			encrypted_text = encrypted_chunk + encrypted_text
		self.assertEqual(encrypted_text, dst_text)

	def _test_enc_backward_ctr(self, data:_TestData, chunk_size:int):
		crypt = _MCrypt(1, data.enc_mode, data.mrk, data.random_access)
		self.assertEqual(crypt.enc_or_dec, 1)
		self._test_ctr_rev(crypt, data, data.lfile, data.rfile, data.block_bytes, chunk_size)

	def _test_dec_backward_ctr(self, data:_TestData, chunk_size:int):
		crypt = _MCrypt(2, data.enc_mode, data.mrk, data.random_access)
		self.assertEqual(crypt.enc_or_dec, 2)
		self._test_ctr_rev(crypt, data, data.rfile, data.lfile, data.block_bytes, chunk_size)

class _Test_MCryptTestCaseBase(_Test_MCryptTestBase):
	def _test_enc_forward_01(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward(data, 1)

	def _test_enc_forward_02(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward(data, data.block_bytes - 1)

	def _test_enc_forward_03(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward(data, data.block_bytes)

	def _test_enc_forward_04(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward(data, data.block_bytes + 1)

	def _test_enc_forward_05(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward(data, data.block_bytes * 2 - 1)

	def _test_enc_forward_06(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward(data, data.block_bytes * 2 + 1)

	def _test_enc_forward_07(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward(data, data.block_bytes * 2 + 1)

	def _test_enc_forward_08(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward(data, len(data.lfile) - 1)

	def _test_enc_forward_09(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward(data, len(data.lfile))

	def _test_enc_forward_10(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward(data, len(data.lfile) + 1)

	def _test_dec_forward_01(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward(data, 1)

	def _test_dec_forward_02(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward(data, data.block_bytes - 1)

	def _test_dec_forward_03(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward(data, data.block_bytes)

	def _test_dec_forward_04(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward(data, data.block_bytes + 1)

	def _test_dec_forward_05(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward(data, data.block_bytes * 2 - 1)

	def _test_dec_forward_06(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward(data, data.block_bytes * 2 + 1)

	def _test_dec_forward_07(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward(data, data.block_bytes * 2 + 1)

	def _test_dec_forward_08(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward(data, len(data.lfile) - 1)

	def _test_dec_forward_09(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward(data, len(data.lfile))

	def _test_dec_forward_10(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward(data, len(data.lfile) + 1)

	def _test_enc_forward_ctr_01(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward_ctr(data, 1)

	def _test_enc_forward_ctr_02(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward_ctr(data, data.block_bytes - 1)

	def _test_enc_forward_ctr_03(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward_ctr(data, data.block_bytes)

	def _test_enc_forward_ctr_04(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward_ctr(data, data.block_bytes + 1)

	def _test_enc_forward_ctr_05(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward_ctr(data, data.block_bytes * 2 - 1)

	def _test_enc_forward_ctr_06(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward_ctr(data, data.block_bytes * 2 + 1)

	def _test_enc_forward_ctr_07(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward_ctr(data, data.block_bytes * 2 + 1)

	def _test_enc_forward_ctr_08(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward_ctr(data, len(data.lfile) - 1)

	def _test_enc_forward_ctr_09(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward_ctr(data, len(data.lfile))

	def _test_enc_forward_ctr_10(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_forward_ctr(data, len(data.lfile) + 1)

	def _test_dec_forward_ctr_01(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward_ctr(data, 1)

	def _test_dec_forward_ctr_02(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward_ctr(data, data.block_bytes - 1)

	def _test_dec_forward_ctr_03(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward_ctr(data, data.block_bytes)

	def _test_dec_forward_ctr_04(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward_ctr(data, data.block_bytes + 1)

	def _test_dec_forward_ctr_05(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward_ctr(data, data.block_bytes * 2 - 1)

	def _test_dec_forward_ctr_06(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward_ctr(data, data.block_bytes * 2 + 1)

	def _test_dec_forward_ctr_07(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward_ctr(data, data.block_bytes * 2 + 1)

	def _test_dec_forward_ctr_08(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward_ctr(data, len(data.lfile) - 1)

	def _test_dec_forward_ctr_09(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward_ctr(data, len(data.lfile))

	def _test_dec_forward_ctr_10(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_forward_ctr(data, len(data.lfile) + 1)

	def _test_enc_backward_ctr_01(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_backward_ctr(data, 1)

	def _test_enc_backward_ctr_02(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_backward_ctr(data, data.block_bytes - 1)

	def _test_enc_backward_ctr_03(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_backward_ctr(data, data.block_bytes)

	def _test_enc_backward_ctr_04(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_backward_ctr(data, data.block_bytes + 1)

	def _test_enc_backward_ctr_05(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_backward_ctr(data, data.block_bytes * 2 - 1)

	def _test_enc_backward_ctr_06(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_backward_ctr(data, data.block_bytes * 2 + 1)

	def _test_enc_backward_ctr_07(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_backward_ctr(data, data.block_bytes * 2 + 1)

	def _test_enc_backward_ctr_08(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_backward_ctr(data, len(data.lfile) - 1)

	def _test_enc_backward_ctr_09(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_backward_ctr(data, len(data.lfile))

	def _test_enc_backward_ctr_10(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_enc_backward_ctr(data, len(data.lfile) + 1)

	def _test_dec_backward_ctr_01(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_backward_ctr(data, 1)

	def _test_dec_backward_ctr_02(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_backward_ctr(data, data.block_bytes - 1)

	def _test_dec_backward_ctr_03(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_backward_ctr(data, data.block_bytes)

	def _test_dec_backward_ctr_04(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_backward_ctr(data, data.block_bytes + 1)

	def _test_dec_backward_ctr_05(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_backward_ctr(data, data.block_bytes * 2 - 1)

	def _test_dec_backward_ctr_06(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_backward_ctr(data, data.block_bytes * 2 + 1)

	def _test_dec_backward_ctr_07(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_backward_ctr(data, data.block_bytes * 2 + 1)

	def _test_dec_backward_ctr_08(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_backward_ctr(data, len(data.lfile) - 1)

	def _test_dec_backward_ctr_09(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_backward_ctr(data, len(data.lfile))

	def _test_dec_backward_ctr_10(self, enc_mode):
		data = _TestDataSet.get_data(enc_mode)
		self._test_dec_backward_ctr(data, len(data.lfile) + 1)

class Test_01_KISA_SEED_128_CBC(_Test_MCryptTestCaseBase):
	def setUp(self) -> None:
		self.enc_mode = 1

	def test_enc_forward_01(self):
		self._test_enc_forward_01(self.enc_mode)
	
	def test_enc_forward_02(self):
		self._test_enc_forward_02(self.enc_mode)

	def test_enc_forward_03(self):
		self._test_enc_forward_03(self.enc_mode)

	def test_enc_forward_04(self):
		self._test_enc_forward_04(self.enc_mode)

	def test_enc_forward_05(self):
		self._test_enc_forward_05(self.enc_mode)

	def test_enc_forward_06(self):
		self._test_enc_forward_06(self.enc_mode)

	def test_enc_forward_07(self):
		self._test_enc_forward_07(self.enc_mode)

	def test_enc_forward_08(self):
		self._test_enc_forward_08(self.enc_mode)

	def test_enc_forward_09(self):
		self._test_enc_forward_09(self.enc_mode)

	def test_enc_forward_10(self):
		self._test_enc_forward_10(self.enc_mode)

	def test_dec_forward_01(self):
		self._test_dec_forward_01(self.enc_mode)
	
	def test_dec_forward_02(self):
		self._test_dec_forward_02(self.enc_mode)

	def test_dec_forward_03(self):
		self._test_dec_forward_03(self.enc_mode)

	def test_dec_forward_04(self):
		self._test_dec_forward_04(self.enc_mode)

	def test_dec_forward_05(self):
		self._test_dec_forward_05(self.enc_mode)

	def test_dec_forward_06(self):
		self._test_dec_forward_06(self.enc_mode)

	def test_dec_forward_07(self):
		self._test_dec_forward_07(self.enc_mode)

	def test_dec_forward_08(self):
		self._test_dec_forward_08(self.enc_mode)

	def test_dec_forward_09(self):
		self._test_dec_forward_09(self.enc_mode)

	def test_dec_forward_10(self):
		self._test_dec_forward_10(self.enc_mode)

	def test_enc_forward_ctr_01(self):
		self._test_enc_forward_ctr_01(self.enc_mode)

	def test_enc_forward_ctr_02(self):
		self._test_enc_forward_ctr_02(self.enc_mode)

	def test_enc_forward_ctr_03(self):
		self._test_enc_forward_ctr_03(self.enc_mode)

	def test_enc_forward_ctr_04(self):
		self._test_enc_forward_ctr_04(self.enc_mode)

	def test_enc_forward_ctr_05(self):
		self._test_enc_forward_ctr_05(self.enc_mode)

	def test_enc_forward_ctr_06(self):
		self._test_enc_forward_ctr_06(self.enc_mode)

	def test_enc_forward_ctr_07(self):
		self._test_enc_forward_ctr_07(self.enc_mode)

	def test_enc_forward_ctr_08(self):
		self._test_enc_forward_ctr_08(self.enc_mode)

	def test_enc_forward_ctr_09(self):
		self._test_enc_forward_ctr_09(self.enc_mode)

	def test_enc_forward_ctr_10(self):
		self._test_enc_forward_ctr_10(self.enc_mode)

	def test_dec_forward_ctr_01(self):
		self._test_dec_forward_ctr_01(self.enc_mode)

	def test_dec_forward_ctr_02(self):
		self._test_dec_forward_ctr_02(self.enc_mode)

	def test_dec_forward_ctr_03(self):
		self._test_dec_forward_ctr_03(self.enc_mode)

	def test_dec_forward_ctr_04(self):
		self._test_dec_forward_ctr_04(self.enc_mode)

	def test_dec_forward_ctr_05(self):
		self._test_dec_forward_ctr_05(self.enc_mode)

	def test_dec_forward_ctr_06(self):
		self._test_dec_forward_ctr_06(self.enc_mode)

	def test_dec_forward_ctr_07(self):
		self._test_dec_forward_ctr_07(self.enc_mode)

	def test_dec_forward_ctr_08(self):
		self._test_dec_forward_ctr_08(self.enc_mode)

	def test_dec_forward_ctr_09(self):
		self._test_dec_forward_ctr_09(self.enc_mode)

	def test_dec_forward_ctr_10(self):
		self._test_dec_forward_ctr_10(self.enc_mode)

	def test_enc_backward_ctr_01(self):
		self._test_enc_backward_ctr_01(self.enc_mode)

	def test_enc_backward_ctr_02(self):
		self._test_enc_backward_ctr_02(self.enc_mode)

	def test_enc_backward_ctr_03(self):
		self._test_enc_backward_ctr_03(self.enc_mode)

	def test_enc_backward_ctr_04(self):
		self._test_enc_backward_ctr_04(self.enc_mode)

	def test_enc_backward_ctr_05(self):
		self._test_enc_backward_ctr_05(self.enc_mode)

	def test_enc_backward_ctr_06(self):
		self._test_enc_backward_ctr_06(self.enc_mode)

	def test_enc_backward_ctr_07(self):
		self._test_enc_backward_ctr_07(self.enc_mode)

	def test_enc_backward_ctr_08(self):
		self._test_enc_backward_ctr_08(self.enc_mode)

	def test_enc_backward_ctr_09(self):
		self._test_enc_backward_ctr_09(self.enc_mode)

	def test_enc_backward_ctr_10(self):
		self._test_enc_backward_ctr_10(self.enc_mode)

	def test_dec_backward_ctr_01(self):
		self._test_dec_backward_ctr_01(self.enc_mode)

	def test_dec_backward_ctr_02(self):
		self._test_dec_backward_ctr_02(self.enc_mode)

	def test_dec_backward_ctr_03(self):
		self._test_dec_backward_ctr_03(self.enc_mode)

	def test_dec_backward_ctr_04(self):
		self._test_dec_backward_ctr_04(self.enc_mode)

	def test_dec_backward_ctr_05(self):
		self._test_dec_backward_ctr_05(self.enc_mode)

	def test_dec_backward_ctr_06(self):
		self._test_dec_backward_ctr_06(self.enc_mode)

	def test_dec_backward_ctr_07(self):
		self._test_dec_backward_ctr_07(self.enc_mode)

	def test_dec_backward_ctr_08(self):
		self._test_dec_backward_ctr_08(self.enc_mode)

	def test_dec_backward_ctr_09(self):
		self._test_dec_backward_ctr_09(self.enc_mode)

	def test_dec_backward_ctr_10(self):
		self._test_dec_backward_ctr_10(self.enc_mode)

class Test_02_KISA_SEED_128_ECB(_Test_MCryptTestCaseBase):
	def setUp(self) -> None:
		self.enc_mode = 2

	def test_enc_forward_01(self):
		self._test_enc_forward_01(self.enc_mode)
	
	def test_enc_forward_02(self):
		self._test_enc_forward_02(self.enc_mode)

	def test_enc_forward_03(self):
		self._test_enc_forward_03(self.enc_mode)

	def test_enc_forward_04(self):
		self._test_enc_forward_04(self.enc_mode)

	def test_enc_forward_05(self):
		self._test_enc_forward_05(self.enc_mode)

	def test_enc_forward_06(self):
		self._test_enc_forward_06(self.enc_mode)

	def test_enc_forward_07(self):
		self._test_enc_forward_07(self.enc_mode)

	def test_enc_forward_08(self):
		self._test_enc_forward_08(self.enc_mode)

	def test_enc_forward_09(self):
		self._test_enc_forward_09(self.enc_mode)

	def test_enc_forward_10(self):
		self._test_enc_forward_10(self.enc_mode)

	def test_dec_forward_01(self):
		self._test_dec_forward_01(self.enc_mode)
	
	def test_dec_forward_02(self):
		self._test_dec_forward_02(self.enc_mode)

	def test_dec_forward_03(self):
		self._test_dec_forward_03(self.enc_mode)

	def test_dec_forward_04(self):
		self._test_dec_forward_04(self.enc_mode)

	def test_dec_forward_05(self):
		self._test_dec_forward_05(self.enc_mode)

	def test_dec_forward_06(self):
		self._test_dec_forward_06(self.enc_mode)

	def test_dec_forward_07(self):
		self._test_dec_forward_07(self.enc_mode)

	def test_dec_forward_08(self):
		self._test_dec_forward_08(self.enc_mode)

	def test_dec_forward_09(self):
		self._test_dec_forward_09(self.enc_mode)

	def test_dec_forward_10(self):
		self._test_dec_forward_10(self.enc_mode)

	# TODO: Random Access관련 Test Case 만들 것

class Test_03_KISA_SEED_128_CTR(_Test_MCryptTestCaseBase):
	def setUp(self) -> None:
		self.enc_mode = 3

	def test_enc_forward_01(self):
		self._test_enc_forward_01(self.enc_mode)
	
	def test_enc_forward_02(self):
		self._test_enc_forward_02(self.enc_mode)

	def test_enc_forward_03(self):
		self._test_enc_forward_03(self.enc_mode)

	def test_enc_forward_04(self):
		self._test_enc_forward_04(self.enc_mode)

	def test_enc_forward_05(self):
		self._test_enc_forward_05(self.enc_mode)

	def test_enc_forward_06(self):
		self._test_enc_forward_06(self.enc_mode)

	def test_enc_forward_07(self):
		self._test_enc_forward_07(self.enc_mode)

	def test_enc_forward_08(self):
		self._test_enc_forward_08(self.enc_mode)

	def test_enc_forward_09(self):
		self._test_enc_forward_09(self.enc_mode)

	def test_enc_forward_10(self):
		self._test_enc_forward_10(self.enc_mode)

	def test_dec_forward_01(self):
		self._test_dec_forward_01(self.enc_mode)
	
	def test_dec_forward_02(self):
		self._test_dec_forward_02(self.enc_mode)

	def test_dec_forward_03(self):
		self._test_dec_forward_03(self.enc_mode)

	def test_dec_forward_04(self):
		self._test_dec_forward_04(self.enc_mode)

	def test_dec_forward_05(self):
		self._test_dec_forward_05(self.enc_mode)

	def test_dec_forward_06(self):
		self._test_dec_forward_06(self.enc_mode)

	def test_dec_forward_07(self):
		self._test_dec_forward_07(self.enc_mode)

	def test_dec_forward_08(self):
		self._test_dec_forward_08(self.enc_mode)

	def test_dec_forward_09(self):
		self._test_dec_forward_09(self.enc_mode)

	def test_dec_forward_10(self):
		self._test_dec_forward_10(self.enc_mode)

	def test_enc_forward_ctr_01(self):
		self._test_enc_forward_ctr_01(self.enc_mode)

	def test_enc_forward_ctr_02(self):
		self._test_enc_forward_ctr_02(self.enc_mode)

	def test_enc_forward_ctr_03(self):
		self._test_enc_forward_ctr_03(self.enc_mode)

	def test_enc_forward_ctr_04(self):
		self._test_enc_forward_ctr_04(self.enc_mode)

	def test_enc_forward_ctr_05(self):
		self._test_enc_forward_ctr_05(self.enc_mode)

	def test_enc_forward_ctr_06(self):
		self._test_enc_forward_ctr_06(self.enc_mode)

	def test_enc_forward_ctr_07(self):
		self._test_enc_forward_ctr_07(self.enc_mode)

	def test_enc_forward_ctr_08(self):
		self._test_enc_forward_ctr_08(self.enc_mode)

	def test_enc_forward_ctr_09(self):
		self._test_enc_forward_ctr_09(self.enc_mode)

	def test_enc_forward_ctr_10(self):
		self._test_enc_forward_ctr_10(self.enc_mode)

	def test_dec_forward_ctr_01(self):
		self._test_dec_forward_ctr_01(self.enc_mode)

	def test_dec_forward_ctr_02(self):
		self._test_dec_forward_ctr_02(self.enc_mode)

	def test_dec_forward_ctr_03(self):
		self._test_dec_forward_ctr_03(self.enc_mode)

	def test_dec_forward_ctr_04(self):
		self._test_dec_forward_ctr_04(self.enc_mode)

	def test_dec_forward_ctr_05(self):
		self._test_dec_forward_ctr_05(self.enc_mode)

	def test_dec_forward_ctr_06(self):
		self._test_dec_forward_ctr_06(self.enc_mode)

	def test_dec_forward_ctr_07(self):
		self._test_dec_forward_ctr_07(self.enc_mode)

	def test_dec_forward_ctr_08(self):
		self._test_dec_forward_ctr_08(self.enc_mode)

	def test_dec_forward_ctr_09(self):
		self._test_dec_forward_ctr_09(self.enc_mode)

	def test_dec_forward_ctr_10(self):
		self._test_dec_forward_ctr_10(self.enc_mode)

	def test_enc_backward_ctr_01(self):
		self._test_enc_backward_ctr_01(self.enc_mode)

	def test_enc_backward_ctr_02(self):
		self._test_enc_backward_ctr_02(self.enc_mode)

	def test_enc_backward_ctr_03(self):
		self._test_enc_backward_ctr_03(self.enc_mode)

	def test_enc_backward_ctr_04(self):
		self._test_enc_backward_ctr_04(self.enc_mode)

	def test_enc_backward_ctr_05(self):
		self._test_enc_backward_ctr_05(self.enc_mode)

	def test_enc_backward_ctr_06(self):
		self._test_enc_backward_ctr_06(self.enc_mode)

	def test_enc_backward_ctr_07(self):
		self._test_enc_backward_ctr_07(self.enc_mode)

	def test_enc_backward_ctr_08(self):
		self._test_enc_backward_ctr_08(self.enc_mode)

	def test_enc_backward_ctr_09(self):
		self._test_enc_backward_ctr_09(self.enc_mode)

	def test_enc_backward_ctr_10(self):
		self._test_enc_backward_ctr_10(self.enc_mode)

	def test_dec_backward_ctr_01(self):
		self._test_dec_backward_ctr_01(self.enc_mode)

	def test_dec_backward_ctr_02(self):
		self._test_dec_backward_ctr_02(self.enc_mode)

	def test_dec_backward_ctr_03(self):
		self._test_dec_backward_ctr_03(self.enc_mode)

	def test_dec_backward_ctr_04(self):
		self._test_dec_backward_ctr_04(self.enc_mode)

	def test_dec_backward_ctr_05(self):
		self._test_dec_backward_ctr_05(self.enc_mode)

	def test_dec_backward_ctr_06(self):
		self._test_dec_backward_ctr_06(self.enc_mode)

	def test_dec_backward_ctr_07(self):
		self._test_dec_backward_ctr_07(self.enc_mode)

	def test_dec_backward_ctr_08(self):
		self._test_dec_backward_ctr_08(self.enc_mode)

	def test_dec_backward_ctr_09(self):
		self._test_dec_backward_ctr_09(self.enc_mode)

	def test_dec_backward_ctr_10(self):
		self._test_dec_backward_ctr_10(self.enc_mode)

class Test_04_KISA_ARIA_128_CBC(_Test_MCryptTestCaseBase):
	def setUp(self) -> None:
		self.enc_mode = 4

	def test_enc_forward_01(self):
		self._test_enc_forward_01(self.enc_mode)
	
	def test_enc_forward_02(self):
		self._test_enc_forward_02(self.enc_mode)

	def test_enc_forward_03(self):
		self._test_enc_forward_03(self.enc_mode)

	def test_enc_forward_04(self):
		self._test_enc_forward_04(self.enc_mode)

	def test_enc_forward_05(self):
		self._test_enc_forward_05(self.enc_mode)

	def test_enc_forward_06(self):
		self._test_enc_forward_06(self.enc_mode)

	def test_enc_forward_07(self):
		self._test_enc_forward_07(self.enc_mode)

	def test_enc_forward_08(self):
		self._test_enc_forward_08(self.enc_mode)

	def test_enc_forward_09(self):
		self._test_enc_forward_09(self.enc_mode)

	def test_enc_forward_10(self):
		self._test_enc_forward_10(self.enc_mode)

	def test_dec_forward_01(self):
		self._test_dec_forward_01(self.enc_mode)
	
	def test_dec_forward_02(self):
		self._test_dec_forward_02(self.enc_mode)

	def test_dec_forward_03(self):
		self._test_dec_forward_03(self.enc_mode)

	def test_dec_forward_04(self):
		self._test_dec_forward_04(self.enc_mode)

	def test_dec_forward_05(self):
		self._test_dec_forward_05(self.enc_mode)

	def test_dec_forward_06(self):
		self._test_dec_forward_06(self.enc_mode)

	def test_dec_forward_07(self):
		self._test_dec_forward_07(self.enc_mode)

	def test_dec_forward_08(self):
		self._test_dec_forward_08(self.enc_mode)

	def test_dec_forward_09(self):
		self._test_dec_forward_09(self.enc_mode)

	def test_dec_forward_10(self):
		self._test_dec_forward_10(self.enc_mode)

	def test_enc_forward_ctr_01(self):
		self._test_enc_forward_ctr_01(self.enc_mode)

	def test_enc_forward_ctr_02(self):
		self._test_enc_forward_ctr_02(self.enc_mode)

	def test_enc_forward_ctr_03(self):
		self._test_enc_forward_ctr_03(self.enc_mode)

	def test_enc_forward_ctr_04(self):
		self._test_enc_forward_ctr_04(self.enc_mode)

	def test_enc_forward_ctr_05(self):
		self._test_enc_forward_ctr_05(self.enc_mode)

	def test_enc_forward_ctr_06(self):
		self._test_enc_forward_ctr_06(self.enc_mode)

	def test_enc_forward_ctr_07(self):
		self._test_enc_forward_ctr_07(self.enc_mode)

	def test_enc_forward_ctr_08(self):
		self._test_enc_forward_ctr_08(self.enc_mode)

	def test_enc_forward_ctr_09(self):
		self._test_enc_forward_ctr_09(self.enc_mode)

	def test_enc_forward_ctr_10(self):
		self._test_enc_forward_ctr_10(self.enc_mode)

	def test_dec_forward_ctr_01(self):
		self._test_dec_forward_ctr_01(self.enc_mode)

	def test_dec_forward_ctr_02(self):
		self._test_dec_forward_ctr_02(self.enc_mode)

	def test_dec_forward_ctr_03(self):
		self._test_dec_forward_ctr_03(self.enc_mode)

	def test_dec_forward_ctr_04(self):
		self._test_dec_forward_ctr_04(self.enc_mode)

	def test_dec_forward_ctr_05(self):
		self._test_dec_forward_ctr_05(self.enc_mode)

	def test_dec_forward_ctr_06(self):
		self._test_dec_forward_ctr_06(self.enc_mode)

	def test_dec_forward_ctr_07(self):
		self._test_dec_forward_ctr_07(self.enc_mode)

	def test_dec_forward_ctr_08(self):
		self._test_dec_forward_ctr_08(self.enc_mode)

	def test_dec_forward_ctr_09(self):
		self._test_dec_forward_ctr_09(self.enc_mode)

	def test_dec_forward_ctr_10(self):
		self._test_dec_forward_ctr_10(self.enc_mode)

	def test_enc_backward_ctr_01(self):
		self._test_enc_backward_ctr_01(self.enc_mode)

	def test_enc_backward_ctr_02(self):
		self._test_enc_backward_ctr_02(self.enc_mode)

	def test_enc_backward_ctr_03(self):
		self._test_enc_backward_ctr_03(self.enc_mode)

	def test_enc_backward_ctr_04(self):
		self._test_enc_backward_ctr_04(self.enc_mode)

	def test_enc_backward_ctr_05(self):
		self._test_enc_backward_ctr_05(self.enc_mode)

	def test_enc_backward_ctr_06(self):
		self._test_enc_backward_ctr_06(self.enc_mode)

	def test_enc_backward_ctr_07(self):
		self._test_enc_backward_ctr_07(self.enc_mode)

	def test_enc_backward_ctr_08(self):
		self._test_enc_backward_ctr_08(self.enc_mode)

	def test_enc_backward_ctr_09(self):
		self._test_enc_backward_ctr_09(self.enc_mode)

	def test_enc_backward_ctr_10(self):
		self._test_enc_backward_ctr_10(self.enc_mode)

	def test_dec_backward_ctr_01(self):
		self._test_dec_backward_ctr_01(self.enc_mode)

	def test_dec_backward_ctr_02(self):
		self._test_dec_backward_ctr_02(self.enc_mode)

	def test_dec_backward_ctr_03(self):
		self._test_dec_backward_ctr_03(self.enc_mode)

	def test_dec_backward_ctr_04(self):
		self._test_dec_backward_ctr_04(self.enc_mode)

	def test_dec_backward_ctr_05(self):
		self._test_dec_backward_ctr_05(self.enc_mode)

	def test_dec_backward_ctr_06(self):
		self._test_dec_backward_ctr_06(self.enc_mode)

	def test_dec_backward_ctr_07(self):
		self._test_dec_backward_ctr_07(self.enc_mode)

	def test_dec_backward_ctr_08(self):
		self._test_dec_backward_ctr_08(self.enc_mode)

	def test_dec_backward_ctr_09(self):
		self._test_dec_backward_ctr_09(self.enc_mode)

	def test_dec_backward_ctr_10(self):
		self._test_dec_backward_ctr_10(self.enc_mode)

class Test_05_KISA_ARIA_128_CTR(_Test_MCryptTestCaseBase):
	def setUp(self) -> None:
		self.enc_mode = 5

	def test_enc_forward_01(self):
		self._test_enc_forward_01(self.enc_mode)
	
	def test_enc_forward_02(self):
		self._test_enc_forward_02(self.enc_mode)

	def test_enc_forward_03(self):
		self._test_enc_forward_03(self.enc_mode)

	def test_enc_forward_04(self):
		self._test_enc_forward_04(self.enc_mode)

	def test_enc_forward_05(self):
		self._test_enc_forward_05(self.enc_mode)

	def test_enc_forward_06(self):
		self._test_enc_forward_06(self.enc_mode)

	def test_enc_forward_07(self):
		self._test_enc_forward_07(self.enc_mode)

	def test_enc_forward_08(self):
		self._test_enc_forward_08(self.enc_mode)

	def test_enc_forward_09(self):
		self._test_enc_forward_09(self.enc_mode)

	def test_enc_forward_10(self):
		self._test_enc_forward_10(self.enc_mode)

	def test_dec_forward_01(self):
		self._test_dec_forward_01(self.enc_mode)
	
	def test_dec_forward_02(self):
		self._test_dec_forward_02(self.enc_mode)

	def test_dec_forward_03(self):
		self._test_dec_forward_03(self.enc_mode)

	def test_dec_forward_04(self):
		self._test_dec_forward_04(self.enc_mode)

	def test_dec_forward_05(self):
		self._test_dec_forward_05(self.enc_mode)

	def test_dec_forward_06(self):
		self._test_dec_forward_06(self.enc_mode)

	def test_dec_forward_07(self):
		self._test_dec_forward_07(self.enc_mode)

	def test_dec_forward_08(self):
		self._test_dec_forward_08(self.enc_mode)

	def test_dec_forward_09(self):
		self._test_dec_forward_09(self.enc_mode)

	def test_dec_forward_10(self):
		self._test_dec_forward_10(self.enc_mode)

	def test_enc_forward_ctr_01(self):
		self._test_enc_forward_ctr_01(self.enc_mode)

	def test_enc_forward_ctr_02(self):
		self._test_enc_forward_ctr_02(self.enc_mode)

	def test_enc_forward_ctr_03(self):
		self._test_enc_forward_ctr_03(self.enc_mode)

	def test_enc_forward_ctr_04(self):
		self._test_enc_forward_ctr_04(self.enc_mode)

	def test_enc_forward_ctr_05(self):
		self._test_enc_forward_ctr_05(self.enc_mode)

	def test_enc_forward_ctr_06(self):
		self._test_enc_forward_ctr_06(self.enc_mode)

	def test_enc_forward_ctr_07(self):
		self._test_enc_forward_ctr_07(self.enc_mode)

	def test_enc_forward_ctr_08(self):
		self._test_enc_forward_ctr_08(self.enc_mode)

	def test_enc_forward_ctr_09(self):
		self._test_enc_forward_ctr_09(self.enc_mode)

	def test_enc_forward_ctr_10(self):
		self._test_enc_forward_ctr_10(self.enc_mode)

	def test_dec_forward_ctr_01(self):
		self._test_dec_forward_ctr_01(self.enc_mode)

	def test_dec_forward_ctr_02(self):
		self._test_dec_forward_ctr_02(self.enc_mode)

	def test_dec_forward_ctr_03(self):
		self._test_dec_forward_ctr_03(self.enc_mode)

	def test_dec_forward_ctr_04(self):
		self._test_dec_forward_ctr_04(self.enc_mode)

	def test_dec_forward_ctr_05(self):
		self._test_dec_forward_ctr_05(self.enc_mode)

	def test_dec_forward_ctr_06(self):
		self._test_dec_forward_ctr_06(self.enc_mode)

	def test_dec_forward_ctr_07(self):
		self._test_dec_forward_ctr_07(self.enc_mode)

	def test_dec_forward_ctr_08(self):
		self._test_dec_forward_ctr_08(self.enc_mode)

	def test_dec_forward_ctr_09(self):
		self._test_dec_forward_ctr_09(self.enc_mode)

	def test_dec_forward_ctr_10(self):
		self._test_dec_forward_ctr_10(self.enc_mode)

	def test_enc_backward_ctr_01(self):
		self._test_enc_backward_ctr_01(self.enc_mode)

	def test_enc_backward_ctr_02(self):
		self._test_enc_backward_ctr_02(self.enc_mode)

	def test_enc_backward_ctr_03(self):
		self._test_enc_backward_ctr_03(self.enc_mode)

	def test_enc_backward_ctr_04(self):
		self._test_enc_backward_ctr_04(self.enc_mode)

	def test_enc_backward_ctr_05(self):
		self._test_enc_backward_ctr_05(self.enc_mode)

	def test_enc_backward_ctr_06(self):
		self._test_enc_backward_ctr_06(self.enc_mode)

	def test_enc_backward_ctr_07(self):
		self._test_enc_backward_ctr_07(self.enc_mode)

	def test_enc_backward_ctr_08(self):
		self._test_enc_backward_ctr_08(self.enc_mode)

	def test_enc_backward_ctr_09(self):
		self._test_enc_backward_ctr_09(self.enc_mode)

	def test_enc_backward_ctr_10(self):
		self._test_enc_backward_ctr_10(self.enc_mode)

	def test_dec_backward_ctr_01(self):
		self._test_dec_backward_ctr_01(self.enc_mode)

	def test_dec_backward_ctr_02(self):
		self._test_dec_backward_ctr_02(self.enc_mode)

	def test_dec_backward_ctr_03(self):
		self._test_dec_backward_ctr_03(self.enc_mode)

	def test_dec_backward_ctr_04(self):
		self._test_dec_backward_ctr_04(self.enc_mode)

	def test_dec_backward_ctr_05(self):
		self._test_dec_backward_ctr_05(self.enc_mode)

	def test_dec_backward_ctr_06(self):
		self._test_dec_backward_ctr_06(self.enc_mode)

	def test_dec_backward_ctr_07(self):
		self._test_dec_backward_ctr_07(self.enc_mode)

	def test_dec_backward_ctr_08(self):
		self._test_dec_backward_ctr_08(self.enc_mode)

	def test_dec_backward_ctr_09(self):
		self._test_dec_backward_ctr_09(self.enc_mode)

	def test_dec_backward_ctr_10(self):
		self._test_dec_backward_ctr_10(self.enc_mode)

class Test_06_KISA_ARIA_192_CBC(_Test_MCryptTestCaseBase):
	def setUp(self) -> None:
		self.enc_mode = 6

	def test_enc_forward_01(self):
		self._test_enc_forward_01(self.enc_mode)
	
	def test_enc_forward_02(self):
		self._test_enc_forward_02(self.enc_mode)

	def test_enc_forward_03(self):
		self._test_enc_forward_03(self.enc_mode)

	def test_enc_forward_04(self):
		self._test_enc_forward_04(self.enc_mode)

	def test_enc_forward_05(self):
		self._test_enc_forward_05(self.enc_mode)

	def test_enc_forward_06(self):
		self._test_enc_forward_06(self.enc_mode)

	def test_enc_forward_07(self):
		self._test_enc_forward_07(self.enc_mode)

	def test_enc_forward_08(self):
		self._test_enc_forward_08(self.enc_mode)

	def test_enc_forward_09(self):
		self._test_enc_forward_09(self.enc_mode)

	def test_enc_forward_10(self):
		self._test_enc_forward_10(self.enc_mode)

	def test_dec_forward_01(self):
		self._test_dec_forward_01(self.enc_mode)
	
	def test_dec_forward_02(self):
		self._test_dec_forward_02(self.enc_mode)

	def test_dec_forward_03(self):
		self._test_dec_forward_03(self.enc_mode)

	def test_dec_forward_04(self):
		self._test_dec_forward_04(self.enc_mode)

	def test_dec_forward_05(self):
		self._test_dec_forward_05(self.enc_mode)

	def test_dec_forward_06(self):
		self._test_dec_forward_06(self.enc_mode)

	def test_dec_forward_07(self):
		self._test_dec_forward_07(self.enc_mode)

	def test_dec_forward_08(self):
		self._test_dec_forward_08(self.enc_mode)

	def test_dec_forward_09(self):
		self._test_dec_forward_09(self.enc_mode)

	def test_dec_forward_10(self):
		self._test_dec_forward_10(self.enc_mode)

	def test_enc_forward_ctr_01(self):
		self._test_enc_forward_ctr_01(self.enc_mode)

	def test_enc_forward_ctr_02(self):
		self._test_enc_forward_ctr_02(self.enc_mode)

	def test_enc_forward_ctr_03(self):
		self._test_enc_forward_ctr_03(self.enc_mode)

	def test_enc_forward_ctr_04(self):
		self._test_enc_forward_ctr_04(self.enc_mode)

	def test_enc_forward_ctr_05(self):
		self._test_enc_forward_ctr_05(self.enc_mode)

	def test_enc_forward_ctr_06(self):
		self._test_enc_forward_ctr_06(self.enc_mode)

	def test_enc_forward_ctr_07(self):
		self._test_enc_forward_ctr_07(self.enc_mode)

	def test_enc_forward_ctr_08(self):
		self._test_enc_forward_ctr_08(self.enc_mode)

	def test_enc_forward_ctr_09(self):
		self._test_enc_forward_ctr_09(self.enc_mode)

	def test_enc_forward_ctr_10(self):
		self._test_enc_forward_ctr_10(self.enc_mode)

	def test_dec_forward_ctr_01(self):
		self._test_dec_forward_ctr_01(self.enc_mode)

	def test_dec_forward_ctr_02(self):
		self._test_dec_forward_ctr_02(self.enc_mode)

	def test_dec_forward_ctr_03(self):
		self._test_dec_forward_ctr_03(self.enc_mode)

	def test_dec_forward_ctr_04(self):
		self._test_dec_forward_ctr_04(self.enc_mode)

	def test_dec_forward_ctr_05(self):
		self._test_dec_forward_ctr_05(self.enc_mode)

	def test_dec_forward_ctr_06(self):
		self._test_dec_forward_ctr_06(self.enc_mode)

	def test_dec_forward_ctr_07(self):
		self._test_dec_forward_ctr_07(self.enc_mode)

	def test_dec_forward_ctr_08(self):
		self._test_dec_forward_ctr_08(self.enc_mode)

	def test_dec_forward_ctr_09(self):
		self._test_dec_forward_ctr_09(self.enc_mode)

	def test_dec_forward_ctr_10(self):
		self._test_dec_forward_ctr_10(self.enc_mode)

	def test_enc_backward_ctr_01(self):
		self._test_enc_backward_ctr_01(self.enc_mode)

	def test_enc_backward_ctr_02(self):
		self._test_enc_backward_ctr_02(self.enc_mode)

	def test_enc_backward_ctr_03(self):
		self._test_enc_backward_ctr_03(self.enc_mode)

	def test_enc_backward_ctr_04(self):
		self._test_enc_backward_ctr_04(self.enc_mode)

	def test_enc_backward_ctr_05(self):
		self._test_enc_backward_ctr_05(self.enc_mode)

	def test_enc_backward_ctr_06(self):
		self._test_enc_backward_ctr_06(self.enc_mode)

	def test_enc_backward_ctr_07(self):
		self._test_enc_backward_ctr_07(self.enc_mode)

	def test_enc_backward_ctr_08(self):
		self._test_enc_backward_ctr_08(self.enc_mode)

	def test_enc_backward_ctr_09(self):
		self._test_enc_backward_ctr_09(self.enc_mode)

	def test_enc_backward_ctr_10(self):
		self._test_enc_backward_ctr_10(self.enc_mode)

	def test_dec_backward_ctr_01(self):
		self._test_dec_backward_ctr_01(self.enc_mode)

	def test_dec_backward_ctr_02(self):
		self._test_dec_backward_ctr_02(self.enc_mode)

	def test_dec_backward_ctr_03(self):
		self._test_dec_backward_ctr_03(self.enc_mode)

	def test_dec_backward_ctr_04(self):
		self._test_dec_backward_ctr_04(self.enc_mode)

	def test_dec_backward_ctr_05(self):
		self._test_dec_backward_ctr_05(self.enc_mode)

	def test_dec_backward_ctr_06(self):
		self._test_dec_backward_ctr_06(self.enc_mode)

	def test_dec_backward_ctr_07(self):
		self._test_dec_backward_ctr_07(self.enc_mode)

	def test_dec_backward_ctr_08(self):
		self._test_dec_backward_ctr_08(self.enc_mode)

	def test_dec_backward_ctr_09(self):
		self._test_dec_backward_ctr_09(self.enc_mode)

	def test_dec_backward_ctr_10(self):
		self._test_dec_backward_ctr_10(self.enc_mode)

class Test_07_KISA_ARIA_192_CTR(_Test_MCryptTestCaseBase):
	def setUp(self) -> None:
		self.enc_mode = 7

	def test_enc_forward_01(self):
		self._test_enc_forward_01(self.enc_mode)
	
	def test_enc_forward_02(self):
		self._test_enc_forward_02(self.enc_mode)

	def test_enc_forward_03(self):
		self._test_enc_forward_03(self.enc_mode)

	def test_enc_forward_04(self):
		self._test_enc_forward_04(self.enc_mode)

	def test_enc_forward_05(self):
		self._test_enc_forward_05(self.enc_mode)

	def test_enc_forward_06(self):
		self._test_enc_forward_06(self.enc_mode)

	def test_enc_forward_07(self):
		self._test_enc_forward_07(self.enc_mode)

	def test_enc_forward_08(self):
		self._test_enc_forward_08(self.enc_mode)

	def test_enc_forward_09(self):
		self._test_enc_forward_09(self.enc_mode)

	def test_enc_forward_10(self):
		self._test_enc_forward_10(self.enc_mode)

	def test_dec_forward_01(self):
		self._test_dec_forward_01(self.enc_mode)
	
	def test_dec_forward_02(self):
		self._test_dec_forward_02(self.enc_mode)

	def test_dec_forward_03(self):
		self._test_dec_forward_03(self.enc_mode)

	def test_dec_forward_04(self):
		self._test_dec_forward_04(self.enc_mode)

	def test_dec_forward_05(self):
		self._test_dec_forward_05(self.enc_mode)

	def test_dec_forward_06(self):
		self._test_dec_forward_06(self.enc_mode)

	def test_dec_forward_07(self):
		self._test_dec_forward_07(self.enc_mode)

	def test_dec_forward_08(self):
		self._test_dec_forward_08(self.enc_mode)

	def test_dec_forward_09(self):
		self._test_dec_forward_09(self.enc_mode)

	def test_dec_forward_10(self):
		self._test_dec_forward_10(self.enc_mode)

	def test_enc_forward_ctr_01(self):
		self._test_enc_forward_ctr_01(self.enc_mode)

	def test_enc_forward_ctr_02(self):
		self._test_enc_forward_ctr_02(self.enc_mode)

	def test_enc_forward_ctr_03(self):
		self._test_enc_forward_ctr_03(self.enc_mode)

	def test_enc_forward_ctr_04(self):
		self._test_enc_forward_ctr_04(self.enc_mode)

	def test_enc_forward_ctr_05(self):
		self._test_enc_forward_ctr_05(self.enc_mode)

	def test_enc_forward_ctr_06(self):
		self._test_enc_forward_ctr_06(self.enc_mode)

	def test_enc_forward_ctr_07(self):
		self._test_enc_forward_ctr_07(self.enc_mode)

	def test_enc_forward_ctr_08(self):
		self._test_enc_forward_ctr_08(self.enc_mode)

	def test_enc_forward_ctr_09(self):
		self._test_enc_forward_ctr_09(self.enc_mode)

	def test_enc_forward_ctr_10(self):
		self._test_enc_forward_ctr_10(self.enc_mode)

	def test_dec_forward_ctr_01(self):
		self._test_dec_forward_ctr_01(self.enc_mode)

	def test_dec_forward_ctr_02(self):
		self._test_dec_forward_ctr_02(self.enc_mode)

	def test_dec_forward_ctr_03(self):
		self._test_dec_forward_ctr_03(self.enc_mode)

	def test_dec_forward_ctr_04(self):
		self._test_dec_forward_ctr_04(self.enc_mode)

	def test_dec_forward_ctr_05(self):
		self._test_dec_forward_ctr_05(self.enc_mode)

	def test_dec_forward_ctr_06(self):
		self._test_dec_forward_ctr_06(self.enc_mode)

	def test_dec_forward_ctr_07(self):
		self._test_dec_forward_ctr_07(self.enc_mode)

	def test_dec_forward_ctr_08(self):
		self._test_dec_forward_ctr_08(self.enc_mode)

	def test_dec_forward_ctr_09(self):
		self._test_dec_forward_ctr_09(self.enc_mode)

	def test_dec_forward_ctr_10(self):
		self._test_dec_forward_ctr_10(self.enc_mode)

	def test_enc_backward_ctr_01(self):
		self._test_enc_backward_ctr_01(self.enc_mode)

	def test_enc_backward_ctr_02(self):
		self._test_enc_backward_ctr_02(self.enc_mode)

	def test_enc_backward_ctr_03(self):
		self._test_enc_backward_ctr_03(self.enc_mode)

	def test_enc_backward_ctr_04(self):
		self._test_enc_backward_ctr_04(self.enc_mode)

	def test_enc_backward_ctr_05(self):
		self._test_enc_backward_ctr_05(self.enc_mode)

	def test_enc_backward_ctr_06(self):
		self._test_enc_backward_ctr_06(self.enc_mode)

	def test_enc_backward_ctr_07(self):
		self._test_enc_backward_ctr_07(self.enc_mode)

	def test_enc_backward_ctr_08(self):
		self._test_enc_backward_ctr_08(self.enc_mode)

	def test_enc_backward_ctr_09(self):
		self._test_enc_backward_ctr_09(self.enc_mode)

	def test_enc_backward_ctr_10(self):
		self._test_enc_backward_ctr_10(self.enc_mode)

	def test_dec_backward_ctr_01(self):
		self._test_dec_backward_ctr_01(self.enc_mode)

	def test_dec_backward_ctr_02(self):
		self._test_dec_backward_ctr_02(self.enc_mode)

	def test_dec_backward_ctr_03(self):
		self._test_dec_backward_ctr_03(self.enc_mode)

	def test_dec_backward_ctr_04(self):
		self._test_dec_backward_ctr_04(self.enc_mode)

	def test_dec_backward_ctr_05(self):
		self._test_dec_backward_ctr_05(self.enc_mode)

	def test_dec_backward_ctr_06(self):
		self._test_dec_backward_ctr_06(self.enc_mode)

	def test_dec_backward_ctr_07(self):
		self._test_dec_backward_ctr_07(self.enc_mode)

	def test_dec_backward_ctr_08(self):
		self._test_dec_backward_ctr_08(self.enc_mode)

	def test_dec_backward_ctr_09(self):
		self._test_dec_backward_ctr_09(self.enc_mode)

	def test_dec_backward_ctr_10(self):
		self._test_dec_backward_ctr_10(self.enc_mode)

class Test_08_KISA_ARIA_256_CBC(_Test_MCryptTestCaseBase):
	def setUp(self) -> None:
		self.enc_mode = 8

	def test_enc_forward_01(self):
		self._test_enc_forward_01(self.enc_mode)
	
	def test_enc_forward_02(self):
		self._test_enc_forward_02(self.enc_mode)

	def test_enc_forward_03(self):
		self._test_enc_forward_03(self.enc_mode)

	def test_enc_forward_04(self):
		self._test_enc_forward_04(self.enc_mode)

	def test_enc_forward_05(self):
		self._test_enc_forward_05(self.enc_mode)

	def test_enc_forward_06(self):
		self._test_enc_forward_06(self.enc_mode)

	def test_enc_forward_07(self):
		self._test_enc_forward_07(self.enc_mode)

	def test_enc_forward_08(self):
		self._test_enc_forward_08(self.enc_mode)

	def test_enc_forward_09(self):
		self._test_enc_forward_09(self.enc_mode)

	def test_enc_forward_10(self):
		self._test_enc_forward_10(self.enc_mode)

	def test_dec_forward_01(self):
		self._test_dec_forward_01(self.enc_mode)
	
	def test_dec_forward_02(self):
		self._test_dec_forward_02(self.enc_mode)

	def test_dec_forward_03(self):
		self._test_dec_forward_03(self.enc_mode)

	def test_dec_forward_04(self):
		self._test_dec_forward_04(self.enc_mode)

	def test_dec_forward_05(self):
		self._test_dec_forward_05(self.enc_mode)

	def test_dec_forward_06(self):
		self._test_dec_forward_06(self.enc_mode)

	def test_dec_forward_07(self):
		self._test_dec_forward_07(self.enc_mode)

	def test_dec_forward_08(self):
		self._test_dec_forward_08(self.enc_mode)

	def test_dec_forward_09(self):
		self._test_dec_forward_09(self.enc_mode)

	def test_dec_forward_10(self):
		self._test_dec_forward_10(self.enc_mode)

	def test_enc_forward_ctr_01(self):
		self._test_enc_forward_ctr_01(self.enc_mode)

	def test_enc_forward_ctr_02(self):
		self._test_enc_forward_ctr_02(self.enc_mode)

	def test_enc_forward_ctr_03(self):
		self._test_enc_forward_ctr_03(self.enc_mode)

	def test_enc_forward_ctr_04(self):
		self._test_enc_forward_ctr_04(self.enc_mode)

	def test_enc_forward_ctr_05(self):
		self._test_enc_forward_ctr_05(self.enc_mode)

	def test_enc_forward_ctr_06(self):
		self._test_enc_forward_ctr_06(self.enc_mode)

	def test_enc_forward_ctr_07(self):
		self._test_enc_forward_ctr_07(self.enc_mode)

	def test_enc_forward_ctr_08(self):
		self._test_enc_forward_ctr_08(self.enc_mode)

	def test_enc_forward_ctr_09(self):
		self._test_enc_forward_ctr_09(self.enc_mode)

	def test_enc_forward_ctr_10(self):
		self._test_enc_forward_ctr_10(self.enc_mode)

	def test_dec_forward_ctr_01(self):
		self._test_dec_forward_ctr_01(self.enc_mode)

	def test_dec_forward_ctr_02(self):
		self._test_dec_forward_ctr_02(self.enc_mode)

	def test_dec_forward_ctr_03(self):
		self._test_dec_forward_ctr_03(self.enc_mode)

	def test_dec_forward_ctr_04(self):
		self._test_dec_forward_ctr_04(self.enc_mode)

	def test_dec_forward_ctr_05(self):
		self._test_dec_forward_ctr_05(self.enc_mode)

	def test_dec_forward_ctr_06(self):
		self._test_dec_forward_ctr_06(self.enc_mode)

	def test_dec_forward_ctr_07(self):
		self._test_dec_forward_ctr_07(self.enc_mode)

	def test_dec_forward_ctr_08(self):
		self._test_dec_forward_ctr_08(self.enc_mode)

	def test_dec_forward_ctr_09(self):
		self._test_dec_forward_ctr_09(self.enc_mode)

	def test_dec_forward_ctr_10(self):
		self._test_dec_forward_ctr_10(self.enc_mode)

	def test_enc_backward_ctr_01(self):
		self._test_enc_backward_ctr_01(self.enc_mode)

	def test_enc_backward_ctr_02(self):
		self._test_enc_backward_ctr_02(self.enc_mode)

	def test_enc_backward_ctr_03(self):
		self._test_enc_backward_ctr_03(self.enc_mode)

	def test_enc_backward_ctr_04(self):
		self._test_enc_backward_ctr_04(self.enc_mode)

	def test_enc_backward_ctr_05(self):
		self._test_enc_backward_ctr_05(self.enc_mode)

	def test_enc_backward_ctr_06(self):
		self._test_enc_backward_ctr_06(self.enc_mode)

	def test_enc_backward_ctr_07(self):
		self._test_enc_backward_ctr_07(self.enc_mode)

	def test_enc_backward_ctr_08(self):
		self._test_enc_backward_ctr_08(self.enc_mode)

	def test_enc_backward_ctr_09(self):
		self._test_enc_backward_ctr_09(self.enc_mode)

	def test_enc_backward_ctr_10(self):
		self._test_enc_backward_ctr_10(self.enc_mode)

	def test_dec_backward_ctr_01(self):
		self._test_dec_backward_ctr_01(self.enc_mode)

	def test_dec_backward_ctr_02(self):
		self._test_dec_backward_ctr_02(self.enc_mode)

	def test_dec_backward_ctr_03(self):
		self._test_dec_backward_ctr_03(self.enc_mode)

	def test_dec_backward_ctr_04(self):
		self._test_dec_backward_ctr_04(self.enc_mode)

	def test_dec_backward_ctr_05(self):
		self._test_dec_backward_ctr_05(self.enc_mode)

	def test_dec_backward_ctr_06(self):
		self._test_dec_backward_ctr_06(self.enc_mode)

	def test_dec_backward_ctr_07(self):
		self._test_dec_backward_ctr_07(self.enc_mode)

	def test_dec_backward_ctr_08(self):
		self._test_dec_backward_ctr_08(self.enc_mode)

	def test_dec_backward_ctr_09(self):
		self._test_dec_backward_ctr_09(self.enc_mode)

	def test_dec_backward_ctr_10(self):
		self._test_dec_backward_ctr_10(self.enc_mode)

class Test_09_KISA_ARIA_256_CTR(_Test_MCryptTestCaseBase):
	def setUp(self) -> None:
		self.enc_mode = 9

	def test_enc_forward_01(self):
		self._test_enc_forward_01(self.enc_mode)
	
	def test_enc_forward_02(self):
		self._test_enc_forward_02(self.enc_mode)

	def test_enc_forward_03(self):
		self._test_enc_forward_03(self.enc_mode)

	def test_enc_forward_04(self):
		self._test_enc_forward_04(self.enc_mode)

	def test_enc_forward_05(self):
		self._test_enc_forward_05(self.enc_mode)

	def test_enc_forward_06(self):
		self._test_enc_forward_06(self.enc_mode)

	def test_enc_forward_07(self):
		self._test_enc_forward_07(self.enc_mode)

	def test_enc_forward_08(self):
		self._test_enc_forward_08(self.enc_mode)

	def test_enc_forward_09(self):
		self._test_enc_forward_09(self.enc_mode)

	def test_enc_forward_10(self):
		self._test_enc_forward_10(self.enc_mode)

	def test_dec_forward_01(self):
		self._test_dec_forward_01(self.enc_mode)
	
	def test_dec_forward_02(self):
		self._test_dec_forward_02(self.enc_mode)

	def test_dec_forward_03(self):
		self._test_dec_forward_03(self.enc_mode)

	def test_dec_forward_04(self):
		self._test_dec_forward_04(self.enc_mode)

	def test_dec_forward_05(self):
		self._test_dec_forward_05(self.enc_mode)

	def test_dec_forward_06(self):
		self._test_dec_forward_06(self.enc_mode)

	def test_dec_forward_07(self):
		self._test_dec_forward_07(self.enc_mode)

	def test_dec_forward_08(self):
		self._test_dec_forward_08(self.enc_mode)

	def test_dec_forward_09(self):
		self._test_dec_forward_09(self.enc_mode)

	def test_dec_forward_10(self):
		self._test_dec_forward_10(self.enc_mode)

	def test_enc_forward_ctr_01(self):
		self._test_enc_forward_ctr_01(self.enc_mode)

	def test_enc_forward_ctr_02(self):
		self._test_enc_forward_ctr_02(self.enc_mode)

	def test_enc_forward_ctr_03(self):
		self._test_enc_forward_ctr_03(self.enc_mode)

	def test_enc_forward_ctr_04(self):
		self._test_enc_forward_ctr_04(self.enc_mode)

	def test_enc_forward_ctr_05(self):
		self._test_enc_forward_ctr_05(self.enc_mode)

	def test_enc_forward_ctr_06(self):
		self._test_enc_forward_ctr_06(self.enc_mode)

	def test_enc_forward_ctr_07(self):
		self._test_enc_forward_ctr_07(self.enc_mode)

	def test_enc_forward_ctr_08(self):
		self._test_enc_forward_ctr_08(self.enc_mode)

	def test_enc_forward_ctr_09(self):
		self._test_enc_forward_ctr_09(self.enc_mode)

	def test_enc_forward_ctr_10(self):
		self._test_enc_forward_ctr_10(self.enc_mode)

	def test_dec_forward_ctr_01(self):
		self._test_dec_forward_ctr_01(self.enc_mode)

	def test_dec_forward_ctr_02(self):
		self._test_dec_forward_ctr_02(self.enc_mode)

	def test_dec_forward_ctr_03(self):
		self._test_dec_forward_ctr_03(self.enc_mode)

	def test_dec_forward_ctr_04(self):
		self._test_dec_forward_ctr_04(self.enc_mode)

	def test_dec_forward_ctr_05(self):
		self._test_dec_forward_ctr_05(self.enc_mode)

	def test_dec_forward_ctr_06(self):
		self._test_dec_forward_ctr_06(self.enc_mode)

	def test_dec_forward_ctr_07(self):
		self._test_dec_forward_ctr_07(self.enc_mode)

	def test_dec_forward_ctr_08(self):
		self._test_dec_forward_ctr_08(self.enc_mode)

	def test_dec_forward_ctr_09(self):
		self._test_dec_forward_ctr_09(self.enc_mode)

	def test_dec_forward_ctr_10(self):
		self._test_dec_forward_ctr_10(self.enc_mode)

	def test_enc_backward_ctr_01(self):
		self._test_enc_backward_ctr_01(self.enc_mode)

	def test_enc_backward_ctr_02(self):
		self._test_enc_backward_ctr_02(self.enc_mode)

	def test_enc_backward_ctr_03(self):
		self._test_enc_backward_ctr_03(self.enc_mode)

	def test_enc_backward_ctr_04(self):
		self._test_enc_backward_ctr_04(self.enc_mode)

	def test_enc_backward_ctr_05(self):
		self._test_enc_backward_ctr_05(self.enc_mode)

	def test_enc_backward_ctr_06(self):
		self._test_enc_backward_ctr_06(self.enc_mode)

	def test_enc_backward_ctr_07(self):
		self._test_enc_backward_ctr_07(self.enc_mode)

	def test_enc_backward_ctr_08(self):
		self._test_enc_backward_ctr_08(self.enc_mode)

	def test_enc_backward_ctr_09(self):
		self._test_enc_backward_ctr_09(self.enc_mode)

	def test_enc_backward_ctr_10(self):
		self._test_enc_backward_ctr_10(self.enc_mode)

	def test_dec_backward_ctr_01(self):
		self._test_dec_backward_ctr_01(self.enc_mode)

	def test_dec_backward_ctr_02(self):
		self._test_dec_backward_ctr_02(self.enc_mode)

	def test_dec_backward_ctr_03(self):
		self._test_dec_backward_ctr_03(self.enc_mode)

	def test_dec_backward_ctr_04(self):
		self._test_dec_backward_ctr_04(self.enc_mode)

	def test_dec_backward_ctr_05(self):
		self._test_dec_backward_ctr_05(self.enc_mode)

	def test_dec_backward_ctr_06(self):
		self._test_dec_backward_ctr_06(self.enc_mode)

	def test_dec_backward_ctr_07(self):
		self._test_dec_backward_ctr_07(self.enc_mode)

	def test_dec_backward_ctr_08(self):
		self._test_dec_backward_ctr_08(self.enc_mode)

	def test_dec_backward_ctr_09(self):
		self._test_dec_backward_ctr_09(self.enc_mode)

	def test_dec_backward_ctr_10(self):
		self._test_dec_backward_ctr_10(self.enc_mode)

class Test_11_MOCO_SEED_128_CBC(_Test_MCryptTestCaseBase):
	def setUp(self) -> None:
		self.enc_mode = 11

	def test_enc_forward_01(self):
		self._test_enc_forward_01(self.enc_mode)
	
	def test_enc_forward_02(self):
		self._test_enc_forward_02(self.enc_mode)

	def test_enc_forward_03(self):
		self._test_enc_forward_03(self.enc_mode)

	def test_enc_forward_04(self):
		self._test_enc_forward_04(self.enc_mode)

	def test_enc_forward_05(self):
		self._test_enc_forward_05(self.enc_mode)

	def test_enc_forward_06(self):
		self._test_enc_forward_06(self.enc_mode)

	def test_enc_forward_07(self):
		self._test_enc_forward_07(self.enc_mode)

	def test_enc_forward_08(self):
		self._test_enc_forward_08(self.enc_mode)

	def test_enc_forward_09(self):
		self._test_enc_forward_09(self.enc_mode)

	def test_enc_forward_10(self):
		self._test_enc_forward_10(self.enc_mode)

	def test_dec_forward_01(self):
		self._test_dec_forward_01(self.enc_mode)
	
	def test_dec_forward_02(self):
		self._test_dec_forward_02(self.enc_mode)

	def test_dec_forward_03(self):
		self._test_dec_forward_03(self.enc_mode)

	def test_dec_forward_04(self):
		self._test_dec_forward_04(self.enc_mode)

	def test_dec_forward_05(self):
		self._test_dec_forward_05(self.enc_mode)

	def test_dec_forward_06(self):
		self._test_dec_forward_06(self.enc_mode)

	def test_dec_forward_07(self):
		self._test_dec_forward_07(self.enc_mode)

	def test_dec_forward_08(self):
		self._test_dec_forward_08(self.enc_mode)

	def test_dec_forward_09(self):
		self._test_dec_forward_09(self.enc_mode)

	def test_dec_forward_10(self):
		self._test_dec_forward_10(self.enc_mode)

	def test_enc_forward_ctr_01(self):
		self._test_enc_forward_ctr_01(self.enc_mode)

	def test_enc_forward_ctr_02(self):
		self._test_enc_forward_ctr_02(self.enc_mode)

	def test_enc_forward_ctr_03(self):
		self._test_enc_forward_ctr_03(self.enc_mode)

	def test_enc_forward_ctr_04(self):
		self._test_enc_forward_ctr_04(self.enc_mode)

	def test_enc_forward_ctr_05(self):
		self._test_enc_forward_ctr_05(self.enc_mode)

	def test_enc_forward_ctr_06(self):
		self._test_enc_forward_ctr_06(self.enc_mode)

	def test_enc_forward_ctr_07(self):
		self._test_enc_forward_ctr_07(self.enc_mode)

	def test_enc_forward_ctr_08(self):
		self._test_enc_forward_ctr_08(self.enc_mode)

	def test_enc_forward_ctr_09(self):
		self._test_enc_forward_ctr_09(self.enc_mode)

	def test_enc_forward_ctr_10(self):
		self._test_enc_forward_ctr_10(self.enc_mode)

	def test_dec_forward_ctr_01(self):
		self._test_dec_forward_ctr_01(self.enc_mode)

	def test_dec_forward_ctr_02(self):
		self._test_dec_forward_ctr_02(self.enc_mode)

	def test_dec_forward_ctr_03(self):
		self._test_dec_forward_ctr_03(self.enc_mode)

	def test_dec_forward_ctr_04(self):
		self._test_dec_forward_ctr_04(self.enc_mode)

	def test_dec_forward_ctr_05(self):
		self._test_dec_forward_ctr_05(self.enc_mode)

	def test_dec_forward_ctr_06(self):
		self._test_dec_forward_ctr_06(self.enc_mode)

	def test_dec_forward_ctr_07(self):
		self._test_dec_forward_ctr_07(self.enc_mode)

	def test_dec_forward_ctr_08(self):
		self._test_dec_forward_ctr_08(self.enc_mode)

	def test_dec_forward_ctr_09(self):
		self._test_dec_forward_ctr_09(self.enc_mode)

	def test_dec_forward_ctr_10(self):
		self._test_dec_forward_ctr_10(self.enc_mode)

	def test_enc_backward_ctr_01(self):
		self._test_enc_backward_ctr_01(self.enc_mode)

	def test_enc_backward_ctr_02(self):
		self._test_enc_backward_ctr_02(self.enc_mode)

	def test_enc_backward_ctr_03(self):
		self._test_enc_backward_ctr_03(self.enc_mode)

	def test_enc_backward_ctr_04(self):
		self._test_enc_backward_ctr_04(self.enc_mode)

	def test_enc_backward_ctr_05(self):
		self._test_enc_backward_ctr_05(self.enc_mode)

	def test_enc_backward_ctr_06(self):
		self._test_enc_backward_ctr_06(self.enc_mode)

	def test_enc_backward_ctr_07(self):
		self._test_enc_backward_ctr_07(self.enc_mode)

	def test_enc_backward_ctr_08(self):
		self._test_enc_backward_ctr_08(self.enc_mode)

	def test_enc_backward_ctr_09(self):
		self._test_enc_backward_ctr_09(self.enc_mode)

	def test_enc_backward_ctr_10(self):
		self._test_enc_backward_ctr_10(self.enc_mode)

	def test_dec_backward_ctr_01(self):
		self._test_dec_backward_ctr_01(self.enc_mode)

	def test_dec_backward_ctr_02(self):
		self._test_dec_backward_ctr_02(self.enc_mode)

	def test_dec_backward_ctr_03(self):
		self._test_dec_backward_ctr_03(self.enc_mode)

	def test_dec_backward_ctr_04(self):
		self._test_dec_backward_ctr_04(self.enc_mode)

	def test_dec_backward_ctr_05(self):
		self._test_dec_backward_ctr_05(self.enc_mode)

	def test_dec_backward_ctr_06(self):
		self._test_dec_backward_ctr_06(self.enc_mode)

	def test_dec_backward_ctr_07(self):
		self._test_dec_backward_ctr_07(self.enc_mode)

	def test_dec_backward_ctr_08(self):
		self._test_dec_backward_ctr_08(self.enc_mode)

	def test_dec_backward_ctr_09(self):
		self._test_dec_backward_ctr_09(self.enc_mode)

	def test_dec_backward_ctr_10(self):
		self._test_dec_backward_ctr_10(self.enc_mode)

class Test_13_MOCO_SEED_128_CTR(_Test_MCryptTestCaseBase):
	def setUp(self) -> None:
		self.enc_mode = 13

	def test_enc_forward_01(self):
		self._test_enc_forward_01(self.enc_mode)
	
	def test_enc_forward_02(self):
		self._test_enc_forward_02(self.enc_mode)

	def test_enc_forward_03(self):
		self._test_enc_forward_03(self.enc_mode)

	def test_enc_forward_04(self):
		self._test_enc_forward_04(self.enc_mode)

	def test_enc_forward_05(self):
		self._test_enc_forward_05(self.enc_mode)

	def test_enc_forward_06(self):
		self._test_enc_forward_06(self.enc_mode)

	def test_enc_forward_07(self):
		self._test_enc_forward_07(self.enc_mode)

	def test_enc_forward_08(self):
		self._test_enc_forward_08(self.enc_mode)

	def test_enc_forward_09(self):
		self._test_enc_forward_09(self.enc_mode)

	def test_enc_forward_10(self):
		self._test_enc_forward_10(self.enc_mode)

	def test_dec_forward_01(self):
		self._test_dec_forward_01(self.enc_mode)
	
	def test_dec_forward_02(self):
		self._test_dec_forward_02(self.enc_mode)

	def test_dec_forward_03(self):
		self._test_dec_forward_03(self.enc_mode)

	def test_dec_forward_04(self):
		self._test_dec_forward_04(self.enc_mode)

	def test_dec_forward_05(self):
		self._test_dec_forward_05(self.enc_mode)

	def test_dec_forward_06(self):
		self._test_dec_forward_06(self.enc_mode)

	def test_dec_forward_07(self):
		self._test_dec_forward_07(self.enc_mode)

	def test_dec_forward_08(self):
		self._test_dec_forward_08(self.enc_mode)

	def test_dec_forward_09(self):
		self._test_dec_forward_09(self.enc_mode)

	def test_dec_forward_10(self):
		self._test_dec_forward_10(self.enc_mode)

	def test_enc_forward_ctr_01(self):
		self._test_enc_forward_ctr_01(self.enc_mode)

	def test_enc_forward_ctr_02(self):
		self._test_enc_forward_ctr_02(self.enc_mode)

	def test_enc_forward_ctr_03(self):
		self._test_enc_forward_ctr_03(self.enc_mode)

	def test_enc_forward_ctr_04(self):
		self._test_enc_forward_ctr_04(self.enc_mode)

	def test_enc_forward_ctr_05(self):
		self._test_enc_forward_ctr_05(self.enc_mode)

	def test_enc_forward_ctr_06(self):
		self._test_enc_forward_ctr_06(self.enc_mode)

	def test_enc_forward_ctr_07(self):
		self._test_enc_forward_ctr_07(self.enc_mode)

	def test_enc_forward_ctr_08(self):
		self._test_enc_forward_ctr_08(self.enc_mode)

	def test_enc_forward_ctr_09(self):
		self._test_enc_forward_ctr_09(self.enc_mode)

	def test_enc_forward_ctr_10(self):
		self._test_enc_forward_ctr_10(self.enc_mode)

	def test_dec_forward_ctr_01(self):
		self._test_dec_forward_ctr_01(self.enc_mode)

	def test_dec_forward_ctr_02(self):
		self._test_dec_forward_ctr_02(self.enc_mode)

	def test_dec_forward_ctr_03(self):
		self._test_dec_forward_ctr_03(self.enc_mode)

	def test_dec_forward_ctr_04(self):
		self._test_dec_forward_ctr_04(self.enc_mode)

	def test_dec_forward_ctr_05(self):
		self._test_dec_forward_ctr_05(self.enc_mode)

	def test_dec_forward_ctr_06(self):
		self._test_dec_forward_ctr_06(self.enc_mode)

	def test_dec_forward_ctr_07(self):
		self._test_dec_forward_ctr_07(self.enc_mode)

	def test_dec_forward_ctr_08(self):
		self._test_dec_forward_ctr_08(self.enc_mode)

	def test_dec_forward_ctr_09(self):
		self._test_dec_forward_ctr_09(self.enc_mode)

	def test_dec_forward_ctr_10(self):
		self._test_dec_forward_ctr_10(self.enc_mode)

	def test_enc_backward_ctr_01(self):
		self._test_enc_backward_ctr_01(self.enc_mode)

	def test_enc_backward_ctr_02(self):
		self._test_enc_backward_ctr_02(self.enc_mode)

	def test_enc_backward_ctr_03(self):
		self._test_enc_backward_ctr_03(self.enc_mode)

	def test_enc_backward_ctr_04(self):
		self._test_enc_backward_ctr_04(self.enc_mode)

	def test_enc_backward_ctr_05(self):
		self._test_enc_backward_ctr_05(self.enc_mode)

	def test_enc_backward_ctr_06(self):
		self._test_enc_backward_ctr_06(self.enc_mode)

	def test_enc_backward_ctr_07(self):
		self._test_enc_backward_ctr_07(self.enc_mode)

	def test_enc_backward_ctr_08(self):
		self._test_enc_backward_ctr_08(self.enc_mode)

	def test_enc_backward_ctr_09(self):
		self._test_enc_backward_ctr_09(self.enc_mode)

	def test_enc_backward_ctr_10(self):
		self._test_enc_backward_ctr_10(self.enc_mode)

	def test_dec_backward_ctr_01(self):
		self._test_dec_backward_ctr_01(self.enc_mode)

	def test_dec_backward_ctr_02(self):
		self._test_dec_backward_ctr_02(self.enc_mode)

	def test_dec_backward_ctr_03(self):
		self._test_dec_backward_ctr_03(self.enc_mode)

	def test_dec_backward_ctr_04(self):
		self._test_dec_backward_ctr_04(self.enc_mode)

	def test_dec_backward_ctr_05(self):
		self._test_dec_backward_ctr_05(self.enc_mode)

	def test_dec_backward_ctr_06(self):
		self._test_dec_backward_ctr_06(self.enc_mode)

	def test_dec_backward_ctr_07(self):
		self._test_dec_backward_ctr_07(self.enc_mode)

	def test_dec_backward_ctr_08(self):
		self._test_dec_backward_ctr_08(self.enc_mode)

	def test_dec_backward_ctr_09(self):
		self._test_dec_backward_ctr_09(self.enc_mode)

	def test_dec_backward_ctr_10(self):
		self._test_dec_backward_ctr_10(self.enc_mode)

class Test_18_MOCO_ARIA_256_CBC(_Test_MCryptTestCaseBase):
	def setUp(self) -> None:
		self.enc_mode = 18

	def test_enc_forward_01(self):
		self._test_enc_forward_01(self.enc_mode)
	
	def test_enc_forward_02(self):
		self._test_enc_forward_02(self.enc_mode)

	def test_enc_forward_03(self):
		self._test_enc_forward_03(self.enc_mode)

	def test_enc_forward_04(self):
		self._test_enc_forward_04(self.enc_mode)

	def test_enc_forward_05(self):
		self._test_enc_forward_05(self.enc_mode)

	def test_enc_forward_06(self):
		self._test_enc_forward_06(self.enc_mode)

	def test_enc_forward_07(self):
		self._test_enc_forward_07(self.enc_mode)

	def test_enc_forward_08(self):
		self._test_enc_forward_08(self.enc_mode)

	def test_enc_forward_09(self):
		self._test_enc_forward_09(self.enc_mode)

	def test_enc_forward_10(self):
		self._test_enc_forward_10(self.enc_mode)

	def test_dec_forward_01(self):
		self._test_dec_forward_01(self.enc_mode)
	
	def test_dec_forward_02(self):
		self._test_dec_forward_02(self.enc_mode)

	def test_dec_forward_03(self):
		self._test_dec_forward_03(self.enc_mode)

	def test_dec_forward_04(self):
		self._test_dec_forward_04(self.enc_mode)

	def test_dec_forward_05(self):
		self._test_dec_forward_05(self.enc_mode)

	def test_dec_forward_06(self):
		self._test_dec_forward_06(self.enc_mode)

	def test_dec_forward_07(self):
		self._test_dec_forward_07(self.enc_mode)

	def test_dec_forward_08(self):
		self._test_dec_forward_08(self.enc_mode)

	def test_dec_forward_09(self):
		self._test_dec_forward_09(self.enc_mode)

	def test_dec_forward_10(self):
		self._test_dec_forward_10(self.enc_mode)

	def test_enc_forward_ctr_01(self):
		self._test_enc_forward_ctr_01(self.enc_mode)

	def test_enc_forward_ctr_02(self):
		self._test_enc_forward_ctr_02(self.enc_mode)

	def test_enc_forward_ctr_03(self):
		self._test_enc_forward_ctr_03(self.enc_mode)

	def test_enc_forward_ctr_04(self):
		self._test_enc_forward_ctr_04(self.enc_mode)

	def test_enc_forward_ctr_05(self):
		self._test_enc_forward_ctr_05(self.enc_mode)

	def test_enc_forward_ctr_06(self):
		self._test_enc_forward_ctr_06(self.enc_mode)

	def test_enc_forward_ctr_07(self):
		self._test_enc_forward_ctr_07(self.enc_mode)

	def test_enc_forward_ctr_08(self):
		self._test_enc_forward_ctr_08(self.enc_mode)

	def test_enc_forward_ctr_09(self):
		self._test_enc_forward_ctr_09(self.enc_mode)

	def test_enc_forward_ctr_10(self):
		self._test_enc_forward_ctr_10(self.enc_mode)

	def test_dec_forward_ctr_01(self):
		self._test_dec_forward_ctr_01(self.enc_mode)

	def test_dec_forward_ctr_02(self):
		self._test_dec_forward_ctr_02(self.enc_mode)

	def test_dec_forward_ctr_03(self):
		self._test_dec_forward_ctr_03(self.enc_mode)

	def test_dec_forward_ctr_04(self):
		self._test_dec_forward_ctr_04(self.enc_mode)

	def test_dec_forward_ctr_05(self):
		self._test_dec_forward_ctr_05(self.enc_mode)

	def test_dec_forward_ctr_06(self):
		self._test_dec_forward_ctr_06(self.enc_mode)

	def test_dec_forward_ctr_07(self):
		self._test_dec_forward_ctr_07(self.enc_mode)

	def test_dec_forward_ctr_08(self):
		self._test_dec_forward_ctr_08(self.enc_mode)

	def test_dec_forward_ctr_09(self):
		self._test_dec_forward_ctr_09(self.enc_mode)

	def test_dec_forward_ctr_10(self):
		self._test_dec_forward_ctr_10(self.enc_mode)

	def test_enc_backward_ctr_01(self):
		self._test_enc_backward_ctr_01(self.enc_mode)

	def test_enc_backward_ctr_02(self):
		self._test_enc_backward_ctr_02(self.enc_mode)

	def test_enc_backward_ctr_03(self):
		self._test_enc_backward_ctr_03(self.enc_mode)

	def test_enc_backward_ctr_04(self):
		self._test_enc_backward_ctr_04(self.enc_mode)

	def test_enc_backward_ctr_05(self):
		self._test_enc_backward_ctr_05(self.enc_mode)

	def test_enc_backward_ctr_06(self):
		self._test_enc_backward_ctr_06(self.enc_mode)

	def test_enc_backward_ctr_07(self):
		self._test_enc_backward_ctr_07(self.enc_mode)

	def test_enc_backward_ctr_08(self):
		self._test_enc_backward_ctr_08(self.enc_mode)

	def test_enc_backward_ctr_09(self):
		self._test_enc_backward_ctr_09(self.enc_mode)

	def test_enc_backward_ctr_10(self):
		self._test_enc_backward_ctr_10(self.enc_mode)

	def test_dec_backward_ctr_01(self):
		self._test_dec_backward_ctr_01(self.enc_mode)

	def test_dec_backward_ctr_02(self):
		self._test_dec_backward_ctr_02(self.enc_mode)

	def test_dec_backward_ctr_03(self):
		self._test_dec_backward_ctr_03(self.enc_mode)

	def test_dec_backward_ctr_04(self):
		self._test_dec_backward_ctr_04(self.enc_mode)

	def test_dec_backward_ctr_05(self):
		self._test_dec_backward_ctr_05(self.enc_mode)

	def test_dec_backward_ctr_06(self):
		self._test_dec_backward_ctr_06(self.enc_mode)

	def test_dec_backward_ctr_07(self):
		self._test_dec_backward_ctr_07(self.enc_mode)

	def test_dec_backward_ctr_08(self):
		self._test_dec_backward_ctr_08(self.enc_mode)

	def test_dec_backward_ctr_09(self):
		self._test_dec_backward_ctr_09(self.enc_mode)

	def test_dec_backward_ctr_10(self):
		self._test_dec_backward_ctr_10(self.enc_mode)

class Test_19_MOCO_ARIA_256_CTR(_Test_MCryptTestCaseBase):
	def setUp(self) -> None:
		self.enc_mode = 19

	def test_enc_forward_01(self):
		self._test_enc_forward_01(self.enc_mode)
	
	def test_enc_forward_02(self):
		self._test_enc_forward_02(self.enc_mode)

	def test_enc_forward_03(self):
		self._test_enc_forward_03(self.enc_mode)

	def test_enc_forward_04(self):
		self._test_enc_forward_04(self.enc_mode)

	def test_enc_forward_05(self):
		self._test_enc_forward_05(self.enc_mode)

	def test_enc_forward_06(self):
		self._test_enc_forward_06(self.enc_mode)

	def test_enc_forward_07(self):
		self._test_enc_forward_07(self.enc_mode)

	def test_enc_forward_08(self):
		self._test_enc_forward_08(self.enc_mode)

	def test_enc_forward_09(self):
		self._test_enc_forward_09(self.enc_mode)

	def test_enc_forward_10(self):
		self._test_enc_forward_10(self.enc_mode)

	def test_dec_forward_01(self):
		self._test_dec_forward_01(self.enc_mode)
	
	def test_dec_forward_02(self):
		self._test_dec_forward_02(self.enc_mode)

	def test_dec_forward_03(self):
		self._test_dec_forward_03(self.enc_mode)

	def test_dec_forward_04(self):
		self._test_dec_forward_04(self.enc_mode)

	def test_dec_forward_05(self):
		self._test_dec_forward_05(self.enc_mode)

	def test_dec_forward_06(self):
		self._test_dec_forward_06(self.enc_mode)

	def test_dec_forward_07(self):
		self._test_dec_forward_07(self.enc_mode)

	def test_dec_forward_08(self):
		self._test_dec_forward_08(self.enc_mode)

	def test_dec_forward_09(self):
		self._test_dec_forward_09(self.enc_mode)

	def test_dec_forward_10(self):
		self._test_dec_forward_10(self.enc_mode)

	def test_enc_forward_ctr_01(self):
		self._test_enc_forward_ctr_01(self.enc_mode)

	def test_enc_forward_ctr_02(self):
		self._test_enc_forward_ctr_02(self.enc_mode)

	def test_enc_forward_ctr_03(self):
		self._test_enc_forward_ctr_03(self.enc_mode)

	def test_enc_forward_ctr_04(self):
		self._test_enc_forward_ctr_04(self.enc_mode)

	def test_enc_forward_ctr_05(self):
		self._test_enc_forward_ctr_05(self.enc_mode)

	def test_enc_forward_ctr_06(self):
		self._test_enc_forward_ctr_06(self.enc_mode)

	def test_enc_forward_ctr_07(self):
		self._test_enc_forward_ctr_07(self.enc_mode)

	def test_enc_forward_ctr_08(self):
		self._test_enc_forward_ctr_08(self.enc_mode)

	def test_enc_forward_ctr_09(self):
		self._test_enc_forward_ctr_09(self.enc_mode)

	def test_enc_forward_ctr_10(self):
		self._test_enc_forward_ctr_10(self.enc_mode)

	def test_dec_forward_ctr_01(self):
		self._test_dec_forward_ctr_01(self.enc_mode)

	def test_dec_forward_ctr_02(self):
		self._test_dec_forward_ctr_02(self.enc_mode)

	def test_dec_forward_ctr_03(self):
		self._test_dec_forward_ctr_03(self.enc_mode)

	def test_dec_forward_ctr_04(self):
		self._test_dec_forward_ctr_04(self.enc_mode)

	def test_dec_forward_ctr_05(self):
		self._test_dec_forward_ctr_05(self.enc_mode)

	def test_dec_forward_ctr_06(self):
		self._test_dec_forward_ctr_06(self.enc_mode)

	def test_dec_forward_ctr_07(self):
		self._test_dec_forward_ctr_07(self.enc_mode)

	def test_dec_forward_ctr_08(self):
		self._test_dec_forward_ctr_08(self.enc_mode)

	def test_dec_forward_ctr_09(self):
		self._test_dec_forward_ctr_09(self.enc_mode)

	def test_dec_forward_ctr_10(self):
		self._test_dec_forward_ctr_10(self.enc_mode)

	def test_enc_backward_ctr_01(self):
		self._test_enc_backward_ctr_01(self.enc_mode)

	def test_enc_backward_ctr_02(self):
		self._test_enc_backward_ctr_02(self.enc_mode)

	def test_enc_backward_ctr_03(self):
		self._test_enc_backward_ctr_03(self.enc_mode)

	def test_enc_backward_ctr_04(self):
		self._test_enc_backward_ctr_04(self.enc_mode)

	def test_enc_backward_ctr_05(self):
		self._test_enc_backward_ctr_05(self.enc_mode)

	def test_enc_backward_ctr_06(self):
		self._test_enc_backward_ctr_06(self.enc_mode)

	def test_enc_backward_ctr_07(self):
		self._test_enc_backward_ctr_07(self.enc_mode)

	def test_enc_backward_ctr_08(self):
		self._test_enc_backward_ctr_08(self.enc_mode)

	def test_enc_backward_ctr_09(self):
		self._test_enc_backward_ctr_09(self.enc_mode)

	def test_enc_backward_ctr_10(self):
		self._test_enc_backward_ctr_10(self.enc_mode)

	def test_dec_backward_ctr_01(self):
		self._test_dec_backward_ctr_01(self.enc_mode)

	def test_dec_backward_ctr_02(self):
		self._test_dec_backward_ctr_02(self.enc_mode)

	def test_dec_backward_ctr_03(self):
		self._test_dec_backward_ctr_03(self.enc_mode)

	def test_dec_backward_ctr_04(self):
		self._test_dec_backward_ctr_04(self.enc_mode)

	def test_dec_backward_ctr_05(self):
		self._test_dec_backward_ctr_05(self.enc_mode)

	def test_dec_backward_ctr_06(self):
		self._test_dec_backward_ctr_06(self.enc_mode)

	def test_dec_backward_ctr_07(self):
		self._test_dec_backward_ctr_07(self.enc_mode)

	def test_dec_backward_ctr_08(self):
		self._test_dec_backward_ctr_08(self.enc_mode)

	def test_dec_backward_ctr_09(self):
		self._test_dec_backward_ctr_09(self.enc_mode)

	def test_dec_backward_ctr_10(self):
		self._test_dec_backward_ctr_10(self.enc_mode)

if __name__ == '__main__':
	unittest.main()
