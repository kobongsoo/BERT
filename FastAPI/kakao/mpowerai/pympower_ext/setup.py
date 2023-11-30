import os
import setuptools
from distutils.core import setup, Extension

top_dir = os.path.dirname(__file__)

if 'nt' == os.name:
	os_define_for_neo_crypto = ('_WINDOWS', 1)
	snf_dir = os.path.join(top_dir, 'common', 'filter4-v4.29.0-windows_64bit_VC9', 'v4')
	snf_lib = 'snf_win'
else:
	os_define_for_neo_crypto = ('_LINUX', 1)
	snf_dir = os.path.join(top_dir, 'common', 'filter4-v4.29.0-centOS-7.2_64bit_gcc_4.8.5', 'v4')
	snf_lib = 'snf'

setup(
	name = 'pympower_ext',
	version = '10.0',
	description = 'Mpower 10.0 extension modules',
	setup_requires=['wheel'],
	ext_modules = [
		Extension(
			name = 'pympower_ext._mcrypt',
			sources = [
				os.path.join(top_dir, 'src', '_mcrypt', '_mcryptmodule.c'),
				os.path.join(top_dir, 'src', '_mcrypt', 'kisa-aria.c'),
				os.path.join(top_dir, 'src', '_mcrypt', 'kisa-ariaenc.c'),
				os.path.join(top_dir, 'src', '_mcrypt', 'kisa-crypto.c'),
				os.path.join(top_dir, 'src', '_mcrypt', 'kisa-seed.c'),
				os.path.join(top_dir, 'src', '_mcrypt', 'kisa-seedenc.c'),
				os.path.join(top_dir, 'src', '_mcrypt', 'md5c.c'),
				os.path.join(top_dir, 'src', '_mcrypt', 'moco-aria.c'),
				os.path.join(top_dir, 'src', '_mcrypt', 'moco-crypto.c'),
				os.path.join(top_dir, 'src', '_mcrypt', 'moco-seed.c'),
				os.path.join(top_dir, 'src', '_mcrypt', 'Sha256.c'),
				os.path.join(top_dir, 'src', '_mcrypt', 'stdafx.c'),
				],
			depends = [
				os.path.join(top_dir, 'src', '_mcrypt', 'global.h'),
				os.path.join(top_dir, 'src', '_mcrypt', 'kisa-aria.h'),
				os.path.join(top_dir, 'src', '_mcrypt', 'kisa-crypto.h'),
				os.path.join(top_dir, 'src', '_mcrypt', 'kisa-seed.h'),
				os.path.join(top_dir, 'src', '_mcrypt', 'md5.h'),
				os.path.join(top_dir, 'src', '_mcrypt', 'moco-aria.h'),
				os.path.join(top_dir, 'src', '_mcrypt', 'moco-crypto.h'),
				os.path.join(top_dir, 'src', '_mcrypt', 'moco-seed.h'),
				os.path.join(top_dir, 'src', '_mcrypt', 'RotateDefs.h'),
				os.path.join(top_dir, 'src', '_mcrypt', 'Sha256.h'),
				os.path.join(top_dir, 'src', '_mcrypt', 'stdafx.h'),
				os.path.join(top_dir, 'src', '_mcrypt', 'Types.h'),
			],
			include_dirs = [
				os.path.join(top_dir, 'common', 'include'),
			],
            define_macros = [
				('UNICODE', 1),
				('_UNICODE', 1),
                ('__USE_MOCOCRYPTO', 1),
				('__USE_MOCOCRYPTO_KISACRYPTO_MIXING', 1),
				os_define_for_neo_crypto,
            ]
		),
		Extension (
			name = 'pympower_ext._snf',
			# 리눅스에서 snf.a를 사용할 때는 c++로 빌드해야 한다.
			language = "c++",
			sources = [
				os.path.join(top_dir, 'src', '_snf', '_snfmodule.c'),
				os.path.join(top_dir, 'src', '_snf', 'status_code.c'),
			],
            depends = [
                os.path.join(top_dir, 'src', '_snf', 'status_code.h'),
            ],
			include_dirs = [
				snf_dir,
			],
			library_dirs = [
				snf_dir,
			],
			libraries = [
				snf_lib,
			],
		)
	]
)
