#pragma once

#define RET_VAL		DWORD			//	return values

////	현재 아래의 4개 방식을 지원한다.
#define AI_ECB					1
#define AI_CBC					2
#define AI_OFB					3
#define AI_CFB					4
// skchoi. 2014.11.28 CTR 모드 추가 
#define AI_CTR					5
// kisa-seedenc.c와 kisa-ariaenc.c의 CTR 모드와
// moco-seed.cpp와 moco-aria.cpp의 CTR 모드는
// 서로 호환되지 않는다.
#if defined(__USE_MOCOCRYPTO)
#define AI_CTR_MOCOCRYPTO		6
#endif // defined(__USE_MOCOCRYPTO)

////	현재 아래의 두 padding을 지원한다.
#define AI_NO_PADDING			1	//	Padding 없음(입력이 16바이트의 배수)
#define AI_PKCS_PADDING			2	//	padding되는 바이트 수로 padding
#if defined(__USE_MOCOCRYPTO)
#define AI_NO_PADDING_DISCARD	3	//  Padding 없음(나머지를 버림, OFB, CTR등에만 유효)
#endif // defined(__USE_MOCOCRYPTO)

#define AI_ENCRYPT				1   // 암호화 
#define AI_DECRYPT				2   // 복호화 

/*************** Constant (Error Code) ************************************/
////	Error Code - 정리하고, 적당히 출력해야 함.
#define CTR_SUCCESS					0
#define CTR_FATAL_ERROR				0x1001
#define CTR_INVALID_USERKEYLEN		0x1002	//	비밀키의 길이가 부적절함.
#define CTR_PAD_CHECK_ERROR			0x1003	//	
#define CTR_DATA_LEN_ERROR			0x1004	//	평문의 길이가 부적절함.
#define CTR_CIPHER_LEN_ERROR		0x1005	//	암호문이 블록의 배수가 아님.

/*************** New Data Types *******************************************/
////////	Determine data types depand on the processor and compiler.
#define BOOL	int					//	1-bit data type
#define BYTE	unsigned char		//	unsigned 1-byte data type
#define WORD	unsigned short int	//	unsigned 2-bytes data type
#define DWORD	unsigned int		//	unsigned 4-bytes data type
#define RET_VAL		DWORD			//	return values


////////////////////////////////////////////
// skchoi. 2014.11.28 CTR 모드 추가 시작

#ifdef WIN32
unsigned __int64 SEED_SwapEndian(unsigned __int64 host_longlong);
#else
uint64_t SEED_SwapEndian(uint64_t host_longlong);
#endif

// skchoi. 2014.11.28 CTR 모드 추가 종료 
////////////////////////////////////////////
