#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include "structmember.h"
#include "Sha256.h"
#include "kisa-aria.h"
#include "kisa-seed.h"
#include "global.h"
#include "md5.h"
#include "moco-crypto.h"
#include "moco-seed.h"
#include "moco-aria.h"
#if !defined(_WIN32)
#include <dlfcn.h>
#endif // !defined(_WIN32)

#if !defined(ARRAYSIZE)
#define ARRAYSIZE(a) (sizeof(a)/sizeof(a[0]))
#endif // !defined(ARRAYSIZE)

typedef struct
{
	int enc_mode;
	int key_bits;
	int key_bytes;
	int block_bits;
	int block_bytes;
	int mode;
	int padding_type;
	bool random_access;
} ENC_MODE_INFO;

static const ENC_MODE_INFO g_cipher_mode_info[] =
{
	{ 1, 128, 16, 128, 16, AI_CBC, AI_PKCS_PADDING, false }, // KISA_SEED_128_CBC
	{ 2, 128, 16, 128, 16, AI_ECB, AI_PKCS_PADDING, true  }, // KISA_SEED_128_ECB
	{ 3, 128, 16, 128, 16, AI_CTR, AI_PKCS_PADDING, true  }, // KISA_SEED_128_CTR
	{ 4, 128, 16, 128, 16, AI_CBC, AI_PKCS_PADDING, false }, // KISA_ARIA_128_CBC
	{ 5, 128, 16, 128, 16, AI_CTR, AI_PKCS_PADDING, true  }, // KISA_ARIA_128_CTR
	{ 6, 192, 24, 128, 16, AI_CBC, AI_PKCS_PADDING, false }, // KISA_ARIA_192_CBC
	{ 7, 192, 24, 128, 16, AI_CTR, AI_PKCS_PADDING, true  }, // KISA_ARIA_192_CTR
	{ 8, 256, 32, 128, 16, AI_CBC, AI_PKCS_PADDING, false }, // KISA_ARIA_256_CBC
	{ 9, 256, 32, 128, 16, AI_CTR, AI_PKCS_PADDING, true  }, // KISA_ARIA_256_CTR

    { 11, 128, 16, 128, 16, AI_CBC, AI_PKCS_PADDING, false }, // MOCO_SEED_128_CBC
	{ 13, 128, 16, 128, 16, AI_CTR, AI_PKCS_PADDING, true  }, // MOCO_SEED_128_CTR
	{ 18, 256, 32, 128, 16, AI_CBC, AI_PKCS_PADDING, false }, // MOCO_ARIA_256_CBC
	{ 19, 256, 32, 128, 16, AI_CTR, AI_PKCS_PADDING, true  }, // MOCO_ARIA_256_CTR
};

static void mpower_getmd5keyiv_ext(const char* szMRK, int nBits, int nKeySize, char* szKey, char* szIV)
{
	char szRandom[1500];
	int keyvallen = 0;
	int iInsertPos = 0;
	char* pDst = NULL;
	char* pSrc = NULL;
	unsigned int i = 0;

	MD5_CTX md_context;
	char md_buffer[128];
	unsigned char md_digest[16];
	unsigned int md_len = 0;
	char szHashCode[128];

	CSha256 sha_context = { 0, };
	Byte sha_digest[32] = { 0, };

	memset(szRandom, 0x00, sizeof(szRandom));
	memset(md_buffer, 0x00, sizeof(md_buffer));
	memset(md_digest, 0x00, sizeof(md_digest));
	memset(szHashCode, 0x00, sizeof(szHashCode));

	strcpy(szRandom,
		"A2BB49D3E72148cf9C6891C4A2CDC771"
		"576FBF23E11741c4A6F865B9D0E8905D"
		"7B246C38F8FE4954A621784C20035B79"
		"DBBB76226C7E4818BD9696FF4545C6C6"
		"CDFE0EE37D274d0eBD0CF8386902F742"
		"E776EBA6EC9B40a587D3E90A0962D045"
		"69B065878FF54d9d83F2A0911DEBFDB0"
		"BD6750ACEEB44fa0BBDF1545AB222585"
		"04FB81DC0BF840fcA73F03BF3EA43024"
		"9D889AE7F5FE422dA01E6631314A7826"
		"ACB1AF144D4C455d98E06122B183D449"
		"A0570B5320934aa8A190CF80A74D5A70"
		"A41ED32F9AA54419821C7F32C19D4D5E"
		"6DCC5BA958594f59AC127D23566C81DE"
		"6089A666E58B45399C02C6D95FE92EC1"
		"DF063B1D2EF443b19FC16360C60498AC"
		"71B2D49F423742db948BFADDFC137DF0"
		"6190EDC63C924cd4A20DEED6D1A46708"
		"8EDE3C14DDE44e6fA97AE6628F418D92"
		"73CC1FB21A0E4898B7E7C2CB33510E69"
		"8DA04E0CB59243ee91021994FD70F332"
		"A260380A1D6B4d759D9CE6C034E18EEA"
		"A99A8CA9C2074e8990F1166072F565E4"
		"792CFE8EA90E4268AD8EA529136A8F14"
		"84158F301BE24289937393910AB61B0B"
		"830C9E35E3CA4fda84FF89301CA30C76"
		"017E43120CCE4e6fBFB7C5BA62790354"
		"91B71D5A0E694c9cB4BB1569B5980D23"
		"EDC0DEE7458D43d88073929FB1936855"
		"79DBECA932774d49AE5F11ED946BE1CE"
		"C066A78616E844399D1A19515BC461C6"
		"F5C34B8391F54e20B29F898CE5920306"
		"363F8EBA5CC240d6A292FE4CA755D2A9"
		"E87E3EC42FA04bf5B6616C8C51A9EA67"
		"0AF876CFB061470187D357776060FE5F"
		"7FC62409EEBD455bB886E0A5B50B276C"
		"2B6CF58BF0D54e9d8D414C4B0AF8A6AC"
		"67C369458A4F42c9BBEE162986956E1D"
		"E2598CB9368344299F4040439380F151"
		"A60E1BBFD6C44137897863C4692393DD");

	keyvallen = strlen(szRandom);
	iInsertPos = strlen(szMRK) + 1;

	for (i = 0; i < strlen(szMRK); i++)
	{
		if (iInsertPos >= keyvallen)
			iInsertPos = 0;

		pDst = &szRandom[iInsertPos + 1];
		pSrc = &szRandom[iInsertPos];
		memmove(pDst, pSrc, strlen(szRandom) - iInsertPos);
		szRandom[iInsertPos] = szMRK[i];

		iInsertPos += strlen(szMRK) + i;
	}

	if (nBits == 128)
	{
		md_len = keyvallen;
		MD5Init(&md_context);
		MD5Update(&md_context, (unsigned char*)szRandom, md_len);
		MD5Final(md_digest, &md_context);
		for (i = 0; i < 16; i++)
		{
			sprintf(&md_buffer[2 * i], "%02x", md_digest[i]);
		}
		memcpy(szHashCode, md_buffer, 32);
	} 
	else
	{
		md_len = keyvallen;
		Sha256_Init(&sha_context);
		Sha256_Update(&sha_context, (Byte*)szRandom, md_len);
		Sha256_Final(&sha_context, sha_digest);
		for (i = 0; i < 32; i++)
		{
			sprintf(&md_buffer[2 * i], "%02x", sha_digest[i]);
		}
		memcpy(szHashCode, md_buffer, 64);
	}

	memcpy(szKey, szHashCode, nKeySize);
	memcpy(szIV, &szHashCode[nKeySize], 16);
}

//////////////////////////////////////////////////////////////////////////////
// 모듈 전역 변수
//////////////////////////////////////////////////////////////////////////////

typedef struct
{
	void *mococrypto_dll;
} _CRYPT_STATE;

static _CRYPT_STATE *get_mcrypt_state();

//////////////////////////////////////////////////////////////////////////////
// _MCrypt
//////////////////////////////////////////////////////////////////////////////

typedef struct __MCrypt
{
	PyObject_HEAD
	bool finished;
	bool random_access;
	int enc_or_dec;
	ENC_MODE_INFO enc_mode_info;
	char *mrk;
	union
	{
		SEED_ALG_INFO kisa_seed;
		ARIA_ALG_INFO kisa_aria;
		MOCO_SEED_ALG_INFO moco_seed;
		MOCO_ARIA_ALG_INFO moco_aria;
	} alg_info;
	bool (*update_func)(struct __MCrypt *self, void *dstbuf, size_t *dstlen, const void *srcbuf, size_t srclen);
	bool (*final_func)(struct __MCrypt *self, void *dstbuf, size_t *dstlen);
	long long (*get_counter)(struct __MCrypt *self);
	void (*set_counter)(struct __MCrypt *self, long long counter);
} _MCrypt;

static PyTypeObject _MCrypt_Type;

static bool _MCrypt_update_kisa_seed_enc(_MCrypt *self, void *dstbuf, size_t *dstlen, const void *srcbuf, size_t srclen);
static bool _MCrypt_update_kisa_seed_dec(_MCrypt *self, void *dstbuf, size_t *dstlen, const void *srcbuf, size_t srclen);
static bool _MCrypt_final_kisa_seed_enc(_MCrypt *self, void *dstbuf, size_t *dstlen);
static bool _MCrypt_final_kisa_seed_dec(_MCrypt *self, void *dstbuf, size_t *dstlen);
static long long _MCrypt_get_counter_kisa_seed(_MCrypt *self);
static void _MCrypt_set_counter_kisa_seed(_MCrypt *self, long long counter);

static bool _MCrypt_update_kisa_aria_enc(_MCrypt *self, void *dstbuf, size_t *dstlen, const void *srcbuf, size_t srclen);
static bool _MCrypt_update_kisa_aria_dec(_MCrypt *self, void *dstbuf, size_t *dstlen, const void *srcbuf, size_t srclen);
static bool _MCrypt_final_kisa_aria_enc(_MCrypt *self, void *dstbuf, size_t *dstlen);
static bool _MCrypt_final_kisa_aria_dec(_MCrypt *self, void *dstbuf, size_t *dstlen);
static long long _MCrypt_get_counter_kisa_aria(_MCrypt *self);
static void _MCrypt_set_counter_kisa_aria(_MCrypt *self, long long counter);

static bool _MCrypt_update_moco_seed_enc(_MCrypt *self, void *dstbuf, size_t *dstlen, const void *srcbuf, size_t srclen);
static bool _MCrypt_update_moco_seed_dec(_MCrypt *self, void *dstbuf, size_t *dstlen, const void *srcbuf, size_t srclen);
static bool _MCrypt_final_moco_seed_enc(_MCrypt *self, void *dstbuf, size_t *dstlen);
static bool _MCrypt_final_moco_seed_dec(_MCrypt *self, void *dstbuf, size_t *dstlen);
static long long _MCrypt_get_counter_moco_seed(_MCrypt *self);
static void _MCrypt_set_counter_moco_seed(_MCrypt *self, long long counter);

static bool _MCrypt_update_moco_aria_enc(_MCrypt *self, void *dstbuf, size_t *dstlen, const void *srcbuf, size_t srclen);
static bool _MCrypt_update_moco_aria_dec(_MCrypt *self, void *dstbuf, size_t *dstlen, const void *srcbuf, size_t srclen);
static bool _MCrypt_final_moco_aria_enc(_MCrypt *self, void *dstbuf, size_t *dstlen);
static bool _MCrypt_final_moco_aria_dec(_MCrypt *self, void *dstbuf, size_t *dstlen);
static long long _MCrypt_get_counter_moco_aria(_MCrypt *self);
static void _MCrypt_set_counter_moco_aria(_MCrypt *self, long long counter);

static int _MCrypt___init___kisa_seed_enc(_MCrypt *self, void *key, void *iv)
{
	self->update_func = &_MCrypt_update_kisa_seed_enc;
	self->final_func = &_MCrypt_final_kisa_seed_enc;
	self->get_counter = &_MCrypt_get_counter_kisa_seed;
	self->set_counter = &_MCrypt_set_counter_kisa_seed;

	SEED_SetAlgInfo(
		self->enc_mode_info.mode,
		self->enc_mode_info.padding_type,
		iv,
		&self->alg_info.kisa_seed
	);
	if(CTR_SUCCESS != SEED_KeySchedule(key, self->enc_mode_info.key_bytes, &self->alg_info.kisa_seed))
	{
		return -1;
	}

	if(CTR_SUCCESS != SEED_EncInit(&self->alg_info.kisa_seed))
	{
		return -1;
	}

	return 0;
}

static int _MCrypt___init___moco_seed_enc(_MCrypt *self, void *key, void *iv)
{
	self->update_func = &_MCrypt_update_moco_seed_enc;
	self->final_func = &_MCrypt_final_moco_seed_enc;
	self->get_counter = &_MCrypt_get_counter_moco_seed;
	self->set_counter = &_MCrypt_set_counter_moco_seed;

	MOCO_SEED_SetAlgInfo(
		self->enc_mode_info.mode,
		self->enc_mode_info.padding_type,
		iv,
		&self->alg_info.moco_seed
	);
	if(CTR_SUCCESS != MOCO_SEED_SetKey(key, self->enc_mode_info.key_bytes, &self->alg_info.moco_seed))
	{
		return -1;
	}

	if(CTR_SUCCESS != MOCO_SEED_EncInit(&self->alg_info.moco_seed))
	{
		return -1;
	}

	return 0;
}

static int _MCrypt___init___kisa_seed_dec(_MCrypt *self, void *key, void *iv)
{
	self->update_func = &_MCrypt_update_kisa_seed_dec;
	self->final_func = &_MCrypt_final_kisa_seed_dec;
	self->get_counter = &_MCrypt_get_counter_kisa_seed;
	self->set_counter = &_MCrypt_set_counter_kisa_seed;

	SEED_SetAlgInfo(
		self->enc_mode_info.mode,
		self->enc_mode_info.padding_type,
		iv,
		&self->alg_info.kisa_seed
	);
	if(CTR_SUCCESS != SEED_KeySchedule(key, self->enc_mode_info.key_bytes, &self->alg_info.kisa_seed))
	{
		PyErr_SetString(PyExc_Exception, "SEED_KeySchedule failure");
		return -1;
	}

	if(CTR_SUCCESS != SEED_DecInit(&self->alg_info.kisa_seed))
	{
		PyErr_SetString(PyExc_Exception, "SEED_DecInit failure");
		return -1;
	}

	return 0;
}

static int _MCrypt___init___moco_seed_dec(_MCrypt *self, void *key, void *iv)
{
	self->update_func = &_MCrypt_update_moco_seed_dec;
	self->final_func = &_MCrypt_final_moco_seed_dec;
	self->get_counter = &_MCrypt_get_counter_moco_seed;
	self->set_counter = &_MCrypt_set_counter_moco_seed;

	MOCO_SEED_SetAlgInfo(
		self->enc_mode_info.mode,
		self->enc_mode_info.padding_type,
		iv,
		&self->alg_info.moco_seed
	);
	if(CTR_SUCCESS != MOCO_SEED_SetKey(key, self->enc_mode_info.key_bytes, &self->alg_info.moco_seed))
	{
		PyErr_SetString(PyExc_Exception, "MOCO_SEED_SetKey failure");
		return -1;
	}

	if(CTR_SUCCESS != MOCO_SEED_DecInit(&self->alg_info.moco_seed))
	{
		PyErr_SetString(PyExc_Exception, "MOCO_SEED_DecInit failure");
		return -1;
	}

	return 0;
}

static int _MCrypt___init___kisa_aria_enc(_MCrypt *self, void *key, void *iv)
{
	self->update_func = &_MCrypt_update_kisa_aria_enc;
	self->final_func = &_MCrypt_final_kisa_aria_enc;
	self->get_counter = &_MCrypt_get_counter_kisa_aria;
	self->set_counter = &_MCrypt_set_counter_kisa_aria;

	ARIA_SetAlgInfo(
		AI_ENCRYPT,
		self->enc_mode_info.key_bits,
		self->enc_mode_info.mode,
		self->enc_mode_info.padding_type,
		iv,
		&self->alg_info.kisa_aria
	);
	if(CTR_SUCCESS != ARIA_KeySchedule(key, self->enc_mode_info.key_bytes, &self->alg_info.kisa_aria))
	{
		PyErr_SetString(PyExc_Exception, "ARIA_KeySchedule failure");
		return -1;
	}

	if(CTR_SUCCESS != ARIA_EncInit(&self->alg_info.kisa_aria))
	{
		PyErr_SetString(PyExc_Exception, "ARIA_EncInit failure");
		return -1;
	}

	return 0;
}

static int _MCrypt___init___moco_aria_enc(_MCrypt *self, void *key, void *iv)
{
	self->update_func = &_MCrypt_update_moco_aria_enc;
	self->final_func = &_MCrypt_final_moco_aria_enc;
	self->get_counter = &_MCrypt_get_counter_moco_aria;
	self->set_counter = &_MCrypt_set_counter_moco_aria;

	MOCO_ARIA_SetAlgInfo(
		AI_ENCRYPT,
		self->enc_mode_info.key_bits,
		self->enc_mode_info.mode,
		self->enc_mode_info.padding_type,
		iv,
		&self->alg_info.moco_aria
	);
	if(CTR_SUCCESS != MOCO_ARIA_SetKey(key, self->enc_mode_info.key_bytes, &self->alg_info.moco_aria))
	{
		PyErr_SetString(PyExc_Exception, "MOCO_ARIA_SetKey failure");
		return -1;
	}

	if(CTR_SUCCESS != MOCO_ARIA_EncInit(&self->alg_info.moco_aria))
	{
		PyErr_SetString(PyExc_Exception, "MOCO_EncInit failure");
		return -1;
	}

	return 0;
}

static int _MCrypt___init___kisa_aria_dec(_MCrypt *self, void *key, void *iv)
{
	self->update_func = &_MCrypt_update_kisa_aria_dec;
	self->final_func = &_MCrypt_final_kisa_aria_dec;
	self->get_counter = &_MCrypt_get_counter_kisa_aria;
	self->set_counter = &_MCrypt_set_counter_kisa_aria;

	ARIA_SetAlgInfo(
		self->enc_mode_info.mode == AI_CTR ? AI_ENCRYPT : AI_DECRYPT,
		self->enc_mode_info.key_bits,
		self->enc_mode_info.mode,
		self->enc_mode_info.padding_type,
		iv,
		&self->alg_info.kisa_aria
	);
	if(CTR_SUCCESS != ARIA_KeySchedule(key, self->enc_mode_info.key_bytes, &self->alg_info.kisa_aria))
	{
		PyErr_SetString(PyExc_Exception, "ARIA_KeySchedule failure");
		return -1;
	}

	if(CTR_SUCCESS != ARIA_DecInit(&self->alg_info.kisa_aria))
	{
		PyErr_SetString(PyExc_Exception, "ARIA_DecInit failure");
		return -1;
	}

	return 0;
}

static int _MCrypt___init___moco_aria_dec(_MCrypt *self, void *key, void *iv)
{
	self->update_func = &_MCrypt_update_moco_aria_dec;
	self->final_func = &_MCrypt_final_moco_aria_dec;
	self->get_counter = &_MCrypt_get_counter_moco_aria;
	self->set_counter = &_MCrypt_set_counter_moco_aria;

	MOCO_ARIA_SetAlgInfo(
		self->enc_mode_info.mode == AI_CTR ? AI_ENCRYPT : AI_DECRYPT,
		self->enc_mode_info.key_bits,
		self->enc_mode_info.mode,
		self->enc_mode_info.padding_type,
		iv,
		&self->alg_info.moco_aria
	);
	if(CTR_SUCCESS != MOCO_ARIA_SetKey(key, self->enc_mode_info.key_bytes, &self->alg_info.moco_aria))
	{
		PyErr_SetString(PyExc_Exception, "MOCO_ARIA_SetKey failure");
		return -1;
	}

	if(CTR_SUCCESS != MOCO_ARIA_DecInit(&self->alg_info.moco_aria))
	{
		PyErr_SetString(PyExc_Exception, "MOCO_ARIA_DecInit failure");
		return -1;
	}

	return 0;
}

static int _MCrypt___init__(PyObject *selfobj, PyObject *args, PyObject *kwargs)
{
	_MCrypt *self;
	int return_value = -1;
	static const char * const _keywords[] = {"enc_or_dec", "enc_mode", "mrk", "random_access", NULL};
	int enc_or_dec;
	int enc_mode;
	char *mrk;
	Py_ssize_t mrklen;
	int random_access;
	ENC_MODE_INFO *enc_mode_info = NULL;
	int mode_index;
	char key[256/8];
	char iv[128/8];
	_CRYPT_STATE *state;

	self = (_MCrypt *) selfobj;

	// PyArg_ParseTupleAndKeywords의 포맷 p(bool) 값을 받을 때, 인자 값은 int형이어야 하며,
	// stdbool.h의 bool을 사용하면 리눅스에서 정상 작동하지 않는다.
	if(!PyArg_ParseTupleAndKeywords(args, kwargs, "iiy#p", _keywords, &enc_or_dec, &enc_mode, &mrk, &mrklen, &random_access))
	{
		goto FUNCTION_EXIT;
	}

	for(mode_index = 0; mode_index < ARRAYSIZE(g_cipher_mode_info); mode_index ++)
	{
		if(enc_mode == g_cipher_mode_info[mode_index].enc_mode)
		{
			enc_mode_info = &g_cipher_mode_info[mode_index];
			break;
		}
	}

	if(NULL == enc_mode_info)
	{
		PyErr_SetString(PyExc_ValueError, "Unknown enc_mode");
		return -1;
	}

	if(random_access)
	{
		if(false == enc_mode_info->random_access)
		{
			PyErr_SetString(PyExc_ValueError, "random access not supported");
		}
	}

	switch(enc_mode_info->enc_mode)
	{
	case 11: case 13: case 18: case 19:
		state = get_mcrypt_state();
		if(NULL == state->mococrypto_dll)
		{
			PyErr_SetString(PyExc_Exception, "mococrypto not initialized");
			return -1;
		}
	}

	self->mrk = PyMem_Malloc(mrklen + sizeof(char));
	if(NULL == self->mrk)
	{
		PyErr_NoMemory();
		return -1;
	}

	self->finished = false;
	self->random_access = random_access;
	self->enc_or_dec = enc_or_dec;
	self->enc_mode_info = *enc_mode_info;
	memcpy(self->mrk, mrk, mrklen);
	self->mrk[mrklen] = '\0';

	mpower_getmd5keyiv_ext(self->mrk, self->enc_mode_info.key_bits, self->enc_mode_info.key_bytes, key, iv);

	switch(self->enc_mode_info.enc_mode)
	{
	case 1: case 2: case 3:
		if(AI_ENCRYPT == enc_or_dec)
		{
			return_value = _MCrypt___init___kisa_seed_enc(self, key, iv);
		}
		else if(AI_DECRYPT == enc_or_dec)
		{
			return_value = _MCrypt___init___kisa_seed_dec(self, key, iv);
		}
		else
		{
			PyErr_SetString(PyExc_ValueError, "Unknown enc_or_dec");
			return_value = -1;
		}
		break;
	case 4: case 5: case 6: case 7: case 8: case 9:
		if(AI_ENCRYPT == enc_or_dec)
		{
			return_value = _MCrypt___init___kisa_aria_enc(self, key, iv);
		}
		else if(AI_DECRYPT == enc_or_dec)
		{
			return_value = _MCrypt___init___kisa_aria_dec(self, key, iv);
		}
		else
		{
			PyErr_SetString(PyExc_ValueError, "Unknown enc_or_dec");
			return_value = -1;
		}
		break;
    case 11: case 13:
        if(AI_ENCRYPT == enc_or_dec)
		{
			return_value = _MCrypt___init___moco_seed_enc(self, key, iv);
		}
		else if(AI_DECRYPT == enc_or_dec)
		{
			return_value = _MCrypt___init___moco_seed_dec(self, key, iv);
		}
		else
		{
			PyErr_SetString(PyExc_ValueError, "Unknown enc_or_dec");
			return_value = -1;
		}
		break;
    case 18: case 19:
		if(AI_ENCRYPT == enc_or_dec)
		{
			return_value = _MCrypt___init___moco_aria_enc(self, key, iv);
		}
		else if(AI_DECRYPT == enc_or_dec)
		{
			return_value = _MCrypt___init___moco_aria_dec(self, key, iv);
		}
		else
		{
			PyErr_SetString(PyExc_ValueError, "Unknown enc_or_dec");
			return_value = -1;
		}
		break;
	default:
		PyErr_SetString(PyExc_Exception, "Unknown enc_mode");
		return_value = -1;
	}

FUNCTION_EXIT:

	if(-1 == return_value)
	{
		if(self->mrk)
		{
			PyMem_Free(self->mrk);
		}
	}

    return return_value;
}

static void _MCrypt_dealloc(_MCrypt *self)
{
	if(self->mrk)
	{
		PyMem_Free(self->mrk);
	}
	Py_TYPE(self)->tp_free((PyObject *) self);
}

static bool _MCrypt_update_kisa_seed_enc(_MCrypt *self, void *dstbuf, size_t *dstlen, const void *srcbuf, size_t srclen)
{
	if(CTR_SUCCESS == SEED_EncUpdate(&self->alg_info.kisa_seed, srcbuf, srclen, dstbuf, dstlen))
	{
		return true;
	}
	else
	{
		PyErr_SetString(PyExc_Exception, "SEED_EncUpdate failure");
		return false;
	}
}

static bool _MCrypt_update_kisa_aria_enc(_MCrypt *self, void *dstbuf, size_t *dstlen, const void *srcbuf, size_t srclen)
{
	if(CTR_SUCCESS == ARIA_EncUpdate(&self->alg_info.kisa_aria, srcbuf, srclen, dstbuf, dstlen))
	{
		return true;
	}
	else
	{
		PyErr_SetString(PyExc_Exception, "ARIA_EncUpdate failure");
		return false;
	}
}

static bool _MCrypt_update_kisa_seed_dec(_MCrypt *self, void *dstbuf, size_t *dstlen, const void *srcbuf, size_t srclen)
{
	if(CTR_SUCCESS == SEED_DecUpdate(&self->alg_info.kisa_seed, srcbuf, srclen, dstbuf, dstlen))
	{
		return true;
	}
	else
	{
		PyErr_SetString(PyExc_Exception, "SEED_DecUpdate failure");
		return false;
	}
}

static bool _MCrypt_update_kisa_aria_dec(_MCrypt *self, void *dstbuf, size_t *dstlen, const void *srcbuf, size_t srclen)
{
	if(CTR_SUCCESS == ARIA_DecUpdate(&self->alg_info.kisa_aria, srcbuf, srclen, dstbuf, dstlen))
	{
		return true;
	}
	else
	{
		PyErr_SetString(PyExc_Exception, "SEED_DecUpdate failure");
		return false;
	}
}

static bool _MCrypt_update_moco_seed_enc(_MCrypt *self, void *dstbuf, size_t *dstlen, const void *srcbuf, size_t srclen)
{
	if(CTR_SUCCESS == MOCO_SEED_EncUpdate(&self->alg_info.moco_seed, srcbuf, srclen, dstbuf, dstlen))
	{
		return true;
	}
	else
	{
		PyErr_SetString(PyExc_Exception, "SEED_EncUpdate failure");
		return false;
	}
}

static bool _MCrypt_update_moco_aria_enc(_MCrypt *self, void *dstbuf, size_t *dstlen, const void *srcbuf, size_t srclen)
{
	if(CTR_SUCCESS == MOCO_ARIA_EncUpdate(&self->alg_info.moco_aria, srcbuf, srclen, dstbuf, dstlen))
	{
		return true;
	}
	else
	{
		PyErr_SetString(PyExc_Exception, "ARIA_EncUpdate failure");
		return false;
	}
}

static bool _MCrypt_update_moco_seed_dec(_MCrypt *self, void *dstbuf, size_t *dstlen, const void *srcbuf, size_t srclen)
{
	if(CTR_SUCCESS == MOCO_SEED_DecUpdate(&self->alg_info.moco_seed, srcbuf, srclen, dstbuf, dstlen))
	{
		return true;
	}
	else
	{
		PyErr_SetString(PyExc_Exception, "SEED_DecUpdate failure");
		return false;
	}
}

static bool _MCrypt_update_moco_aria_dec(_MCrypt *self, void *dstbuf, size_t *dstlen, const void *srcbuf, size_t srclen)
{
	if(CTR_SUCCESS == MOCO_ARIA_DecUpdate(&self->alg_info.moco_aria, srcbuf, srclen, dstbuf, dstlen))
	{
		return true;
	}
	else
	{
		PyErr_SetString(PyExc_Exception, "SEED_DecUpdate failure");
		return false;
	}
}

static PyObject *_MCrypt_update(PyObject *selfobj, PyObject *args)
{
	_MCrypt *self;
	PyObject *output = NULL;
	size_t outputlen;
	char *input;
	Py_ssize_t inputlen;

	self = (_MCrypt *) selfobj;

	if(!PyArg_ParseTuple(args, "y#", &input, &inputlen))
	{
		return NULL;
	}

	if(self->finished)
	{
		PyErr_SetString(PyExc_Exception, "Already finished");
		return NULL;
	}

	outputlen = inputlen + self->enc_mode_info.block_bytes - inputlen % self->enc_mode_info.block_bytes;

	output = PyBytes_FromStringAndSize(NULL, outputlen);
	if(NULL == output)
	{
		PyErr_NoMemory();
		return NULL;
	}

	if(self->update_func(self, PyBytes_AS_STRING(output), &outputlen, input, inputlen))
	{
		_PyBytes_Resize(&output, outputlen);
		return output;
	}
	else
	{
		if(output)
		{
			Py_DECREF(output);
		}
		return NULL;
	}
}

static bool _MCrypt_final_kisa_seed_enc(_MCrypt *self, void *dstbuf, size_t *dstlen)
{
	if(CTR_SUCCESS == SEED_EncFinal(&self->alg_info.kisa_seed, dstbuf, dstlen))
	{
		return true;
	}
	else
	{
		PyErr_SetString(PyExc_Exception, "SEED_EncFinal failure");
		return false;
	}
}

static bool _MCrypt_final_kisa_aria_enc(_MCrypt *self, void *dstbuf, size_t *dstlen)
{
	if(CTR_SUCCESS == ARIA_EncFinal(&self->alg_info.kisa_aria, dstbuf, dstlen))
	{
		return true;
	}
	else
	{
		PyErr_SetString(PyExc_Exception, "ARIA_EncFinal failure");
		return false;
	}
}

static bool _MCrypt_final_kisa_seed_dec(_MCrypt *self, void *dstbuf, size_t *dstlen)
{
	if(CTR_SUCCESS == SEED_DecFinal(&self->alg_info.kisa_seed, dstbuf, dstlen))
	{
		return true;
	}
	else
	{
		PyErr_SetString(PyExc_Exception, "SEED_DecFinal failure");
		return false;
	}
}

static bool _MCrypt_final_kisa_aria_dec(_MCrypt *self, void *dstbuf, size_t *dstlen)
{
	if(CTR_SUCCESS == ARIA_DecFinal(&self->alg_info.kisa_aria, dstbuf, dstlen))
	{
		return true;
	}
	else
	{
		PyErr_SetString(PyExc_Exception, "ARIA_DecFinal failure");
		return false;
	}
}

static bool _MCrypt_final_moco_seed_enc(_MCrypt *self, void *dstbuf, size_t *dstlen)
{
	if(CTR_SUCCESS == MOCO_SEED_EncFinal(&self->alg_info.moco_seed, dstbuf, dstlen))
	{
		return true;
	}
	else
	{
		PyErr_SetString(PyExc_Exception, "SEED_EncFinal failure");
		return false;
	}
}

static bool _MCrypt_final_moco_aria_enc(_MCrypt *self, void *dstbuf, size_t *dstlen)
{
	if(CTR_SUCCESS == MOCO_ARIA_EncFinal(&self->alg_info.moco_aria, dstbuf, dstlen))
	{
		return true;
	}
	else
	{
		PyErr_SetString(PyExc_Exception, "ARIA_EncFinal failure");
		return false;
	}
}

static bool _MCrypt_final_moco_seed_dec(_MCrypt *self, void *dstbuf, size_t *dstlen)
{
	if(CTR_SUCCESS == MOCO_SEED_DecFinal(&self->alg_info.moco_seed, dstbuf, dstlen))
	{
		return true;
	}
	else
	{
		PyErr_SetString(PyExc_Exception, "SEED_DecFinal failure");
		return false;
	}
}

static bool _MCrypt_final_moco_aria_dec(_MCrypt *self, void *dstbuf, size_t *dstlen)
{
	if(CTR_SUCCESS == MOCO_ARIA_DecFinal(&self->alg_info.moco_aria, dstbuf, dstlen))
	{
		return true;
	}
	else
	{
		PyErr_SetString(PyExc_Exception, "ARIA_DecFinal failure");
		return false;
	}
}

static PyObject *_MCrypt_final(_MCrypt *self, PyObject *unused_args)
{
	PyObject *output = NULL;
	size_t dstlen = self->enc_mode_info.block_bytes;

	if(self->finished)
	{
		PyErr_SetString(PyExc_Exception, "Already finished");
		return NULL;
	}

	output = PyBytes_FromStringAndSize(NULL, dstlen);
	if(NULL == output)
	{
		PyErr_NoMemory();
		return NULL;
	}

	if(self->final_func(self, PyBytes_AS_STRING(output), &dstlen))
	{
		_PyBytes_Resize(&output, dstlen);
		if(false == self->random_access)
		{
			self->finished = true;
		}
		return output;
	}
	else
	{
		if(output)
		{
			Py_DECREF(output);
		}
		return NULL;
	}
}

static void _MCrypt_set_counter_kisa_seed(_MCrypt *self, long long counter)
{
	self->alg_info.kisa_seed.n64CTRBlcokNumber = counter;
	self->alg_info.kisa_seed.BufLen = 0;
}

static void _MCrypt_set_counter_kisa_aria(_MCrypt *self, long long counter)
{
	self->alg_info.kisa_aria.n64CTRBlcokNumber = counter;
	self->alg_info.kisa_aria.BufLen = 0;
}

static void _MCrypt_set_counter_moco_seed(_MCrypt *self, long long counter)
{
	self->alg_info.moco_seed.n64NextBlockNumber = counter;
	self->alg_info.moco_seed.cbRemainingCipherOrPlainText = 0;
}

static void _MCrypt_set_counter_moco_aria(_MCrypt *self, long long counter)
{
	self->alg_info.moco_aria.n64NextBlockNumber = counter;
	self->alg_info.moco_aria.cbRemainingCipherOrPlainText = 0;
}

static PyObject *_MCrypt_set_counter(_MCrypt *selfobj, PyObject *args)
{
	_MCrypt *self;
	long long counter;

	self = (_MCrypt *) selfobj;

	if(false == self->random_access)
	{
		PyErr_SetString(PyExc_Exception, "not random access");
		return NULL;
	}

	if(!PyArg_ParseTuple(args, "L", &counter))
	{
		return NULL;
	}

	self->set_counter(self, counter);

	Py_RETURN_NONE;
}

static long long _MCrypt_get_counter_kisa_seed(_MCrypt *self)
{
	return self->alg_info.kisa_seed.n64CTRBlcokNumber;
}

static long long _MCrypt_get_counter_kisa_aria(_MCrypt *self)
{
	return self->alg_info.kisa_aria.n64CTRBlcokNumber;
}

static long long _MCrypt_get_counter_moco_seed(_MCrypt *self)
{
	return self->alg_info.moco_seed.n64NextBlockNumber;
}

static long long _MCrypt_get_counter_moco_aria(_MCrypt *self)
{
	return self->alg_info.moco_aria.n64NextBlockNumber;
}

static PyObject *_MCrypt_get_counter(_MCrypt *selfobj, PyObject *args)
{
	_MCrypt *self;
	long long counter;
	PyObject *return_value;

	self = (_MCrypt *) selfobj;

	if(!_PyArg_NoPositional("get_counter", args))
	{
		return NULL;
	}

	counter = self->get_counter(self);
	return PyLong_FromLongLong(counter);
}


static PyObject *_MCrypt_is_finished(_MCrypt *self, PyObject *arg)
{
	return self->finished ? Py_True : Py_False;
}

static PyMethodDef _MCrypt_methods[] =
{
	{ "update", _MCrypt_update, METH_VARARGS, ""},
	{ "final", _MCrypt_final, METH_NOARGS, ""},
	{ "set_counter", _MCrypt_set_counter, METH_VARARGS, "" },
	{ "get_counter", _MCrypt_get_counter, METH_VARARGS, "" },
	{ "is_finished", _MCrypt_is_finished, METH_NOARGS, ""},
	{ NULL, NULL, 0, NULL }
};

static PyMemberDef _MCrypt_members[] =
{
	{ "finished", T_BOOL, offsetof(_MCrypt, finished), READONLY, NULL },
	{ "enc_or_dec", T_INT, offsetof(_MCrypt, enc_or_dec), READONLY, NULL },
	{ "enc_mode", T_INT, offsetof(_MCrypt, enc_mode_info.enc_mode), READONLY, NULL },
	{ "key_bits", T_INT, offsetof(_MCrypt, enc_mode_info.key_bits), READONLY, NULL },
	{ "key_bytes", T_INT, offsetof(_MCrypt, enc_mode_info.key_bytes), READONLY, NULL },
	{ "block_bits", T_INT, offsetof(_MCrypt, enc_mode_info.block_bits), READONLY, NULL },
	{ "block_bytes", T_INT, offsetof(_MCrypt, enc_mode_info.block_bytes), READONLY, NULL },
	{ "mode", T_INT, offsetof(_MCrypt, enc_mode_info.mode), READONLY, NULL },
	{ "padding_type", T_INT, offsetof(_MCrypt, enc_mode_info.padding_type), READONLY, NULL },
	{ "random_access", T_BOOL, offsetof(_MCrypt, random_access), READONLY, NULL },
	{ NULL }
};

static PyTypeObject _MCrypt_Type = {
	PyVarObject_HEAD_INIT(NULL, 0) "pympower_ext._mcrypt._MCrypt",	/* tp_name */
	sizeof(_MCrypt),				/* tp_basicsize */
	0,									/* tp_itemsize */
	(destructor) _MCrypt_dealloc,	/* tp_dealloc */
	0,									/* tp_vectorcall_offset */
	0,									/* tp_getattr */
	0,									/* tp_setattr */
	0,									/* tp_as_async */
	0,									/* tp_repr */
	0,									/* tp_as_number */
	0,									/* tp_as_sequence */
	0,									/* tp_as_mapping */
	0,									/* tp_hash  */
	0,									/* tp_call */
	0,									/* tp_str */
	0,									/* tp_getattro */
	0,									/* tp_setattro */
	0,									/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	0,									/* tp_doc */
	0,									/* tp_traverse */
	0,									/* tp_clear */
	0,									/* tp_richcompare */
	0,									/* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	_MCrypt_methods,				/* tp_methods */
	_MCrypt_members,				/* tp_members */
	0,									/* tp_getset */
	0,									/* tp_base */
	0,									/* tp_dict */
	0,									/* tp_descr_get */
	0,									/* tp_descr_set */
	0,									/* tp_dictoffset */
	_MCrypt___init__,				/* tp_init */
	0,									/* tp_alloc */
	PyType_GenericNew,					/* tp_new */
};

//////////////////////////////////////////////////////////////////////////////
// Crypt 모듈
//////////////////////////////////////////////////////////////////////////////

PyDoc_STRVAR(module_doc,
"Mpower 10.0 crypt extension"
);

static PyObject *_mcrypt_load_mococrypto(PyObject *module, PyObject *args)
{
#ifdef _WIN32
	static const char *args_format = "u";
	wchar_t *path;
	PyObject *pathobj;
#else // !_WIN32
	static const char *args_format = "s";
	char *path;
#endif // !_WIN32
	_CRYPT_STATE *state = (_CRYPT_STATE *) PyModule_GetState(module);

	if(state->mococrypto_dll)
	{
		PyErr_SetString(PyExc_Exception, "mococrypto already initialized");
		return NULL;
	}

	if(!PyArg_ParseTuple(args, args_format, &path))
	{
		return NULL;
	}

#ifdef _WIN32
	state->mococrypto_dll = LoadLibrary(path);
#else // !_WIN32
	state->mococrypto_dll = dlopen(path, RTLD_LAZY);
#endif // !_WIN32
	if(NULL == state->mococrypto_dll)
	{
#ifdef _WIN32
		DWORD dwErrorCode = GetLastError();
		pathobj = PyTuple_GetItem(args, 0);
		PyErr_SetExcFromWindowsErrWithFilenameObjects(PyExc_OSError, dwErrorCode, pathobj, NULL);
#else // !_WIN32
		PyErr_SetString(PyExc_Exception, dlerror());
#endif // !_WIN32
		return NULL;
	}

	if(FALSE == MOCO_LoadModule(state->mococrypto_dll))
	{
#ifdef _WIN32
		FreeLibrary(state->mococrypto_dll);
#else // !_WIN32
		dlclose(state->mococrypto_dll);
#endif // !_WIN32
		state->mococrypto_dll = NULL;
		PyErr_SetString(PyExc_Exception, "failed to initialize mococrypto");
		return NULL;
	}

	Py_RETURN_NONE;
}

static PyMethodDef _mcrypt_methods[] = {
    { "load_mococrypto",  _mcrypt_load_mococrypto, METH_VARARGS, "" },
    { NULL, NULL, 0, NULL }
};

static int _mcrypt_free(PyObject *module)
{
    _CRYPT_STATE *state = (_CRYPT_STATE *) PyModule_GetState(module);
    if(state->mococrypto_dll)
	{
#ifdef _WIN32
		FreeLibrary(state->mococrypto_dll);
#else // !_WIN32
		dlclose(state->mococrypto_dll);
#endif // !_WIN32
		MOCO_CleanupModule();
	}
    return 0;
}

static struct PyModuleDef moduledef = {
	PyModuleDef_HEAD_INIT,
	"pympower_ext._mcrypt",
	module_doc,
	sizeof(_CRYPT_STATE),
	_mcrypt_methods,
	NULL,
	NULL,
	NULL,
	(freefunc) _mcrypt_free
};

static _CRYPT_STATE *get_mcrypt_state()
{
	PyObject *module = PyState_FindModule(&moduledef);
    return (_CRYPT_STATE *) PyModule_GetState(module);
}

PyMODINIT_FUNC PyInit__mcrypt()
{
	PyObject *module = PyModule_Create(&moduledef);
	if (NULL == module)
	{
		return NULL;
	}

#define ADD_TYPE(type)									\
	if(0 > PyModule_AddType(module, type))				\
	{													\
		goto FUNCTION_ERROR_EXIT;						\
	}

	ADD_TYPE(&_MCrypt_Type)

	return module;

FUNCTION_ERROR_EXIT:
	Py_DECREF(module);
	return NULL;
}
