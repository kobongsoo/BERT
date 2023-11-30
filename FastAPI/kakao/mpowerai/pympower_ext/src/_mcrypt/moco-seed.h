#pragma once

#if defined(__USE_MOCOCRYPTO)

typedef struct _MOCO_SEED_ALG_INFO
{
	DWORD	dwModeID;
	DWORD	dwPadType;
	BYTE	abtIV[SEED_BLOCK_SIZE_BYTE];
	BYTE	abtChainingBlock[SEED_BLOCK_SIZE_BYTE];
	BYTE	abtRemainingCipherOrPlainText[SEED_BLOCK_SIZE_BYTE];
	DWORD	cbRemainingCipherOrPlainText;
	BYTE	abtKey[SEED_128_KEY_SIZE_BYTE];
	// CTR 모드 전용
	LONGLONG n64NextBlockNumber;
	LONG	nRemainSize;
} MOCO_SEED_ALG_INFO;

void MOCO_SEED_SetAlgInfo(DWORD dwModeID, DWORD dwPadType, BYTE *pbtIV, MOCO_SEED_ALG_INFO *pAlgInfo);
DWORD MOCO_SEED_SetKey(
	BYTE				*pbtUserKey,	//	사용자 비밀키 입력
	DWORD				cbUserKey,		//	사용자 비밀키의 바이트 수
	MOCO_SEED_ALG_INFO	*pAlgInfo);		//	암호용/복호용 Round Key 생성/저장
DWORD MOCO_SEED_EncInit(MOCO_SEED_ALG_INFO *pAlgInfo);
DWORD MOCO_SEED_EncUpdate(
	MOCO_SEED_ALG_INFO	*pAlgInfo,
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				cbPlainTxt,		//	입력되는 평문의 바이트 수
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				*pcbCipherTxt);	//	출력되는 암호문의 바이트 수
DWORD MOCO_SEED_EncUpdate_CBC(
	MOCO_SEED_ALG_INFO	*pAlgInfo,
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				cbPlainTxt,		//	입력되는 평문의 바이트 수
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				*pcbCipherTxt);	//	출력되는 암호문의 바이트 수
DWORD MOCO_SEED_EncUpdate_CTR(
	MOCO_SEED_ALG_INFO	*pAlgInfo,
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				cbPlainTxt,		//	입력되는 평문의 바이트 수
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				*pcbCipherTxt);	//	출력되는 암호문의 바이트 수
DWORD MOCO_SEED_EncFinal(
	MOCO_SEED_ALG_INFO	*pAlgInfo,
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				*pcbCipherTxt);	//	출력되는 암호문의 바이트 수
DWORD MOCO_SEED_EncFinal_CBC(
	MOCO_SEED_ALG_INFO	*pAlgInfo,
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				*pcbCipherTxt);	//	출력되는 암호문의 바이트 수
DWORD MOCO_SEED_EncFinal_CTR(
	MOCO_SEED_ALG_INFO	*pAlgInfo,
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				*pcbCipherTxt);	//	출력되는 암호문의 바이트 수

DWORD MOCO_SEED_DecInit(MOCO_SEED_ALG_INFO *pAlgInfo);
DWORD MOCO_SEED_DecUpdate(
	MOCO_SEED_ALG_INFO	*pAlgInfo,
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				cbCipherTxt,	//	출력되는 암호문의 바이트 수
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				*pcbPlainTxt);	//	입력되는 평문의 바이트 수
DWORD MOCO_SEED_DecUpdate_CBC(
	MOCO_SEED_ALG_INFO	*pAlgInfo,
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				cbCipherTxt,	//	출력되는 암호문의 바이트 수
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				*pcbPlainTxt);	//	입력되는 평문의 바이트 수
DWORD MOCO_SEED_DecUpdate_CTR(
	MOCO_SEED_ALG_INFO	*pAlgInfo,
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				cbCipherTxt,	//	출력되는 암호문의 바이트 수
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				*pcbPlainTxt);	//	입력되는 평문의 바이트 수
DWORD MOCO_SEED_DecFinal(
	MOCO_SEED_ALG_INFO	*pAlgInfo,
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				*pcbPlainTxt);	//	입력되는 평문의 바이트 수
DWORD MOCO_SEED_DecFinal_CBC(
	MOCO_SEED_ALG_INFO	*pAlgInfo,
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				*pcbPlainTxt);	//	입력되는 평문의 바이트 수
DWORD MOCO_SEED_DecFinal_CTR(
	MOCO_SEED_ALG_INFO	*pAlgInfo,
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				*pcbPlainTxt);	//	입력되는 평문의 바이트 수

DWORD MOCO_SEED_CTRUpdate(
	MOCO_SEED_ALG_INFO	*pAlgInfo,
	LONGLONG			n64Position,
	BYTE				*inData, 	//	입력되는 암호문의 pointer
	DWORD				inLen,		//	입력되는 암호문의 바이트 수
	BYTE				*outData,	//	평문이 출력될 pointer
	DWORD				*outLen);	//	출력되는 평문의 바이트 수

#endif // defined(__USE_MOCOCRYPTO)
