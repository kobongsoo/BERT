/***************************************************************************
* Copyright (c) 2000-2004, Future Systems, Inc. / Seoul, Republic of Korea *
* All Rights Reserved.                                                     *
*                                                                          *
* This document contains proprietary and confidential information.  No     *
* parts of this document or the computer program it embodies may be in     *
* any way copied, duplicated, reproduced, translated into a different      *
* programming language, or distributed to any person, company, or          *
* corporation without the prior written consent of Future Systems, Inc.    *
*                              Hyo Sun Hwang                               *
*                372-2 YangJae B/D 6th Floor, Seoul, Korea                 *
*                           +82-2-578-0581 (552)                           *
***************************************************************************/

/*--------------------- [ Version/Command in detais] ---------------------*\
Description : seed.h
			(head file) head file for seed.c : Block Cipher SEED

C0000 : Created by Hyo Sun Hwang (hyosun@future.co.kr) 2000/12/31

C0001 : Modified by Hyo Sun Hwang (hyosun@future.co.kr) 2000/00/00

\*------------------------------------------------------------------------*/

#ifndef _SEED_H
#define _SEED_H

/*************** Header files *********************************************/
#include <stdlib.h>
#include <string.h>
#include <memory.h>
//#include "cryptcom.h"

#ifndef WIN32
#include <inttypes.h>
#endif

/*************** Assertions ***********************************************/
////////	Define the Endianness	////////
#undef BIG_ENDIAN
#undef LITTLE_ENDIAN

#if defined(USER_BIG_ENDIAN)
	#define BIG_ENDIAN
#elif defined(USER_LITTLE_ENDIAN)
	#define LITTLE_ENDIAN
#else
	#if 0
		#define BIG_ENDIAN		//	Big-Endian machine with pointer casting
	#elif defined(_MSC_VER)
		#define LITTLE_ENDIAN	//	Little-Endian machine with pointer casting
	#else
		#if defined (WIN32)
			#error
		#else
			#define LITTLE_ENDIAN	//	Little-Endian machine with pointer casting
		#endif
	#endif
#endif

#ifndef EXTERN_C_BEGIN
#ifdef __cplusplus
#define EXTERN_C_BEGIN extern "C" {
#define EXTERN_C_END }
#else
#define EXTERN_C_BEGIN
#define EXTERN_C_END
#endif
#endif

EXTERN_C_BEGIN


/*************** Macros ***************************************************/
////////	rotate by using shift operations	////////
#if defined(_MSC_VER)
	#define ROTL_DWORD(x, n) _lrotl((x), (n))
	#define ROTR_DWORD(x, n) _lrotr((x), (n))
#else
	#define ROTL_DWORD(x, n) ( (DWORD)((x) << (n)) | (DWORD)((x) >> (32-(n))) )
	#define ROTR_DWORD(x, n) ( (DWORD)((x) >> (n)) | (DWORD)((x) << (32-(n))) )
#endif

////////	reverse the byte order of DWORD(DWORD:4-bytes integer) and WORD.
#define ENDIAN_REVERSE_DWORD(dwS)	( (ROTL_DWORD((dwS),  8) & 0x00ff00ff)	\
									 | (ROTL_DWORD((dwS), 24) & 0xff00ff00) )

////////	move DWORD type to BYTE type and BYTE type to DWORD type
#if defined(BIG_ENDIAN)		////	Big-Endian machine
	#define BIG_B2D(B, D)		D = *(DWORD *)(B)
	#define BIG_D2B(D, B)		*(DWORD *)(B) = (DWORD)(D)
	#define LITTLE_B2D(B, D)	D = ENDIAN_REVERSE_DWORD(*(DWORD *)(B))
	#define LITTLE_D2B(D, B)	*(DWORD *)(B) = ENDIAN_REVERSE_DWORD(D)
#elif defined(LITTLE_ENDIAN)	////	Little-Endian machine
	#define BIG_B2D(B, D)		D = ENDIAN_REVERSE_DWORD(*(DWORD *)(B))
	#define BIG_D2B(D, B)		*(DWORD *)(B) = ENDIAN_REVERSE_DWORD(D)
	#define LITTLE_B2D(B, D)	D = *(DWORD *)(B)
	#define LITTLE_D2B(D, B)	*(DWORD *)(B) = (DWORD)(D)
#else
	#error ERROR : Invalid DataChangeType
#endif

/*************** Definitions / Macros *************************************/
#include "kisa-crypto.h"

////	SEED에 관련된 상수들
#define SEED_BLOCK_LEN			16		//	in BYTEs
#define SEED_USER_KEY_LEN		16		//	in BYTEs
#define SEED_NO_ROUNDS			16
#define SEED_NO_ROUNDKEY		(2*SEED_NO_ROUNDS)	//	in DWORDs

////	SEED..
typedef struct{
	DWORD		ModeID;						//	ECB or CBC
	DWORD		PadType;					//	블록암호의 Padding type
	BYTE		IV[SEED_BLOCK_LEN];			//	Initial Vector
	BYTE		ChainVar[SEED_BLOCK_LEN];	//	Chaining Variable
	BYTE		Buffer[SEED_BLOCK_LEN];		//	Buffer for unfilled block
	DWORD		BufLen; 					//	Buffer의 유효 바이트 수
	DWORD		RoundKey[SEED_NO_ROUNDKEY];	//	라운드 키의 DWORD 수
	//skchoi. 2014.11.28 CTR 모드 추가
#ifdef WIN32
	__int64		n64CTRBlcokNumber;
#else
	int64_t		n64CTRBlcokNumber;
#endif
} SEED_ALG_INFO;

/*************** Prototypes ***********************************************/
////	데이타 타입 SEED_ALG_INFO에 mode, padding 종류 및 IV 값을 초기화한다.
void	SEED_SetAlgInfo(
		DWORD			ModeID,
		DWORD			PadType,
		BYTE			*IV,
		SEED_ALG_INFO	*AlgInfo);

////	입력된 SEED_USER_KEY_LEN바인트의 비밀키로 라운드 키 생성
RET_VAL SEED_KeySchedule(
		BYTE			*UserKey,		//	사용자 비밀키를 입력함.
		DWORD			UserKeyLen,
		SEED_ALG_INFO	*AlgInfo);		//	암복호용 Round Key가 저장됨.

////	Init/Update/Final 형식을 암호화.
RET_VAL	SEED_EncInit(
		SEED_ALG_INFO	*AlgInfo);
RET_VAL	SEED_EncUpdate(
		SEED_ALG_INFO	*AlgInfo,
		BYTE			*PlainTxt,		//	평문이 입력됨.
		DWORD			PlainTxtLen,
		BYTE			*CipherTxt, 	//	암호문이 출력됨.
		DWORD			*CipherTxtLen);

RET_VAL	SEED_EncFinal(
		SEED_ALG_INFO	*AlgInfo,
		BYTE			*CipherTxt, 	//	암호문이 출력됨.
		DWORD			*CipherTxtLen);

////	Init/Update/Final 형식을 복호화.
RET_VAL	SEED_DecInit(
		SEED_ALG_INFO	*AlgInfo);
RET_VAL	SEED_DecUpdate(
		SEED_ALG_INFO	*AlgInfo,
		BYTE			*CipherTxt,		//	암호문이 입력됨.
		DWORD			CipherTxtLen,
		BYTE			*PlainTxt,		//	복호문이 출력됨.
		DWORD			*PlainTxtLen);
RET_VAL	SEED_DecFinal(
		SEED_ALG_INFO	*AlgInfo,
		BYTE			*PlainTxt,		//	복호문이 출력됨.
		DWORD			*PlainTxtLen);

//////////////////////////////////////////////
// skchoi. 2014.11.28 CTR 모드 추가 시작
RET_VAL CTR_EncUpdate(
		SEED_ALG_INFO	*AlgInfo,		//
		BYTE		*PlainTxt,		//	입력되는 평문의 pointer
		DWORD		PlainTxtLen,	//	입력되는 평문의 바이트 수
		BYTE		*CipherTxt, 	//	암호문이 출력될 pointer
		DWORD		*CipherTxtLen);	//	출력되는 암호문의 바이트 수

RET_VAL CTR_EncFinal(
		SEED_ALG_INFO	*AlgInfo,		//	
		BYTE		*CipherTxt, 	//	암호문이 출력될 pointer
		DWORD		*CipherTxtLen);	//	출력되는 암호문의 바이트 수

RET_VAL CTR_DecUpdate(
		SEED_ALG_INFO	*AlgInfo,
		BYTE		*CipherTxt, 	//	입력되는 암호문의 pointer
		DWORD		CipherTxtLen,	//	입력되는 암호문의 바이트 수
		BYTE		*PlainTxt,		//	평문이 출력될 pointer
		DWORD		*PlainTxtLen);	//	출력되는 평문의 바이트 수

RET_VAL CTR_DecFinal(
		SEED_ALG_INFO	*AlgInfo,
		BYTE		*PlainTxt,		//	평문이 출력될 pointer
		DWORD		*PlainTxtLen);	//	출력되는 평문의 바이트 수



/*
RET_VAL	SEED_CTR_Update(
		SEED_ALG_INFO	*AlgInfo,
		__int64			n64Postion,
		BYTE			*inData,		//	평문이 입력됨.
		DWORD			inDateLen,
		BYTE			*outData, 	//	암호문이 출력됨.
		DWORD			*outDataLen);
*/
// skchoi. 2014.11.28 CTR 모드 추가 종료 
//////////////////////////////////////////////

/*************** END OF FILE **********************************************/

EXTERN_C_END

#endif	//	_SEED_H
