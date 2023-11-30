#include "stdafx.h"
#include <string.h>
#if defined(__USE_MOCOCRYPTO)
#if defined(_WIN32)
#include <windows.h>
#else // !defined(_WIN32)
#include <dlfcn.h>
#include <endian.h>
#endif // !defined(_WIN32)
#include "moco-crypto.h"

NEO_ARIA_256_Encrypt_FUNC g_lpfnNEO_ARIA_256_Encrypt;
NEO_ARIA_256_Decrypt_FUNC g_lpfnNEO_ARIA_256_Decrypt;

NEO_ARIA_256_CTR_Encrypt_FUNC g_lpfnNEO_ARIA_256_CTR_Encrypt;
NEO_ARIA_256_CTR_Decrypt_FUNC g_lpfnNEO_ARIA_256_CTR_Decrypt;

NEO_ARIA_256_CBC_Encrypt_FUNC g_lpfnNEO_ARIA_256_CBC_Encrypt;
NEO_ARIA_256_CBC_Decrypt_FUNC g_lpfnNEO_ARIA_256_CBC_Decrypt;

NEO_SEED_128_Encrypt_FUNC g_lpfnNEO_SEED_128_Encrypt;
NEO_SEED_128_Decrypt_FUNC g_lpfnNEO_SEED_128_Decrypt;

NEO_SEED_128_CTR_Encrypt_FUNC g_lpfnNEO_SEED_128_CTR_Encrypt;
NEO_SEED_128_CTR_Decrypt_FUNC g_lpfnNEO_SEED_128_CTR_Decrypt;

NEO_SEED_128_CBC_Encrypt_FUNC g_lpfnNEO_SEED_128_CBC_Encrypt;
NEO_SEED_128_CBC_Decrypt_FUNC g_lpfnNEO_SEED_128_CBC_Decrypt;

NEO_SHA_256_Init_FUNC g_lpfnNEO_SHA_256_Init;
NEO_SHA_256_Update_FUNC g_lpfnNEO_SHA_256_Update;
NEO_SHA_256_Final_FUNC g_lpfnNEO_SHA_256_Final;
NEO_SHA_256_Free_FUNC g_lpfnNEO_SHA_256_Free;
NEO_SHA_256_FUNC g_lpfnNEO_SHA_256;

NEO_HMAC_SHA_256_Init_FUNC g_lpfnNEO_HMAC_SHA_256_Init;
NEO_HMAC_SHA_256_Update_FUNC g_lpfnNEO_HMAC_SHA_256_Update;
NEO_HMAC_SHA_256_Final_FUNC g_lpfnNEO_HMAC_SHA_256_Final;
NEO_HMAC_SHA_256_Free_FUNC g_lpfnNEO_HMAC_SHA_256_Free;
NEO_HMAC_SHA_256_FUNC g_lpfnNEO_HMAC_SHA_256;

NEO_DRBG_Instantiate_FUNC g_lpfnNEO_DRBG_Instantiate;
NEO_DRBG_Reseed_FUNC g_lpfnNEO_DRBG_Reseed;
NEO_DRBG_Generate_FUNC g_lpfnNEO_DRBG_Generate;
NEO_DRBG_SetReseedInterval_FUNC g_lpfnNEO_DRBG_SetReseedInterval;
NEO_DRBG_GetReseedInterval_FUNC g_lpfnNEO_DRBG_GetReseedInterval;
NEO_DRBG_Uninstantiate_FUNC g_lpfnNEO_DRBG_Uninstantiate;

NEO_PreOperationalSelfTest_FUNC g_lpfnNEO_PreOperationalSelfTest;

NEO_GetMocoCryptoStatus_FUNC g_lpfnNEO_GetMocoCryptoStatus;

NEO_GetMocoCryptoVersionInfo_FUNC g_lpfnNEO_GetMocoCryptoVersionInfo;

#if defined(_WIN32)
#define DL_FETCH_SYMBOL(h, sym) GetProcAddress(h, sym)
#else // !defined(_WIN32)
#define DL_FETCH_SYMBOL(h, sym) dlsym(h, sym)
#endif // !defined(_WIN32)

bool MOCO_LoadModule(void* hModule)
{
	g_lpfnNEO_ARIA_256_Encrypt = (NEO_ARIA_256_Encrypt_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_ARIA_256_Encrypt");
	if(g_lpfnNEO_ARIA_256_Encrypt == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_ARIA_256_Decrypt = (NEO_ARIA_256_Decrypt_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_ARIA_256_Decrypt");
	if(g_lpfnNEO_ARIA_256_Decrypt == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_ARIA_256_CTR_Encrypt = (NEO_ARIA_256_CTR_Encrypt_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_ARIA_256_CTR_Encrypt");
	if(g_lpfnNEO_ARIA_256_CTR_Encrypt == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_ARIA_256_CTR_Decrypt = (NEO_ARIA_256_CTR_Decrypt_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_ARIA_256_CTR_Decrypt");
	if(g_lpfnNEO_ARIA_256_CTR_Decrypt == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_ARIA_256_CBC_Encrypt = (NEO_ARIA_256_CBC_Encrypt_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_ARIA_256_CBC_Encrypt");
	if(g_lpfnNEO_ARIA_256_CBC_Encrypt == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_ARIA_256_CBC_Decrypt = (NEO_ARIA_256_CBC_Decrypt_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_ARIA_256_CBC_Decrypt");
	if(g_lpfnNEO_ARIA_256_CBC_Decrypt == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_SEED_128_Encrypt = (NEO_SEED_128_Encrypt_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_SEED_128_Encrypt");
	if(g_lpfnNEO_SEED_128_Encrypt == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_SEED_128_Decrypt = (NEO_SEED_128_Decrypt_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_SEED_128_Decrypt");
	if(g_lpfnNEO_SEED_128_Decrypt == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_SEED_128_CTR_Encrypt = (NEO_SEED_128_CTR_Encrypt_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_SEED_128_CTR_Encrypt");
	if(g_lpfnNEO_SEED_128_CTR_Encrypt == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_SEED_128_CTR_Decrypt = (NEO_SEED_128_CTR_Decrypt_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_SEED_128_CTR_Decrypt");
	if(g_lpfnNEO_SEED_128_CTR_Decrypt == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_SEED_128_CBC_Encrypt = (NEO_SEED_128_CBC_Encrypt_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_SEED_128_CBC_Encrypt");
	if(g_lpfnNEO_SEED_128_CBC_Encrypt == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_SEED_128_CBC_Decrypt = (NEO_SEED_128_CBC_Decrypt_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_SEED_128_CBC_Decrypt");
	if(g_lpfnNEO_SEED_128_CBC_Decrypt == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_SHA_256_Init = (NEO_SHA_256_Init_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_SHA_256_Init");
	if(g_lpfnNEO_SHA_256_Init == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_SHA_256_Update = (NEO_SHA_256_Update_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_SHA_256_Update");
	if(g_lpfnNEO_SHA_256_Update == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_SHA_256_Final = (NEO_SHA_256_Final_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_SHA_256_Final");
	if(g_lpfnNEO_SHA_256_Final == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_SHA_256_Free = (NEO_SHA_256_Free_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_SHA_256_Free");
	if(g_lpfnNEO_SHA_256_Free == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_SHA_256 = (NEO_SHA_256_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_SHA_256");
	if(g_lpfnNEO_SHA_256 == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_HMAC_SHA_256_Init = (NEO_HMAC_SHA_256_Init_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_HMAC_SHA_256_Init");
	if(g_lpfnNEO_HMAC_SHA_256_Init == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_HMAC_SHA_256_Update = (NEO_HMAC_SHA_256_Update_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_HMAC_SHA_256_Update");
	if(g_lpfnNEO_HMAC_SHA_256_Update == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_HMAC_SHA_256_Final = (NEO_HMAC_SHA_256_Final_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_HMAC_SHA_256_Final");
	if(g_lpfnNEO_HMAC_SHA_256_Final == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_HMAC_SHA_256_Free = (NEO_HMAC_SHA_256_Free_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_HMAC_SHA_256_Free");
	if(g_lpfnNEO_HMAC_SHA_256_Free == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_HMAC_SHA_256 = (NEO_HMAC_SHA_256_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_HMAC_SHA_256");
	if(g_lpfnNEO_HMAC_SHA_256 == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_DRBG_Instantiate = (NEO_DRBG_Instantiate_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_DRBG_Instantiate");
	if(g_lpfnNEO_DRBG_Instantiate == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_DRBG_Reseed = (NEO_DRBG_Reseed_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_DRBG_Reseed");
	if(g_lpfnNEO_DRBG_Reseed == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_DRBG_Generate = (NEO_DRBG_Generate_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_DRBG_Generate");
	if(g_lpfnNEO_DRBG_Generate == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_DRBG_SetReseedInterval = (NEO_DRBG_SetReseedInterval_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_DRBG_SetReseedInterval");
	if(g_lpfnNEO_DRBG_SetReseedInterval == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_DRBG_GetReseedInterval = (NEO_DRBG_GetReseedInterval_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_DRBG_GetReseedInterval");
	if(g_lpfnNEO_DRBG_GetReseedInterval == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_DRBG_Uninstantiate = (NEO_DRBG_Uninstantiate_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_DRBG_Uninstantiate");
	if(g_lpfnNEO_DRBG_Uninstantiate == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_PreOperationalSelfTest = (NEO_PreOperationalSelfTest_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_PreOperationalSelfTest");
	if(g_lpfnNEO_PreOperationalSelfTest == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_GetMocoCryptoStatus = (NEO_GetMocoCryptoStatus_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_GetMocoCryptoStatus");
	if(g_lpfnNEO_GetMocoCryptoStatus == NULL)
	{
		return FALSE;
	}
	g_lpfnNEO_GetMocoCryptoVersionInfo = (NEO_GetMocoCryptoVersionInfo_FUNC)DL_FETCH_SYMBOL(hModule, "NEO_GetMocoCryptoVersionInfo");
	if(g_lpfnNEO_GetMocoCryptoVersionInfo == NULL)
	{
		return FALSE;
	}

	return TRUE;
}

void MOCO_CleanupModule()
{
	g_lpfnNEO_ARIA_256_Encrypt = NULL;
	g_lpfnNEO_ARIA_256_Decrypt = NULL;
	g_lpfnNEO_ARIA_256_CTR_Encrypt = NULL;
	g_lpfnNEO_ARIA_256_CTR_Decrypt = NULL;
	g_lpfnNEO_ARIA_256_CBC_Encrypt = NULL;
	g_lpfnNEO_ARIA_256_CBC_Decrypt = NULL;
	g_lpfnNEO_SEED_128_Encrypt = NULL;
	g_lpfnNEO_SEED_128_Decrypt = NULL;
	g_lpfnNEO_SEED_128_CTR_Encrypt = NULL;
	g_lpfnNEO_SEED_128_CTR_Decrypt = NULL;
	g_lpfnNEO_SEED_128_CBC_Encrypt = NULL;
	g_lpfnNEO_SEED_128_CBC_Decrypt = NULL;
	g_lpfnNEO_SHA_256_Init = NULL;
	g_lpfnNEO_SHA_256_Update = NULL;
	g_lpfnNEO_SHA_256_Final = NULL;
	g_lpfnNEO_SHA_256_Free = NULL;
	g_lpfnNEO_SHA_256 = NULL;
	g_lpfnNEO_HMAC_SHA_256_Init = NULL;
	g_lpfnNEO_HMAC_SHA_256_Update = NULL;
	g_lpfnNEO_HMAC_SHA_256_Final = NULL;
	g_lpfnNEO_HMAC_SHA_256_Free = NULL;
	g_lpfnNEO_HMAC_SHA_256 = NULL;
	g_lpfnNEO_DRBG_Instantiate = NULL;
	g_lpfnNEO_DRBG_Reseed = NULL;
	g_lpfnNEO_DRBG_Generate = NULL;
	g_lpfnNEO_DRBG_SetReseedInterval = NULL;
	g_lpfnNEO_DRBG_GetReseedInterval = NULL;
	g_lpfnNEO_DRBG_Uninstantiate = NULL;
	g_lpfnNEO_PreOperationalSelfTest = NULL;
	g_lpfnNEO_GetMocoCryptoStatus = NULL;
	g_lpfnNEO_GetMocoCryptoVersionInfo = NULL;
}

DWORD MOCO_PaddSet(
	BYTE	*pbOutBuffer,
	DWORD	dRmdLen,
	DWORD	dBlockLen,
	DWORD	dPaddingType)
{
	DWORD dPadLen;

	switch( dPaddingType ) {
		case AI_NO_PADDING :
			if( dRmdLen==0 )	return 0;
			else				return CTR_DATA_LEN_ERROR;

		case AI_PKCS_PADDING :
			dPadLen = dBlockLen - dRmdLen;
			memset(pbOutBuffer+dRmdLen, (char)dPadLen, (int)dPadLen);
			return dPadLen;

		default :
			return CTR_FATAL_ERROR;
	}
}

DWORD MOCO_PaddCheck(
	BYTE	*pbOutBuffer,
	DWORD	dBlockLen,
	DWORD	dPaddingType)
{
	DWORD i, dPadLen;

	switch( dPaddingType ) {
		case AI_NO_PADDING :
			return 0;			//	padding된 데이타가 0바이트임.

		case AI_PKCS_PADDING :
			dPadLen = pbOutBuffer[dBlockLen-1];
			if( ((int)dPadLen<=0) || (dPadLen>(int)dBlockLen) )
				return CTR_PAD_CHECK_ERROR;
			for( i=1; i<=dPadLen; i++)
				if( pbOutBuffer[dBlockLen-i] != dPadLen )
					return CTR_PAD_CHECK_ERROR;
			return dPadLen;

		default :
			return CTR_FATAL_ERROR;
	}
}

static ULONGLONG MOCO_BE64ToH(ULONGLONG u64BE)
{
#if defined(_WIN32)
	return _byteswap_uint64(u64BE);
#else // !defined(_WIN32)
	return be64toh(u64BE);
#endif // !defined(_WIN32)
}

void MOCO_MakeNonceAndCounter(
	BYTE* lpbtNonce,			// 출력, 8바이트 버퍼, Nonce
	ULONGLONG* lpullCounter,	// 출력, ULONGLONG, 카운터
	BYTE* lpbtIV,				// 입력, 16바이트 버퍼, IV
	LONGLONG n64BlockNumber		// 입력, 암호화할 블록 번호
	)
{
	ULONGLONG u64IVHighPartBE;
	ULONGLONG u64IVLowPartBE;
	memcpy(&u64IVHighPartBE, lpbtIV, sizeof(ULONGLONG));
	memcpy(&u64IVLowPartBE, &lpbtIV[sizeof(ULONGLONG)], sizeof(ULONGLONG));

	ULONGLONG u64IVHighPart = MOCO_BE64ToH(u64IVHighPartBE);
	ULONGLONG u64IVLowPart = MOCO_BE64ToH(u64IVLowPartBE);

	ULONGLONG u64CTRHighPart;
	// u64IVLowPartLE + u64BlockNumber에서 오버플로우가 발생하는지 검사
	if(UINT64_MAX - u64IVLowPart < (ULONGLONG) n64BlockNumber)
	{
		// 오버 플로우되면 u64CTRHighPartLE에 1을 더 함.
		u64CTRHighPart = u64IVHighPart + 1;
	}
	else
	{
		u64CTRHighPart = u64IVHighPart;
	}
	ULONGLONG u64CTRLowPart = u64IVLowPart + (ULONGLONG) n64BlockNumber;

	// 생성한 Nonce와 Counter 복사
	ULONGLONG u64CTRHighPartBE = MOCO_BE64ToH(u64CTRHighPart);
	memcpy(lpbtNonce, &u64CTRHighPartBE, CTR_NONCE_SIZE_BYTE);
	*lpullCounter = u64CTRLowPart;
}

#endif // defined(__USE_MOCOCRYPTO)
