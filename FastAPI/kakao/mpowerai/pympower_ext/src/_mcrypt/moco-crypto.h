// MocoCrypto 라이브러리를 사용하는 함호화 함수.
// 엠파워 소스의 kisa-seed.h와 kisa-aria.h를 참조해 만들었으며,
// moco-crypto.h를 추가 함.
#pragma once

#if defined(__USE_MOCOCRYPTO)

#include <wchar.h>
#if defined(_WIN32)
#define WCHAR wchar_t
#endif // defined(_WIN32)
#define BOOL NEOCRYPTO_BOOL
#include <NEOCrypto.h>
#undef BOOL
#if defined(_WIN32)
#undef WCHAR
#endif // defined(_WIN32)

#include "kisa-crypto.h"

#include <stdbool.h>
bool MOCO_LoadModule(void* hModule);
void MOCO_CleanupModule();

extern NEO_ARIA_256_Encrypt_FUNC g_lpfnNEO_ARIA_256_Encrypt;
extern NEO_ARIA_256_Decrypt_FUNC g_lpfnNEO_ARIA_256_Decrypt;

extern NEO_ARIA_256_CTR_Encrypt_FUNC g_lpfnNEO_ARIA_256_CTR_Encrypt;
extern NEO_ARIA_256_CTR_Decrypt_FUNC g_lpfnNEO_ARIA_256_CTR_Decrypt;

extern NEO_ARIA_256_CBC_Encrypt_FUNC g_lpfnNEO_ARIA_256_CBC_Encrypt;
extern NEO_ARIA_256_CBC_Decrypt_FUNC g_lpfnNEO_ARIA_256_CBC_Decrypt;

extern NEO_SEED_128_Encrypt_FUNC g_lpfnNEO_SEED_128_Encrypt;
extern NEO_SEED_128_Decrypt_FUNC g_lpfnNEO_SEED_128_Decrypt;

extern NEO_SEED_128_CTR_Encrypt_FUNC g_lpfnNEO_SEED_128_CTR_Encrypt;
extern NEO_SEED_128_CTR_Decrypt_FUNC g_lpfnNEO_SEED_128_CTR_Decrypt;

extern NEO_SEED_128_CBC_Encrypt_FUNC g_lpfnNEO_SEED_128_CBC_Encrypt;
extern NEO_SEED_128_CBC_Decrypt_FUNC g_lpfnNEO_SEED_128_CBC_Decrypt;

extern NEO_SHA_256_Init_FUNC g_lpfnNEO_SHA_256_Init;
extern NEO_SHA_256_Update_FUNC g_lpfnNEO_SHA_256_Update;
extern NEO_SHA_256_Final_FUNC g_lpfnNEO_SHA_256_Final;
extern NEO_SHA_256_Free_FUNC g_lpfnNEO_SHA_256_Free;
extern NEO_SHA_256_FUNC g_lpfnNEO_SHA_256;

extern NEO_HMAC_SHA_256_Init_FUNC g_lpfnNEO_HMAC_SHA_256_Init;
extern NEO_HMAC_SHA_256_Update_FUNC g_lpfnNEO_HMAC_SHA_256_Update;
extern NEO_HMAC_SHA_256_Final_FUNC g_lpfnNEO_HMAC_SHA_256_Final;
extern NEO_HMAC_SHA_256_Free_FUNC g_lpfnNEO_HMAC_SHA_256_Free;
extern NEO_HMAC_SHA_256_FUNC g_lpfnNEO_HMAC_SHA_256;

extern NEO_DRBG_Instantiate_FUNC g_lpfnNEO_DRBG_Instantiate;
extern NEO_DRBG_Reseed_FUNC g_lpfnNEO_DRBG_Reseed;
extern NEO_DRBG_Generate_FUNC g_lpfnNEO_DRBG_Generate;
extern NEO_DRBG_SetReseedInterval_FUNC g_lpfnNEO_DRBG_SetReseedInterval;
extern NEO_DRBG_GetReseedInterval_FUNC g_lpfnNEO_DRBG_GetReseedInterval;
extern NEO_DRBG_Uninstantiate_FUNC g_lpfnNEO_DRBG_Uninstantiate;

extern NEO_PreOperationalSelfTest_FUNC g_lpfnNEO_PreOperationalSelfTest;

extern NEO_GetMocoCryptoStatus_FUNC g_lpfnNEO_GetMocoCryptoStatus;

extern NEO_GetMocoCryptoVersionInfo_FUNC g_lpfnNEO_GetMocoCryptoVersionInfo;

DWORD MOCO_PaddSet(
	BYTE	*pbOutBuffer,
	DWORD	dRmdLen,
	DWORD	dBlockLen,
	DWORD	dPaddingType);

DWORD MOCO_PaddCheck(
	BYTE	*pbOutBuffer,
	DWORD	dBlockLen,
	DWORD	dPaddingType);

// IV와 파일의 Block 번호를 이용해 NEO_SEED_128_CTR_Encrypt,
// NEO_SEED_128_CTR_Decrypt, NEO_ARIA_256_CTR_Encrypt,
// NEO_ARIA_256_CTR_Decrypt등의 함수의 입력 값으로 사용할
// Nonce와 Counter를 생성하는 함수
void MOCO_MakeNonceAndCounter(
	BYTE* lpbtNonce,			// 출력, 8바이트 버퍼, Nonce
	ULONGLONG* lpullCounter,	// 출력, ULONGLONG, 카운터
	BYTE* lpbtIV,				// 입력, 16바이트 버퍼, IV
	LONGLONG n64BlockNumber		// 입력, 암호화할 블록 번호
	);

#endif // defined(__USE_MOCOCRYPTO)
