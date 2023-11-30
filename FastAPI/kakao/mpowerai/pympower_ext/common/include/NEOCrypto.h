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

// �Լ� ���� ���� ����
#define NEO_SUCCESS										0		   // �Լ� ȣ�� ����
#define ERROR_NEO_INVALID_PARAMETER						0xE0000041 // �Լ� ���ڰ� �ùٸ��� ���� ����
#define ERROR_NEO_NOT_ENOUGH_MEMORY						0xE0000042 // �޸� �Ҵ� ����
#define ERROR_NEO_SELFTESTING							0xE0000043 // �ڰ����� ���� ����

#define ERROR_NEO_SELFTEST_FAIL							0xE0000071 // �ڰ����� ����
#define ERROR_NEO_NOISE_SOURCE_COLLECTION_FAIL			0xE0000072 // ���� �߻��� ������ ���� ���� �Ǵ� ���� �߻��� ���ο��� �����Ǵ� �� ���� ����
#define ERROR_NEO_INITIALIZATION						0xE0000073 // �ʱ�ȭ ����


// ARIA ���Ű ũ��(32����Ʈ/256��Ʈ)
#define ARIA_256_KEY_SIZE_BYTE				32		

// ARIA ��� ũ��
#define ARIA_BLOCK_SIZE_BYTE				16

// SEED ���Ű ũ��(16����Ʈ/128��Ʈ)
#define SEED_128_KEY_SIZE_BYTE				16		// 16����Ʈ/128��Ʈ

// SEED ��� ũ��
#define SEED_BLOCK_SIZE_BYTE				16

// NONCE ũ��. 8����Ʈ
#define CTR_NONCE_SIZE_BYTE					8

// SHA-256 �޽��� ��������Ʈ ũ��
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
// ARIA �������̽�
////////////////////////////////////////////////////////////////

// ARIA ���� ��� ��ȣȭ�� �����ϴ� �Լ��μ�, �� ����� PlainTextBlock�� ��ȣȭ�Ͽ�, CipherTextBlock�� ��ȣ�� ����� ����Ѵ�.
typedef ULONG
(*NEO_ARIA_256_Encrypt_FUNC)(IN CONST UCHAR Key[ARIA_256_KEY_SIZE_BYTE],
							 IN CONST UCHAR PlainTextBlock[ARIA_BLOCK_SIZE_BYTE],
							 OUT UCHAR CipherTextBlock[ARIA_BLOCK_SIZE_BYTE]);

// ARIA ���� ��� ��ȣȭ�� �����ϴ� �Լ��μ�, ��ȣ�� ����� CipherTextBlock�� ��ȣȭ�Ͽ�, PlainTextBlock�� �� ����� ����Ѵ�.
typedef ULONG
(*NEO_ARIA_256_Decrypt_FUNC)(IN CONST UCHAR Key[ARIA_256_KEY_SIZE_BYTE],
							 IN CONST UCHAR CipherTextBlock[ARIA_BLOCK_SIZE_BYTE],
							 OUT UCHAR PlainTextBlock[ARIA_BLOCK_SIZE_BYTE]);

// ARIA CTR ����� ��ȣȭ�� �����ϴ� �Լ��μ�, ���� pPlainText�� ��ȣȭ�Ͽ�, pCipherText�� ��ȣ���� ����Ѵ�.
// ��µǴ� ��ȣ���� pCipherText�� ũ��� PlainTextSize�� ũ�Ⱑ ���� �е�ó���� �������� �ʴ´�. 
// ����, ������� pCipherText�� PlainTextSize���� ���� �޸� �Ҵ��� �Ǿ��ٸ�, exception ������ �߻��ϹǷ�, ������� pCipherText�� PlainTextSize�� ���ų� ũ�� �޸𸮸� �Ҵ��ؾ� �Ѵ�.
typedef ULONG
(*NEO_ARIA_256_CTR_Encrypt_FUNC)(IN CONST UCHAR Key[ARIA_256_KEY_SIZE_BYTE],						 
								 IN CONST UCHAR Nonce[CTR_NONCE_SIZE_BYTE],
								 IN ULONGLONG Counter,
								 IN CONST PUCHAR pPlainText,
								 IN ULONGLONG PlainTextSize,
								 OUT PUCHAR pCipherText);

// ARIA CTR ����� ��ȣȭ�� �����ϴ� �Լ��μ�, ��ȣ���� pCipherText�� ��ȣȭ�Ͽ�, pPlainText�� ���� ����Ѵ�.
// ��µǴ� ���� pPlainText�� ũ��� CipherTextSize�� ũ�Ⱑ ���� �е�ó���� �������� �ʴ´�.
// ����, ������� pPlainText�� CipherTextSize���� ���� �޸� �Ҵ��� �Ǿ��ٸ�, exception ������ �߻��ϹǷ�, ������� pPlainText�� CipherTextSize�� ���ų� ũ�� �޸𸮸� �Ҵ��ؾ� �Ѵ�.
typedef ULONG
(*NEO_ARIA_256_CTR_Decrypt_FUNC)(IN CONST UCHAR Key[ARIA_256_KEY_SIZE_BYTE],						 
								 IN CONST UCHAR Nonce[CTR_NONCE_SIZE_BYTE],
								 IN ULONGLONG Counter,
								 IN CONST PUCHAR pCipherText,
								 IN ULONGLONG CipherTextSize,
								 OUT PUCHAR pPlainText);

// ARIA CBC ����� ��ȣȭ�� �����ϴ� �Լ��μ�, ���� pPlainText�� ��ȣȭ�Ͽ�, pCipherText�� ��ȣ���� ����ϰ�, Zero �е��� �����Ѵ�.
// ��µǴ� ��ȣ���� pCipherText�� ũ��� PlainTextSize�� 16(��� ũ��)�� ����̸� PlainTextSize�� ����, 16(��� ũ��)�� ����� �ƴϸ� Zero �е��� ����Ǿ PlainTextSize ���� ū 16(��� ũ��)�� ��� ũ���̴�.(ex, PlainTextSize �� 14�̸�, ���ũ��� Zero �е��� ����Ǿ 16(��� ũ��)�� �ȴ�.)
// ����, ������� pCipherText�� PlainTextSize�� 16(��� ũ��)�� ����̸� PlainTextSize�� ���ų� ũ�� �޸𸮸� �Ҵ��ؾ� �ϰ�, PlainTextSize�� 16(��� ũ��)�� ����� �ƴϸ�, PlainTextSize���� ū 16(��� ũ��)�� ��� ũ��� ���ų� ũ�� �Ҵ��ؾ� �Ѵ�.
// �׷��� ������, exception ������ �߻��Ѵ�.
typedef ULONG
(*NEO_ARIA_256_CBC_Encrypt_FUNC)(IN CONST UCHAR Key[ARIA_256_KEY_SIZE_BYTE],						 
								 IN CONST UCHAR InitialVector[ARIA_BLOCK_SIZE_BYTE],
								 IN CONST PUCHAR pPlainText,
								 IN ULONGLONG PlainTextSize,
								 OUT PUCHAR pCipherText,
								 IN OUT PULONGLONG pCipherTextSize);

// ARIA CBC ����� ��ȣȭ�� �����ϴ� �Լ��μ�, ��ȣ���� pCipherText�� ��ȣȭ�Ͽ�, pPlainText�� ���� ����Ѵ�.
// pCipherText�� ũ��� 16(��� ũ��)�� ����̾�� �Ѵ�.
// ��µǴ� ���� pPlainText�� ũ��� CipherTextSize�� ũ�Ⱑ ����.
// ����, ������� pPlainText�� CipherTextSize���� ���� �޸� �Ҵ��� �Ǿ��ٸ�, exception ������ �߻��ϹǷ�, ������� pPlainText�� CipherTextSize�� ���ų� ũ�� �޸𸮸� �Ҵ��ؾ� �Ѵ�.
// ��ȣ���� pCipherText�� Zero �е��� ��ȣ���̹Ƿ�, ��µǴ� ���� pPlainText���� �е��� �����͸� �� �� ���ٴ� ���� �����ؾ� �Ѵ�. 
typedef ULONG
(*NEO_ARIA_256_CBC_Decrypt_FUNC)(IN CONST UCHAR Key[ARIA_256_KEY_SIZE_BYTE],						 
								 IN CONST UCHAR InitialVector[ARIA_BLOCK_SIZE_BYTE],
								 IN CONST PUCHAR pCipherText,
								 IN ULONGLONG CipherTextSize,
								 OUT PUCHAR pPlainText);

////////////////////////////////////////////////////////////////
// SEED �������̽�
////////////////////////////////////////////////////////////////

// SEED ���� ��� ��ȣȭ�� �����ϴ� �Լ��μ�, �� ����� PlainTextBlock�� ��ȣȭ�Ͽ�, CipherTextBlock�� ��ȣ�� ����� ����Ѵ�.
typedef ULONG
(*NEO_SEED_128_Encrypt_FUNC)(IN CONST UCHAR Key[SEED_128_KEY_SIZE_BYTE],
							 IN CONST UCHAR PlainTextBlock[SEED_BLOCK_SIZE_BYTE],
							 OUT UCHAR CipherTextBlock[SEED_BLOCK_SIZE_BYTE]);

// SEED ���� ��� ��ȣȭ�� �����ϴ� �Լ��μ�, ��ȣ�� ����� CipherTextBlock�� ��ȣȭ�Ͽ�, PlainTextBlock�� �� ����� ����Ѵ�.
typedef ULONG
(*NEO_SEED_128_Decrypt_FUNC)(IN CONST UCHAR Key[SEED_128_KEY_SIZE_BYTE],
							 IN CONST UCHAR CipherTextBlock[SEED_BLOCK_SIZE_BYTE],
							 OUT UCHAR PlainTextBlock[SEED_BLOCK_SIZE_BYTE]);

// SEED CTR ����� ��ȣȭ�� �����ϴ� �Լ��μ�, ���� pPlainText�� ��ȣȭ�Ͽ�, pCipherText�� ��ȣ���� ����Ѵ�.
// ��µǴ� ��ȣ���� pCipherText�� ũ��� PlainTextSize�� ũ�Ⱑ ���� �е�ó���� �������� �ʴ´�. 
// ����, ������� pCipherText�� PlainTextSize���� ���� �޸� �Ҵ��� �Ǿ��ٸ�, exception ������ �߻��ϹǷ�, ������� pCipherText�� PlainTextSize�� ���ų� ũ�� �޸𸮸� �Ҵ��ؾ� �Ѵ�.
typedef ULONG
(*NEO_SEED_128_CTR_Encrypt_FUNC)(IN CONST UCHAR Key[SEED_128_KEY_SIZE_BYTE],						 
								 IN CONST  UCHAR Nonce[CTR_NONCE_SIZE_BYTE],
								 IN ULONGLONG Counter,
								 IN CONST PUCHAR pPlainText,
								 IN ULONGLONG PlainTextSize,
								 OUT PUCHAR pCipherText);

// SEED CTR ����� ��ȣȭ�� �����ϴ� �Լ��μ�, ��ȣ���� pCipherText�� ��ȣȭ�Ͽ�, pPlainText�� ���� ����Ѵ�.
// ��µǴ� ���� pPlainText�� ũ��� CipherTextSize�� ũ�Ⱑ ���� �е�ó���� �������� �ʴ´�.
// ����, ������� pPlainText�� CipherTextSize���� ���� �޸� �Ҵ��� �Ǿ��ٸ�, exception ������ �߻��ϹǷ�, ������� pPlainText�� CipherTextSize�� ���ų� ũ�� �޸𸮸� �Ҵ��ؾ� �Ѵ�.
typedef ULONG
(*NEO_SEED_128_CTR_Decrypt_FUNC)(IN CONST UCHAR Key[SEED_128_KEY_SIZE_BYTE],						 
								 IN CONST UCHAR Nonce[CTR_NONCE_SIZE_BYTE],
								 IN ULONGLONG Counter,
								 IN CONST PUCHAR pCipherText,
								 IN ULONGLONG CipherTextSize,
								 OUT PUCHAR pPlainText);

// SEED CBC ����� ��ȣȭ�� �����ϴ� �Լ��μ�, ���� pPlainText�� ��ȣȭ�Ͽ�, pCipherText�� ��ȣ���� ����ϰ�, Zero �е��� �����Ѵ�.
// ��µǴ� ��ȣ���� pCipherText�� ũ��� PlainTextSize�� 16(��� ũ��)�� ����̸� PlainTextSize�� ����, 16(��� ũ��)�� ����� �ƴϸ� Zero �е��� ����Ǿ PlainTextSize ���� ū 16(��� ũ��)�� ��� ũ���̴�.(ex, PlainTextSize �� 14�̸�, ���ũ��� Zero �е��� ����Ǿ 16(��� ũ��)�� �ȴ�.)
// ����, ������� pCipherText�� PlainTextSize�� 16(��� ũ��)�� ����̸� PlainTextSize�� ���ų� ũ�� �޸𸮸� �Ҵ��ؾ� �ϰ�, PlainTextSize�� 16(��� ũ��)�� ����� �ƴϸ�, PlainTextSize���� ū 16(��� ũ��)�� ��� ũ��� ���ų� ũ�� �Ҵ��ؾ� �Ѵ�.
// �׷��� ������, exception ������ �߻��Ѵ�.
typedef ULONG
(*NEO_SEED_128_CBC_Encrypt_FUNC)(IN CONST UCHAR Key[SEED_128_KEY_SIZE_BYTE],						 
								 IN CONST UCHAR InitialVector[SEED_BLOCK_SIZE_BYTE],
								 IN CONST PUCHAR pPlainText,
								 IN ULONGLONG PlainTextSize,
								 OUT PUCHAR pCipherText,
								 IN OUT PULONGLONG pCipherTextSize);

// SEED CBC ����� ��ȣȭ�� �����ϴ� �Լ��μ�, ��ȣ���� pCipherText�� ��ȣȭ�Ͽ�, pPlainText�� ���� ����Ѵ�.
// pCipherText�� ũ��� 16(��� ũ��)�� ����̾�� �Ѵ�.
// ��µǴ� ���� pPlainText�� ũ��� CipherTextSize�� ũ�Ⱑ ����.
// ����, ������� pPlainText�� CipherTextSize���� ���� �޸� �Ҵ��� �Ǿ��ٸ�, exception ������ �߻��ϹǷ�, ������� pPlainText�� CipherTextSize�� ���ų� ũ�� �޸𸮸� �Ҵ��ؾ� �Ѵ�.
// ��ȣ���� pCipherText�� Zero �е��� ��ȣ���̹Ƿ�, ��µǴ� ���� pPlainText���� �е��� �����͸� �� �� ���ٴ� ���� �����ؾ� �Ѵ�. 
typedef ULONG
(*NEO_SEED_128_CBC_Decrypt_FUNC)(IN CONST UCHAR Key[SEED_128_KEY_SIZE_BYTE],						 
								 IN CONST UCHAR InitialVector[SEED_BLOCK_SIZE_BYTE],
								 IN CONST PUCHAR pCipherText,
								 IN ULONGLONG CipherTextSize,
								 OUT PUCHAR pPlainText);

////////////////////////////////////////////////////////////////
// SHA-256 �������̽�
////////////////////////////////////////////////////////////////

// SHA-256 �ʱ�ȭ�� �����ϴ� �Լ��μ�, �ʱ� �ؽð��� �����ϰ�, SHA-256 ������ ���� ���ؽ�Ʈ�� �����ϰ�, �̿� ���� �ڵ��� ����Ѵ�. 
typedef ULONG
(*NEO_SHA_256_Init_FUNC)(OUT PHSHA256 phSHA256);

// SHA-256 �ؽð��� �����ϴ� �Լ��μ�, �Է� �޽����� ���� �ؽð��� ����Ͽ� SHA-256 ���ؽ�Ʈ�� �����Ѵ�.
typedef ULONG
(*NEO_SHA_256_Update_FUNC)(IN HSHA256 hSHA256,
						   IN CONST PUCHAR pMessage,
						   IN ULONGLONG MessageSize);

// SHA-256 �ؽð��� ��� �Լ��μ�, NEO_SHA_256_Update �Լ����� �ԷµǾ��� �޽����� ���� �ؽð��� ��´�.
typedef ULONG
(*NEO_SHA_256_Final_FUNC)(IN HSHA256 hSHA256,
						  OUT UCHAR MessageDigest[SHA_256_MESSAGE_DIGEST_SIZE_BYTE]);

// SHA-256 ������ �����ϴ� �Լ��μ�, SHA-256 �ڵ�κ��� SHA-256 ���ؽ�Ʈ�� �����Ѵ�.
typedef ULONG
(*NEO_SHA_256_Free_FUNC)(IN HSHA256 hSHA256);

// SHA-256 �ؽð��� �����ϰ� ��� �Լ��μ�, pMessage ���ؼ� �ؽð��� �����Ͽ�, MessageDigest�� �ؽð��� ����Ѵ�.
// �� �Լ� ���������δ� NEO_SHA_256_Init, NEO_SHA_256_Update, NEO_SHA_256_Final, NEO_SHA_256_Free �Լ����� ȣ���� �Լ��� �״�� ����ȴ�.
// ����, �ؽð��� �����ϱ� ���ؼ�, �� �Լ��� ����ϳ� NEO_SHA_256_Init, NEO_SHA_256_Update, NEO_SHA_256_Final, NEO_SHA_256_Free �Լ��� ����ϳ� ����� �����ϴ�.
typedef ULONG
(*NEO_SHA_256_FUNC)(IN CONST PUCHAR pMessage,
					IN ULONGLONG MessageSize,
					OUT UCHAR MessageDigest[SHA_256_MESSAGE_DIGEST_SIZE_BYTE]);

////////////////////////////////////////////////////////////////
// HMAC(SHA-256) �������̽�
////////////////////////////////////////////////////////////////

// HMAC(SHA-256) �ʱ�ȭ�� �����ϴ� �Լ��μ�, HMAC(SHA-256) ������ ���� ���ؽ�Ʈ�� �����ϰ�, �̿� ���� �ڵ��� ����Ѵ�.
typedef ULONG
(*NEO_HMAC_SHA_256_Init_FUNC)(IN CONST PUCHAR pKey,
							  IN ULONG KeySize,
							  OUT PHHMACSHA256 phHMACSHA256);

// HMAC(SHA-256) �޽��������ڵ带 �����ϴ� �Լ��μ�, �Է� �޽����� ���� �޽��������ڵ带 ����Ͽ� HMAC(SHA-256) ���ؽ�Ʈ�� �����Ѵ�.
typedef ULONG
(*NEO_HMAC_SHA_256_Update_FUNC)(IN HHMACSHA256 hHMACSHA256,
								IN CONST PUCHAR pMessage,
								IN ULONGLONG MessageSize);

// HMAC(SHA-256) �޽��������ڵ带 ��� �Լ��μ�, NEO_HMAC_SHA_256_Update �Լ����� �ԷµǾ��� �޽����� ���� �޽��������ڵ带 ��´�.
typedef ULONG
(*NEO_HMAC_SHA_256_Final_FUNC)(IN HSHA256 hHMACSHA256,
							   OUT PUCHAR pMAC,
							   IN ULONG MACSize);

// HMAC(SHA-256) ������ �����ϴ� �Լ��μ�, HMAC(SHA-256) �ڵ�κ��� HMAC(SHA-256) ���ؽ�Ʈ�� �����Ѵ�.
typedef ULONG
(*NEO_HMAC_SHA_256_Free_FUNC)(IN HHMACSHA256 hHMACSHA256);

// HMAC(SHA-256) �޽��������ڵ带 �����ϰ� ��� �Լ��μ�, ���Ű�� pKey��pMessage ���ؼ� �޽��������ڵ带 �����Ͽ�, MAC�� �޽��������ڵ带 ����Ѵ�.
// �� �Լ� ���������δ� NEO_HMAC_SHA_256_Init, NEO_HMAC_SHA_256_Update, NEO_HMAC_SHA_256_Final, NEO_HMAC_SHA_256_Free �Լ����� ȣ���� �Լ��� �״�� ����ȴ�.
// ����, �ؽð��� �����ϱ� ���ؼ�, �� �Լ��� ����ϳ� NEO_HMAC_SHA_256_Init, NEO_HMAC_SHA_256_Update, NEO_HMAC_SHA_256_Final, NEO_HMAC_SHA_256_Free �Լ��� ����ϳ� ����� �����ϴ�.
typedef ULONG
(*NEO_HMAC_SHA_256_FUNC)(IN CONST PUCHAR pKey,
						 IN ULONG KeySize,
						 IN CONST PUCHAR pMessage,
						 IN ULONGLONG MessageSize,
						 OUT PUCHAR pMAC,
						 IN ULONG MACSize);

////////////////////////////////////////////////////////////////
// HMAC(SHA-256)_DRBG �������̽�
////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////
// SP800-90A ���� : 9.1 Instantiating a DRBG
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
// SP800-90A ���� : 9.2 Reseeding a DRBG Instantiation
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
// SP800-90A ���� : 9.3.1 The Generate Function
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

// DRBG_Reseed �Լ��� ����Ǵ� �ֱ� ����
typedef ULONG
(*NEO_DRBG_SetReseedInterval_FUNC)(IN HDRBG hDRBG,
								   IN ULONG ReseedInterval);

// DRBG_Reseed �Լ��� ����Ǵ� �ֱ� ���
typedef ULONG
(*NEO_DRBG_GetReseedInterval_FUNC)(IN HDRBG hDRBG,
								   OUT PULONG pReseedInterval);

///////////////////////////////////////////////////////////////////////
// SP800-90A ���� : 9.4 Removing a DRBG Instantiation
// 1. If state_handle indicates an invalid state, then return an ERROR_FLAG.
// 2. Erase the contents of the internal state indicated by state_handle.
// 3. Return SUCCESS.
///////////////////////////////////////////////////////////////////////
typedef ULONG
(*NEO_DRBG_Uninstantiate_FUNC)(IN HDRBG hDRBG);

////////////////////////////////////////////////////////////////
// �ڰ����� �������̽�
////////////////////////////////////////////////////////////////

// ���� �� �ڰ������� �����ϴ� �Լ��μ�, ����Ʈ���� ���Ἲ ����, �ٽ� ��ɽ������μ� ��ȣ�˰��� ������ KAT�� ��Ʈ���� ������ �����Ѵ�.
typedef ULONG
(*NEO_PreOperationalSelfTest_FUNC)();

////////////////////////////////////////////////////////////////
// ������ �������̽�
////////////////////////////////////////////////////////////////

// ��ȣ��� ���� ���
typedef ULONG
(*NEO_GetMocoCryptoStatus_FUNC)();

// ��ȣ����� �������� ���
typedef ULONG
(*NEO_GetMocoCryptoVersionInfo_FUNC)(OUT WCHAR VersionInfo[16]);
