import os
import sys
from abc import abstractmethod
import subprocess
import regex
import json
import dpath.util
from io import TextIOBase
from typing import Iterable, Any, Generator
from random import Random
from itertools import islice
import nltk
import kss
import fasttext
#import tensorflow as tf
#import tensorflow_hub as hub
#import tensorflow_text as text # 사용하지 않더라도 import해야 tfhub_handle_encoder 관련 기능이 정상 작동한다.
from pympower.common.global_val import global_val
from pympower.common.statuscode import StatusCode
from pympower.classes.mbase import *
from pympower.classes.mcrypt import MCrypt
from pympower.classes.mshaai import MShaAI
global_val = global_val.load_global_val()

_SENTENCE_CUT_PREDICTION_BATCH_SIZE = 32

##############################################################################
# MPreprocessor
##############################################################################

class MPreprocessor(MToFromConfigClass):
    @abstractmethod
    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        pass

class MSentenceMergingChecker(MToFromConfigClass):
    @abstractmethod
    def isMergeable(self, sentence1: str, sentence2: str) -> bool:
        pass

##############################################################################
# 팩토리
##############################################################################

class MPreprocessorFactory(MToFromConfigClassFactory):
    def createInstance(self, name:str, options:Any) -> MPreprocessor:
        return super().createInstance(name, options)

    def createInstanceFromConfig(self, config:dict) -> MPreprocessor:
        return super().createInstanceFromConfig(config)

class MSentenceMergingCheckerFactory(MToFromConfigClassFactory):
    def createInstance(self, name:str, options:Any) -> MSentenceMergingChecker:
        return super().createInstance(name, options)


    def createInstanceFromConfig(self, config:dict) -> MSentenceMergingChecker:
        return super().createInstanceFromConfig(config)

##############################################################################
# 팩토리 전역 변수 선언
##############################################################################

preprocessorFactory = MPreprocessorFactory()

sentenceMergingCheckerFactory = MSentenceMergingCheckerFactory()

##############################################################################
# 합성 전처리기
##############################################################################

class MCompositePreprocessor(MPreprocessor):
    def __init__(self, preprocessors:list[MPreprocessor]):
        self.preprocessors = preprocessors

    def createFromConfig(config:dict) -> MPreprocessor:
        return MCompositePreprocessor(
            preprocessors=[
                preprocessorFactory.createInstanceFromConfig(preprocessorConfig) for preprocessorConfig in config['preprocessors']
            ]
        )

    def exportToConfig(self) -> dict:
        preprocessorsFactoryConfig = []
        for preprocessor in self.preprocessors:
            preprocessorsFactoryConfig.append(preprocessorFactory.exportInstanceToConfig(preprocessor))
        return {
            'preprocessors': preprocessorsFactoryConfig
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for preprocessor in self.preprocessors:
            texts = preprocessor.preprocess(texts)
        return texts

class MMultiLevelPreprocessor(MPreprocessor):
    def __init__(self, preprocessors:list[MPreprocessor]):
        self.preprocessors = preprocessors

    def createFromConfig(config:dict) -> MPreprocessor:
        return MCompositePreprocessor(
            preprocessors=[
                preprocessorFactory.createInstanceFromConfig(preprocessorConfig) for preprocessorConfig in config['preprocessors']
            ]
        )

    def exportToConfig(self) -> dict:
        preprocessorsFactoryConfig = []
        for preprocessor in self.preprocessors:
            preprocessorsFactoryConfig.append(preprocessorFactory.exportInstanceToConfig(preprocessor))
        return {
            'preprocessors': preprocessorsFactoryConfig
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        return self._preprocessRec(0, texts)

    def _preprocessRec(self, index:int, texts:Iterable[str]) -> Generator[str, None, None]:
        if index == len(self.preprocessors):
            for text in texts:
                yield text
        else:
            preprocessor = self.preprocessors[index]
            for texts in preprocessor.preprocess(texts):
                for text in self._preprocessRec(index + 1, [texts]):
                    yield text

# TODO: 제거 할 것
class MPassthroughPreprocessor(MPreprocessor):
    def createFromConfig(config:dict) -> MPreprocessor:
        return MPassthroughPreprocessor()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        return texts

##############################################################################
# 정규식
##############################################################################

class MRegExSplitter(MPreprocessor):
    def __init__(self, pattern:str, flags:int = 0):
        self.pattern = pattern
        self.flags = flags

        self.splitter = regex.compile(pattern, flags)

    def createFromConfig(config:dict) -> MPreprocessor:
        return MRegExSplitter(
            regex=config['regex'],
            flags=config['flags'],
        )

    def exportToConfig(self) -> dict:
        return {
            'regex': self.pattern,
            'flags': self.flags,
        }

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        for text in texts:
            for text in self.splitter.split(text):
                if 0 == len(text):
                    continue
                yield text

class MRegExReplacer(MPreprocessor):
    def __init__(self, pattern:str, flags:int, replacement:str):
        self.pattern = pattern
        self.flags = flags
        self.replacement = replacement

        self.replacer = regex.compile(pattern, flags)

    def createFromConfig(config:dict) -> MPreprocessor:
        return MRegExSplitter(
            pattern=config['pattern'],
            flags=config['flags'],
            replacement=config['replacement'],
        )

    def exportToConfig(self) -> dict:
        return {
            'pattern': self.pattern,
            'flags': self.flags,
            'replacement': self.replacement,
        }

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        for text in texts:
            yield self.replacer.sub(self.replacement, text)

##############################################################################
# 코퍼스 분리
##############################################################################

class MCorpusPageSplitter(MRegExSplitter):
    def __init__(self):
        super().__init__(r'^\.\.PAGE:.+$', regex.MULTILINE)

    def createFromConfig(config:dict) -> MPreprocessor:
        return MCorpusPageSplitter()

    def exportToConfig(self) -> dict:
        pass

class MCorpusPageMarkerRemover(MRegExReplacer):
    def __init__(self):
        super().__init__(r'^\.\.PAGE:.+$', regex.MULTILINE, '')

    def createFromConfig(config:dict) -> MPreprocessor:
        return MCorpusPageMarkerRemover()

    def exportToConfig(self) -> dict:
        pass

class MCorpusSheetSplitter(MRegExSplitter):
    def __init__(self):
        super().__init__(r'^\.\.SHEET:.+$', regex.MULTILINE)

    def createFromConfig(config:dict) -> MPreprocessor:
        return MCorpusSheetSplitter()

    def exportToConfig(self) -> dict:
        pass

class MCorpusExcelCellSplitter(MRegExSplitter):
    def __init__(self):
        # ~*~는 엑셀인 경우 셀 구분자이기도 하지만,
        # OLE의 경우 ~*~OLE START~*~와 ~*~OLE END~*~가 사용되기 때문에,
        # OLE 마커를 출력한 경우 이 함수를 사용하면 잘못된 결과를 얻을 수 있다.
        super().__init__(r'~[\*\^]~', regex.MULTILINE)

    def createFromConfig(config:dict) -> MPreprocessor:
        return MCorpusExcelCellSplitter()

    def exportToConfig(self) -> dict:
        pass

##############################################################################
# 코퍼스 전처리기 매퍼
##############################################################################

class MCorpusPreprocessorMapper:
    def __init__(
        self,
        wordPreprocessor:MPreprocessor,
        excelPreprocessor:MPreprocessor,
        powerpointPreprocessor:MPreprocessor,
        pdfPreprocessor:MPreprocessor,
        textPreprocessor:MPreprocessor,
    ):
        self.preprocessros = {
            # 워드
            60000: wordPreprocessor, # Microsoft Word Document
            60001: wordPreprocessor, # Microsoft Word 6 Document
            60002: wordPreprocessor, # Spanish Microsoft Word 6 document data
            60003: wordPreprocessor, # Microsoft Word document data
            60004: wordPreprocessor, # Microsoft Word Document
            60005: wordPreprocessor, # Microsoft Word 6 Document

            60300: wordPreprocessor, # HWP Wordian,2000 or 2002 Document
            60305: wordPreprocessor, # HWP Document file (Encrypted)
            60310: wordPreprocessor, # HWP Document file
            60311: wordPreprocessor, # HWP Document file, version 1
            60312: wordPreprocessor, # HWP Document file, version 2
            60313: wordPreprocessor, # HWP Document file, version 3
            60320: wordPreprocessor, # HWP Document file (Encrypted)

            60400: wordPreprocessor, # Hunminjeongeum (.gul) File

            80101: wordPreprocessor, # OpenOffice Word File

            192600: wordPreprocessor, # iWork Pages (.pages) File

            300100: wordPreprocessor, # Microsoft Office 2007 Word XML
            300102: wordPreprocessor, # Microsoft Office 2007 Word XML
            300103: wordPreprocessor, # Microsoft Office 2007 Word XML
            300104: wordPreprocessor, # Microsoft Office 2007 Word XML

            301200: wordPreprocessor, # Hangul Standard(.hwpx) File

            37300: wordPreprocessor, # Rich Text Format Document
            # 확인 필요
            37910: wordPreprocessor, # XML Office document text
            37920: wordPreprocessor, # XML Office document text
            37950: wordPreprocessor, # XML HWP document text

            # 엑셀
            80201: excelPreprocessor, # OpenOffice Spread Sheet File
            60200: excelPreprocessor, # Microsoft Excel Document
            60201: excelPreprocessor, # Microsoft Excel95 Document
            60202: excelPreprocessor, # Microsoft Excel 5 Worksheet
            60203: excelPreprocessor, # Microsoft Excel 5 Worksheet

            80201: excelPreprocessor, # OpenOffice Spread Sheet File

            191100: excelPreprocessor, # iWork Numbers (.numbers) File
            192800: excelPreprocessor, # iWork Numbers (.numbers) File

            300300: excelPreprocessor, # Microsoft Office 2007 Spreadsheet XML
            300302: excelPreprocessor, # Microsoft Office 2007 Spreadsheet XML
            300303: excelPreprocessor, # Microsoft Office 2007 Spreadsheet XML
            300304: excelPreprocessor, # Microsoft Office 2007 Spreadsheet XML

            300800: excelPreprocessor, # Hancom Show 2010 File
            300900: excelPreprocessor, # Hancom Cell 2004 File
            301000: excelPreprocessor, # Hancom Cell 2010 File
            301100: excelPreprocessor, # Hancom Cell 2014 File
            301300: excelPreprocessor, # Microsoft Office Spreadsheet XML with Binary
            301302: excelPreprocessor, # Microsoft Office Spreadsheet XML with Binary
            301303: excelPreprocessor, # Microsoft Office Spreadsheet XML with Binary
            321000: excelPreprocessor, # Microsoft Office Macro-Enabled Spreadsheet XML
            321002: excelPreprocessor, # Microsoft Office Macro-Enabled Spreadsheet XML
            321003: excelPreprocessor, # Microsoft Office Macro-Enabled Spreadsheet XML
            321004: excelPreprocessor, # Microsoft Office Macro-Enabled Spreadsheet XML
            321033: excelPreprocessor, # Microsoft Office Excel Open XML Macro-Enabled Add-In

            # 파워 포인트
            60100: powerpointPreprocessor, # Microsoft PowerPoint Document

            80301: powerpointPreprocessor, # OpenOffice Presentation File

            192700: powerpointPreprocessor, # iWork Keynote (.key) File

            300500: powerpointPreprocessor, # Microsoft Office 2007 Presentation XML
            300502: powerpointPreprocessor, # Microsoft Office 2007 Presentation XML
            300503: powerpointPreprocessor, # Microsoft Office 2007 Presentation XML
            300504: powerpointPreprocessor, # Microsoft Office 2007 Presentation XML

            301402: powerpointPreprocessor, # Microsoft Office Presenttaion Template XML
            301403: powerpointPreprocessor, # Microsoft Office Presenttaion Template XML
            301432: powerpointPreprocessor, # Microsoft Office Presentation Template XML With Macro
            301433: powerpointPreprocessor, # Microsoft Office Presentation Template XML With Macro
            301462: powerpointPreprocessor, # Microsoft Office Presentation Slide Show XML
            301463: powerpointPreprocessor, # Microsoft Office Presentation Slide Show XML
            301464: powerpointPreprocessor, # Microsoft Office Presentation Slide Show XML
            301492: powerpointPreprocessor, # Microsoft Office Presentation Slide Show XML With Macro
            301493: powerpointPreprocessor, # Microsoft Office Presentation Slide Show XML With Macro
            301595: powerpointPreprocessor, # Microsoft Office Presentation Theme XML
            311002: powerpointPreprocessor, # Microsoft Office Macro-Enabled Presentation XML
            311003: powerpointPreprocessor, # Microsoft Office Macro-Enabled Presentation XML

            # PDF
            35200: pdfPreprocessor, # PDF document
            35220: pdfPreprocessor, # Adobe Acrobat PDF (.pdf) (Encrypted) File
            300600: pdfPreprocessor, # XML Paper Specification
            300601: pdfPreprocessor, # XML Paper Specification

            # 일반 텍스트
            50000: textPreprocessor, # ASCII Text
            50001: textPreprocessor, # Non-ISO extended-ASCII Text
            50002: textPreprocessor, # EBCDIC Text
            50100: textPreprocessor, # UTF-8 Unicode Text
            50200: textPreprocessor, # Little-endian UTF-16 Unicode Text
            50300: textPreprocessor, # Big-endian UTF-16 Unicode Text
            50301: textPreprocessor, # Big-endian UTF-32 Unicode Text
            50400: textPreprocessor, # Japanese Encoding Text (euc-jp)
            50401: textPreprocessor, # Korean Encoding Text (euc-kr, cp949)
            50500: textPreprocessor, # Chinese Simplified Encoding Text (gb2312)
            50600: textPreprocessor, # Cyrillic Encoding Text (cp1251)
            50700: textPreprocessor, # Japanese Encoding Text (shift-jis)
            50800: textPreprocessor, # Chinese Traditional Encoding Text (big5)
            50900: textPreprocessor, # ISO-2022-JP (iso2022jp)

            # 소스코드
            29300: pdfPreprocessor, # MS-DOS batch file text
        }

    def isSupportedType(self, formatCode:int) -> bool:
        return (formatCode in self.preprocessros) and (None != self.preprocessros[formatCode])

    def getPreprocessor(self, formatCode:int) -> MPreprocessor:
        return self.preprocessros[formatCode]

##############################################################################
# 문장 분리
##############################################################################

class MLineSplitter(MPreprocessor):
    def __init__(self, keepends:bool):
        self.keepends = keepends

    def createFromConfig(config:dict) -> MPreprocessor:
        return MLineSplitter(
            keepends=config['keepends'],
        )

    def exportToConfig(self) -> dict:
        return {
            'keepends': self.keepends
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            text = text.replace('\r\n', '\n')
            for splittedText in text.splitlines(self.keepends):
                yield splittedText

class MMultipleEmptyLineSplitter(MPreprocessor):
    '''
    n줄 이상 빈 라인이 있는 경우 분리한다.
    분리된 두 텍스트 사이의 공백은 모두 제거한다.
    '''
    def __init__(self, minEmptyLines:int):
        self.minEmptyLines = minEmptyLines

        self.splitter = regex.compile(r'((?:[ \t]*\n){' + str(int(minEmptyLines)) + r',})', regex.MULTILINE)

    def createFromConfig(config:dict) -> MPreprocessor:
        return MMultipleEmptyLineSplitter(
            minEmptyLines=config['minEmptyLines'],
        )

    def exportToConfig(self) -> dict:
        return {
            'minEmptyLines': self.minEmptyLines
        }

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        for text in texts:
            for text in self.splitter.split(text):
                if 0 == len(text):
                    continue
                yield text

class MNonLetterLineSplitter(MPreprocessor):
    def __init__(self):
        self.splitter = regex.compile(r'^[\W\s]+\n', regex.MULTILINE)

    def createFromConfig(config:dict) -> MPreprocessor:
        return MNonLetterLineSplitter()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        for text in texts:
            for text in self.splitter.split(text):
                if 0 == len(text):
                    continue
                yield text

class MPostpositionSeparatorsSplitter(MPreprocessor):
    '''
    문장 뒤에 오는 구분자를 기준으로 문장을 자른다.
    구체적으로 마침표, 물음표, 느낌표 등의 기호를 말한다.
    '''

    def __init__(self, separators:list[str]):
        self.separators = separators

    def createFromConfig(config:dict) -> MPreprocessor:
        return MPostpositionSeparatorsSplitter(
            separators=config['separators']
        )

    def exportToConfig(self) -> dict:
        return {
            'separators': self.separators
        }

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        separatorsSet = {separator for separator in self.separators}

        for text in texts:
            currentTokens = []
            for ch in text:
                currentTokens.append(ch)
                if ch in separatorsSet:
                    yield ''.join(currentTokens)
                    currentTokens = []

            if len(currentTokens):
                yield ''.join(currentTokens)

class MPostpositionPunctuationMarkSplitter(MRegExSplitter):
    '''
    문장 뒤에 오는 구분자를 기준으로 문장을 자른다.
    구체적으로 마침표, 물음표, 느낌표 등의 기호를 말한다.
    '''
    def __init__(self):
        # 예외
        # URL로 추정되는 경우: 예시 www.mocomsys.com
        # IP주소로 추정되는 경우: 127.0.0.1
        # 숫자가 붙은 제목으로 추정되는 경우 예: 1. 개요
        # ...... <- 점이 여러게 있는 경우 하나로 분리
        super().__init__(r'(?:(?<=\!+)(?!\!)|(?<=\?+)(?!\?)|(?<=\D\.\s)|(?<=\.+)(?!\.)|(?<=。+)(?!。)|(?<=！+)(?!！)|(?<=？)(?!？))')

    def createFromConfig(config:dict) -> MPreprocessor:
        return MPostpositionSeparatorsSplitter()

    def exportToConfig(self) -> dict:
        pass

class MParagraphPunctuationMarkSplitter(MPreprocessor):
    def __init__(self):
        self.splitter = regex.compile(r'(?<=[!?.。！？])(\s*\n)')

    def createFromConfig(config:dict) -> MPreprocessor:
        return MParagraphPunctuationMarkSplitter()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        texts = list(texts)
        for text in texts:
            for text in self.splitter.split(text):
                if 0 == len(text):
                    continue
                yield text

class MListItemSplitter(MPreprocessor):
    '''
    다음과 같은 리스트 항목은 문장 합치기 과정에서 앞 문장과 합쳐질 가능성이 있다.
    가. 항목 내용
    나. 항목 내용
    다. 항목 내용
    
    예를 들면 다음과 같이 병합하는 경우이다.

    가. 항목내용나. 항목내용다. 항목내용

    이런 리스트 항목의 병합을 방지하기 위해 MergeableUnit에서 분리한다.
    '''
    def __init__(self):
        arithmeticSign = r'[×+±÷/]'
        #super().__init__(r'(?=^\s{0,8}(?:[가-하]|\d{1,2}|I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII|XIV|XV|XVI|XVII|XVIII|XIX|XX)\.\s)', regex.MULTILINE)
        # olBullets: 그 자체로 일반 문자열과 구분되지 않아 구분 기호가 추가로 필요한 기호
        # 예시: 다음과 같이 사용하는 경우는 없을 것이라 가정
        # 1 항목 1
        # 2 항목 2
        # 추가 구분자를 사용한 예시
        # 1. 항목 1
        # 2. 항목 2
        #
        # olBullets2: 그 자체로 구분되기 때문에 별다른 기호가 필요치 않은 기호
        # 예시: 다음과 같이 사용할 수 있다고 가정
        # ❶ 항목 1
        # ❷ 항목 2
        # 추가 구분자를 사용한 예시
        # ❶. 항목 1
        # ❷. 항목 2
        olBullets = (
            r'(?:'
            r'['
            r'가-하A-Za-z'
            r'갑을병정무기경신임계'
            r'甲乙丙丁戊己庚辛壬癸'
            r'①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳'
            r'⓿❶❷❸❹❺❻❼❽❾❿⓫⓬⓭⓮⓯⓰⓱⓲⓳⓴'
            r'ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ'
            r'ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ'
            r']'
            r'|\d{1,2}'
            r'|I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII|XIV|XV|XVI|XVII|XVIII|XIX|XX'
            r')'
        )
        # ㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚㉛㉜㉝㉞㉟㊱㊲㊳㊴㊵㊶㊷㊸㊹㊺㊻㊼㊽㊾㊿

        # 예시
        # * 항목 1
        # * 항목 2
        self.bulletSplitter = regex.compile(
            # 공공문서에 한글 ㅇ을 사용하는 경우가 있다.
            # 특이하게도 아래아(ㆍ)를 사용하는 경우도 있다.
            r'^\s*(?![' + arithmeticSign + r'])(?=(?:ㅇ|ㆍ|\p{So}|\p{Sm}|\p{Pd}|\p{Po}|\p{Co})\s)',
            regex.IGNORECASE | regex.MULTILINE
        )

        # 예시
        # (1) 항목 1
        # (2) 항목 2
        self.parenthesesSplitter = regex.compile(r'(?=^\s*\p{Ps}?' + olBullets + r'\p{Pe}\s)', regex.IGNORECASE | regex.MULTILINE)

        # 예시
        # 1. 항목 1
        # 2. 항목 2
        self.numberingSplitter = regex.compile(r'(?=^\s*' + olBullets + r'\p{Po}\s)', regex.IGNORECASE | regex.MULTILINE)

        # 예시
        # ① 항목 1
        self.numberingSplitter2 = regex.compile(
            r'(?=^\s*'
            r'['
            r'①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳'
            r'⓿❶❷❸❹❺❻❼❽❾❿⓫⓬⓭⓮⓯⓰⓱⓲⓳⓴'
            r'ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ'
            r'ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ'
            r']'
            r'\s*(?!' + arithmeticSign + r')'
            r')',
            regex.IGNORECASE | regex.MULTILINE
        )

        # 예시
        # Q1. 문의 1
        # A1. 답변 1
        self.qaSplitter = regex.compile(r'(?=^\s*[QA]\d{1,3}\.)', regex.IGNORECASE | regex.MULTILINE)

    def createFromConfig(config: dict) -> MPreprocessor:
        return MListItemSplitter()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts:Iterable[str]) -> list[str]:
        texts = MListItemSplitter.split(self.bulletSplitter, texts)
        texts = MListItemSplitter.split(self.parenthesesSplitter, texts)
        texts = MListItemSplitter.split(self.numberingSplitter, texts)
        texts = MListItemSplitter.split(self.numberingSplitter2, texts)
        texts = MListItemSplitter.split(self.bulletSplitter, texts)
        texts = MListItemSplitter.split(self.qaSplitter, texts)
        return texts

    @staticmethod
    def split(splitter:regex.Pattern, texts:list[str]):
        splittedTexts = []
        for text in texts:
            for text in splitter.split(text):
                if 0 == len(text):
                    continue
                splittedTexts.append(text)
        return splittedTexts

##############################################################################
# 문장 병합 가능한지 확인
##############################################################################

class MMaxLengthSentenceMergingChecker(MSentenceMergingChecker):
    # TODO: max_sentence_length를 줄일 것
    def __init__(self, max_sentence_length:int = 1024):
        self.max_sentence_length = max_sentence_length

    def createFromConfig(config:dict) -> MSentenceMergingChecker:
        return MMaxLengthSentenceMergingChecker(
            max_sentence_length=config['max_sentence_length']
        )

    def exportToConfig(self) -> dict:
        pass

    def isMergeable(self, sentence1: str, sentence2: str) -> bool:
        if self.max_sentence_length < len(sentence1) + len(sentence2):
            return False
        else:
            return True
            
class MMinLengthSentenceMergingChecker(MSentenceMergingChecker):
    '''
    두 문장 모두, 또는 두 문장 가운데 최소 하나는 일정 길이 이상인 경우에만
    문장 합치기 대상으로 판단한다.

    한 문장이 둘로 쪼개졌다면, 뒷 문장은 짧더라도,
    앞 문장은 한줄을 가득 채울정도로 길기 때문에 잘린다고 가정하고,
    앞 문장이 너무 짧은 경우 에초에 잘린 문장일리 없다는 논리를 사용한다.

    하지만 PPT의 글상자에 쓰여진 글의 한 줄이 바뀌는 글자수와 워드 등의
    한줄이 바뀌는 글자수는 크게 다를 수 있음에 주의해야 한다.

    또한 다른 전처리기에 의해 원래 문장보다 짧게 쪼개진 문장을
    처리하는 경우 이 논리를 적용할 수 없음에도 주의해야 한다.
    '''
    def __init__(self, min_length1:int = 1, min_length2:int = None):
        self.min_length1 = min_length1
        self.min_length2 = min_length2

    def createFromConfig(config:dict) -> MSentenceMergingChecker:
        return MMinLengthSentenceMergingChecker(
            min_length1=config['min_length1'],
            min_length2=config['min_length2'],
        )

    def exportToConfig(self) -> dict:
        return {
            'min_length1': self.min_length1,
            'min_length2': self.min_length2,
        }

    def isMergeable(self, sentence1: str, sentence2: str) -> bool:
        if None != self.min_length1 and len(sentence1) < self.min_length1:
            return False
        if None != self.min_length2 and len(sentence2) < self.min_length2:
            return False
        return True

##############################################################################
# 문장 병합 전처리기
##############################################################################

class MPostpositionPunctuationMarkSplittedTextKeepMergingDropPreprocessor(MPreprocessor):
    def __init__(self):
        self.mergeIfBOSProbabilityLessThen = 0.1
        self.mergeIfEOSProbabilityLessThen = 0.1
        self.dropIfLanguageProbabilityLessThen = 0.5
        self.dropIfBOSProbabilityLessThen = 0.5
        self.dropIfEOSProbabilityLessThen = 0.9

        self.languagePredictor = _MLanguagePredictor()
        self.bosPredictor = MTFHubBertBinaryClassificationPredictor(
            global_val.TFHUB_HANDLE_PREPROCESS,
            global_val.TFHUB_HANDLE_ENCODER,
            global_val.CP_BOS_PREDICTION,
        )
        self.eosPredictor = MTFHubBertBinaryClassificationPredictor(
            global_val.TFHUB_HANDLE_PREPROCESS,
            global_val.TFHUB_HANDLE_ENCODER,
            global_val.CP_EOS_PREDICTION,
        )

    def createFromConfig(config:dict) -> 'MPostpositionPunctuationMarkSplittedTextKeepMergingDropPreprocessor':
        return MPostpositionPunctuationMarkSplittedTextKeepMergingDropPreprocessor()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts:Iterable[str]) -> Generator[str, None, None]:
        for batchTexts in self._getSentenceCutBatchTexts(texts):
            bosPredictions = self.bosPredictor.predict(batchTexts)
            eosPredictions = self.eosPredictor.predict(batchTexts)
            for text in self._processKeepMergingDrop(bosPredictions, eosPredictions, batchTexts):
                yield text

    def _getSentenceCutBatchTexts(self, texts:str) -> Generator[list[str], None, None]:
        batchTexts = []
        for text in texts:
            languageLabel, probabilities = self.languagePredictor.predict(text)
            if probabilities < self.dropIfLanguageProbabilityLessThen:
                if len(batchTexts):
                    yield batchTexts
                else:
                    continue
            if False == self._isSupportedLanguage(languageLabel):
                if len(batchTexts):
                    yield batchTexts
                else:
                    continue
            batchTexts.append(text)
            if len(batchTexts) == _SENTENCE_CUT_PREDICTION_BATCH_SIZE:
                yield batchTexts
                batchTexts = []
        if len(batchTexts):
            yield batchTexts

    def _isSupportedLanguage(self, _:str):
        # TODO: 구현할 것
        return True

    def _processKeepMergingDrop(self, bosPredictions:list[float], eosPredictions:list[float], texts:list[str]) -> list[str]:
        processedTexts:list[str] = []
        lastBOSProbability = None
        lastEOSProbability = None
        lastText = None
        for index, text in enumerate(texts):
            bosProbability = bosPredictions[index]
            eosProbability = eosPredictions[index]
            if None == lastText:
                lastBOSProbability = bosProbability
                lastEOSProbability = eosProbability
                lastText = text
                continue

            # BOS 확률 값을 기반으로 Drop
            if (self.dropIfBOSProbabilityLessThen > lastBOSProbability):
                lastBOSProbability = bosProbability
                lastEOSProbability = eosProbability
                lastText = text
                continue

            # 병합
            if (self.mergeIfEOSProbabilityLessThen > lastEOSProbability
                and self.mergeIfBOSProbabilityLessThen > bosProbability):
                lastEOSProbability = eosProbability
                lastText += text
                continue

            # Keep
            processedTexts.append(lastText)
            lastBOSProbability = bosProbability
            lastEOSProbability = eosProbability
            lastText = text

        if None == lastText:
            return processedTexts

        # EOS 확률 값을 기반으로 Drop
        if (self.dropIfEOSProbabilityLessThen > lastEOSProbability):
            return processedTexts

        processedTexts.append(lastText)
        return processedTexts

class MSentenceMerger(MPreprocessor):
    def __init__(self, merging_checkers: list[MSentenceMergingChecker]):
        self.merging_checkers = merging_checkers

    def createFromConfig(config:dict) -> 'MSentenceMerger':
        return MSentenceMerger(
            merging_checkers=[sentenceMergingCheckerFactory.createInstanceFromConfig(config) for config in config['merging_checkers']],
        )

    def exportToConfig(self) -> dict:
        return {
            'merging_checkers': sentenceMergingCheckerFactory.exportInstanceToConfig(self.merging_checkers)
        }

    def preprocess(self, texts:Iterable) -> Iterable:
        last_text = None
        for text in texts:
            if None == last_text:
                last_text = text
                continue

            if self._isMergeable(last_text, text):
                last_text = last_text + text
            else:
                yield last_text
                last_text = text

        if None != last_text:
            yield last_text

    def _isMergeable(self, sentence1: str, sentence2: str) -> bool:
        for merging_examiner in self.merging_checkers:
            if False == merging_examiner.isMergeable(sentence1, sentence2):
                return False
        return True


##############################################################################
# 문장 단위 제거
##############################################################################

class MInstanceFilter(MPreprocessor):
    def __init__(self, types:list[type], whitelist:bool):
        self.types = types
        self.whitelist = whitelist

    def createFromConfig(config:dict) -> MPreprocessor:
        return MInstanceFilter()

    def exportToConfig(self) -> dict:
        return {
            'types': [_type.__name__ for _type in self.types]
        }

    def preprocess(self, texts:Iterable[Any]) -> Iterable[Any]:
        types_tuple = tuple(self.types)
        for text in texts:
            if self.whitelist == isinstance(text, types_tuple):
                yield text

class MEmptyTextFilter(MPreprocessor):
    def createFromConfig(config:dict) -> MPreprocessor:
        return MEmptyTextFilter()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            if 0 == len(text.strip()):
                continue
            yield text

class MMinLengthFilter(MPreprocessor):
    def __init__(self, min_length:int):
        self.min_length = min_length

    def createFromConfig(config:dict) -> MPreprocessor:
        return MMinLengthFilter(
            min_length=config['min_length']
        )

    def exportToConfig(self) -> dict:
        return {
            'min_length': self.min_length
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            if len(text) < self.min_length:
                continue

            yield text

class MMinLetterFilter(MPreprocessor):
    '''
    최소 글자 수로 거름
    '''
    def __init__(self, minLetterCount:int):
        self.minLetterCount = minLetterCount

        self.matcher = regex.compile(r'\p{L}')

    def createFromConfig(config:dict) -> MPreprocessor:
        return MMinLengthFilter(
            minLetterCount=config['minLetterCount']
        )

    def exportToConfig(self) -> dict:
        return {
            'minLetterCount': self.minLetterCount
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            if len(self.matcher.findall(text)) <= self.minLetterCount:
                continue
            yield text

class MMinTokenFilter(MPreprocessor):
    def __init__(self, minTokenCount:int):
        self.minTokenCount = minTokenCount

        self.splitter = regex.compile(r'[\r\n\t ]+')

    def createFromConfig(config:dict) -> MPreprocessor:
        return MMinTokenFilter(
            minTokenCount=config['minTokenCount']
        )

    def exportToConfig(self) -> dict:
        return {
            'minTokenCount': self.minTokenCount
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            if sum([1 if len(token.strip()) else 0 for token in self.splitter.split(text)]) <= self.minTokenCount:
                continue
            yield text

class MMaxWordLengthFilter(MPreprocessor):
    def __init__(self, maxWordLength:int):
        self.maxWordLength = maxWordLength

        self.wordFinder = regex.compile(r'\p{L}+')

    def createFromConfig(config:dict) -> MPreprocessor:
        return MMaxWordLengthFilter()

    def exportToConfig(self) -> dict:
        return {
            'maxWordLength': self.maxWordLength
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            founds = self.wordFinder.findall(text)
            if len(max(founds, key=len)) > self.maxWordLength:
                continue
            yield text

class MMaxWordAtLeastFilter(MPreprocessor):
    def __init__(self, maxWordAtLeast:int):
        self.maxWordAtLeast = maxWordAtLeast

        self.wordFinder = regex.compile(r'\p{L}+')

    def createFromConfig(config:dict) -> MPreprocessor:
        return MMaxWordAtLeastFilter(
            maxWordAtLeast=config['maxWordAtLeast']
        )

    def exportToConfig(self) -> dict:
        return {
            'maxWordAtLeast': self.maxWordAtLeast
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            founds = self.wordFinder.findall(text)
            maxWordLen = len(max(founds, key=len)) if len(founds) else 0
            if maxWordLen < self.maxWordAtLeast:
                continue
            yield text

class MPartialSentenceFilter(MPreprocessor):
    def __init__(self, bosProbabilityAtLeast:float, eosProbabilityAtLeast:float) -> None:
        self.bosProbabilityAtLeast = bosProbabilityAtLeast
        self.eosProbabilityAtLeast = eosProbabilityAtLeast

    def createFromConfig(config:dict) -> MPreprocessor:
        return MPartialSentenceFilter(
            bosProbabilityAtLeast=config['bosProbabilityAtLeast'],
            eosProbabilityAtLeast=config['eosProbabilityAtLeast'],
        )

    def exportToConfig(self) -> dict:
        return {
            'bosProbabilityAtLeast': self.bosProbabilityAtLeast,
            'eosProbabilityAtLeast': self.eosProbabilityAtLeast,
        }

    def preprocess(self, texts:Iterable[tuple]) -> Generator[str, None, None]:
        for text, bosProbability, eosProbability in texts:
            if bosProbability < self.bosProbabilityAtLeast:
                continue

            if eosProbability < self.eosProbabilityAtLeast:
                continue

            yield text

class MKeepSkipFilter(MPreprocessor):
    class Pattern:
        def is_keep(self) -> bool:
            pass

        def get_count(self) -> int:
            pass
    
    class Keep(Pattern):
        def __init__(self, count:int):
            self.count = count

        def is_keep(self) -> bool:
            return True

        def get_count(self) -> int:
            return self.count

    class Skip(Pattern):
        def __init__(self, count:int):
            self.count = count

        def is_keep(self) -> bool:
            return False

        def get_count(self) -> int:
            return self.count

    def __init__(self, pattern:list[Pattern]):
        '''
        pattern[i][0] = Type(KEEP or SKIP)
        pattern[i][1] = count
        '''
        self.pattern = pattern

    def createFromConfig(config:dict) -> MPreprocessor:
        return MKeepSkipFilter(
            pattern=config['pattern'],
        )

    def exportToConfig(self) -> dict:
        return {
            'pattern': self.pattern,
        }

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        '''
        전체 texts가 1000개이고 self.limit이 100이면 100개만 잘라 리턴한다.
        전체 texts가 10개이고 self.limit이 100이면 10개모두를 리턴한다.
        '''
        pattern_i = 0
        i = 0
        curpattern = self.pattern[pattern_i]
        next_i = curpattern.get_count()
        for text in texts:
            if curpattern.is_keep():
                yield text
            i += 1
            if next_i == i:
                pattern_i += 1
                if len(self.pattern) == pattern_i:
                    i = 0
                    pattern_i = 0
                    next_i = 0
                curpattern = self.pattern[pattern_i]
                next_i += curpattern.get_count()

class MCountLimitter(MPreprocessor):
    def __init__(self, limit:int):
        self.limit=limit

    def createFromConfig(config:dict) -> MPreprocessor:
        return MCountLimitter(
            limit=config['limit'],
        )

    def exportToConfig(self) -> dict:
        return {
            'limit': self.limit,
        }

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        '''
        전체 texts가 1000개이고 self.limit이 100이면 100개만 잘라 리턴한다.
        전체 texts가 10개이고 self.limit이 100이면 10개를 리턴한다.
        '''
        slice = islice(texts, self.limit)
        for text in slice:
            yield text

class MSourceCodeSemicolonFilter(MPreprocessor):
    '''
    세미콜론 유무로 소스코드를 판단하고 제거한다.

    maxSemicolonCount=1로 설정하는 경우 세미콜론을 최대 1개까지는 허용하고
    2개 이상부터 제거한다는 의미이다.
    '''
    def __init__(self, maxSemicolonCount:int):
        self.maxSemicolonCount = maxSemicolonCount

        self.semicolonFinder = regex.compile(r';\s')

    def createFromConfig(config:dict) -> MPreprocessor:
        return MSourceCodeSemicolonFilter(
            maxSemicolonCount=config['maxSemicolonCount'],
        )

    def exportToConfig(self) -> dict:
        return {
            'maxSemicolonCount': self.maxSemicolonCount,
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            if len(self.semicolonFinder.findall(text)) > self.maxSemicolonCount:
                continue
            yield text

class MSourceCodeCommentFilter(MPreprocessor):
    '''
    /* 어떤 주석 */

    위와 같은 형식을 걸러낸다.
    '''
    def __init__(self):
        self.commentBeginFinder = regex.compile(r'/\*')
        self.commentEndFinder = regex.compile(r'\*/')

    def createFromConfig(config:dict) -> MPreprocessor:
        return MSourceCodeCommentFilter()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            if len(self.commentBeginFinder.findall(text)) or len(self.commentEndFinder.findall(text)):
                continue
            yield text

class MSourceCodePatternFilter(MPreprocessor):
    def __init__(self):
        self.patterns = [
            # 정규식, 임계 치
            (regex.compile(r';[\s$]', regex.MULTILINE), 0), # ;
            (regex.compile(r'/\*'), 0), # /*
            (regex.compile(r'\*/'), 0), # */
            (regex.compile(r'//'), 0), # //
            (regex.compile(r'\./[a-zA-Z]'), 0), # 예시: ./some/path
            (regex.compile(r'--[a-z]'), 0), # 예시: --some-flag
            (regex.compile(r'\\u[0-9A-Za-z]{4}'), 0), # 예시: \u0020
            (regex.compile(r'#(?:if|elif|else|endif|define|undef|pargma|include)'), 0), # C언어 #키워드
            (regex.compile(r'(?<!\S)(?:if|for|foreach|while|echo|print|_dump|_r)\s?\('), 0), # C언어, PHP등 괄호 열기 함수 호출...
            (regex.compile(
                r'(?:SELECT |INSERT INTO |VALUES\s?\(|CREATE TABLE |DROP TABLE |ALTER TABLE |TRUNCATE TABLE |'
                r'GRANT ALL |REVOKE ALL |DELETE FROM |COMMIT|ROLLBACK)'
            ), 0), # SQL 키워드
            (regex.compile(r'(?<!\S)[a-z]{2,}[A-Z][a-z]', regex.MULTILINE), 0), # camelCase, 단 eMail, iPhone등 1글자 인 경우 제외
            (regex.compile(r'(?<!\S)[a-z][A-Z][a-z]{2,}[A-Z][a-z]', regex.MULTILINE), 0), # camelCase, 단, 소문자 1글자로 시작하고 대문자가 2번 이상 반복
            (regex.compile(r'(?<!\S)[A-Z]{1,5}[a-z]{2,}[A-Z][a-z]', regex.MULTILINE), 0), # PascalCase
            (regex.compile(r'(?<!\S)[a-z]{2,}_[a-z]', regex.MULTILINE), 0), # snake_case
            (regex.compile(r'(?<!\S)[A-Z]{2,}_[A-Z]', regex.MULTILINE), 0), # SCREAMING_SNAKE_CASE
            (regex.compile(r'[\{\s,]".{1,32}"\s?:\s?[\dtfn"]'), 0), # JSON
            (regex.compile(r'[\\/"\'\{\}\[\]\(\)=]'), 5), # 너무 많은 코딩용 특수 기호
            (regex.compile(r'[A-Za-z0-9+/]{4,}='), 1), # Base64
        ]

    def createFromConfig(config:dict) -> MPreprocessor:
        return MSourceCodePatternFilter()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            source = False
            for finder, allowCount in self.patterns:
                if len(finder.findall(text)) > allowCount:
                    source = True
                    break
            if source:
                continue
            yield text

class MLanguageFilter(MPreprocessor):
    '''
    /* 어떤 주석 */

    위와 같은 형식을 걸러낸다.
    '''
    def __init__(self, languages:set):
        self.languages = set(languages)

    def createFromConfig(config:dict) -> MPreprocessor:
        return MLanguageFilter()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            (language,), _ = languagePredictor.predict(text)
            if language not in self.languages:
                continue
            yield text

class MFollowedBySameTextFilter(MPreprocessor):
    def createFromConfig(config:dict) -> MPreprocessor:
        return MFollowedBySameTextFilter()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        lastSentence = None
        for text in texts:
            if None == lastSentence:
                lastSentence = text
                continue
            if lastSentence == text:
                continue
            yield lastSentence
            lastSentence = text
        if None != lastSentence:
            yield lastSentence

##############################################################################
# 문장 복사
##############################################################################

class MDuplicator:
    def __init__(self, count:int):
        self.count=count

    def createFromConfig(config:dict) -> MPreprocessor:
        return MDuplicator(
            count=config['count'],
        )

    def exportToConfig(self) -> dict:
        return {
            'count': self.count,
        }

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        for text in texts:
            for _ in range(self.count):
                yield text

##############################################################################
# 문장 자르기
##############################################################################

class MRandomHeadCutter(MPreprocessor):
    '''
    문장의 앞 부분을 무작위로 잘라냄
    '''
    def __init__(self, cut_at_least:int, seed:Any=None):
        '''
        cut_at_least = 잘라낼 최소 크기
        '''
        self.cut_at_least = cut_at_least
        self.seed = seed

    def createFromConfig(config:dict) -> MPreprocessor:
        kwargs = {}

        if 'seed' in config: kwargs['seed']=config['seed']

        return MRandomHeadCutter(
            cut_at_least=config['cut_at_least'],
            **kwargs
        )

    def exportToConfig(self) -> dict:
        return {
            'cut_at_least': self.cut_at_least,
            'seed': self.seed
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        rng = Random(self.seed) if None != self.seed else Random()

        for text in texts:
            if len(text) <= self.cut_at_least:
                # 최소 크기보다 작거나 같은 길이의 문장은 전체 문장이 잘려 나가는 경우로 처리 함
                yield ''
            else:
                curpos = len(text) - rng.randint(self.cut_at_least, len(text) - self.cut_at_least)
                yield text[curpos:]

class MRandomTailCutter(MPreprocessor):
    '''
    문장의 뒷 부분을 무작위로 잘라냄
    '''
    def __init__(self, cut_at_least:int, seed:Any=None):
        '''
        cut_at_least = 잘라낼 최소 크기
        '''
        self.cut_at_least = cut_at_least
        self.seed = seed

    def createFromConfig(config:dict) -> MPreprocessor:
        kwargs = {}

        if 'seed' in config: kwargs['seed']=config['seed']

        return MRandomHeadCutter(
            cut_at_least=config['cut_at_least'],
            **kwargs
        )

    def exportToConfig(self) -> dict:
        return {
            'cut_at_least': self.cut_at_least,
            'seed': self.seed
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        rng = Random(self.seed) if None != self.seed else Random()

        for text in texts:
            if len(text) <= self.cut_at_least:
                # 최소 크기보다 작거나 같은 길이의 문장은 전체 문장이 잘려 나가는 경우로 처리 함
                yield ''
            else:
                cutpos = rng.randint(self.cut_at_least, len(text) - self.cut_at_least)
                yield text[:cutpos]

class MMaxLengthHeadCutter(MPreprocessor):
    '''
    한 문장의 길이가 max_length보다 크면 앞 부분을 잘라내고 뒷 부분을 남김
    '''
    def __init__(self, max_length:int):
        self.max_length = max_length

    def createFromConfig(config:dict) -> MPreprocessor:
        return MMaxLengthHeadCutter(
            max_length=config['max_length'],
        )

    def exportToConfig(self) -> dict:
        return {
            'max_length': self.max_length,
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            if len(text) > self.max_length:
                text = text[len(text) - self.max_length:]
            yield text

class MMaxLengthTailCutter(MPreprocessor):
    '''
    한 문장의 길이가 max_length보다 크면 뒷 부분을 잘라내고 앞부분을 남김
    '''
    def __init__(self, max_length:int):
        self.max_length = max_length

    def createFromConfig(config:dict) -> MPreprocessor:
        return MMaxLengthTailCutter(
            max_length=config['max_length'],
        )

    def exportToConfig(self) -> dict:
        return {
            'max_length': self.max_length,
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            if len(text) > self.max_length:
                text = text[:self.max_length]
            yield text

class MSplitAndPickFirst(MPreprocessor):
    def __init__(self, splitter:MPreprocessor):
        self.splitter = splitter

    def createFromConfig(config:dict) -> MPreprocessor:
        return MSplitAndPickFirst(
            splitter=preprocessorFactory.createInstanceFromConfig(config['splitter']),
        )

    def exportToConfig(self) -> dict:
        return {
            'splitter': preprocessorFactory.exportInstanceToConfig(self.splitter),
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        '''
        예시
        자르는 방식: .으로 자름

        입력:
        동해물과. 백두산이. 마르고. 닳도록.

        출력:
        동해물과.
        '''
        for text in texts:
            splitted_text = self.splitter.preprocess([text])
            for text in splitted_text:
                yield text
                break

class MSplitAndPickLast(MPreprocessor):
    def __init__(self, splitter:MPreprocessor):
        self.splitter = splitter

    def createFromConfig(config:dict) -> MPreprocessor:
        return MSplitAndPickLast(
            splitter=preprocessorFactory.createInstanceFromConfig(config['splitter']),
        )

    def exportToConfig(self) -> dict:
        return {
            'splitter': preprocessorFactory.exportInstanceToConfig(self.splitter),
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        '''
        예시
        자르는 방식: .으로 자름

        입력:
        동해물과. 백두산이. 마르고. 닳도록.

        출력:
         닳도록.
        '''
        for text in texts:
            splitted_text = self.splitter.preprocess([text])
            for text in splitted_text:
                pass
            yield text

class MSplitAndMergingForward(MPreprocessor):
    def __init__(self, splitter:MPreprocessor):
        self.splitter = splitter

    def createFromConfig(config:dict) -> MPreprocessor:
        return MSplitAndMergingForward(
            splitter=preprocessorFactory.createInstanceFromConfig(config['splitter']),
        )

    def exportToConfig(self) -> dict:
        return {
            'splitter': preprocessorFactory.exportInstanceToConfig(self.splitter),
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        '''
        예시
        자르는 방식: .으로 자름

        입력:
        동해물과. 백두산이. 마르고. 닳도록.

        출력:
        동해물과.
        동해물과. 백두산이.
        동해물과. 백두산이. 마르고.
        동해물과. 백두산이. 마르고. 닳도록.
        '''
        for text in texts:
            splitted_texts = list(self.splitter.preprocess([text]))
            merging = []
            for splitted_text in splitted_texts:
                merging.append(splitted_text)
                yield ''.join(merging)

class MSplitAndMergingBackward(MPreprocessor):
    def __init__(self, splitter:MPreprocessor):
        self.splitter = splitter

    def createFromConfig(config:dict) -> MPreprocessor:
        return MSplitAndMergingBackward(
            splitter=preprocessorFactory.createInstanceFromConfig(config['splitter']),
        )

    def exportToConfig(self) -> dict:
        return {
            'splitter': preprocessorFactory.exportInstanceToConfig(self.splitter),
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        '''
        예시
        자르는 방식: .으로 자름

        입력:
        동해물과. 백두산이. 마르고. 닳도록.

        출력:
        닳도록.
        마르고. 닳도록.
        백두산이. 마르고. 닳도록.
        동해물과. 백두산이. 마르고. 닳도록.
        '''
        for text in texts:
            splitted_texts = list(self.splitter.preprocess([text]))
            merging = []
            for splitted_text in reversed(splitted_texts):
                merging.append(splitted_text)
                yield ''.join(reversed(merging))

##############################################################################
# 문장 내용 수정
##############################################################################

class MUpperCaseConverter(MPreprocessor):
    def createFromConfig(config:dict) -> MPreprocessor:
        return MUpperCaseConverter()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        for text in texts:
            yield text.upper()

class MLowerCaseConverter(MPreprocessor):
    def createFromConfig(config:dict) -> MPreprocessor:
        return MLowerCaseConverter()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        for text in texts:
            yield text.lower()

class MPunctuationRemover(MPreprocessor):
    '''
    글자, 숫자, 공백을 제외한 모든 특수 문자 제거
    '''

    def createFromConfig(config:dict) -> MPreprocessor:
        return MPunctuationRemover()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        for text in texts:
            yield regex.sub(r'([^\w\s])+', '', text)

class MTrimmer(MPreprocessor):
    def __init__(self, chars:str):
        self.chars = chars

    def createFromConfig(config:dict) -> MPreprocessor:
        return MTrimmer(
            chars=config['chars'],
        )

    def exportToConfig(self) -> dict:
        return {
            'chars': self.chars
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            text = text.strip(self.chars)
            yield text

class MWhitespaceTrimmer(MPreprocessor):

    def createFromConfig(config:dict) -> MPreprocessor:
        return MWhitespaceTrimmer()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            yield text.strip()

class MWhiteSpaceCompactor(MRegExReplacer):
    def __init__(self):
        super().__init__(r'\s+', regex.MULTILINE, ' ')

    def createFromConfig(config:dict) -> MPreprocessor:
        return MWhiteSpaceCompactor()

    def exportToConfig(self) -> dict:
        pass

class MPunctuationCompactor(MRegExReplacer):
    def __init__(self):
        super().__init__(r'(\p{P})\1{2,}', regex.MULTILINE, r'\1\1')

    def createFromConfig(config:dict) -> MPreprocessor:
        return MPunctuationCompactor()

    def exportToConfig(self) -> dict:
        pass

class MRepeatWordCompactor(MPreprocessor):
    def __init__(self, minRepeat:int):
        self.compactor = regex.compile(r'(\p{L}+\s+)\1{' + str(int(minRepeat - 1)) + r',}', regex.MULTILINE)

    def createFromConfig(config:dict) -> MPreprocessor:
        return MRepeatWordCompactor()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            processedText = self.compactor.sub(r'\1', text)
            while processedText != text:
                text = processedText
                processedText = self.compactor.sub(r'\1', text)
            yield processedText

class MPUARemover(MRegExReplacer):
    def __init__(self):
        super().__init__(r'\p{Co}+', 0, '')

    def createFromConfig(config:dict) -> MPreprocessor:
        return MPUARemover()

    def exportToConfig(self) -> dict:
        pass

class MNonBMPRemover(MRegExReplacer):
    def __init__(self):
        super().__init__(
            '[^'
            + str(b'\x00\x00', encoding='utf-16-be') + '-' + str(b'\xFF\xFF', encoding='utf-16-be')
            + ']+',
            0,
            ''
        )

    def createFromConfig(config:dict) -> MPreprocessor:
        return MNonBMPRemover()

    def exportToConfig(self) -> dict:
        pass


class MListItemBulletRemover(MPreprocessor):
    def __init__(self):
        arithmeticSign = r'[×+±÷/]'
        # olBullets: 그 자체로 일반 문자열과 구분되지 않아 구분 기호가 추가로 필요한 기호
        # 예시: 다음과 같이 사용하는 경우는 없을 것이라 가정
        # 1 항목 1
        # 2 항목 2
        # 추가 구분자를 사용한 예시
        # 1. 항목 1
        # 2. 항목 2
        #
        # olBullets2: 그 자체로 구분되기 때문에 별다른 기호가 필요치 않은 기호
        # 예시: 다음과 같이 사용할 수 있다고 가정
        # ❶ 항목 1
        # ❷ 항목 2
        # 추가 구분자를 사용한 예시
        # ❶. 항목 1
        # ❷. 항목 2
        olBullets = (
            r'(?:'
            r'['
            r'가-하A-Za-z'
            r'갑을병정무기경신임계'
            r'甲乙丙丁戊己庚辛壬癸'
            r'①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳'
            r'⓿❶❷❸❹❺❻❼❽❾❿⓫⓬⓭⓮⓯⓰⓱⓲⓳⓴'
            r'ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ'
            r'ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ'
            r']'
            r'|\d{1,2}'
            r'|I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII|XIV|XV|XVI|XVII|XVIII|XIX|XX'
            r')'
        )

        # 예시
        # * 항목 1
        # * 항목 2
        # 공공문서에 한글 ㅇ을 사용하는 경우가 있다.
        # 특이하게도 아래아(ㆍ)를 사용하는 경우도 있다.
        self.bulletRemover = regex.compile(r'^\s*(ㅇ|ㆍ|\p{So}|\p{Sm}|\p{Pd}|\p{Po}|\p{Co})(?!\1)\s+', regex.IGNORECASE)

        # 예시
        # (1) 항목 1
        # (2) 항목 2
        self.parenthesesRemover = regex.compile(r'^\s*\p{Ps}?' + olBullets + r'\p{Pe}\s+', regex.IGNORECASE)

        # 예시
        # 1. 항목 1
        # 2. 항목 2
        self.numberingRemover = regex.compile(r'^\s*' + olBullets + r'\p{Po}\s+', regex.IGNORECASE)

        # 예시
        # ① 항목 1
        self.numberingRemover2 = regex.compile(
            r'(?>'
            r'^\s*'
            r'['
            r'①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳'
            r'⓿❶❷❸❹❺❻❼❽❾❿⓫⓬⓭⓮⓯⓰⓱⓲⓳⓴'
            r'ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ'
            r'ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ'
            r']'
            r'\s*'
            r')'
            r'(?!' + arithmeticSign + r')',
            regex.IGNORECASE
        )

    def createFromConfig(config:dict) -> MPreprocessor:
        return MListItemBulletRemover()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            bulletRemoved = self.bulletRemover.sub('', text)
            if bulletRemoved == text:
                bulletRemoved = self.parenthesesRemover.sub('', text)
            if bulletRemoved == text:
                bulletRemoved = self.numberingRemover.sub('', text)
            if bulletRemoved == text:
                bulletRemoved = self.numberingRemover2.sub('', text)
            yield bulletRemoved

class MTabToSpaceConverter(MPreprocessor):
    def createFromConfig(config:dict) -> MPreprocessor:
        return MTabToSpaceConverter()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            yield text.replace('\t', '\n')

##############################################################################
# 문자열 코덱
#
# 문자열 코덱 전처리기는 다른 전처리기와 달리 문자열이 아닌 값들을 리턴하고,
# 규칙역시 다른 전처리기와 다르다.
#
# 예를 들어 MLineSplitter는 배열을 입력 받아 각 항목을 newline(\n) 기호로 분리한 후
# 리스트의 쪼개진 배열을 병합해 하나의 배열로 반환한다.
# 예: 1개 항목(문자열)을 가진 입력 배열 -> 2개 항목(문자열)을 가진 출력 배열
# ['안녕하세요.\n세상'] -> ['안녕하세요.', '세상']
#
# 반면 코덱 전처리기, 예를 들어 MJsonDecoder는 입력된 리스트의 Json문자열을 객체로
# 변한한 후 그 배열을 반환한다.
# 예: 1개 항목(문자열)을 가진 입력 배열 -> 1개의 항목(객체)을 가진 출력 배열
# ['{"greeding": "안녕하세요.", "to": "세상"}']
# -> [{"greeding": "안녕하세요.", "to": "세상"}]
#
# 이렇게 쪼개진 값을 전처리기의 최종 출력으로 하여 그대로 사용하거나,
# 전처리기가 객체를 입력 받은 경우 Encoder를 사용해 문자열로 변경할 수 있다.
# 또는 MJsonDecoder로 쪼개진 값을 MDictToTupleFilter와 MTupleTextJoiner등
# 데이터 변환 전처기기를 이용해 객체를 문자열로 변환해 사용할 수도 있다.
#
# 이는 TSVDecoder등 다른 코덱도 마찬가지이다.
##############################################################################

class MJsonEncoder(MPreprocessor):
    def createFromConfig(config:dict) -> MPreprocessor:
        return MJsonEncoder()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            yield json.dumps(text, ensure_ascii=False)

class MJsonDecoder(MPreprocessor):
    def createFromConfig(config:dict) -> MPreprocessor:
        return MJsonDecoder()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            yield json.loads(text)

class MTsvEncoder(MPreprocessor):
    def createFromConfig(config:dict) -> MPreprocessor:
        return MTsvEncoder()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts:Iterable[Iterable[str]]) -> Iterable[str]:
        for columns in texts:
            yield '\t'.join(
                # FIXME: 버그 있 음
                [str(column).replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r') for column in columns]
            )

class MTsvDecoder(MPreprocessor):
    type_factory = {
        int.__name__: int,
        str.__name__: str,
    }
    def __init__(self, types:list = None):
        self.types = types

    def createFromConfig(config:dict) -> MPreprocessor:
        kwargs = []

        if 'types' in config:
            kwargs['types'] = config['types']

        return MTsvDecoder(
            **kwargs
        )

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            decoded = []
            for index, column in enumerate(text.split('\t')):
                column = column.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')
                if None == self.types:
                    decoded.append(column)
                else:
                    decoded.append(self.type_factory[self.types[index]](column))
            yield tuple(decoded)

##############################################################################
# 객체간 변환
##############################################################################

class MDictToTupleFilter(MPreprocessor):
    def __init__(self, paths:list):
        self.paths = paths

    def createFromConfig(config:dict) -> MPreprocessor:
        return MDictToTupleFilter(
            paths=config['paths'],
        )

    def exportToConfig(self) -> dict:
        return {
            'paths': self.paths,
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for dobj in texts:
            yield tuple([dpath.util.get(dobj, path) for path in self.paths])

class MDictToValueFilter(MPreprocessor):
    def __init__(self, path:str):
        self.path = path

    def createFromConfig(config:dict) -> MPreprocessor:
        return MDictToValueFilter(
            path=config['path'],
        )

    def exportToConfig(self) -> dict:
        return {
            'path': self.path,
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for dobj in texts:
            yield dpath.util.get(dobj, self.path)

class MTupleToTupleFilter(MPreprocessor):
    def __init__(self, index:list):
        self.index = index

    def createFromConfig(config:dict) -> MPreprocessor:
        return MTupleToTupleFilter(
            index=config['index'],
        )

    def exportToConfig(self) -> dict:
        return {
            'index': self.index,
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            yield tuple([text[index] for index in self.index])

class MTupleToValueFilter(MPreprocessor):
    def __init__(self, index:str):
        self.index = index

    def createFromConfig(config:dict) -> MPreprocessor:
        return MTupleToValueFilter(
            index=config['index'],
        )

    def exportToConfig(self) -> dict:
        return {
            'index': self.index,
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for text in texts:
            yield text[self.index]

class MTupleTextJoiner():
    def __init__(self, joinstr:str):
        self.joinstr = joinstr

    def createFromConfig(config:dict) -> MPreprocessor:
        return MTupleTextJoiner(
            joinstr=config['joinstr'],
        )

    def exportToConfig(self) -> dict:
        return {
            'joinstr': self.joinstr,
        }

    def preprocess(self, texts:Iterable[str]) -> Iterable[str]:
        for strs in texts:
            yield self.joinstr.join(strs)

##############################################################################
# 순서 섞기
##############################################################################

class MRandomShuffler(MPreprocessor):
    def __init__(self, buffer_size:int=None, seed:Any=None):
        self.buffer_size = buffer_size
        self.seed = seed

    def createFromConfig(config:dict) -> MPreprocessor:
        kwargs = {}
        if 'buffer_size' in config['buffer_size']: kwargs['buffer_size'] = config['buffer_size']
        if 'seed' in config['seed']: kwargs['seed'] = config['seed']

        return MRandomShuffler(
            **kwargs,
        )

    def exportToConfig(self) -> dict:
        return {
            'buffer_size': self.buffer_size,
            'seed': self.seed,
        }

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        rng = Random(self.seed) if None != self.seed else Random()

        if self.buffer_size:
            i = iter(texts)
            while True:
                buffer = []
                try:
                    [buffer.append(next(i)) for _ in range(self.buffer_size)]
                except StopIteration:
                    break
                finally:
                    if len(buffer):
                        rng.shuffle(buffer)
                        for text in buffer:
                            yield text
        else:
            texts = list(texts)
            rng.shuffle(texts)
            for text in texts:
                yield text

class FileLineRandomShuffler(MPreprocessor):
    def __init__(self, seed:Any=None):
        self.seed = seed

    def createFromConfig(config:dict) -> MPreprocessor:
        kwargs = {}
        if 'seed' in config: kwargs['seed'] = config['seed']

        return FileLineRandomShuffler(
            **kwargs,
        )

    def exportToConfig(self) -> dict:
        return {
            'seed': self.seed,
        }

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        texts = list(texts)
        preprocessors = [MCompositePreprocessor([
            MTextFileLineReader(),
            MRandomShuffler(seed=self.seed, buffer_size=None),
            MTextFileLineWriter(filename=filename),
        ]) for filename in texts]
        for preprocessor in preprocessors:
            for text in preprocessor.preprocess(texts):
                yield text

##############################################################################
# 파일 처리
##############################################################################

class MDirectoryReader(MPreprocessor):
    def __init__(self, recursive:bool=False, filesonly:bool=True, fullpath:bool=True):
        self.recursive = recursive
        self.filesonly = filesonly
        self.fullpath = fullpath

    def createFromConfig(config:dict) -> MPreprocessor:
        return MDirectoryReader(
            recursive=config['recursive'],
            filesonly=config['filesonly'],
            fullpath=config['fullpath'],
        )

    def exportToConfig(self) -> dict:
        return {
            'recursive': self.recursive,
            'filesonly': self.filesonly,
            'fullpath': self.fullpath,
        }

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        for text in texts:
            for filename in os.listdir(text):
                fullpath = os.path.join(text, filename)
                if False == self.filesonly or os.path.isfile(fullpath):
                    yield fullpath if True == self.fullpath else filename

                if self.recursive and os.path.isdir(fullpath):
                    for rectext in self.preprocess([fullpath]):
                        yield rectext

class MTextFileLineReader(MPreprocessor):

    def createFromConfig(config:dict) -> MPreprocessor:
        return MTextFileLineReader()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        for text in texts:
            with open(text, 'r', encoding='utf-8') as f:
                for line in f:
                    yield regex.sub(r'\n$', '', line)

class MMultiFileRoundRobinReader(MPreprocessor):
    def createFromConfig(config:dict) -> MPreprocessor:
        return MMultiFileRoundRobinReader()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        texts = list(texts)
        generators = [iter(MTextFileLineReader().preprocess([filename])) for filename in texts]
        i = 0
        while True:
            if 0 == len(generators):
                break

            generator_index = i % len(generators)
            generator = generators[generator_index]
            try:
                line = next(generator)
                yield line
                i += 1
            except StopIteration:
                generators.pop(generator_index)
                if 0 == len(generators):
                    break

class MTextFileLineWriter(MPreprocessor):
    def __init__(self, filename:str):
        self.filename = filename

    def createFromConfig(config:dict) -> MPreprocessor:
        return MTextFileLineWriter(
            filename=config['filename'],
        )

    def exportToConfig(self) -> dict:
        return {
            'filename': self.filename,
        }

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        size = 0
        with open(self.filename, 'w', encoding='utf-8') as f:
            for text in texts:
                f.write(text + '\n')
                size += 1
        return [{'filename': self.filename,'size': size}]

class MMultiTextFileLineWriter(MPreprocessor):
    def __init__(self, path:str, each_limit:int, prefix:str, postfix:str):
        self.path = path
        self.each_limit = each_limit
        self.prefix = prefix
        self.postfix = postfix

        self.utilClass = MClassFactory.getUtility()

    def createFromConfig(config:dict) -> MPreprocessor:
        return MMultiTextFileLineWriter(
            path=config['path'],
            each_limit=config['each_limit'],
        )

    def exportToConfig(self) -> dict:
        return {
            'path': self.path,
            'each_limit': self.each_limit,
        }

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        write_count = 0
        filename = self.utilClass.makeUniqueID(self.prefix, self.postfix)
        writer = self._get_next_writer(filename)
        for text in texts:
            if self.each_limit == write_count:
                writer.close()
                yield self._make_result(filename, write_count)
                write_count = 0
                filename = self.utilClass.makeUniqueID(self.prefix, self.postfix)
                writer = self._get_next_writer(filename)

            writer.write(text + '\n')
            write_count += 1

        writer.close()
        if write_count:
            yield self._make_result(filename, write_count)

    def _get_next_writer(self, filename:str) -> TextIOBase:
        return open(os.path.join(self.path, filename), 'w', encoding='utf-8')

    def _make_result(self, filename:str, write_count:int):
        return {
            'path': os.path.join(self.path, filename),
            'size': write_count,
        }

##############################################################################
# 엠파워 파일 처리
##############################################################################

class MDecryptingPreprocessor(MPreprocessor):
    def __init__(self, output_dir:str, output_ext:str='.dec'):
        self.output_dir = output_dir
        self.output_ext = output_ext

    def createFromConfig(config:dict) -> MPreprocessor:
        return MDecryptingPreprocessor(
            output_dir=config['output_dir'],
            output_ext=config['output_ext'],
        )

    def exportToConfig(self) -> dict:
        return {
            'output_dir': self.output_dir,
            'output_ext': self.output_ext,
        }

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        '''
        입력 값: RFile 복호화 정보
        {
            'path':str,
            'enc_mode':int,
            'mrk':str,
        }
        리턴 값: 복호화한 파일 경로
        '''
        crypt = MCrypt()
        for text in texts:
            rfile_name = os.path.basename(text['path'])
            output_file = os.path.join(self.output_dir, rfile_name + self.output_ext)
            crypt.mpowerDecrypt(
                srcPath=text['path'],
                tgtPath=output_file,
                encMode=text['enc_mode'],
                zipMode=text['zip_mode'],
                MRK=text['mrk'],
            )
            yield output_file

##############################################################################
# 텍스트 추출
##############################################################################

class MTextExtractingToFilePreprocessor(MPreprocessor):
    def __init__(self, output_dir:str):
        self.output_dir = output_dir

    def createFromConfig(config:dict) -> MPreprocessor:
        return MTextExtractingToFilePreprocessor(
            output_dir=config['output_dir'],
        )

    def exportToConfig(self) -> dict:
        return {
            'output_dir': self.output_dir,
        }

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        shaai = MShaAI()
        for text in texts:
            _, workDir, corpusList = shaai.extract(
                srcPath=text,
                tgtPath=self.output_dir,
            )

            for corpus in corpusList:
                yield os.path.join(workDir, corpus)

class MTextExtracingToMultiFilePreproessor(MPreprocessor):
    def __init__(self, output_dir:str):
        self.output_dir = output_dir

    def createFromConfig(config:dict) -> MPreprocessor:
        return MTextExtracingToMultiFilePreproessor(
            output_dir=config['output_dir'],
        )

    def exportToConfig(self) -> dict:
        return {
            'output_dir': self.output_dir,
        }

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        # TODO: 구현 할 것
        pass

##############################################################################
# 라벨링
##############################################################################

class MStaticTupleLabeler(MPreprocessor):
    def __init__(self, label:Any):
        self.label = label

    def createFromConfig(config:dict) -> MPreprocessor:
        return MStaticTupleLabeler(
            label=config['label'],
        )

    def exportToConfig(self) -> dict:
        return {
            'label': self.label,
        }

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        for text in texts:
            yield self.label, text

class MStaticDictLabeler(MPreprocessor):
    def __init__(self, label:Any):
        self.label = label

    def createFromConfig(config:dict) -> MPreprocessor:
        return MStaticDictLabeler(
            label=config['label'],
        )

    def exportToConfig(self) -> dict:
        return {
            'label': self.label,
        }

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        for text in texts:
            yield {
                'label': self.label,
                'text': text,
            }

class MTupleBoWEmbedder(MPreprocessor):
    def __init__(self, index:int, bow:dict):
        self.index = index
        self.bow = bow

    def createFromConfig(config:dict) -> MPreprocessor:
        return MTupleBoWEmbedder(
            path=config['index'],
            bow=config['bow'],
        )

    def exportToConfig(self) -> dict:
        return {
            'index': self.index,
            'bow': self.bow,
        }

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        for tobj in texts:
            tobj = list(tobj)
            tobj[self.index] = self.bow[tobj[self.index]]
            yield tuple(tobj)

##############################################################################
## 학습 데이터 읽기
##############################################################################

class MJsonLabeledDatasetReader(MPreprocessor):
    def createFromConfig(config:dict) -> MPreprocessor:
        return MJsonLabeledDatasetReader()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        preprocessor = MCompositePreprocessor([
            MTextFileLineReader(),
            MJsonDecoder(),
            MDictToValueFilter('/path'),
            MTextFileLineReader(),
            MJsonDecoder(),
            MDictToTupleFilter(['/label', '/text'])
        ])
        return preprocessor.preprocess(texts)

class MJsonLabeledDatasetWriter(MPreprocessor):
    def createFromConfig(config:dict) -> MPreprocessor:
        return MJsonLabeledDatasetWriter()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        preprocessor = MCompositePreprocessor([
            # TODO: 구현 할 것
        ])
        return preprocessor.preprocess(texts)

class MJsonLabeledDatasetCounter(MPreprocessor):
    def createFromConfig(config:dict) -> MPreprocessor:
        return MJsonLabeledDatasetCounter()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        preprocessor = MCompositePreprocessor([
            MTextFileLineReader(),
            MJsonDecoder(),
            MDictToValueFilter('/size'),
            MSumAggregator(),
        ])
        return preprocessor.preprocess(texts)

##############################################################################
## 집계
##############################################################################

class MCountAggregator(MPreprocessor):
    def createFromConfig(config:dict) -> MPreprocessor:
        return MCountAggregator()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        return [sum([1 for _ in texts])]

class MSumAggregator(MPreprocessor):
    def createFromConfig(config:dict) -> MPreprocessor:
        return MSumAggregator()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        return [sum([int(text) for text in texts])]

##############################################################################
## 위키 코퍼스 전처리기
##############################################################################

class MWikiXmlToJson(MPreprocessor):
    def createFromConfig(config:dict) -> MPreprocessor:
        return MWikiXmlToJson()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        '''
        입력 값: (xml_path, output_dir)의 tuple 리스트
        출력 값: output_dir
        '''
        for xml_path, output_dir in texts:
            completed_process = subprocess.run([
                sys.executable,
                '-m', 'wikiextractor.WikiExtractor',
                '--json',
                '-o', output_dir,
                xml_path,
            ],
            capture_output=True)
            if len(completed_process.stderr):
                raise RuntimeError(str(completed_process.stderr))

            yield output_dir

class MWikiJsonReader(MPreprocessor):
    def createFromConfig(config:dict) -> MPreprocessor:
        return MWikiJsonReader()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        '''
        입력 값: json 파일이 있는 폴더 경로
        '''
        preprocessor = MCompositePreprocessor([
            MDirectoryReader(recursive=True, filesonly=True, fullpath=True),
            MTextFileLineReader(),
            MJsonDecoder(),
            MDictToValueFilter('/text'),
        ])
        return preprocessor.preprocess(texts)

##############################################################################
# fasttext language predictor
##############################################################################

class _MLanguagePredictor:
    def __init__(self):
        self.model = fasttext.load_model(global_val.FASTTEXT_MODEL_PATH)

    def predict(self, text: str, k: int = 1):
        '''
        문장의 언어를 예측하는 함수.
        k = 몇 개의 언어 예측을 반환할지
        '''

        def remove_label_prefix(prediction: str):
            '''
            fasttext의 결과 값은 __label__ko 형식으로 리턴된다.
            앞에 있는 __label__을 제거하는 함수이다.
            '''
            return regex.sub(r'^__label__', '', prediction)

        def remove_label_prefixes(predictions):
            return tuple([remove_label_prefix(prediction) for prediction in predictions])

        (labels, probabilities) = self.model.predict(text, k=k)

        return (remove_label_prefixes(labels), probabilities)

languagePredictor = _MLanguagePredictor()

##############################################################################
# fasttext Preprocessor
##############################################################################

class MSameLanguageSentenceMergingChecker(MSentenceMergingChecker):
    def createFromConfig(config:dict) -> MSentenceMergingChecker:
        return MSameLanguageSentenceMergingChecker()

    def exportToConfig(self):
        pass

    def isMergeable(self, sentence1: str, sentence2: str) -> bool:
        (sentence1_lang_ids, _) = languagePredictor.predict(sentence1)
        (sentence2_lang_ids, _) = languagePredictor.predict(sentence2)

        return sentence1_lang_ids[0] == sentence2_lang_ids[0]

##############################################################################
# NLTK Preprocessor
##############################################################################

class MWesternSentenceSplitter(MPreprocessor):
    '''
    nltk를 사용하여 문장을 분리한다.
    '''
    _nltk_language_map = {
        'cs': 'czech',
        'da': 'danish',
        'nl': 'dutch',
        'en': 'english',
        'et': 'estonian',
        'fi': 'finnish',
        'fr': 'french',
        'de': 'german',
        'el': 'greek',
        'it': 'italian',
        'nn': 'norwegian',
        'pl': 'polish',
        'pt': 'portuguese',
        'ru': 'russian',
        'sl': 'slovene',
        'es': 'spanish',
        'sv': 'swedish',
        'tr': 'turkish',
    }

    def __init__(self, default_language='english', probability_at_least:float = 0.0):
        self.default_language = default_language
        self.probability_at_least = probability_at_least

    def createFromConfig(config:dict) -> MPreprocessor:
        return MWesternSentenceSplitter(
            default_language=config['default_language'],
            probability_at_least=config['probability_at_least'],
        )

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        for text in texts:
            ((first_lang_id, second_lang_id), [_, second_lang_id_probability]) = languagePredictor.predict(text, k=2)
            language = self._get_language(first_lang_id, second_lang_id, second_lang_id_probability)
            for text in nltk.sent_tokenize(text, language=language):
                yield text

    def _get_language(self, first_lang_id: str, second_lang_id: str, second_lang_id_probability: float) -> str:
        if first_lang_id in self._nltk_language_map:
            return self._nltk_language_map[first_lang_id]
        elif second_lang_id_probability >= self.probability_at_least and second_lang_id in self._nltk_language_map:
            return self._nltk_language_map[second_lang_id]
        else:
            return self.default_language

##############################################################################
# KSS Preprocessor
##############################################################################

class MKoreanSentenceSplitter(MPreprocessor):
    '''
    KSS를 사용하여 문장을 분리한다.
    '''
    def createFromConfig(config:dict) -> MPreprocessor:
        return MKoreanSentenceSplitter()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts: Iterable[str]) -> Iterable[str]:
        sentences = []

        for text in texts:
            ((first_lang_id, second_lang_id), _) = languagePredictor.predict(text, k=2)

            if 'ko' == first_lang_id or 'ko' == second_lang_id:
                for text in kss.split_sentences(text, num_workers=1):
                    yield text
            else:
                yield text

        return sentences

##############################################################################
# BERT Preprocessor
##############################################################################

class MTFHubBertBinaryClassificationPredictor:
    def __init__(self, tfhub_handle_preprocess:str, tfhub_handle_encoder:str, checkpoint:str):
        self.tfhub_handle_preprocess = tfhub_handle_preprocess
        self.tfhub_handle_encoder = tfhub_handle_encoder
        self.checkpoint = checkpoint

        text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
        preprocessing_layer = hub.KerasLayer(self.tfhub_handle_preprocess, name='preprocessing')
        encoder_inputs = preprocessing_layer(text_input)
        encoder = hub.KerasLayer(self.tfhub_handle_encoder, trainable=True, name='BERT_encoder')
        outputs = encoder(encoder_inputs)
        net = outputs['pooled_output']
        net = tf.keras.layers.Dense(1, activation='sigmoid', name='classifier')(net)
        self.model = tf.keras.Model(text_input, net)
        self.model.load_weights(self.checkpoint)

    def createFromConfig(config:dict) -> 'MTFHubBertBinaryClassificationPredictor':
        return MTFHubBertBinaryClassificationPredictor(
            tfhub_handle_preprocess=config['tfhub_handle_preprocess'],
            tfhub_handle_encoder=config['tfhub_handle_encoder'],
            checkpoint=config['checkpoint'],
        )

    def exportToConfig(self) -> dict:
        return {
            'tfhub_handle_preprocess': self.tfhub_handle_preprocess,
            'tfhub_handle_encoder': self.tfhub_handle_encoder,
            'checkpoint': self.checkpoint,
        }

    def predict(self, texts:list[str]) -> list[float]:
        predictions = self.model(tf.constant(texts))
        predictions = tf.reshape(predictions, shape=(-1))
        predictions = predictions.numpy()
        predictions = predictions.tolist()
        return predictions

class MSentenceCutPrediction:
    def __init__(self, headcutProbability:float, tailcutProbability:float, text:str):
        self.headcutProbability = headcutProbability
        self.tailcutProbability = tailcutProbability
        self.text = text

class MSentenceCutPredictor(MPreprocessor):
    def __init__(self):
        self.bosPredictor = MTFHubBertBinaryClassificationPredictor(
            global_val.TFHUB_HANDLE_PREPROCESS,
            global_val.TFHUB_HANDLE_ENCODER,
            global_val.CP_BOS_PREDICTION,
        )
        self.eosPredictor = MTFHubBertBinaryClassificationPredictor(
            global_val.TFHUB_HANDLE_PREPROCESS,
            global_val.TFHUB_HANDLE_ENCODER,
            global_val.CP_EOS_PREDICTION,
        )

    def createFromConfig(config:dict) -> 'MSentenceCutPredictor':
        return MSentenceCutPredictor()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts: Iterable[str]) -> Generator[MSentenceCutPrediction, None, None]:
        for batchTexts in self._getBatchTexts(texts):
            bosPredictions = self.bosPredictor.predict(batchTexts)
            eosPredictions = self.eosPredictor.predict(batchTexts)
            for index, text in enumerate(batchTexts):
                yield MSentenceCutPrediction(
                    bosPredictions[index],
                    eosPredictions[index],
                    text
                )

    def _getBatchTexts(self, texts:str) -> Generator[list[str], None, None]:
        batchTexts = []
        for index, text in enumerate(texts, start=1):
            batchTexts.append(text)
            if 0 == (index % _SENTENCE_CUT_PREDICTION_BATCH_SIZE):
                yield batchTexts
                batchTexts = []
        if len(batchTexts):
            yield batchTexts

class MTFHubBertSentenceMergingChecker(MSentenceMergingChecker):
    def __init__(self, preprocessor:MPreprocessor, bos_predictor:MTFHubBertBinaryClassificationPredictor, eos_predictor:MTFHubBertBinaryClassificationPredictor):
        self.preprocessor = preprocessor
        self.bos_predictor = bos_predictor
        self.eos_predictor = eos_predictor

    def createFromConfig(config:dict) -> MSentenceMergingChecker:
        return MTFHubBertSentenceMergingChecker(
            preprocessor=preprocessorFactory(config['preprocessor']),
            bos_predictor=MTFHubBertBinaryClassificationPredictor.createFromConfig(config['bos_predictor']),
            eos_predictor=MTFHubBertBinaryClassificationPredictor.createFromConfig(config['eos_predictor']),
        )

    def exportToConfig(self) -> dict:
        return {
            'preprocessor': preprocessorFactory.exportInstanceToConfig(self.preprocessor),
            'bos_predictor': self.bos_predictor.exportToConfig(),
            'eos_predictor': self.eos_predictor.exportToConfig(),
        }

    def isMergeable(self, sentence1: str, sentence2: str) -> bool:
        sentence1_eos_prob = self.eos_predictor.predict(list(self.preprocessor.preprocess([sentence1])))[0]
        sentence2_bos_prob = self.bos_predictor.predict(list(self.preprocessor.preprocess([sentence2])))[0]
        if (0.5 > sentence1_eos_prob and 0.5 > sentence2_bos_prob):
            return True
        else:
            return False

class MSentenceCutPredictionPreprocessor(MPreprocessor):
    def __init__(self):
        ...

    def createFromConfig(config:dict) -> 'MSentenceCutPredictionPreprocessor':
        return MSentenceCutPredictionPreprocessor()

    def exportToConfig(self) -> dict:
        pass

    def preprocess(self, texts: Iterable[MSentenceCutPrediction]) -> Generator[MSentenceCutPrediction, None, None]:
        ...

##############################################################################
# Toeknizer
##############################################################################

class MHRSentenceTokenizer:
    '''
    언어별 전용 토크나이저를 사용하는 방식
    '''
    def __init__(self):
        self.preprocessor = MCompositePreprocessor([
            MLineSplitter(keepends=False),
            MWesternSentenceSplitter(),
            MKoreanSentenceSplitter(),
        ])

    def tokenize(self, texts:Iterable[str]) -> list[str]:
        return list(self.preprocessor.preprocess(texts))

class MWikiCutSentenceTokenizer:
    '''
    언어와 무관하게 단어를 자르고, BERT 문장 합치기를 통해 문장을 합침
    '''
    def __init__(self):
        self.preprocessor = MCompositePreprocessor([
            MLineSplitter(keepends=False),
            MPostpositionSeparatorsSplitter(separators=global_val.EOS_MARKS),
            MSentenceMerger([
                MMaxLengthSentenceMergingChecker(),
                MSameLanguageSentenceMergingChecker(),
                MTFHubBertSentenceMergingChecker(
                    preprocessor=MPassthroughPreprocessor(),
                    bos_predictor=MTFHubBertBinaryClassificationPredictor(
                        tfhub_handle_preprocess=global_val.TFHUB_HANDLE_PREPROCESS,
                        tfhub_handle_encoder=global_val.TFHUB_HANDLE_ENCODER,
                        checkpoint=global_val.CP_BOS_PREDICTION,
                    ),
                    eos_predictor=MTFHubBertBinaryClassificationPredictor(
                        tfhub_handle_preprocess=global_val.TFHUB_HANDLE_PREPROCESS,
                        tfhub_handle_encoder=global_val.TFHUB_HANDLE_ENCODER,
                        checkpoint=global_val.CP_EOS_PREDICTION,
                    ),
                ),
            ]),
        ])

    def tokenize(self, texts:Iterable[str]) -> list[str]:
        return list(self.preprocessor.preprocess(texts))

class MCorpusMergeableUnitSplitter:
    def __init__(self):
        self.mapper = MCorpusPreprocessorMapper(
            wordPreprocessor=MCompositePreprocessor([
                MCorpusPageMarkerRemover(),
                MCorpusSheetSplitter(),
                MCorpusExcelCellSplitter(),
                MMultipleEmptyLineSplitter(minEmptyLines=2),
                MListItemSplitter(),
                MWhitespaceTrimmer(),
                MEmptyTextFilter(),
            ]),
            excelPreprocessor=MCompositePreprocessor([
                MCorpusSheetSplitter(),
                MCorpusExcelCellSplitter(),
                MMultipleEmptyLineSplitter(minEmptyLines=2),
                MListItemSplitter(),
                MWhitespaceTrimmer(),
                MEmptyTextFilter(),
            ]),
            powerpointPreprocessor=MCompositePreprocessor([
                MCorpusPageSplitter(),
                MCorpusSheetSplitter(),
                MCorpusExcelCellSplitter(),
                MMultipleEmptyLineSplitter(minEmptyLines=2),
                MListItemSplitter(),
                MWhitespaceTrimmer(),
                MEmptyTextFilter(),
            ]),
            pdfPreprocessor=MCompositePreprocessor([
                MCorpusPageMarkerRemover(),
                MMultipleEmptyLineSplitter(minEmptyLines=2),
                MListItemSplitter(),
                MWhitespaceTrimmer(),
                MEmptyTextFilter(),
            ]),
        )

    def split(self, formatCode: int, texts: Iterable[str]) -> Iterable[str]:
        preprocessor = self.mapper.getPreprocessor(formatCode)
        return preprocessor.preprocess(texts)

class MParagraphSplitter:
    def __init__(self):
        self.mapper = MCorpusPreprocessorMapper(
            wordPreprocessor=MCompositePreprocessor([
                MCorpusPageMarkerRemover(),
                #MCorpusSheetSplitter(),
                #MCorpusExcelCellSplitter(),
                MMultipleEmptyLineSplitter(minEmptyLines=2),
                MNonLetterLineSplitter(),
                #MParagraphPunctuationMarkSplitter(),
                MListItemSplitter(),
                MMinLetterFilter(minLetterCount=1),
                MListItemBulletRemover(),
                MWhiteSpaceCompactor(),
                MPunctuationCompactor(),
                MMinTokenFilter(minTokenCount=2),
                MMaxWordAtLeastFilter(maxWordAtLeast=2),
                MMaxWordLengthFilter(maxWordLength=31),
                MWhitespaceTrimmer(),
                MEmptyTextFilter(),
            ]),
            excelPreprocessor=MCompositePreprocessor([
                MCorpusSheetSplitter(),
                MCorpusExcelCellSplitter(),
                MMultipleEmptyLineSplitter(minEmptyLines=2),
                MNonLetterLineSplitter(),
                #MParagraphPunctuationMarkSplitter(),
                MListItemSplitter(),
                MMinLetterFilter(minLetterCount=1),
                MListItemBulletRemover(),
                MWhiteSpaceCompactor(),
                MPunctuationCompactor(),
                MMinTokenFilter(minTokenCount=2),
                MMaxWordAtLeastFilter(maxWordAtLeast=2),
                MMaxWordLengthFilter(maxWordLength=31),
                MWhitespaceTrimmer(),
                MEmptyTextFilter(),
            ]),
            powerpointPreprocessor=MCompositePreprocessor([
                MCorpusPageSplitter(),
                #MCorpusSheetSplitter(),
                #MCorpusExcelCellSplitter(),
                MMultipleEmptyLineSplitter(minEmptyLines=2),
                MNonLetterLineSplitter(),
                #MParagraphPunctuationMarkSplitter(),
                MListItemSplitter(),
                MMinLetterFilter(minLetterCount=1),
                MListItemBulletRemover(),
                MWhiteSpaceCompactor(),
                MPunctuationCompactor(),
                MMinTokenFilter(minTokenCount=2),
                MMaxWordAtLeastFilter(maxWordAtLeast=2),
                MMaxWordLengthFilter(maxWordLength=31),
                MWhitespaceTrimmer(),
                MEmptyTextFilter(),
            ]),
            # PDF 관려 주의
            # 여러 단으로 구성된 문서의 경우 여러 단이 섞여서 추출된다.
            # 2단으로 구성된 문서 예시
            #
            # PDF에 보이는 문서 (국문단 | 영문단)
            # 가나다라마바사  | abcdefg
            # 아자차카타파하  | hijklmn
            #
            # 실제 문서 내용
            # 가나다라마바사아자차카타파하
            # abcdefghijklmn
            #
            # 추출된 문서
            # 가나다라마바사 \n abcdefg
            # 아자차카타파하 \n hijklmn
            pdfPreprocessor=MCompositePreprocessor([
                # PDF 문서가 워드 형식으로 작성된 경우 페이지 별로 구분하면 안되고(MCorpusPageMarkerRemover를 사용)
                # PDF 문서가 파워포인트 형식으로 작성된 경우 페이지 별로 구분해야 한다.(MCorpusPageSplitter를 사용)
                # 영문의 경우 전자가 우세하고, 국문의 경우 후자가 우세하다.
                #MCorpusPageMarkerRemover(),
                MCorpusPageSplitter(),
                MMultipleEmptyLineSplitter(minEmptyLines=2),
                MNonLetterLineSplitter(),
                MParagraphPunctuationMarkSplitter(),
                MListItemSplitter(),
                MMinLetterFilter(minLetterCount=1),
                MListItemBulletRemover(),
                # PDF의 경우 문서상에 공백으로 보이는 부분이 추출될 때 tab으로 추출되는 경우가 많다.
                # 그래서 MTabToSpaceConverter를 사용해 tab을 일괄 공백으로 변경한다.
                MTabToSpaceConverter(),
                MWhiteSpaceCompactor(),
                MPunctuationCompactor(),
                # PDF의 경우 굵은 글씨는 폰트가 굵은 것이 아니라 동일한 글자가
                # 주위에 여러번 겹처 써서 굵은 폰트를 표시하기 때문에 동일 문자열이
                # 여러번 반복해서 추출되는 경우가 있다.
                # MRepeatWordCompactor는 이런 반복되는 단어를 하나로 줄이는 함수로
                # 다른 일반적인 워드 프로세서에서는 없는 증상으로 PDF에서만 사용한다.
                MRepeatWordCompactor(minRepeat=2),
                MMinTokenFilter(minTokenCount=2),
                MMaxWordAtLeastFilter(maxWordAtLeast=2),
                MMaxWordLengthFilter(maxWordLength=31),
                MFollowedBySameTextFilter(),
                MWhitespaceTrimmer(),
                MEmptyTextFilter(),
            ]),
            textPreprocessor=MCompositePreprocessor([
                MSourceCodePatternFilter(),
                MMultipleEmptyLineSplitter(minEmptyLines=2),
                MNonLetterLineSplitter(),
                MParagraphPunctuationMarkSplitter(),
                MListItemSplitter(),
                MMinLetterFilter(minLetterCount=1),
                MListItemBulletRemover(),
                MWhiteSpaceCompactor(),
                MPunctuationCompactor(),
                MMinTokenFilter(minTokenCount=2),
                MMaxWordAtLeastFilter(maxWordAtLeast=2),
                MMaxWordLengthFilter(maxWordLength=31),
                MFollowedBySameTextFilter(),
                MWhitespaceTrimmer(),
                MEmptyTextFilter(),
            ])
        )

    def isSupportedType(self, formatCode:int) -> bool:
        return self.mapper.isSupportedType(formatCode)

    def split(self, formatCode: int, texts: Iterable[str]) -> Iterable[str]:
        preprocessor = self.mapper.getPreprocessor(formatCode)
        return preprocessor.preprocess(texts)

class MCorpusTokenizer:
    def __init__(self):
        postpositionPunctuationMarkSplittedTextPreprocessor = MPostpositionPunctuationMarkSplittedTextKeepMergingDropPreprocessor()
        self.mapper = MCorpusPreprocessorMapper(
            wordPreprocessor=MMultiLevelPreprocessor([
                MCompositePreprocessor([
                    MCorpusSheetSplitter(),
                    MCorpusExcelCellSplitter(),
                    MMultipleEmptyLineSplitter(minEmptyLines=2),
                    MListItemSplitter(),
                    MWhitespaceTrimmer(),
                    MEmptyTextFilter(),
                ]),
                MCompositePreprocessor([
                    MLineSplitter(keepends=False),
                    MPostpositionPunctuationMarkSplitter(),
                    postpositionPunctuationMarkSplittedTextPreprocessor,
                ]),
            ]),
            excelPreprocessor=MMultiLevelPreprocessor([
                MCompositePreprocessor([
                    MCorpusSheetSplitter(),
                    MCorpusExcelCellSplitter(),
                    MMultipleEmptyLineSplitter(minEmptyLines=2),
                    MListItemSplitter(),
                    MWhitespaceTrimmer(),
                    MEmptyTextFilter(),
                ]),
                MCompositePreprocessor([
                    MLineSplitter(keepends=False),
                    MPostpositionPunctuationMarkSplitter(),
                    postpositionPunctuationMarkSplittedTextPreprocessor,
                ]),
            ]),
            powerpointPreprocessor=MMultiLevelPreprocessor([
                MCompositePreprocessor([
                    MCorpusPageSplitter(),
                    MCorpusSheetSplitter(),
                    MCorpusExcelCellSplitter(),
                    MMultipleEmptyLineSplitter(minEmptyLines=2),
                    MListItemSplitter(),
                    MWhitespaceTrimmer(),
                    MEmptyTextFilter(),
                ]),
                MCompositePreprocessor([
                    MLineSplitter(keepends=False),
                    MPostpositionPunctuationMarkSplitter(),
                    postpositionPunctuationMarkSplittedTextPreprocessor,
                ]),
            ]),
            pdfPreprocessor=MMultiLevelPreprocessor([
                MCompositePreprocessor([
                    MCorpusPageMarkerRemover(),
                    MMultipleEmptyLineSplitter(minEmptyLines=2),
                    MListItemSplitter(),
                    MWhitespaceTrimmer(),
                    MEmptyTextFilter(),
                ]),
                MCompositePreprocessor([
                    MLineSplitter(keepends=False),
                    MPostpositionPunctuationMarkSplitter(),
                    postpositionPunctuationMarkSplittedTextPreprocessor,
                ]),
            ]),
        )

        self.commonPreprocessor = MCompositePreprocessor([
            MWhitespaceTrimmer(),
            MEmptyTextFilter(),
        ])

    def tokenize(self, formatCode: int, texts: Iterable[str]) -> Iterable[str]:
        preprocessor = self.mapper.getPreprocessor(formatCode)
        texts = preprocessor.preprocess(texts)
        return self.commonPreprocessor.preprocess(texts)

##############################################################################
# 미리 구성된 전처리기 서비스
##############################################################################

class MPreconfiguredPreprocessors:
    def __init__(self):
        self.instances = {}
        self.configs = {}

    def get_instance(self, name:str) -> MPreprocessor:
        if name not in self.instances:
            config = self.get_config(name)

            self.instances[name] = preprocessorFactory.createInstance(
                config['factory'],
                config['options'],
            )

        return self.instances[name]

    def get_config(self, name: str) -> dict:
        if name not in self.configs:
            raise MpowerException(
                f"preprocessor configuration '{name}' not found.",
                StatusCode.SC_SYS_CONFIG_ERR.value, -1, StatusCode.SC_SYS_CONFIG_ERR.name
            )

        return self.configs[name]

    def add_config(self, name:str, config:dict):
        if name in self.configs:
            raise MpowerException(
                f"preprocessor configuration '{name}' already exists",
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )

        self.configs[name] = config

    def add_configs(self, configs:dict):
        for name in configs:
            self.add_config(name, configs[name])

##############################################################################
# 데이터 셋
# pympower.classes.mdata.MDataset으로 분리했다. 병합할 내용이 있는지 확인하고
# MPreprocessingDataset과 그 하위 클래스는 삭제할 것.
##############################################################################

class MPreprocessingDataset:
    def get_size(self) -> int:
        pass

    def get_data(self) -> Iterable:
        pass

##############################################################################
# BulkJsonDataSet
##############################################################################

class MBulkJsonDataset(MPreprocessingDataset):
    def __init__(self, dataset_dir:str, read_preprocessor:MPreprocessor=None):
        self.dataset_dir = dataset_dir
        # TODO: 수정 할 것
        self.read_preprocessor = read_preprocessor

        if False == os.path.exists(dataset_dir):
            raise MpowerException(
                f"Dataset directory '{dataset_dir}' does not exist.",
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )

        # 파일 이름 구성 정보
        self.summary_filename = 'summary.json' # TODO: 삭제할 것
        self.datalist_filename = 'datafiles.json'
        self.data_filename_prefix = 'datafile_'
        self.data_filename_digit_width = 4
        self.data_filename_ext = '.bulkjson'
        self.each_data_limit = 100_000

    def get_summary_filepath(self) -> str:
        return os.path.join(self.dataset_dir, self.summary_filename)

    def get_summary(self) -> dict:
        path = self.get_summary_filepath()
        with open(path, 'r', encoding='utf-8') as f:
            return json.loads(f.read())

    def set_summary(self, summary:dict):
        path = self.get_summary_filepath()
        with open(path, 'w', encoding='utf-8') as f:
            return f.write(json.dumps(summary, ensure_ascii=False, indent=4))

    def get_datalist_filepath(self) -> str:
        return os.path.join(self.dataset_dir, self.datalist_filename)

    def data_exists(self) -> bool:
        return os.path.exists(self.get_datalist_filepath())

    def get_size(self) -> int:
        with open(self.get_datalist_filepath(), 'r', encoding='utf-8') as f:
            filelist = json.loads(f.read())
        return sum([int(fileinfo['size']) for fileinfo in filelist])

    def get_data(self) -> Iterable:
        with open(self.get_datalist_filepath(), 'r', encoding='utf-8') as f:
            filelist = json.loads(f.read())
        filelist = [os.path.join(self.dataset_dir, fileinfo['filename']) for fileinfo in filelist]

        if None != self.read_preprocessor:
            preprocessor = MCompositePreprocessor([
                MTextFileLineReader(),
                MJsonDecoder(),
                self.read_preprocessor,
            ])
        else:
            preprocessor = MCompositePreprocessor([
                MTextFileLineReader(),
                MJsonDecoder(),
            ])

        return preprocessor.preprocess(filelist)

    def set_data(self, texts:Iterable) -> None:
        listfile = open(self.get_datalist_filepath(), 'x', encoding='utf-8')

        preprocessor = MCompositePreprocessor([
            MJsonEncoder(),
            MMultiTextFileLineWriter(
                path=self.dataset_dir,
                each_limit=self.each_data_limit,
            ),
        ])

        filelist = preprocessor.preprocess(texts)
        filelist = [{
            'filename': os.path.relpath(fileinfo['path'], self.dataset_dir),
            'size': fileinfo['size'],
        } for fileinfo in filelist]
        filelist = json.dumps(filelist, ensure_ascii=False, indent=4)

        listfile.write(filelist)
        listfile.close()

    def remove_data(self):
        pass

    def shuffle_filelist(self, seed:int):
        rng = Random(seed)

        # 파일 목록 섞기
        with open(self.get_datalist_filepath(), 'r', encoding='utf-8') as f:
            filelist = json.loads(f.read())

        rng.shuffle(filelist)

        with open(self.get_datalist_filepath(), 'w', encoding='utf-8') as f:
            f.write(json.dumps(filelist, ensure_ascii=False, indent=4))

    def shuffle_data(self, seed:int):
        rng = Random(seed)

        # 파일 목록 섞기
        with open(self.get_datalist_filepath(), 'r', encoding='utf-8') as f:
            filelist = json.loads(f.read())

        # 데이터 섞기
        read_preprocessor = MCompositePreprocessor([
            MTextFileLineReader(),
            MJsonDecoder(),
        ])
        for fileinfo in filelist:
            path = os.path.join(self.dataset_dir, fileinfo['filename'])
            data = list(read_preprocessor.preprocess([path]))
            rng.shuffle(data)
            write_preprocessor = MCompositePreprocessor([
                MJsonEncoder(),
                MTextFileLineWriter(path),
            ])
            list(write_preprocessor.preprocess(data))

class MBulkJsonDatasetCollection:
    def __init__(self, collection_dir:str):
        self.collection_dir = collection_dir

        if False == os.path.exists(self.collection_dir):
            raise MpowerException(
                f"Collection directory '{self.collection_dir}' does not exist.",
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )

        self.collection_filename = 'collection.json'

    def _load_collection(self) -> dict:
        filename = os.path.join(self.collection_dir, self.collection_filename)

        if False == os.path.exists(filename):
            return {}

        with open(filename, 'r', encoding='utf-8') as f:
            return json.loads(f.read())

    def _save_collection(self, data:dict):
        filename = os.path.join(self.collection_dir, self.collection_filename)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))

    def _is_name_ok(self, name:str) -> bool:
        # TODO: 구현 할 것
        return True

    def exists(self, name:str):
        return name in self._load_collection()

    def create(self, name:str) -> MBulkJsonDataset:
        collection = self._load_collection()
        if name in collection:
            raise MpowerException(
                f"Dataset '{name}' already exists.",
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )

        if False == self._is_name_ok(name):
            raise MpowerException(
                f"Dataset '{name}' cannot be created.",
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )

        dataset_dir = os.path.join(self.collection_dir, name)
        if os.path.exists(dataset_dir):
            raise MpowerException(
                f"Dataset directory '{name}' already exists.",
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )

        os.makedirs(dataset_dir)

        collection[name] = name

        self._save_collection(collection)

        return MBulkJsonDataset(dataset_dir)

    def remove(self, name:str):
        dataset = self.get(name)
        dataset.remove_data()
        os.remove(dataset.dataset_dir)

    def get(self, name:str) -> MBulkJsonDataset:
        collection = self._load_collection()
        if name not in collection:
            raise MpowerException(
                f"Dataset '{name}' does not exist.",
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )
        
        dataset_dir = os.path.join(self.collection_dir, collection[name])

        return MBulkJsonDataset(dataset_dir)

    def list(self) -> list:
        collection = self._load_collection()
        return [collection[name] for name in collection]

##############################################################################
# 팩토리 전역 변수 초기화
##############################################################################

_PREPROCESSOR_CLASSES = {
    # 합성 전처리기
    MCompositePreprocessor,
    MMultiLevelPreprocessor,
    MPassthroughPreprocessor,
    # 정규식
    MRegExSplitter,
    MRegExReplacer,
    # 코퍼스 분리
    MCorpusPageSplitter,
    MCorpusPageMarkerRemover,
    MCorpusSheetSplitter,
    MCorpusExcelCellSplitter,
    # 문장 분리기
    MLineSplitter,
    MMultipleEmptyLineSplitter,
    MPostpositionSeparatorsSplitter,
    MPostpositionPunctuationMarkSplitter,
    # 문장 병합기
    MSentenceMerger,
    # 문장 걸러내기
    MInstanceFilter,
    MEmptyTextFilter,
    MMinLengthFilter,
    MMinLetterFilter,
    MMinTokenFilter,
    MMaxWordLengthFilter,
    MMaxWordAtLeastFilter,
    MPartialSentenceFilter,
    MKeepSkipFilter,
    MCountLimitter,
    MSourceCodeSemicolonFilter,
    MSourceCodeCommentFilter,
    MSourceCodePatternFilter,
    MLanguageFilter,
    MFollowedBySameTextFilter,
    # 분장 복사
    MDuplicator,
    # 문장 자르기
    MRandomHeadCutter,
    MRandomTailCutter,
    MMaxLengthHeadCutter,
    MMaxLengthTailCutter,
    MSplitAndPickFirst,
    MSplitAndPickLast,
    MSplitAndMergingForward,
    MSplitAndMergingBackward,
    # 문장 내용 변경
    MUpperCaseConverter,
    MLowerCaseConverter,
    MPunctuationRemover,
    MTrimmer,
    MWhitespaceTrimmer,
    MWhiteSpaceCompactor,
    MPunctuationCompactor,
    MRepeatWordCompactor,
    MPUARemover,
    MNonBMPRemover,
    MListItemBulletRemover,
    # 문장 코덱
    MJsonEncoder,
    MJsonDecoder,
    MTsvEncoder,
    MTsvDecoder,
    # 객체간 변환
    MDictToTupleFilter,
    MDictToValueFilter,
    MTupleToTupleFilter,
    MTupleToValueFilter,
    MTupleTextJoiner,
    # 문장 섞기
    MRandomShuffler,
    FileLineRandomShuffler,
    # 파일 처리
    MDirectoryReader,
    MTextFileLineReader,
    MMultiFileRoundRobinReader,
    MTextFileLineWriter,
    MMultiTextFileLineWriter,
    # 엠파워 파일 처리
    MDecryptingPreprocessor,
    # 텍스트 추출
    MTextExtractingToFilePreprocessor,
    MTextExtracingToMultiFilePreproessor,
    # 라벨링
    MStaticTupleLabeler,
    MStaticDictLabeler,
    MTupleBoWEmbedder,
    # 학습 데이터
    MJsonLabeledDatasetReader,
    MJsonLabeledDatasetWriter,
    MJsonLabeledDatasetCounter,
    # 집계
    MCountAggregator,
    MSumAggregator,
    # 위키 코퍼스 전처리기
    MWikiXmlToJson,
    MWikiJsonReader,
    # NLP 전처리기
    MWesternSentenceSplitter,
    MKoreanSentenceSplitter,
}

_SENTENCE_MERGING_CHECKER_CLASSES = {
    MMaxLengthSentenceMergingChecker,
    MMinLengthSentenceMergingChecker,
    MTFHubBertSentenceMergingChecker,
    MSameLanguageSentenceMergingChecker,
    MTFHubBertSentenceMergingChecker,
}

preprocessorFactory.addClasses(_PREPROCESSOR_CLASSES)
sentenceMergingCheckerFactory.addClasses(_SENTENCE_MERGING_CHECKER_CLASSES)

preconfiguredPreprocessors = MPreconfiguredPreprocessors()

##############################################################################
# __all__ 구성
##############################################################################

__all__ =  [
    MPreprocessor.__name__,
    MPreprocessorFactory.__name__,
    *[klass.__name__ for klass in _PREPROCESSOR_CLASSES],

    MSentenceMergingChecker.__name__,
    MSentenceMergingCheckerFactory.__name__,
    *[klass.__name__ for klass in _SENTENCE_MERGING_CHECKER_CLASSES],

    MTFHubBertBinaryClassificationPredictor.__name__,

    MHRSentenceTokenizer.__name__,
    MWikiCutSentenceTokenizer.__name__,
    MCorpusMergeableUnitSplitter.__name__,
    MParagraphSplitter.__name__,
    MCorpusTokenizer.__name__,

    'languagePredictor',

    'preprocessorFactory',
    'sentenceMergingCheckerFactory',
    'preconfiguredPreprocessors',
]
