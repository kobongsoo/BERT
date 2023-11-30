
from asyncio.log import logger
from io import FileIO
import subprocess
from pympower.common.session import MSESSION
from pympower.common.statuscode import StatusCode
from pympower.common.global_val import global_val
from pympower.classes.mbase import *
from pympower.classes.snf import *
global_val = global_val.load_global_val();


class MShaAI(MBase):
    
    SNF_FILE_SEP = '..FILE:'; # 사이냅 필터 파일 구분자
    
    def __init__(self, powerdb_con:MpowerDB2=None):
        super().__init__(powerdb_con);
        self.utilClass = MClassFactory.getUtility(powerdb_con);
        self.cryptClass = MClassFactory.getMCrypt();
        self.excludeList = [];
        self.archiveList = [];
        self.excludeExtList = {};
        self.includeExtList = {};
        
        self.aiPolicy = None;
        self.corpusPolicy = None;
        self.indexPolicy = None;
        self.searchPolicy = None;
        self.summaryPolicy = None;
        bExcludeArchive = True;
        
        if global_val.defined('USE_AI'):
            self.aiPolicy = global_val.USE_AI;
            if 'corpus' in self.aiPolicy:
                self.corpusPolicy = self.aiPolicy['corpus'];
            if 'index' in self.aiPolicy:
                self.indexPolicy = self.aiPolicy['index'];
            if 'search' in self.aiPolicy:
                self.searchPolicy = self.aiPolicy['search'];
            if 'summary' in self.aiPolicy:
                self.summaryPolicy = self.aiPolicy['summary'];

        if  self.corpusPolicy != None and \
            'uncompressDepth' in self.corpusPolicy and \
            self.corpusPolicy['uncompressDepth'] > 0:
                bExcludeArchive = False;     
                
        self._loadExcludeFormat(bExcludeArchive);
        self._loadExcludeExtList(bExcludeArchive);
        self._loadIncludeExtList(not bExcludeArchive);


    def close(self):
        pass
    
    def setLogger(self, logger: "MLogger"):
        super().setLogger(logger);
        self.utilClass.setLogger(logger);
        self.cryptClass.setLogger(logger);
        
    def _loadExcludeFormat(self, bExcludeArchive:bool = True):
        if self.excludeList != None:
            self.excludeList.clear();
        
	    # 아래는 synap document filter에서 텍스트 추출이 가능한 문서 포맷이다.
	    # 이중 사용하지 않을 것을 선택한다.
        self.excludeList.append(10000); # MPEG video stream data
        self.excludeList.append(10100); # MPEG system stream data
        self.excludeList.append(10200); # MP3 Audio data, ID3 Tag
        self.excludeList.append(10300); # MP3
        self.excludeList.append(10400); # MP2
        self.excludeList.append(10500); # MPEG
        self.excludeList.append(10501); # MP3
        self.excludeList.append(10502); # MP2
        self.excludeList.append(10600); # Silicon Graphics movie file (movi)
        self.excludeList.append(10700); # Apple QuickTime movie file (moov)
        self.excludeList.append(10800); # Apple QuickTime movie file (mdat)
        self.excludeList.append(10900); # Microsoft ASF
        self.archiveList.append(11000); # ARC archive data, dynamic LZW
        self.archiveList.append(11100); # ARC archive data, squashed
        self.archiveList.append(11200); # ARC archive data, uncompressed
        self.archiveList.append(11300); # ARC archive data, packed
        self.archiveList.append(11400); # ARC archive data, squeezed
        self.archiveList.append(11500); # ARC archive data, crunched
        self.archiveList.append(11600); # ARJ archive data
        self.archiveList.append(11700); # LHarc 1.x archive data [lh0]
        self.archiveList.append(11800); # LHarc 1.x archive data [lh1]
        self.archiveList.append(11900); # LHarc 1.x archive data [lz4]
        self.archiveList.append(12000); # LHarc 1.x archive data [lz5]
        self.archiveList.append(12100); # LHa 2.x? archive data [lzs]
        self.archiveList.append(12200); # LHa 2.x? archive data [lh ]
        self.archiveList.append(12300); # LHa 2.x? archive data [lhd]
        self.archiveList.append(12400); # LHa 2.x? archive data [lh2]
        self.archiveList.append(12500); # LHa 2.x? archive data [lh3]
        self.archiveList.append(12600); # LHa (2.x) archive data [lh4]
        self.archiveList.append(12700); # LHa (2.x) archive data [lh5]
        self.archiveList.append(12800); # LHa (2.x) archive data [lh6]
        self.archiveList.append(12900); # LHa (2.x) archive data [lh7]
        self.archiveList.append(13000); # RAR archive data
        self.archiveList.append(13100); # Zip archive data
        self.archiveList.append(13200); # Zoo archive data
        self.excludeList.append(13300); # Microsoft cabinet file data,
        self.excludeList.append(13400); # Sun/NeXT audio data:
        self.excludeList.append(13500); # DEC audio data:
        self.excludeList.append(13600); # Standard MIDI data
        self.excludeList.append(13700); # Creative Music (CMF) data
        self.excludeList.append(13800); # SoundBlaster instrument data
        self.excludeList.append(13900); # Creative Labs voice data
        self.excludeList.append(14000); # MultiTrack sound data
        self.excludeList.append(14100); # Extended MOD sound data,
        self.excludeList.append(14200); # RealAudio sound file
        self.excludeList.append(14300); # RealMedia file
        self.excludeList.append(14400); # CDDB(tm) format CD text data
        self.archiveList.append(17900); # GNU Tar Archive
        self.archiveList.append(18000); # gzip compressed data
        self.excludeList.append(18100); # packed data
        self.excludeList.append(18200); # old packed data
        self.excludeList.append(18300); # compacted data
        self.excludeList.append(18400); # compacted data
        self.excludeList.append(18500); # huf output
        self.excludeList.append(18700); # squeezed data,
        self.excludeList.append(18800); # crunched data,
        self.archiveList.append(18900); # LZH compressed data,
        self.excludeList.append(19000); # frozen file 2.1
        self.excludeList.append(19100); # frozen file 1 (or gzip 0.5)
        self.excludeList.append(19200); # SCO compress -H (LZH) data
        self.archiveList.append(19300); # bzip compressed data
        self.archiveList.append(19320); # bzip2 compressed data
        self.excludeList.append(19400); # Berkeley DB
        self.excludeList.append(19500); # Berkeley DB
        self.excludeList.append(19600); # Berkeley DB 1.85/1.86
        self.excludeList.append(19700); # Berkeley DB 1.85/1.86
        self.excludeList.append(19800); # Berkeley DB 1.85/1.86
        self.excludeList.append(19900); # Berkeley DB
        self.excludeList.append(20000); # Berkeley DB
        self.excludeList.append(20100); # Berkeley DB
        self.excludeList.append(20200); # Berkeley DB
        self.excludeList.append(20300); # Berkeley DB
        self.excludeList.append(20400); # Berkeley DB
        self.excludeList.append(20500); # Berkeley DB
        self.excludeList.append(20600); # Berkeley DB
        self.excludeList.append(20700); # Berkeley DB
        self.excludeList.append(20800); # Macromedia Flash data
        self.excludeList.append(20801); # Macromedia Flash data
        self.excludeList.append(20802); # Macromedia Flash data
        self.excludeList.append(20900); # FrameMaker document
        self.excludeList.append(21000); # FrameMaker MIF (ASCII) file
        self.excludeList.append(21100); # FrameMaker Dictionary text
        self.excludeList.append(21200); # FrameMaker Font file
        self.excludeList.append(21300); # FrameMaker MML file
        self.excludeList.append(21400); # FrameMaker Book file
        self.excludeList.append(21500); # Intermediate Print File\x09FrameMaker IPL file
        self.excludeList.append(21700); # Targa image data - Map
        self.excludeList.append(21800); # Targa image data - RGB
        self.excludeList.append(21900); # Targa image data - Mono
        self.excludeList.append(22000); # Netpbm PBM image text
        self.excludeList.append(22100); # Netpbm PGM image text
        self.excludeList.append(22200); # Netpbm PPM image text
        self.excludeList.append(22300); # Netpbm PBM \rawbits\" image data"
        self.excludeList.append(22400); # Netpbm PGM \rawbits\" image data"
        self.excludeList.append(22500); # Netpbm PPM \rawbits\" image data"
        self.excludeList.append(22600); # Netpbm PAM image file
        self.excludeList.append(22700); # NIFF image data
        self.excludeList.append(22800); # TIFF image data, big-endian
        self.excludeList.append(22900); # TIFF image data, little-endian
        self.excludeList.append(23000); # PNG image data,
        self.excludeList.append(23100); # PNG image data, CORRUPTED
        self.excludeList.append(23200); # GIF image data
        self.excludeList.append(23201); # GIF image data, version 87a
        self.excludeList.append(23202); # GIF image data, version 89a
        self.excludeList.append(23300); # MIFF image data
        self.excludeList.append(23400); # PHIGS clear text archive
        self.excludeList.append(23500); # SunPHIGS
        self.excludeList.append(23600); # GKS Metafile
        self.excludeList.append(23700); # clear text Computer Graphics Metafile
        self.excludeList.append(23800); # binary Computer Graphics Metafile
        self.excludeList.append(24400); # FBM image data
        self.excludeList.append(24500); # group 3 fax data
        self.excludeList.append(24600); # PC bitmap data
        self.excludeList.append(24700); # PC icon data
        self.excludeList.append(24800); # PC pointer image data
        self.excludeList.append(24900); # PC color icon data
        self.excludeList.append(25000); # PC color pointer image data
        self.excludeList.append(25100); # Sun raster image data
        self.excludeList.append(25200); # SGI image data
        self.excludeList.append(25300); # FIT image data
        self.excludeList.append(25400); # FIT image data
        self.excludeList.append(25500); # Kodak Photo CD image pack file
        self.excludeList.append(25600); # Kodak Photo CD overview pack file
        self.excludeList.append(25700); # FITS image data
        self.excludeList.append(25800); # PDS (JPL) image data
        self.excludeList.append(25900); # PDS (JPL) image data
        self.excludeList.append(26000); # PDS (CCSD) image data
        self.excludeList.append(26100); # PDS (CCSD) image data
        self.excludeList.append(26200); # PDS image data
        self.excludeList.append(26300); # PDS (VICAR) image data
        self.excludeList.append(26400); # compiled Java class data,
        self.excludeList.append(26500); # Java serialization data
        self.excludeList.append(26600); # JPEG image data
        self.excludeList.append(26601); # JPEG image data, JFIF standard
        self.excludeList.append(26602); # JPEG image data, EXIF standard
        self.excludeList.append(26700); # JPEG image data, HSI proprietary
        self.excludeList.append(26800); # Linux/i386 impure executable (OMAGIC)
        self.excludeList.append(26900); # Linux/i386 pure executable (NMAGIC)
        self.excludeList.append(27000); # Linux/i386 demand-paged executable (ZMAGIC)
        self.excludeList.append(27100); # Linux/i386 demand-paged executable (QMAGIC)
        self.excludeList.append(27200); # Linux/i386 object file
        self.excludeList.append(27300); # Linux-8086 impure executable
        self.excludeList.append(27400); # Linux-8086 executable
        self.excludeList.append(27500); # Linux-8086 object file
        self.excludeList.append(27600); # Minix-386 impure executable
        self.excludeList.append(27700); # Minix-386 executable
        self.excludeList.append(27800); # Linux/i386 core file
        self.excludeList.append(27900); # Linux/i386 LILO boot/chain loader
        self.excludeList.append(28100); # Linux/i386 PC Screen Font data,
        self.excludeList.append(28200); # Linux/i386 swap file
        self.excludeList.append(28300); # Linux/i386 swap file (new style)
        self.excludeList.append(28400); # ECOFF alpha
        self.excludeList.append(28500); # Linux kernel
        self.excludeList.append(28600); # Linux kernel
        self.excludeList.append(28700); # Linux Software Map entry text
        self.excludeList.append(28800); # SAS
        self.excludeList.append(28900); # SPSS Portable File
        self.excludeList.append(29000); # SPSS System File
        self.excludeList.append(29100); # Mathematica version 2 notebook
        self.excludeList.append(29200); # Mathematica version 2 notebook
        self.excludeList.append(29300); # MS-DOS batch file text
        self.excludeList.append(29400); # MS Windows PE
        self.excludeList.append(29500); # MS Windows COFF Intel 80386 object file
        self.excludeList.append(29600); # MS Windows COFF MIPS R4000 object file
        self.excludeList.append(29700); # MS Windows COFF Alpha object file
        self.excludeList.append(29800); # MS Windows COFF Motorola 68000 object file
        self.excludeList.append(29900); # MS Windows COFF PowerPC object file
        self.excludeList.append(30000); # MS Windows COFF PA-RISC object file
        self.excludeList.append(30100); # MS-DOS executable (EXE)
        self.excludeList.append(30101); # MS-DOS executable (EXE), OS/2 or MS Windows
        self.excludeList.append(30102); # MS-DOS executable (EXE), LH/2 Self-Extract
        self.excludeList.append(30103); # MS-DOS executable (EXE), PKSFX2
        self.excludeList.append(30104); # MS-DOS executable (EXE), Windows self-extracting ZIP
        self.excludeList.append(30105); # MS-DOS executable (EXE), ARJ SFX
        self.excludeList.append(30106); # MS-DOS executable (EXE), diet compressed
        self.excludeList.append(30107); # MS-DOS executable (EXE), PKSFX
        self.excludeList.append(30108); # MS-DOS executable (EXE), PKLITE compressed
        self.excludeList.append(30109); # MS-DOS executable (EXE), LHa's SFX
        self.excludeList.append(30110); # MS-DOS executable (EXE), LHA's SFX
        self.excludeList.append(30111); # MS-DOS executable (EXE), LHa SFX archive v2.13S
        self.excludeList.append(30112); # MS-DOS executable (EXE), RAR self-extracting archive
        self.excludeList.append(30113); # MS-DOS executable (EXE), PKZIP SFX archive v1.1
        self.excludeList.append(30114); # MS-DOS executable (EXE), PKZIP SFX archive v1.93a
        self.excludeList.append(30115); # MS-DOS executable (EXE), PKZIP2 SFX archive v1.09
        self.excludeList.append(30116); # MS-DOS executable (EXE), PKZIP SFX archive v2.04g
        self.excludeList.append(30117); # MS-DOS executable (EXE), PKZIP2 SFX archive v1.02
        self.excludeList.append(30118); # MS-DOS executable (EXE), Info-ZIP SFX archive v5.12
        self.excludeList.append(30119); # MS-DOS executable (EXE), Info-ZIP SFX archive v5.12 w/decryption
        self.excludeList.append(30120); # MS-DOS executable (EXE), Info-ZIP SFX archive v5.12
        self.excludeList.append(30121); # MS-DOS executable (EXE), Info-ZIP SFX archive v5.12 w/decryption
        self.excludeList.append(30122); # MS-DOS executable (EXE), Info-ZIP NT SFX archive v5.12 w/decryption
        self.excludeList.append(30123); # MS-DOS executable (EXE), CODEC archive v3.21
        self.excludeList.append(30200); # MS-DOS executable (built-in)
        self.excludeList.append(30300); # Windows NT Registry file
        #self.excludeList.append(30900); # Microsoft Office Document
        #self.excludeList.append(31000); # Microsoft Office Document
        #self.excludeList.append(31100); # Microsoft Office Document
        #self.excludeList.append(31400); # Lotus 36925
        #self.excludeList.append(31500); # Lotus 36925
        #self.excludeList.append(31600); # MS Windows Help Data
        self.excludeList.append(31700); # Microsoft CAB file
        self.excludeList.append(31800); # Winamp plug in
        self.excludeList.append(31900); # hyperterm
        self.excludeList.append(32000); # ms-windows metafont .wmf
        self.excludeList.append(32100); # tz3 ms-works file
        self.excludeList.append(32200); # tz3 ms-works file
        self.excludeList.append(32300); # tz3 ms-works file
        self.excludeList.append(32400); # PGP sig
        self.excludeList.append(32500); # PGP sig
        self.excludeList.append(32600); # PGP sig
        self.excludeList.append(32700); # PGP sig
        self.excludeList.append(32800); # PGP sig
        self.excludeList.append(32900); # PGP sig
        self.excludeList.append(33000); # Ms-windows special zipped file
        self.excludeList.append(33100); # ms-windows help cache
        self.excludeList.append(33200); # Ms-windows 3.1 group files
        self.excludeList.append(33300); # ms-Windows shortcut
        self.excludeList.append(33400); # Icon for ms-windows
        self.excludeList.append(33500); # ms-windows icon resource
        self.excludeList.append(33600); # MS-Windows TRUE type font .ttf
        self.excludeList.append(33700); # ms-windows recycled bin info
        self.excludeList.append(33800); # Microsoft Visual C .APS file
        self.excludeList.append(33900); # MSVC .ide
        self.excludeList.append(34000); # MSVC .res
        self.excludeList.append(34100); # MSVC .res
        self.excludeList.append(34200); # MSVC .res
        self.excludeList.append(34300); # Microsoft Visual C library
        self.excludeList.append(34400); # Microsoft Visual C library
        self.excludeList.append(34500); # Microsoft Visual C library
        self.excludeList.append(34600); # Microsoft Visual C .pch
        self.excludeList.append(34700); # MSVC program database
        self.excludeList.append(34800); # MSVC .sbr
        self.excludeList.append(34900); # MSVC .bsc
        self.excludeList.append(35000); # MSVC .wsp version 1.0000.0000
        self.excludeList.append(35100); # \compact bitmap\" format (Poskanzer)"
        #self.excludeList.append(35200); # PDF document
        #self.excludeList.append(35210); # PDF document
        #self.excludeList.append(35220); # PDF document (Encrypted)
        self.excludeList.append(36000); # PGP key public ring
        self.excludeList.append(36100); # PGP key security ring
        self.excludeList.append(36200); # PGP key security ring
        self.excludeList.append(36300); # PGP encrypted data
        self.excludeList.append(36400); # PGP armored data
        #self.excludeList.append(36500); # PostScript document text
        #self.excludeList.append(36600); # PostScript document text
        #self.excludeList.append(36700); # PostScript document
        self.excludeList.append(36800); # DOS EPS Binary File
        self.excludeList.append(36900); # PPD file
        self.excludeList.append(37000); # RIFF (little-endian) data
        self.excludeList.append(37001); # RIFF (little-endian) data, palette
        self.excludeList.append(37004); # RIFF (little-endian) data, device-independent bitmap
        self.excludeList.append(37016); # RIFF (little-endian) data, MIDI
        self.excludeList.append(37017); # RIFF (little-endian) data, multimedia movie
        self.excludeList.append(37018); # RIFF (little-endian) data, WAVE audio
        self.excludeList.append(37034); # RIFF (little-endian) data, AVI
        self.excludeList.append(37035); # RIFF (little-endian) data, animated cursor
        self.excludeList.append(37100); # RIFF (big-endian) data
        self.excludeList.append(37101); # RIFF (big-endian) data, palette
        self.excludeList.append(37104); # RIFF (big-endian) data, device-independent bitmap
        self.excludeList.append(37116); # RIFF (big-endian) data, MIDI
        self.excludeList.append(37117); # RIFF (big-endian) data, multimedia movie
        self.excludeList.append(37118); # RIFF (big-endian) data, WAVE audio
        self.excludeList.append(37125); # RIFF (big-endian) data, AVI
        self.excludeList.append(37126); # RIFF (big-endian) data, animated cursor
        self.excludeList.append(37127); # RIFF (big-endian) data, Notation Interchange File Format
        self.excludeList.append(37128); # RIFF (big-endian) data, SoundFont 2
        self.excludeList.append(37300); # Rich Text Format Document
        self.excludeList.append(37400); # SCCS archive data
        #self.excludeList.append(37500); # HTML document text
        #self.excludeList.append(37600); # HTML document text
        #self.excludeList.append(37700); # HTML document text
        #self.excludeList.append(37800); # HTML document text
        #self.excludeList.append(37900); # XML document text
        #self.excludeList.append(37910); # XML Office document text
        #self.excludeList.append(37920); # XML Office document text
        #self.excludeList.append(37950); # XML HWP document text
        #self.excludeList.append(38300); # Sketch document text
        self.excludeList.append(38400); # uuencoded or xxencoded text
        self.excludeList.append(38500); # btoa'd text
        self.excludeList.append(38600); # ship'd binary text
        self.excludeList.append(38700); # bencoded News text
        self.excludeList.append(38800); # BinHex binary text
        self.archiveList.append(38900); # ACE archive file
        #self.excludeList.append(39100); # HandySoft Arirang
        self.excludeList.append(52000); # Web Video Text Tracks Format
        #self.excludeList.append(60001); # Microsoft Word 6 Document
        #self.excludeList.append(60002); # Spanish Microsoft Word 6 document data
        #self.excludeList.append(60003); # Microsoft Word document data
        #self.excludeList.append(60004); # Microsoft Word Document
        #self.excludeList.append(60005); # Microsoft Word 6 Document
        #self.excludeList.append(60202); # Microsoft Excel 5 Worksheet
        #self.excludeList.append(60203); # Microsoft Excel 5 Worksheet
        #self.excludeList.append(60305); # HWP Document file (Encrypted)
        #self.excludeList.append(60310); # HWP Document file
        #self.excludeList.append(60311); # HWP Document file, version 1
        #self.excludeList.append(60312); # HWP Document file, version 2
        #self.excludeList.append(60313); # HWP Document file, version 3
        #self.excludeList.append(60320); # HWP Document file (Encrypted)
        self.excludeList.append(70008); # Autocad drawing file, version R11
        self.excludeList.append(70009); # Autocad drawing file, version R12
        self.excludeList.append(70010); # Autocad drawing file, version R12(pre R13)
        self.excludeList.append(70012); # Autocad drawing file, version R13
        self.excludeList.append(70014); # Autocad drawing file, version R14
        self.excludeList.append(70015); # Autocad drawing file, version R2k
        self.excludeList.append(70018); # Autocad drawing file, version R2004
        #self.excludeList.append(90100); # Microsoft compressed HTML help files
        #self.excludeList.append(90101); # Microsoft compressed HTML help files, version 1
        #self.excludeList.append(90102); # Microsoft compressed HTML help files, version 2
        #self.excludeList.append(90103); # Microsoft compressed HTML help files, version 3
        #self.excludeList.append(90104); # Microsoft compressed HTML help files, version 4
        self.excludeList.append(60601); # IWD Document file, version 1
        self.excludeList.append(60602); # IWD Document file, version 2
        self.excludeList.append(60603); # IWD Document file, version 3
        #self.excludeList.append(80400); # Open Office Document file (Encrypted)
        self.excludeList.append(100100); # Microsoft Document Image files
        #self.excludeList.append(110402); # WordPerfect Document file, version 4.2
        #self.excludeList.append(111200); # WordPerfect Document file, version 5, 6, 7, 8, 9,
        #self.excludeList.append(120100); # EastSoft ALZIP Compressed File
        #self.excludeList.append(140100); # Hwx for Handysoft Groupware
        #self.excludeList.append(140200); # Hwn for Handysoft Groupware
        self.archiveList.append(150101); # 7Zip Archive
        self.excludeList.append(190300); # PACS, DICOM (Digital Imaging and Communications in Medicine)
        self.excludeList.append(190500); # PST (Outlook Personal Folders File)
        #self.excludeList.append(190700); # iWork Keynote (.key) File
        #self.excludeList.append(190900); # iWork Pages (.pages) File
        #self.excludeList.append(191100); # iWork Numbers (.numbers) File
        self.excludeList.append(191500); # FASOO.com DRM Document
        self.excludeList.append(191600); # Fujixerox DocuWorks
        #self.excludeList.append(191700); # Microsoft Write File
        #self.excludeList.append(191800); # KoreaSoft EMS7
        self.archiveList.append(191900); # EstSoft EGG Compressed File
        self.excludeList.append(192500); # SoftCamp DRM Document
        #self.excludeList.append(192600); # iWork Pages14(.pages) File
        #self.excludeList.append(192700); # iWork Keynote14 (.key) File
        #self.excludeList.append(192800); # iWork Numbers14 (.numbers) File
        self.excludeList.append(192900); # EMF Image File
        #self.excludeList.append(193500); # Excel BIFF 2
        #self.excludeList.append(300600); # XPS
        #self.excludeList.append(300800); # SHOW
        #self.excludeList.append(300900); # NXL
        #self.excludeList.append(301000); # CELL
        #self.excludeList.append(301100); # CELL2014
        #self.excludeList.append(301200); # HWPX
        #self.excludeList.append(301300); # XLSB
        #self.excludeList.append(301400); # POTX
        #self.excludeList.append(301430); # POTM
        #self.excludeList.append(301460); # PPSX
        #self.excludeList.append(301490); # PPSM
        #self.excludeList.append(301590); # PPAM
        #self.excludeList.append(301595); # THMX

        if bExcludeArchive:
            for formatId in self.archiveList:
                self.excludeList.append(formatId);

    def _loadExcludeExtList(self, bExcludeArchive:bool = True):
        self.excludeExtList.clear();
        
        self.excludeExtList['gul'] = 'HunminJungum';

        # Virtual
        self.excludeExtList['qcow2'] = 'Virtual Software';
        self.excludeExtList['ova'] = 'Virtual Software';
        self.excludeExtList['vdi'] = 'Virtual Software';
        self.excludeExtList['vmdk'] = 'Virtual Software';
        self.excludeExtList['vmem'] = 'Virtual Software';

        # 동영상
        self.excludeExtList['3gp'] = 'Multimedia stream';
        self.excludeExtList['asf'] = 'Multimedia stream';
        self.excludeExtList['asx'] = 'Multimedia stream';
        self.excludeExtList['avi'] = 'Multimedia stream';
        self.excludeExtList['flv'] = 'Multimedia stream';
        self.excludeExtList['mkv'] = 'Multimedia stream';
        self.excludeExtList['mp4'] = 'Multimedia stream';
        self.excludeExtList['mpg'] = 'Multimedia stream';
        self.excludeExtList['mpge'] = 'Multimedia stream';
        self.excludeExtList['mov'] = 'Multimedia stream';
        self.excludeExtList['ogm'] = 'Multimedia stream';
        self.excludeExtList['ogv'] = 'Multimedia stream';
        self.excludeExtList['ram'] = 'Multimedia stream';
        self.excludeExtList['rm'] = 'Multimedia stream';
        self.excludeExtList['swf'] = 'Multimedia stream';
        self.excludeExtList['wmv'] = 'Multimedia stream';

        # 오디오 
        self.excludeExtList['aac'] = 'Audio';
        self.excludeExtList['ac3'] = 'Audio';
        self.excludeExtList['flac'] = 'Audio';
        self.excludeExtList['mid'] = 'Audio';
        self.excludeExtList['mp3'] = 'Audio';
        self.excludeExtList['ogg'] = 'Audio';
        self.excludeExtList['ra'] = 'Audio';
        self.excludeExtList['wav'] = 'Audio';
        self.excludeExtList['wma'] = 'Audio';

        # 이미지 
        self.excludeExtList['ai'] = 'Image';
        self.excludeExtList['bmp'] = 'Image';
        self.excludeExtList['dib'] = 'Image';
        self.excludeExtList['emf'] = 'Image';
        self.excludeExtList['eps'] = 'Image';
        self.excludeExtList['frm'] = 'Image';
        self.excludeExtList['fpx'] = 'Image';
        self.excludeExtList['icb'] = 'Image';
        self.excludeExtList['ico'] = 'Image';
        self.excludeExtList['iff'] = 'Image';
        self.excludeExtList['jpeg'] = 'Image';
        self.excludeExtList['jpg'] = 'Image';
        self.excludeExtList['gif'] = 'Image';
        self.excludeExtList['miff'] = 'Image';
        self.excludeExtList['pct'] = 'Image';
        self.excludeExtList['pic'] = 'Image';
        self.excludeExtList['png'] = 'Image';
        self.excludeExtList['psd'] = 'Image';
        self.excludeExtList['pxr'] = 'Image';
        self.excludeExtList['raw'] = 'Image';
        self.excludeExtList['rle'] = 'Image';
        self.excludeExtList['svg'] = 'Image';
        self.excludeExtList['svgz'] = 'Image';
        self.excludeExtList['tga'] = 'Image';
        self.excludeExtList['tiff'] = 'Image';
        self.excludeExtList['tif'] = 'Image';
        self.excludeExtList['niff'] = 'Image';
        self.excludeExtList['vda'] = 'Image';
        self.excludeExtList['vst'] = 'Image';

        if bExcludeArchive:
            self.excludeExtList['7z'] = 'Compressed archive';
            self.excludeExtList['alz'] = 'Compressed archive';
            self.excludeExtList['ace'] = 'Compressed archive';
            self.excludeExtList['arc'] = 'Compressed archive';
            self.excludeExtList['arj'] = 'Compressed archive';
            self.excludeExtList['bz'] = 'Compressed archive';
            self.excludeExtList['bz2'] = 'Compressed archive';
            self.excludeExtList['cab'] = 'Compressed archive';
            self.excludeExtList['ear'] = 'Compressed archive';
            self.excludeExtList['egg'] = 'Compressed archive';
            self.excludeExtList['gz'] = 'Compressed archive';
            self.excludeExtList['jar'] = 'Compressed archive';
            self.excludeExtList['lha'] = 'Compressed archive';
            self.excludeExtList['lzh'] = 'Compressed archive';
            self.excludeExtList['rar'] = 'Compressed archive';
            self.excludeExtList['tar'] = 'Compressed archive';
            self.excludeExtList['tgz'] = 'Compressed archive';
            self.excludeExtList['war'] = 'Compressed archive';
            self.excludeExtList['z'] = 'Compressed archive';
            self.excludeExtList['zip'] = 'Compressed archive';
            self.excludeExtList['zoo'] = 'Compressed archive';

        # Disk image
        self.excludeExtList['dmg'] = 'Disk image';
        self.excludeExtList['img'] = 'Disk image';
        self.excludeExtList['iso'] = 'Disk image';
        self.excludeExtList['lcd'] = 'Disk image';
        self.excludeExtList['wim'] = 'Disk image';

        # 실행/설치 파일
        self.excludeExtList['apk'] = 'Executable, Installer';
        self.excludeExtList['com'] = 'Executable, Installer';
        self.excludeExtList['class'] = 'Executable, Installer';
        self.excludeExtList['dll'] = 'Executable, Installer';
        self.excludeExtList['exe'] = 'Executable, Installer';
        self.excludeExtList['ipa'] = 'Executable, Installer';
        self.excludeExtList['ipsw'] = 'Executable, Installer';
        self.excludeExtList['msi'] = 'Executable, Installer';
        self.excludeExtList['msu'] = 'Executable, Installer';
        self.excludeExtList['rpm'] = 'Executable, Installer';
        self.excludeExtList['scrypt3'] = 'Executable, Installer';
        self.excludeExtList['scrypt4'] = 'Executable, Installer';
        self.excludeExtList['vcrypt2'] = 'Executable, Installer';
        self.excludeExtList['whl'] = 'Executable, Installer'; # python 

        # 메일 아카이브 
        self.excludeExtList['pst'] = 'Personal Storage Table';

        # 기타 
        self.excludeExtList['dmp'] = 'Others';
        self.excludeExtList['dts'] = 'Others';

            
    def _checkExcludeExt(self, ext:str):
        if (ext == '' or ext == None):
            return False;
        ext = ext.lower();
        if ext in self.excludeExtList:
            return True;
        return False;
            
    def _loadIncludeExtList(self, bIncludeArchive:bool = False):
        self.includeExtList.clear();
        
        # text 
        self.includeExtList['txt'] = 'text';
        self.includeExtList['csv'] = 'text';
        self.includeExtList['prn'] = 'text';
        self.includeExtList['log'] = 'text';
        self.includeExtList['ini'] = 'text';
        self.includeExtList['inf'] = 'text';

        # 워드패드 
        self.includeExtList['rtf'] = 'wordpad';

        self.includeExtList['docx'] = 'MS Word';
        self.includeExtList['doc'] = 'MS Word';
        self.includeExtList['docm'] = 'MS Word';
        self.includeExtList['dot'] = 'MS Word';
        self.includeExtList['dotx'] = 'MS Word';
        self.includeExtList['dotm'] = 'MS Word';

        self.includeExtList['xlsx'] = 'MS Excel';
        self.includeExtList['xls'] = 'MS Excel';
        self.includeExtList['xlsm'] = 'MS Excel';
        self.includeExtList['xlsb'] = 'MS Excel';
        self.includeExtList['xltx'] = 'MS Excel';
        self.includeExtList['xltm'] = 'MS Excel';
        self.includeExtList['xlt'] = 'MS Excel';

        self.includeExtList['pptx'] = 'MS PowerPoint';
        self.includeExtList['ppt'] = 'MS PowerPoint';
        self.includeExtList['pptm'] = 'MS PowerPoint';
        self.includeExtList['potx'] = 'MS PowerPoint';
        self.includeExtList['potm'] = 'MS PowerPoint';
        self.includeExtList['pot'] = 'MS PowerPoint';
        self.includeExtList['ppsx'] = 'MS PowerPoint';
        self.includeExtList['ppsm'] = 'MS PowerPoint';
        self.includeExtList['pps'] = 'MS PowerPoint';
        self.includeExtList['ppa'] = 'MS PowerPoint';
        self.includeExtList['ppam'] = 'MS PowerPoint';

        self.includeExtList['odt'] = 'OpenOffice Document';
        self.includeExtList['ott'] = 'OpenOffice Document';
        self.includeExtList['odm'] = 'OpenOffice Document';

        self.includeExtList['ods'] = 'OpenOffice Spreadsheet';
        self.includeExtList['ots'] = 'OpenOffice Spreadsheet';

        self.includeExtList['odf'] = 'OpenOffice Presentation';
        self.includeExtList['odc'] = 'OpenOffice Presentation';
        self.includeExtList['odg'] = 'OpenOffice Presentation';
        self.includeExtList['odb'] = 'OpenOffice Presentation';

        self.includeExtList['msg'] = 'E-Mail';
        self.includeExtList['eml'] = 'E-Mail';

        self.includeExtList['pdf'] = 'PDF';
        self.includeExtList['xml'] = 'XML';

        self.includeExtList['xps'] = 'XPS';
        self.includeExtList['oxps'] = 'XPS';

        self.includeExtList['hwp'] = 'HWP';
        self.includeExtList['hwt'] = 'HWP';
        self.includeExtList['cell'] = 'HanCell';
        self.includeExtList['show'] = 'HanShow';

        self.includeExtList['htm'] = 'HTML';
        self.includeExtList['html'] = 'HTML';
        self.includeExtList['mhtml'] = 'HTML';
        self.includeExtList['mht'] = 'HTML';
        self.includeExtList['xhtml'] = 'HTML';

        self.includeExtList['java'] = 'Application Source';
        self.includeExtList['c'] = 'Application Source';
        self.includeExtList['cpp'] = 'Application Source';
        self.includeExtList['h'] = 'Application Source';
        self.includeExtList['hpp'] = 'Application Source';
        self.includeExtList['php'] = 'Application Source';
        self.includeExtList['asp'] = 'Application Source';
        self.includeExtList['aspx'] = 'Application Source';
        self.includeExtList['asax'] = 'Application Source';
        self.includeExtList['jsp'] = 'Application Source';
        self.includeExtList['cgi'] = 'Application Source';
        self.includeExtList['pl'] = 'Application Source';
        self.includeExtList['pm'] = 'Application Source';
        self.includeExtList['js'] = 'Application Source';
        self.includeExtList['vbs'] = 'Application Source';
        self.includeExtList['vb'] = 'Application Source';
        self.includeExtList['cs'] = 'Application Source';
        self.includeExtList['css'] = 'Application Source';
        self.includeExtList['py'] = 'Application Source';
        self.includeExtList['rb'] = 'Application Source';
        self.includeExtList['erb'] = 'Application Source';
        self.includeExtList['pas'] = 'Application Source';
        self.includeExtList['sql'] = 'Application Source';

        if bIncludeArchive:
            self.includeExtList['7z'] = 'Compressed archive';
            self.includeExtList['alz'] = 'Compressed archive';
            self.includeExtList['ace'] = 'Compressed archive';
            self.includeExtList['arc'] = 'Compressed archive';
            self.includeExtList['arj'] = 'Compressed archive';
            self.includeExtList['bz'] = 'Compressed archive';
            self.includeExtList['bz2'] = 'Compressed archive';
            self.includeExtList['cab'] = 'Compressed archive';
            self.includeExtList['ear'] = 'Compressed archive';
            self.includeExtList['egg'] = 'Compressed archive';
            self.includeExtList['gz'] = 'Compressed archive';
            self.includeExtList['jar'] = 'Compressed archive';
            self.includeExtList['lha'] = 'Compressed archive';
            self.includeExtList['lzh'] = 'Compressed archive';
            self.includeExtList['rar'] = 'Compressed archive';
            self.includeExtList['tar'] = 'Compressed archive';
            self.includeExtList['tgz'] = 'Compressed archive';
            self.includeExtList['war'] = 'Compressed archive';
            self.includeExtList['z'] = 'Compressed archive';
            self.includeExtList['zip'] = 'Compressed archive';
            self.includeExtList['zoo'] = 'Compressed archive';
        
    def _checkIncludeExt(self, ext:str):
        if (ext == '' or ext == None):
            return False;
        ext = ext.lower();
        if ext in self.includeExtList:
            return True;
        return False;

    def _isAvailableCorpusExt(self, ext:str):
        if self.corpusPolicy == None or 'extType' not in self.corpusPolicy:
            return False;
        if self.corpusPolicy['extType'] == 'include':
            if self._checkIncludeExt(ext):
                return True;
        elif not self.corpusPolicy['extType'] == 'exclude':
            if not self._checkExcludeExt(ext):
                return True;
        return False;            
            
    def detectFileFormat(self, path:str):
        try:
            fmt_id = snf_fmt_detect(path)
            fmt_name = snf_fmt_format_name(fmt_id)
            return fmt_id, fmt_name
        except SNFError as e:
            error_func, error_code = e.args
            raise MpowerException(
                f"function fail. '{error_func}'",
                StatusCode.ERR_PI_EXTRACT_FATAL.value, -1, StatusCode.ERR_PI_EXTRACT_FATAL.name,
                error_code
            )

    def extract(self, srcPath:str, tgtPath:str, checkMultiple:bool=True):
        phpPath = HostName.MPOWER_SCRIPT_HOME + '/util/python_cmd.php';
        phpPath = self.utilClass.changeDirectorySeparator(path=phpPath);
        args = ["php", "-f", phpPath, "--", "-m", "ext", "-s", srcPath, "-t", tgtPath];
        response = subprocess.run(args, stdout=subprocess.PIPE);
        if (response.returncode != 0):
            resultStr = response.stdout.decode("utf-8");            
            result = json.loads(resultStr); 
            msg = '';
            native = '';
            if 'msg' in result:
                msg = result['msg'];
            if 'native' in result:
                native = result['native'];
            raise MpowerException(msg, response.returncode, -1, '', native);
        
        isMultiple = False;
        workDir = 'not defined';
        corpusList = None;
        if checkMultiple:
            isMultiple = self.isMultiFile(tgtPath);
            if isMultiple:
                # tgtPath의 directory에 폴더를 만든다. 
                tgtDir = self.utilClass.get_file_dir(path=tgtPath);
                workDir = tgtDir + "/" + self.utilClass.makeUniqueID();
                corpusList = self._splitCorpusFile(rawPath=tgtPath, workDir=workDir);
        
        return isMultiple, workDir, corpusList;
        
    def isMultiFile(self, path:str):
        fd = None;
        try:
            fd = open(path, 'r');
            buffer = fd.read(7);
            if not buffer:
                return False;
            if len(buffer) == len(MShaAI.SNF_FILE_SEP) and buffer == MShaAI.SNF_FILE_SEP:
                return True;
        except Exception as ex:
            raise MpowerException(
                    "%s (%s)" % (ex, path), 
                    StatusCode.SC_NOT_READ_FILE.value, -1, 
                    StatusCode.SC_NOT_READ_FILE.name, 
                    type(ex).__name__);
        finally:
            if not fd:
                fd.close();
                
    def _splitCorpusFile(self, rawPath:str, workDir:str):
        if (not os.path.exists(rawPath) or not os.path.isfile(rawPath)):
            raise MpowerException(
                    "file not found (%s)" % (rawPath), 
                    StatusCode.SC_NOT_FOUND_FILE.value, -1, 
                    StatusCode.SC_NOT_FOUND_FILE.name);
        self.utilClass.createAllDirectory(workDir);
        
        rawHandle:FileIO = None;
        corpusHandle:FileIO = None;
        corpusList:list = [];
        corpus:dict = {};
        
        try:
            rawHandle = open(rawPath, 'r');
        except Exception as ex:
            raise MpowerException(
                'failed to open raw file. %s %s' % (rawPath, ex), 
                StatusCode.SC_NOT_OPEN_FILE.value, -1, 
                StatusCode.SC_NOT_OPEN_FILE.name, 
                type(ex).__name__);

        bComplete = False;
        try:

            while (True):
                line = rawHandle.readline();
                if not line:
                    break;
                if 0 == line.find(MShaAI.SNF_FILE_SEP):
                    # 새로운 파일이다. 
                    
                    # 기존 핸들을 종료시킨다.
                    if corpusHandle:
                        corpusHandle.flush();
                        corpusHandle.close();
                        corpusHandle = None;
                        
                        # 코퍼스 정보를 정리한다.
                        fsize = self.utilClass.getFileSize(corpus['CRPS_RAW_TEXT_PATH']);
                        corpus['CRPS_LFILE_SIZE'] = fsize;
                        corpus['CRPS_RFILE_SIZE'] = fsize;
                        #self.logger.logging(MLogger.LOG_DEBUG, "corpus size:%d, ext:%s" % (fsize, corpus['CRPS_LFILE_EXT']));
                        # 코퍼스 크기 및 대상 확장자 여부를 점검한다.
                        if fsize > 0 and self._isAvailableCorpusExt(corpus['CRPS_LFILE_EXT']):
                            corpus_copy = corpus.copy();
                            corpusList.append(corpus_copy);
                        else:
                            #self.logger.logging(MLogger.LOG_DEBUG, "delete corpus. path:%s" % (corpus['CRPS_RAW_TEXT_PATH']));
                            if os.path.exists(corpus['CRPS_RAW_TEXT_PATH']):
                                os.remove(corpus['CRPS_RAW_TEXT_PATH']);
                        
                    # 라인 separator를 없앤다.
                    line = line.rstrip('\n');
                    
                    # 파일 전체 경로를 얻어낸다.
                    filepath = line[len(MShaAI.SNF_FILE_SEP):];
                    fdir = self.utilClass.get_file_dir(filepath);
                    fname = self.utilClass.get_file_name(filepath);
                    fext = self.utilClass.get_file_ext(filepath);
                    if fext != '' and len(fext) > 0:
                        fname = fname + '.' + fext;
                    curDate = self.utilClass.getCurrentTime();   
                    if len(corpus) > 0:
                        corpus.clear();
                        
                    corpusDir = workDir + "/" + fdir;
                    corpusDir = self.utilClass.changeDirectorySeparator(corpusDir);
                    self.utilClass.createAllDirectory(corpusDir);
                    corpusPath = corpusDir + "/" + fname + ".raw";
                    corpusPath = self.utilClass.changeDirectorySeparator(corpusPath);
                    #self.logger.logging(MLogger.LOG_DEBUG, "corpus path:%s" % (corpusPath));
                    
                    corpus['PROC_TIME'] = curDate;
                    corpus['CRPS_LFILE_NAME'] = fname;
                    corpus['CRPS_LFILE_PATH'] = fdir;
                    corpus['CRPS_LFILE_EXT'] = fext.lower();
                    corpus['CRPS_LFILE_SIZE'] = 0;
                    corpus['CRPS_RAW_TEXT_PATH'] = corpusPath;
                    
                    corpusHandle = open(corpusPath, 'w');
                else:
                    # 에러가 발생하면 Exception이 발생할 것으로 예상됨. 
                    wsize = corpusHandle.write(line);
                    #if wsize != len(line):
                    #    raise MpowerException
            
            # 기존 핸들을 종료시킨다        
            if corpusHandle:
                corpusHandle.flush();
                corpusHandle.close();
                corpusHandle = None;

                # 코퍼스 정보를 정리한다.
                fsize = self.utilClass.getFileSize(corpus['CRPS_RAW_TEXT_PATH']);
                corpus['CRPS_LFILE_SIZE'] = fsize;
                corpus['CRPS_RFILE_SIZE'] = fsize;
                # 코퍼스 크기 및 대상 확장자 여부를 점검한다.
                if fsize > 0 and self._isAvailableCorpusExt(corpus['CRPS_LFILE_EXT']):
                    corpus_copy = corpus.copy();
                    corpusList.append(corpus_copy);
                else:
                    if os.path.exists(corpus['CRPS_RAW_TEXT_PATH']):
                        os.remove(corpus['CRPS_RAW_TEXT_PATH']);

            bComplete = True;
            
        except Exception as ex:
            raise MpowerException(
                'failed to splite raw file. %s %s' % (rawPath, ex), 
                StatusCode.SC_NOT_WRITE_FILE.value, -1, 
                StatusCode.SC_NOT_WRITE_FILE.name, 
                type(ex).__name__);
        except MpowerException as ex2:
            raise ex2;                    
        finally:
            if rawHandle:
                rawHandle.close();
                rawHandle = None;
            if corpusHandle:
                corpusHandle.close();
                corpusHandle = None;   
            if not bComplete and os.path.exists(workDir) and os.path.isdir(workDir):
                self.utilClass.deleteAllDirectory(workDir);
                
        return corpusList;                                
