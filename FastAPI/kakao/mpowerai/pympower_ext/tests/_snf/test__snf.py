import os
import unittest
import pympower_ext._snf as _snf

class TestSnf(unittest.TestCase):
	contents = {
		'test file 1.txt': '이것은 테스트 파일 1 입니다.',
		'test file 2.txt': '이것은 테스트 파일 2 입니다.',
	}
	unload_dir = os.path.dirname(__file__)

	def setUp(self):
		self.unloaded_raw_data = {}
		self.extract_chars = 5
		self.user_func_call_count = 0
		self.extracted_text = ''

		_snf.snf_gbl_setcfg(
			None,
			# SN3FILETYPE_ALL
			0xffffffffffffffff,
			# SN3OPTION_ARCHIVE_EXTRACT
			0x000001
			# SN3OPTION_ARCHIVE_NOFILENAME
			| 0x000100
			# SN3OPTION_EXTENSION_NO_CHECK
			| 0x000010
			# SN3OPTION_EMBEDED_OLE_FILTER
			| 0x000020
			# SN3OPTION_EXCEL_NOLIMIT
			| 0x004000,
			0
		)

	def _user_func(self, buf:_snf.SN3BUF, user_data:'TestSnf'):
		self.assertEqual(self, user_data)

		self.user_func_call_count += 1

		if self.user_func_call_count == self.extract_chars:
			self.assertEqual(buf.size(), self.user_func_call_count)
			self.extracted_text += buf.get_text(buf.size())

	def _marker_func(self, buf:_snf.SN3BUF, marker_data:'TestSnf', marker:_snf.SN3MARKER) -> int:
		self.assertEqual(self, marker_data)

		if 9 == marker.state:
			# 9 == UNZIP_FILE_STATE
			self.assertIsNotNone(marker.unzipMFI)
			self.assertNotEqual(0, len(marker.marker))

			if None != marker.unzipMFI and 0 != len(marker.marker):
				unload_path = os.path.join(self.unload_dir, marker.marker)
				self.assertFalse(os.path.exists(unload_path))
				marker.unzipMFI.unload(unload_path)
				self.assertTrue(os.path.exists(unload_path))

				with open(unload_path, 'rb') as f:
					marker_data.unloaded_raw_data[marker.marker] = f.read()

				os.remove(unload_path)

		# 0 == SN3_USER_CONTINUE
		return 0

	def test_callback_and_unload(self):
		filename = os.path.join(os.path.dirname(__file__), 'test.zip')
		mfi = _snf.SN3MFI()
		mfi.fopen(filename)

		buf = _snf.SN3BUF()
		buf.set_user_func(self._user_func)
		buf.set_user_data(self)
		buf.set_marker_func(self._marker_func)
		buf.set_marker_data(self)

		buf.filter_m(mfi, False)

		for filename in self.unloaded_raw_data:
			self.assertEqual(self.unloaded_raw_data[filename].decode('utf-8'), self.contents[filename])

		# 나머지 출력
		size = buf.size()
		text = buf.get_text(size)
		self.assertEqual(self.extracted_text + text, '\n'.join([self.contents[filename] for filename in self.contents]))

if __name__ == '__main__':
	unittest.main()