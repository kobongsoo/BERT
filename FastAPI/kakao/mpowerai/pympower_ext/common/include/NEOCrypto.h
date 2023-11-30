#pragma once

/*
* COPYRIGHT : 2010 MOCOMSYS
* FILEPATH  : /Inlcude/NEOCrypto.h
* COMMENT   : 
*/

////////////////////////////////////////////////////////////////
// INCLUDES
////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////
// DEFINES
////////////////////////////////////////////////////////////////

#define CONST const

#define VOID void

#define FALSE		0
#define TRUE		1

#define IN
#define OUT
#define OPTIONAL

// 함수 리턴 오류 상태
#define NEO_SUCCESS										0		   // 함수 호출 성공
#define ERROR_NEO_INVALID_PARAMETER						0xE0000041 // 함수 인자가 올바르지 않은 오류
#define ERROR_NEO_NOT_ENOUGH_MEMORY						0xE0000042 // 메모리 할당 오류
#define ERROR_NEO_SELFTESTING							0xE0000043 // 자가시험 중인 상태

#define ERROR_NEO_SELFTEST_FAIL							0xE0000071 // 자가시험 오류
#define ERROR_NEO_NOISE_SOURCE_COLLECTION_FAIL			0xE0000072 // 난수 발생기 잡음원 수집 오류 또는 난수 발생기 내부에서 생성되는 논스 생성 오류
#define ERROR_NEO_INITIALIZATION						0xE0000073 // 초기화 오류


// ARIA 비밀키 크기(32바이트/256비트)
#define ARIA_256_KEY_SIZE_BYTE				32		

// ARIA 블록 크기
#define ARIA_BLOCK_SIZE_BYTE				16

// SEED 비밀키 크기(16바이트/128비트)
#define SEED_128_KEY_SIZE_BYTE				16		// 16바이트/128비트

// SEED 블록 크기
#define SEED_BLOCK_SIZE_BYTE				16

// NONCE 크기. 8바이트
#define CTR_NONCE_SIZE_BYTE					8

// SHA-256 메시지 다이제스트 크기
#define SHA_256_MESSAGE_DIGEST_SIZE_BYTE	32
#define SHA_256_MESSAGE_DIGEST_SIZE_BIT		256

////////////////////////////////////////////////////////////////
// TYPEDEFES
////////////////////////////////////////////////////////////////
#pragma pack(1)

typedef char CHAR;
typedef CHAR* PCHAR;
typedef unsigned char UCHAR;
typedef UCHAR* PUCHAR;

typedef short SHORT;
typedef unsigned short USHORT;
typedef USHORT* PUSHORT;

#ifdef _WINDOWS
typedef long LONG;
typedef unsigned long ULONG;
typedef ULONG* PULONG;
#endif // _WINDOWS

#ifdef _LINUX
typedef int LONG;
typedef unsigned int ULONG;
typedef ULONG* PULONG;
#endif // _LINUX

typedef unsigned char boolean;
typedef boolean BOOLEAN;

typedef int BOOL;

#ifdef _WINDOWS
typedef __int64 LONGLONG;
typedef LONGLONG* PLONGLONG;

typedef unsigned __int64 ULONGLONG;
typedef ULONGLONG* PULONGLONG;
#endif // _WINDOWS

#ifdef _LINUX
typedef long long LONGLONG;
typedef LONGLONG* PLONGLONG;

typedef unsigned long long ULONGLONG;
typedef ULONGLONG* PULONGLONG;
#endif // _LINUX

typedef void* PVOID;

typedef void* HANDLE;

#ifdef _LINUX
typedef wchar_t WCHAR;
#endif // _LINUX

typedef PVOID HSHA256;
typedef PVOID* PHSHA256;

typedef PVOID HHMACSHA256;
typedef PVOID* PHHMACSHA256;

typedef PVOID HDRBG;
typedef PVOID* PHDRBG;

#pragma pack()

////////////////////////////////////////////////////////////////
// VARIABLES
////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////
// FUNCTIONS
////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////
// ARIA 인터페이스
////////////////////////////////////////////////////////////////

// ARIA 단일 블록 암호화를 수행하는 함수로서, 평문 블록인 PlainTextBlock를 암호화하여, CipherTextBlock에 암호문 블록을 출력한다.
typedef ULONG
(*NEO_ARIA_256_Encrypt_FUNC)(IN CONST UCHAR Key[ARIA_256_KEY_SIZE_BYTE],
							 IN CONST UCHAR PlainTextBlock[ARIA_BLOCK_SIZE_BYTE],
							 OUT UCHAR CipherTextBlock[ARIA_BLOCK_SIZE_BYTE]);

// ARIA 단일 블록 복호화를 수행하는 함수로서, 암호문 블록인 CipherTextBlock를 복호화하여, PlainTextBlock에 평문 블록을 출력한다.
typedef ULONG
(*NEO_ARIA_256_Decrypt_FUNC)(IN CONST UCHAR Key[ARIA_256_KEY_SIZE_BYTE],
							 IN CONST UCHAR CipherTextBlock[ARIA_BLOCK_SIZE_BYTE],
							 OUT UCHAR PlainTextBlock[ARIA_BLOCK_SIZE_BYTE]);

// ARIA CTR 운영모드로 암호화를 수행하는 함수로서, 평문인 pPlainText를 암호화하여, pCipherText에 암호문을 출력한다.
// 출력되는 암호문인 pCipherText의 크기는 PlainTextSize와 크기가 같고 패딩처리는 수행하지 않는다. 
// 따라서, 출력인자 pCipherText가 PlainTextSize보다 적게 메모리 할당이 되었다면, exception 에러가 발생하므로, 출력인자 pCipherText는 PlainTextSize와 같거나 크게 메모리를 할당해야 한다.
typedef ULONG
(*NEO_ARIA_256_CTR_Encrypt_FUNC)(IN CONST UCHAR Key[ARIA_256_KEY_SIZE_BYTE],						 
								 IN CONST UCHAR Nonce[CTR_NONCE_SIZE_BYTE],
								 IN ULONGLONG Counter,
								 IN CONST PUCHAR pPlainText,
								 IN ULONGLONG PlainTextSize,
								 OUT PUCHAR pCipherText);

// ARIA CTR 운영모드로 복호화를 수행하는 함수로서, 암호문인 pCipherText를 복호화하여, pPlainText에 평문을 출력한다.
// 출력되는 평문인 pPlainText의 크기는 CipherTextSize와 크기가 같고 패딩처리는 수행하지 않는다.
// 따라서, 출력인자 pPlainText가 CipherTextSize보다 적게 메모리 할당이 되었다면, exception 에러가 발생하므로, 출력인자 pPlainText는 CipherTextSize와 같거나 크게 메모리를 할당해야 한다.
typedef ULONG
(*NEO_ARIA_256_CTR_Decrypt_FUNC)(IN CONST UCHAR Key[ARIA_256_KEY_SIZE_BYTE],						 
								 IN CONST UCHAR Nonce[CTR_NONCE_SIZE_BYTE],
								 IN ULONGLONG Counter,
								 IN CONST PUCHAR pCipherText,
								 IN ULONGLONG CipherTextSize,
								 OUT PUCHAR pPlainText);

// ARIA CBC 운영모드로 암호화를 수행하는 함수로서, 평문인 pPlainText를 암호화하여, pCipherText에 암호문을 출력하고, Zero 패딩을 수행한다.
// 출력되는 암호문인 pCipherText의 크기는 PlainTextSize가 16(블록 크기)의 배수이면 PlainTextSize와 같고, 16(블록 크기)의 배수가 아니면 Zero 패딩이 수행되어서 PlainTextSize 보다 큰 16(블록 크기)의 배수 크기이다.(ex, PlainTextSize 가 14이면, 출력크기는 Zero 패딩이 수행되어서 16(블록 크기)가 된다.)
// 따라서, 출력인자 pCipherText는 PlainTextSize가 16(블록 크기)의 배수이면 PlainTextSize와 같거나 크게 메모리를 할당해야 하고, PlainTextSize가 16(블록 크기)의 배수가 아니면, PlainTextSize보다 큰 16(블록 크기)의 배수 크기와 같거나 크게 할당해야 한다.
// 그렇지 않으면, exception 에러가 발생한다.
typedef ULONG
(*NEO_ARIA_256_CBC_Encrypt_FUNC)(IN CONST UCHAR Key[ARIA_256_KEY_SIZE_BYTE],						 
								 IN CONST UCHAR InitialVector[ARIA_BLOCK_SIZE_BYTE],
								 IN CONST PUCHAR pPlainText,
								 IN ULONGLONG PlainTextSize,
								 OUT PUCHAR pCipherText,
								 IN OUT PULONGLONG pCipherTextSize);

// ARIA CBC 운영모드로 복호화를 수행하는 함수로서, 암호문인 pCipherText를 복호화하여, pPlainText에 평문을 출력한다.
// pCipherText의 크기는 16(블록 크기)의 배수이어야 한다.
// 출력되는 평문인 pPlainText의 크기는 CipherTextSize와 크기가 같다.
// 따라서, 출력인자 pPlainText가 CipherTextSize보다 적게 메모리 할당이 되었다면, exception 에러가 발생하므로, 출력인자 pPlainText는 CipherTextSize와 같거나 크게 메모리를 할당해야 한다.
// 암호문인 pCipherText가 Zero 패딩된 암호문이므로, 출력되는 평문인 pPlainText에서 패딩된 데이터를 알 수 없다는 것을 주의해야 한다. 
typedef ULONG
(*NEO_ARIA_256_CBC_Decrypt_FUNC)(IN CONST UCHAR Key[ARIA_256_KEY_SIZE_BYTE],						 
								 IN CONST UCHAR InitialVector[ARIA_BLOCK_SIZE_BYTE],
								 IN CONST PUCHAR pCipherText,
								 IN ULONGLONG CipherTextSize,
								 OUT PUCHAR pPlainText);

////////////////////////////////////////////////////////////////
// SEED 인터페이스
////////////////////////////////////////////////////////////////

// SEED 단일 블록 암호화를 수행하는 함수로서, 평문 블록인 PlainTextBlock를 암호화하여, CipherTextBlock에 암호문 블록을 출력한다.
typedef ULONG
(*NEO_SEED_128_Encrypt_FUNC)(IN CONST UCHAR Key[SEED_128_KEY_SIZE_BYTE],
							 IN CONST UCHAR PlainTextBlock[SEED_BLOCK_SIZE_BYTE],
							 OUT UCHAR CipherTextBlock[SEED_BLOCK_SIZE_BYTE]);

// SEED 단일 블록 복호화를 수행하는 함수로서, 암호문 블록인 CipherTextBlock를 복호화하여, PlainTextBlock에 평문 블록을 출력한다.
typedef ULONG
(*NEO_SEED_128_Decrypt_FUNC)(IN CONST UCHAR Key[SEED_128_KEY_SIZE_BYTE],
							 IN CONST UCHAR CipherTextBlock[SEED_BLOCK_SIZE_BYTE],
							 OUT UCHAR PlainTextBlock[SEED_BLOCK_SIZE_BYTE]);

// SEED CTR 운영모드로 암호화를 수행하는 함수로서, 평문인 pPlainText를 암호화하여, pCipherText에 암호문을 출력한다.
// 출력되는 암호문인 pCipherText의 크기는 PlainTextSize와 크기가 같고 패딩처리는 수행하지 않는다. 
// 따라서, 출력인자 pCipherText가 PlainTextSize보다 적게 메모리 할당이 되었다면, exception 에러가 발생하므로, 출력인자 pCipherText는 PlainTextSize와 같거나 크게 메모리를 할당해야 한다.
typedef ULONG
(*NEO_SEED_128_CTR_Encrypt_FUNC)(IN CONST UCHAR Key[SEED_128_KEY_SIZE_BYTE],						 
								 IN CONST  UCHAR Nonce[CTR_NONCE_SIZE_BYTE],
								 IN ULONGLONG Counter,
								 IN CONST PUCHAR pPlainText,
								 IN ULONGLONG PlainTextSize,
								 OUT PUCHAR pCipherText);

// SEED CTR 운영모드로 복호화를 수행하는 함수로서, 암호문인 pCipherText를 복호화하여, pPlainText에 평문을 출력한다.
// 출력되는 평문인 pPlainText의 크기는 CipherTextSize와 크기가 같고 패딩처리는 수행하지 않는다.
// 따라서, 출력인자 pPlainText가 CipherTextSize보다 적게 메모리 할당이 되었다면, exception 에러가 발생하므로, 출력인자 pPlainText는 CipherTextSize와 같거나 크게 메모리를 할당해야 한다.
typedef ULONG
(*NEO_SEED_128_CTR_Decrypt_FUNC)(IN CONST UCHAR Key[SEED_128_KEY_SIZE_BYTE],						 
								 IN CONST UCHAR Nonce[CTR_NONCE_SIZE_BYTE],
								 IN ULONGLONG Counter,
								 IN CONST PUCHAR pCipherText,
								 IN ULONGLONG CipherTextSize,
								 OUT PUCHAR pPlainText);

// SEED CBC 운영모드로 암호화를 수행하는 함수로서, 평문인 pPlainText를 암호화하여, pCipherText에 암호문을 출력하고, Zero 패딩을 수행한다.
// 출력되는 암호문인 pCipherText의 크기는 PlainTextSize가 16(블록 크기)의 배수이면 PlainTextSize와 같고, 16(블록 크기)의 배수가 아니면 Zero 패딩이 수행되어서 PlainTextSize 보다 큰 16(블록 크기)의 배수 크기이다.(ex, PlainTextSize 가 14이면, 출력크기는 Zero 패딩이 수행되어서 16(블록 크기)가 된다.)
// 따라서, 출력인자 pCipherText는 PlainTextSize가 16(블록 크기)의 배수이면 PlainTextSize와 같거나 크게 메모리를 할당해야 하고, PlainTextSize가 16(블록 크기)의 배수가 아니면, PlainTextSize보다 큰 16(블록 크기)의 배수 크기와 같거나 크게 할당해야 한다.
// 그렇지 않으면, exception 에러가 발생한다.
typedef ULONG
(*NEO_SEED_128_CBC_Encrypt_FUNC)(IN CONST UCHAR Key[SEED_128_KEY_SIZE_BYTE],						 
								 IN CONST UCHAR InitialVector[SEED_BLOCK_SIZE_BYTE],
								 IN CONST PUCHAR pPlainText,
								 IN ULONGLONG PlainTextSize,
								 OUT PUCHAR pCipherText,
								 IN OUT PULONGLONG pCipherTextSize);

// SEED CBC 운영모드로 복호화를 수행하는 함수로서, 암호문인 pCipherText를 복호화하여, pPlainText에 평문을 출력한다.
// pCipherText의 크기는 16(블록 크기)의 배수이어야 한다.
// 출력되는 평문인 pPlainText의 크기는 CipherTextSize와 크기가 같다.
// 따라서, 출력인자 pPlainText가 CipherTextSize보다 적게 메모리 할당이 되었다면, exception 에러가 발생하므로, 출력인자 pPlainText는 CipherTextSize와 같거나 크게 메모리를 할당해야 한다.
// 암호문인 pCipherText가 Zero 패딩된 암호문이므로, 출력되는 평문인 pPlainText에서 패딩된 데이터를 알 수 없다는 것을 주의해야 한다. 
typedef ULONG
(*NEO_SEED_128_CBC_Decrypt_FUNC)(IN CONST UCHAR Key[SEED_128_KEY_SIZE_BYTE],						 
								 IN CONST UCHAR InitialVector[SEED_BLOCK_SIZE_BYTE],
								 IN CONST PUCHAR pCipherText,
								 IN ULONGLONG CipherTextSize,
								 OUT PUCHAR pPlainText);

////////////////////////////////////////////////////////////////
// SHA-256 인터페이스
////////////////////////////////////////////////////////////////

// SHA-256 초기화를 수행하는 함수로서, 초기 해시값을 설정하고, SHA-256 동작을 위한 컨텍스트를 생성하고, 이에 대한 핸들을 출력한다. 
typedef ULONG
(*NEO_SHA_256_Init_FUNC)(OUT PHSHA256 phSHA256);

// SHA-256 해시값을 생성하는 함수로서, 입력 메시지에 대한 해시값을 계산하여 SHA-256 컨텍스트에 저장한다.
typedef ULONG
(*NEO_SHA_256_Update_FUNC)(IN HSHA256 hSHA256,
						   IN CONST PUCHAR pMessage,
						   IN ULONGLONG MessageSize);

// SHA-256 해시값을 얻는 함수로서, NEO_SHA_256_Update 함수에서 입력되었던 메시지에 대한 해시값을 얻는다.
typedef ULONG
(*NEO_SHA_256_Final_FUNC)(IN HSHA256 hSHA256,
						  OUT UCHAR MessageDigest[SHA_256_MESSAGE_DIGEST_SIZE_BYTE]);

// SHA-256 해제를 수행하는 함수로서, SHA-256 핸들로부터 SHA-256 컨텍스트를 해제한다.
typedef ULONG
(*NEO_SHA_256_Free_FUNC)(IN HSHA256 hSHA256);

// SHA-256 해시값을 생성하고 얻는 함수로서, pMessage 대해서 해시값을 생성하여, MessageDigest에 해시값을 출력한다.
// 이 함수 내부적으로는 NEO_SHA_256_Init, NEO_SHA_256_Update, NEO_SHA_256_Final, NEO_SHA_256_Free 함수에서 호출한 함수가 그대로 적용된다.
// 따라서, 해시값을 생성하기 위해서, 이 함수를 사용하나 NEO_SHA_256_Init, NEO_SHA_256_Update, NEO_SHA_256_Final, NEO_SHA_256_Free 함수를 사용하나 결과는 동일하다.
typedef ULONG
(*NEO_SHA_256_FUNC)(IN CONST PUCHAR pMessage,
					IN ULONGLONG MessageSize,
					OUT UCHAR MessageDigest[SHA_256_MESSAGE_DIGEST_SIZE_BYTE]);

////////////////////////////////////////////////////////////////
// HMAC(SHA-256) 인터페이스
////////////////////////////////////////////////////////////////

// HMAC(SHA-256) 초기화를 수행하는 함수로서, HMAC(SHA-256) 동작을 위한 컨텍스트를 생성하고, 이에 대한 핸들을 출력한다.
typedef ULONG
(*NEO_HMAC_SHA_256_Init_FUNC)(IN CONST PUCHAR pKey,
							  IN ULONG KeySize,
							  OUT PHHMACSHA256 phHMACSHA256);

// HMAC(SHA-256) 메시지인증코드를 생성하는 함수로서, 입력 메시지에 대한 메시지인증코드를 계산하여 HMAC(SHA-256) 컨텍스트에 저장한다.
typedef ULONG
(*NEO_HMAC_SHA_256_Update_FUNC)(IN HHMACSHA256 hHMACSHA256,
								IN CONST PUCHAR pMessage,
								IN ULONGLONG MessageSize);

// HMAC(SHA-256) 메시지인증코드를 얻는 함수로서, NEO_HMAC_SHA_256_Update 함수에서 입력되었던 메시지에 대한 메시지인증코드를 얻는다.
typedef ULONG
(*NEO_HMAC_SHA_256_Final_FUNC)(IN HSHA256 hHMACSHA256,
							   OUT PUCHAR pMAC,
							   IN ULONG MACSize);

// HMAC(SHA-256) 해제를 수행하는 함수로서, HMAC(SHA-256) 핸들로부터 HMAC(SHA-256) 컨텍스트를 해제한다.
typedef ULONG
(*NEO_HMAC_SHA_256_Free_FUNC)(IN HHMACSHA256 hHMACSHA256);

// HMAC(SHA-256) 메시지인증코드를 생성하고 얻는 함수로서, 비밀키인 pKey로pMessage 대해서 메시지인증코드를 생성하여, MAC에 메시지인증코드를 출력한다.
// 이 함수 내부적으로는 NEO_HMAC_SHA_256_Init, NEO_HMAC_SHA_256_Update, NEO_HMAC_SHA_256_Final, NEO_HMAC_SHA_256_Free 함수에서 호출한 함수가 그대로 적용된다.
// 따라서, 해시값을 생성하기 위해서, 이 함수를 사용하나 NEO_HMAC_SHA_256_Init, NEO_HMAC_SHA_256_Update, NEO_HMAC_SHA_256_Final, NEO_HMAC_SHA_256_Free 함수를 사용하나 결과는 동일하다.
typedef ULONG
(*NEO_HMAC_SHA_256_FUNC)(IN CONST PUCHAR pKey,
						 IN ULONG KeySize,
						 IN CONST PUCHAR pMessage,
						 IN ULONGLONG MessageSize,
						 OUT PUCHAR pMAC,
						 IN ULONG MACSize);

////////////////////////////////////////////////////////////////
// HMAC(SHA-256)_DRBG 인터페이스
////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////
// SP800-90A 문서 : 9.1 Instantiating a DRBG
// 1. If requested_instantiation_security_strength > highest_supported_security_strength, then return an ERROR_FLAG.
// 2. If prediction_resistance_flag is set, and prediction resistance is not supported, then return an ERROR_FLAG.
// 3. If the length of the personalization_string > max_personalization_string_length, return an ERROR_FLAG.
// 4. Set security_strength to the lowest security strength greater than or equal to requested_instantiation_security_strength from the set {112, 128, 192, 256}.
// 5. Null step. Comment: This is intended to replace a step from the previous version without changing the step numbers
// 6. (status, entropy_input) = Get_entropy_input (security_strength, min_length, max_length, prediction_resistance_request).
// 7. If an ERROR is returned in step 6, return a CATASTROPHIC_ERROR_FLAG.
// 8. Obtain a nonce.
// 9. initial_working_state = Instantiate_algorithm (entropy_input, nonce, personalization_string, security_strength).
// 10. Get a state_handle for a currently empty internal state. If an empty internal state cannot be found, return an ERROR_FLAG.
// 11. Set the internal state for the new instantiation (e.g., as indicated by state_handle) to the initial values for the internal state (i.e., set the working_state to the values returned as initial_working_state in step 9 and any other values required for the working_state (see Section 10), and set the administrative information to the appropriate values (e.g., the values of security_strength and the prediction_resistance_flag).
// 12. Return SUCCESS and state_handle.
///////////////////////////////////////////////////////////////////////
typedef ULONG
(*NEO_DRBG_Instantiate_FUNC)(IN CONST PUCHAR pPersonalizationString,
							 IN ULONG PersonalizationStringSize,
							 OUT PHDRBG phDRBG);

///////////////////////////////////////////////////////////////////////
// SP800-90A 문서 : 9.2 Reseeding a DRBG Instantiation
// 1. Using state_handle, obtain the current internal state. If state_handle indicates an invalid or unused internal state, return an ERROR_FLAG.
// 2. If prediction_resistance_request is set, and prediction_resistance_flag is not set, then return an ERROR_FLAG.
// 3. If the length of the additional_input > max_additional_input_length, return an ERROR_FLAG.
// 4. (status, entropy_input) = Get_entropy_input (security_strength, min_length, max_length, prediction_resistance_request).
// 5. If an ERROR is returned in step 4, return a CATASTROPHIC_ERROR_FLAG.
// 6. new_working_state = Reseed_algorithm (working_state, entropy_input, additional_input).
// 7. Replace the working_state in the internal state for the DRBG instantiation (e.g., as indicated by state_handle) with the values of new_working_state obtained in step 6.
// 8. Return SUCCESS.
///////////////////////////////////////////////////////////////////////
typedef ULONG
(*NEO_DRBG_Reseed_FUNC)(IN HDRBG hDRBG,
						IN CONST PUCHAR pAdditionalInput,
						IN ULONG AdditionalInputSize);

///////////////////////////////////////////////////////////////////////
// SP800-90A 문서 : 9.3.1 The Generate Function
// 1. Using state_handle, obtain the current internal state for the instantiation. If state_handle indicates an invalid or unused internal state, then return an ERROR_FLAG.
// 2. If requested_number_of_bits > max_number_of_bits_per_request, then return an ERROR_FLAG.
// 3. If requested_security_strength > the security_strength indicated in the internal state, then return an ERROR_FLAG.
// 4. If the length of the additional_input > max_additional_input_length, then return an ERROR_FLAG.
// 5. If prediction_resistance_request is set, and prediction_resistance_flag is not set, then return an ERROR_FLAG.
// 6. Clear the reseed_required_flag.
// 7. If reseed_required_flag is set, or if prediction_resistance_request is set, then
//	7.1 status = Reseed_function (state_handle, prediction_resistance_request, additional_input).
//	7.2 If status indicates an ERROR, then return status.
//	7.3 Using state_handle, obtain the new internal state.
//	7.4 additional_input = the Null string.
//	7.5 Clear the reseed_required_flag.
// 8. (status, pseudorandom_bits, new_working_state) = Generate_algorithm (working_state, requested_number_of_bits, additional_input).
// 9. If status indicates that a reseed is required before the requested bits can be generated, then
//	9.1 Set the reseed_required_flag.
//	9.2 If the prediction_resistance_flag is set, then set the prediction_resistance request indication.
//	9.3 Go to step 7.
// 10. Replace the old working_state in the internal state of the DRBG instantiation (e.g., as indicated by state_handle) with the values of new_working_state.
// 11. Return SUCCESS and pseudorandom_bits.
///////////////////////////////////////////////////////////////////////
typedef ULONG
(*NEO_DRBG_Generate_FUNC)(IN HDRBG hDRBG,
						  IN BOOLEAN bIsPredictionResistance,
						  IN CONST PUCHAR pAdditionalInput,
						  IN ULONG AdditionalInputSize,
						  OUT PUCHAR pPseudoRandom,
						  IN ULONG PseudoRandomSize);

// DRBG_Reseed 함수가 실행되는 주기 설정
typedef ULONG
(*NEO_DRBG_SetReseedInterval_FUNC)(IN HDRBG hDRBG,
								   IN ULONG ReseedInterval);

// DRBG_Reseed 함수가 실행되는 주기 얻기
typedef ULONG
(*NEO_DRBG_GetReseedInterval_FUNC)(IN HDRBG hDRBG,
								   OUT PULONG pReseedInterval);

///////////////////////////////////////////////////////////////////////
// SP800-90A 문서 : 9.4 Removing a DRBG Instantiation
// 1. If state_handle indicates an invalid state, then return an ERROR_FLAG.
// 2. Erase the contents of the internal state indicated by state_handle.
// 3. Return SUCCESS.
///////////////////////////////////////////////////////////////////////
typedef ULONG
(*NEO_DRBG_Uninstantiate_FUNC)(IN HDRBG hDRBG);

////////////////////////////////////////////////////////////////
// 자가시험 인터페이스
////////////////////////////////////////////////////////////////

// 동작 전 자가시험을 수행하는 함수로서, 소프트웨어 무결성 시험, 핵심 기능시험으로서 암호알고리즘 시험인 KAT와 엔트로피 시험을 수행한다.
typedef ULONG
(*NEO_PreOperationalSelfTest_FUNC)();

////////////////////////////////////////////////////////////////
// 모듈관리 인터페이스
////////////////////////////////////////////////////////////////

// 암호모듈 상태 얻기
typedef ULONG
(*NEO_GetMocoCryptoStatus_FUNC)();

// 암호모듈의 버전정보 얻기
typedef ULONG
(*NEO_GetMocoCryptoVersionInfo_FUNC)(OUT WCHAR VersionInfo[16]);
