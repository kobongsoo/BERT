#pragma once

#if defined(__USE_MOCOCRYPTO)

typedef struct _MOCO_ARIA_ALG_INFO
{
	DWORD	dwModeID;
	DWORD	dwPadType;
	BYTE	abtIV[ARIA_BLOCK_SIZE_BYTE];
	BYTE	abtChainingVar[ARIA_BLOCK_SIZE_BYTE];
	BYTE	abtRemainingCipherOrPlainText[ARIA_BLOCK_SIZE_BYTE];
	DWORD	cbRemainingCipherOrPlainText;
	BYTE	abtKey[ARIA_256_KEY_SIZE_BYTE];
	// CTR 모드 전용
	LONGLONG n64NextBlockNumber;
} MOCO_ARIA_ALG_INFO;

void MOCO_ARIA_SetAlgInfo(int nOpType, int nKeyBits, DWORD dwModeID, DWORD dwPadType, BYTE *pbtIV, MOCO_ARIA_ALG_INFO *pAlgInfo);
DWORD MOCO_ARIA_SetKey(
	BYTE				*pbtUserKey,	//	사용자 비밀키를 입력함.
	DWORD				cbUserKey,
	MOCO_ARIA_ALG_INFO	*pAlgInfo);		//	암복호용 Round Key가 저장됨.
DWORD MOCO_ARIA_EncInit(MOCO_ARIA_ALG_INFO *pAlgInfo);
DWORD MOCO_ARIA_EncUpdate(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				cbPlainTxt,		//	입력되는 평문의 바이트 수
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				*pcbCipherTxt);	//	출력되는 암호문의 바이트 수
DWORD MOCO_ARIA_EncUpdate_CBC(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				cbPlainTxt,		//	입력되는 평문의 바이트 수
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				*pcbCipherTxt);	//	출력되는 암호문의 바이트 수
DWORD MOCO_ARIA_EncUpdate_CTR(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				cbPlainTxt,		//	입력되는 평문의 바이트 수
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				*pcbCipherTxt);	//	출력되는 암호문의 바이트 수
DWORD MOCO_ARIA_EncFinal(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				*pcbCipherTxt);	//	출력되는 암호문의 바이트 수
DWORD MOCO_ARIA_EncFinal_CBC(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				*pcbCipherTxt);	//	출력되는 암호문의 바이트 수
DWORD MOCO_ARIA_EncFinal_CTR(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				*pcbCipherTxt);	//	출력되는 암호문의 바이트 수

DWORD MOCO_ARIA_DecInit(MOCO_ARIA_ALG_INFO *pAlgInfo);
DWORD MOCO_ARIA_DecUpdate(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				cbCipherTxt,	//	출력되는 암호문의 바이트 수
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				*pcbPlainTxt);	//	입력되는 평문의 바이트 수
DWORD MOCO_ARIA_DecUpdate_CBC(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				cbCipherTxt,	//	출력되는 암호문의 바이트 수
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				*pcbPlainTxt);	//	입력되는 평문의 바이트 수
DWORD MOCO_ARIA_DecUpdate_CTR(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				cbCipherTxt,	//	출력되는 암호문의 바이트 수
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				*pcbPlainTxt);	//	입력되는 평문의 바이트 수
DWORD MOCO_ARIA_DecFinal(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				*pcbPlainTxt);	//	입력되는 평문의 바이트 수
DWORD MOCO_ARIA_DecFinal_CBC(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				*pcbPlainTxt);	//	입력되는 평문의 바이트 수
DWORD MOCO_ARIA_DecFinal_CTR(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				*pcbPlainTxt);	//	입력되는 평문의 바이트 수

DWORD MOCO_ARIA_CTRUpdate(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	LONGLONG			n64Position, 
	BYTE				*inData, 	//	입력되는 암호문의 pointer
	DWORD				inLen,		//	입력되는 암호문의 바이트 수
	BYTE				*outData,	//	평문이 출력될 pointer
	DWORD				*outLen);	//	출력되는 평문의 바이트 수

#endif // defined(__USE_MOCOCRYPTO)
