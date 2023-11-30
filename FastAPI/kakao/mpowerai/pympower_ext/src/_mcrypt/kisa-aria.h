#ifndef _ARIA_H
#define _ARIA_H


/*
 * A 32-bit implementation for ARIA
 *
 * follows the specifications given in
 * the ARIA specification at
 *
 * Note:
 *    - Main body optimized for speed for 32 bit platforms
 *       * Utilizes 32-bit optimization techniques presented in ICISC 2003
 *       * Only four 32-bit tables are used
 *
 *    - Implemented some ideas for optimization from the creators of ARIA,
 *         and adopted some ideas from works submitted to ARIA implementation contest on Aug. 2004.
 *
 *    - Handles endian problem pretty well.
 *       * For optimization, for little endian architecture key setup functions return
 *         endian-reversed round keys; Crypt() function handles this correctly.
 *
 * 17, January 2005
 * Aaram Yun
 * National Security Research Institute, KOREA
 *
 * Substantial portion of the code originally written by Jin Hong.
 *
 */

/* 사용 플랫폼의 endian 특성에 따라 LITTLE_ENDIAN 혹은
 * BIG_ENDIAN 둘 중 하나를 정의해야 컴파일 됩니다.
 * Windows+Intel 플랫폼의 경우에는 LITTLE_ENDIAN이고,
 * 그 외에는 많은 경우 BIG_ENDIAN입니다.  잘 모르겠으면
 * 아무 쪽이나 선택해서 컴파일 후 실행하십시오.  ARIA_test() 
 * 함수에서 ENDIAN 확인을 하기 때문에 올바른 선택이었는지를
 * 점검할 수 있습니다. */

/* #define LITTLE_ENDIAN */
/* #define BIG_ENDIAN */

/*********************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <memory.h>

#ifndef WIN32
#include <inttypes.h>
#endif


//#define Byte unsigned char
//#define Word unsigned int

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


#ifndef __USE_CUSTON_BYTE
typedef unsigned char Byte;
#define __USE_CUSTON_BYTE 1
#endif

typedef unsigned int  Word;

/*
#define BOOL	int					//	1-bit data type
#define BYTE	unsigned char		//	unsigned 1-byte data type
#define WORD	unsigned short int	//	unsigned 2-bytes data type
#define DWORD	unsigned int		//	unsigned 4-bytes data type
#define RET_VAL		DWORD			//	return values
*/


#ifdef BIG_ENDIAN
#undef LITTLE_ENDIAN
#else
#ifndef LITTLE_ENDIAN
#define LITTLE_ENDIAN
/*
#error In order to compile this, you have to	\
  define either LITTLE_ENDIAN or BIG_ENDIAN.	\
  If unsure, try define either of one and run	\
  checkEndian() function to see if your guess	\
  is correct.
  */
#endif
#endif

// -D Option으로 compile해도 적용이 안됨. 강제로 소스코드에 넣음. 
// 만약 인텔 계열이 아닐 경우 BIG_ENDIAN 으로 변경해야 함. 
#undef BIG_ENDIAN
#ifndef LITTLE_ENDIAN
#define LITTLE_ENDIAN
#endif









/* BY(X, Y)는 Word X의 Y번째 바이트
 * BRF(T,R)은 T>>R의 하위 1바이트
 * WO(X, Y)는 Byte array X를 Word array로 간주할 때 Y번째 Word
 */

#define BY(X,Y) (((Byte *)(&X))[Y])
#define BRF(T,R) ((Byte)((T)>>(R)))
#define WO(X,Y) (((Word *)(X))[Y])

/* abcd의 4 Byte로 된 Word를 dcba로 변환하는 함수  */
#if defined(_MSC_VER)
/* MSC 사용 환경의 경우에는 _lrotr() 함수를
 * 이용할 수 있으므로 약간의 속도 향상이 가능하다. */
#define ReverseWord(W) {						\
    (W)=(0xff00ff00 & _lrotr((W), 8)) ^ (0x00ff00ff & _lrotl((W), 8));	\
  }
#else
#define ReverseWord(W) {						\
    (W)=(W)<<24 ^ (W)>>24 ^ ((W)&0x0000ff00)<<8 ^ ((W)&0x00ff0000)>>8;	\
  }
#endif

/* Byte array를 Word에 싣는 함수.  LITTLE_ENDIAN의 경우
 * 엔디안 변환 과정을 거친다. */
#ifdef LITTLE_ENDIAN
#define WordLoad(ORIG, DEST) {			\
    Word ___t;					\
    BY(___t,0)=BY(ORIG,3);			\
    BY(___t,1)=BY(ORIG,2);			\
    BY(___t,2)=BY(ORIG,1);			\
    BY(___t,3)=BY(ORIG,0);			\
    DEST=___t;					\
  }
#else
#define WordLoad(ORIG, DEST) {			\
    DEST = ORIG;				\
  }
#endif

#if defined(_MSC_VER)
#undef WordLoad
#define WordLoad(ORIG, DEST) {						\
    (DEST) = (0xff00ff00 & _lrotr((ORIG), 8)) ^ (0x00ff00ff & _lrotl((ORIG), 8)); \
  }
#endif

/* Key XOR Layer */
#define KXL {							\
    t0^=WO(rk,0); t1^=WO(rk,1); t2^=WO(rk,2); t3^=WO(rk,3);	\
    rk += 16;							\
  }

/* S-Box Layer 1 + M 변환 */
#define SBL1_M(T0,T1,T2,T3) {						\
    T0=S1[BRF(T0,24)]^S2[BRF(T0,16)]^X1[BRF(T0,8)]^X2[BRF(T0,0)];	\
    T1=S1[BRF(T1,24)]^S2[BRF(T1,16)]^X1[BRF(T1,8)]^X2[BRF(T1,0)];	\
    T2=S1[BRF(T2,24)]^S2[BRF(T2,16)]^X1[BRF(T2,8)]^X2[BRF(T2,0)];	\
    T3=S1[BRF(T3,24)]^S2[BRF(T3,16)]^X1[BRF(T3,8)]^X2[BRF(T3,0)];	\
  }
/* S-Box Layer 2 + M 변환 */
#define SBL2_M(T0,T1,T2,T3) {						\
    T0=X1[BRF(T0,24)]^X2[BRF(T0,16)]^S1[BRF(T0,8)]^S2[BRF(T0,0)];	\
    T1=X1[BRF(T1,24)]^X2[BRF(T1,16)]^S1[BRF(T1,8)]^S2[BRF(T1,0)];	\
    T2=X1[BRF(T2,24)]^X2[BRF(T2,16)]^S1[BRF(T2,8)]^S2[BRF(T2,0)];	\
    T3=X1[BRF(T3,24)]^X2[BRF(T3,16)]^S1[BRF(T3,8)]^S2[BRF(T3,0)];	\
  }
/* 워드 단위의 변환 */
#define MM(T0,T1,T2,T3) {			\
    (T1)^=(T2); (T2)^=(T3); (T0)^=(T1);		\
    (T3)^=(T1); (T2)^=(T0); (T1)^=(T2);		\
  }
/* P 변환.  확산 계층의 중간에 들어가는 바이트 단위 변환이다.
 * 이 부분은 endian과 무관하다.  */
#if defined(_MSC_VER)
#define P(T0,T1,T2,T3) {					\
    (T1) = (((T1)<< 8)&0xff00ff00) ^ (((T1)>> 8)&0x00ff00ff);	\
    (T2) = _lrotr((T2),16);					\
    ReverseWord((T3));						\
  }
#else
#define P(T0,T1,T2,T3) {					\
    (T1) = (((T1)<< 8)&0xff00ff00) ^ (((T1)>> 8)&0x00ff00ff);	\
    (T2) = (((T2)<<16)&0xffff0000) ^ (((T2)>>16)&0x0000ffff);	\
    ReverseWord((T3));						\
  }
#endif

 /* FO: 홀수번째 라운드의 F 함수
  * FE: 짝수번째 라운드의 F 함수
  * MM과 P는 바이트 단위에서 endian에 무관하게 동일한 결과를 주며,
  * 또한 endian 변환과 가환이다.  또한, SBLi_M은 LITTLE_ENDIAN에서
  * 결과적으로 Word 단위로 endian을 뒤집은 결과를 준다.
  * 즉, FO, FE는 BIG_ENDIAN 환경에서는 ARIA spec과 동일한 결과를,
  * LITTLE_ENDIAN 환경에서는 ARIA spec에서 정의한 변환+endian 변환을
  * 준다. */
#define FO {SBL1_M(t0,t1,t2,t3) MM(t0,t1,t2,t3) P(t0,t1,t2,t3) MM(t0,t1,t2,t3)}
#define FE {SBL2_M(t0,t1,t2,t3) MM(t0,t1,t2,t3) P(t2,t3,t0,t1) MM(t0,t1,t2,t3)}

/* n-bit right shift of Y XORed to X */
/* Word 단위로 정의된 블록에서의 회전 + XOR이다. */
#define GSRK(X, Y, n) {							\
    q = 4-((n)/32);							\
    r = (n) % 32;							\
    WO(rk,0) = ((X)[0]) ^ (((Y)[(q  )%4])>>r) ^ (((Y)[(q+3)%4])<<(32-r)); \
    WO(rk,1) = ((X)[1]) ^ (((Y)[(q+1)%4])>>r) ^ (((Y)[(q  )%4])<<(32-r)); \
    WO(rk,2) = ((X)[2]) ^ (((Y)[(q+2)%4])>>r) ^ (((Y)[(q+1)%4])<<(32-r)); \
    WO(rk,3) = ((X)[3]) ^ (((Y)[(q+3)%4])>>r) ^ (((Y)[(q+2)%4])<<(32-r)); \
    rk += 16;								\
  }

/* DecKeySetup()에서 사용하는 마크로 */
#if defined(_MSC_VER)
#define WordM1(X,Y) {				\
    w=_lrotr((X), 8);				\
    (Y)=w^_lrotr((X)^w, 16);			\
  }
#else
#define WordM1(X,Y) {						\
    Y=(X)<<8 ^ (X)>>8 ^ (X)<<16 ^ (X)>>16 ^ (X)<<24 ^ (X)>>24;	\
  }
#endif

//////////////////////////////////////////////////////////
// skchoi 2013.04.09
// 아래 사항은 기존의 SEED 코드를 재활용하기 위해 추가함

/*************** Definitions / Macros *************************************/
#include "kisa-crypto.h"

////	상수들
#define ARIA_BLOCK_LEN			16		//	in BYTEs
#define ARIA_USER_KEY_LEN		16		//	in BYTEs

// SKCHOI 2013.04.09
// 아래사항은 ROUNDKEY의 버퍼를 지정하기 위해 사용됨. 
// 최대인 256bit를 사용함으로써, 128, 192 등을 동시 지원할 수 있도록 함. 
#define ARIA256_NO_ROUNDS			16
#define ARIA256_NO_ROUNDKEY		(ARIA_BLOCK_LEN * (ARIA256_NO_ROUNDS+1))	//	in DWORDs

// SKCHOI 2013.04.09
// SEED에서보다 더 많은 부분이 존재함. 
typedef struct{
	int			OpType;							// 실행유형. AI_ENCRYPT/AI_DECRYPT
	int			KeyBits;						//	Key Bits
	int			NumberOfRounds;					//	라운드 수 
	DWORD		ModeID;							//	ECB or CBC
	DWORD		PadType;						//	블록암호의 Padding type
	BYTE		IV[ARIA_BLOCK_LEN];				//	Initial Vector
	BYTE		ChainVar[ARIA_BLOCK_LEN];		//	Chaining Variable
	BYTE		Buffer[ARIA_BLOCK_LEN];			//	Buffer for unfilled block
	DWORD		BufLen; 						//	Buffer의 유효 바이트 수
	BYTE		RoundKey[ARIA256_NO_ROUNDKEY];	//	라운드 키의 DWORD 수. 일단 최대치로 잡아둔다. 
#ifdef WIN32
	__int64		n64CTRBlcokNumber;
#else
	int64_t		n64CTRBlcokNumber;
#endif
} ARIA_ALG_INFO;


/*************** Prototypes ***********************************************/

// SKCHOI 2013.04.09
// SEED와 동일한 형태로 동작하도록 하기 위해 추가함. 
////	데이타 타입 SEED_ALG_INFO에 mode, padding 종류 및 IV 값을 초기화한다.
void	ARIA_SetAlgInfo(
		int				OpType, 
		int				KeyBits, 
		DWORD			ModeID,
		DWORD			PadType,
		BYTE			*IV,
		ARIA_ALG_INFO	*AlgInfo);

////	입력된 SEED_USER_KEY_LEN바인트의 비밀키로 라운드 키 생성
RET_VAL ARIA_KeySchedule(
		BYTE			*UserKey,		//	사용자 비밀키를 입력함.
		DWORD			UserKeyLen,
		ARIA_ALG_INFO	*AlgInfo);		//	암복호용 Round Key가 저장됨.



RET_VAL	ARIA_EncInit(
		ARIA_ALG_INFO	*AlgInfo);
RET_VAL	ARIA_EncUpdate(
		ARIA_ALG_INFO	*AlgInfo,
		BYTE		*PlainTxt,		//	입력되는 평문의 pointer
		DWORD		PlainTxtLen,	//	입력되는 평문의 바이트 수
		BYTE		*CipherTxt, 	//	암호문이 출력될 pointer
		DWORD		*CipherTxtLen);	//	출력되는 암호문의 바이트 수
RET_VAL	ARIA_EncFinal(
		ARIA_ALG_INFO	*AlgInfo,
		BYTE		*CipherTxt, 	//	암호문이 출력될 pointer
		DWORD		*CipherTxtLen);	//	출력되는 암호문의 바이트 수

////	Init/Update/Final 형식을 복호화.
RET_VAL	ARIA_DecInit(
		ARIA_ALG_INFO	*AlgInfo);
RET_VAL	ARIA_DecUpdate(
		ARIA_ALG_INFO	*AlgInfo,
		BYTE		*CipherTxt, 	//	암호문이 출력될 pointer
		DWORD		CipherTxtLen,	//	출력되는 암호문의 바이트 수
		BYTE		*PlainTxt,		//	입력되는 평문의 pointer
		DWORD		*PlainTxtLen);	//	입력되는 평문의 바이트 수
RET_VAL	ARIA_DecFinal(
		ARIA_ALG_INFO	*AlgInfo,
		BYTE		*PlainTxt,		//	입력되는 평문의 pointer
		DWORD		*PlainTxtLen);	//	입력되는 평문의 바이트 수
//
///////////////////////////////////////////////////////////

void ARIA_Crypt(const Byte *i, int Nr, const Byte *rk, Byte *o);
int ARIA_EncKeySetup(const Byte *mk, Byte *rk, int keyBits);
int ARIA_DecKeySetup(const Byte *mk, Byte *rk, int keyBits);

EXTERN_C_END

#endif  // _ARIA_H

/*
 * vim: ts=4 sts=4 sw=4 noet
 */
