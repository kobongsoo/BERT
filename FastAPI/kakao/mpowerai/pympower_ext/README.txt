최소 지원 버전

python 3.9

빌드 방법

python setup.py build

테스트 방법

윈도우
set PYTHONPATH=%CD%\build\lib.win-amd64-3.9
python -m unittest discover

리눅스
MocoCrypto.so를 로드하기 위해 LD_LIBRARY_PATH 사용
LD_LIBRARY_PATH=/MOCOMSYS/util74/lib PYTHONPATH=`pwd`/build/lib.linux-x86_64-3.9 python -m unittest discover

whl 생성 방법

python setup.py bdist_wheel

whl 설치 방법

윈도우
pip install dist/pympower_ext-10.0-cp39-cp39-win_amd64.whl

리눅스
pip install dist/pympower_ext-10.0-cp39-cp39-linux_x86_64.whl

whl 삭제 방법

pip uninstall pympower_ext

