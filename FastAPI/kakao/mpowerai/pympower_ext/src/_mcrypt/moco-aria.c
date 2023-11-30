#include "stdafx.h"
#include <assert.h>
#include <malloc.h>
#include <string.h>
#if defined(__USE_MOCOCRYPTO)
#include "moco-crypto.h"
#include "moco-aria.h"

// kisa-seed.cpp 파일의 소스코드를 복사하고
// 수정하기 쉽도록 SEED 관련 상수 제거
#undef SEED_128_KEY_SIZE_BYTE
#undef SEED_BLOCK_SIZE_BYTE

void MOCO_ARIA_SetAlgInfo(int nOpType, int nKeyBits, DWORD dwModeID, DWORD dwPadType, BYTE *pbtIV, MOCO_ARIA_ALG_INFO *pAlgInfo)
{
	pAlgInfo->dwModeID = dwModeID;
	pAlgInfo->dwPadType = dwPadType;
	memcpy(pAlgInfo->abtIV, pbtIV, ARIA_BLOCK_SIZE_BYTE);
}

DWORD MOCO_ARIA_SetKey(
	BYTE				*pbtUserKey,	//	사용자 비밀키를 입력함.
	DWORD				cbUserKey,
	MOCO_ARIA_ALG_INFO	*pAlgInfo)		//	암복호용 Round Key가 저장됨.
{
	if(ARIA_256_KEY_SIZE_BYTE != cbUserKey)
	{
		return CTR_INVALID_USERKEYLEN;
	}

	memcpy(pAlgInfo->abtKey, pbtUserKey, cbUserKey);

	return CTR_SUCCESS;
}

DWORD MOCO_ARIA_EncInit(MOCO_ARIA_ALG_INFO *pAlgInfo)
{
	pAlgInfo->cbRemainingCipherOrPlainText = 0L;
	if( pAlgInfo->dwModeID !=AI_ECB )
		memcpy(pAlgInfo->abtChainingVar, pAlgInfo->abtIV, ARIA_BLOCK_SIZE_BYTE);
	pAlgInfo->n64NextBlockNumber = 0ll;
	return CTR_SUCCESS;
}

DWORD MOCO_ARIA_EncUpdate(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				cbPlainTxt,		//	입력되는 평문의 바이트 수
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				*pcbCipherTxt)	//	출력되는 암호문의 바이트 수
{
	switch(pAlgInfo->dwModeID)
	{
	case AI_CBC:
		return MOCO_ARIA_EncUpdate_CBC(pAlgInfo, pbtPlainTxt, cbPlainTxt, pbtCipherTxt, pcbCipherTxt);
	case AI_CTR:
		return MOCO_ARIA_EncUpdate_CTR(pAlgInfo, pbtPlainTxt, cbPlainTxt, pbtCipherTxt, pcbCipherTxt);
	default:
		return CTR_FATAL_ERROR;
	}
}

DWORD MOCO_ARIA_EncUpdate_CBC(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				cbPlainTxt,		//	입력되는 평문의 바이트 수
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				*pcbCipherTxt)	//	출력되는 암호문의 바이트 수
{
	const DWORD cbTotalPlainText = pAlgInfo->cbRemainingCipherOrPlainText + cbPlainTxt;
	if(cbTotalPlainText <= ARIA_BLOCK_SIZE_BYTE)
	{
		// 암호화할 평문 크기가 ARIA_BLOCK_SIZE_BYTE보다 작으면 버퍼에 보관해두고 성공으로 반환.
		memcpy(&pAlgInfo->abtRemainingCipherOrPlainText[pAlgInfo->cbRemainingCipherOrPlainText],
			pbtPlainTxt, cbPlainTxt);
		pAlgInfo->cbRemainingCipherOrPlainText = cbTotalPlainText;
		*pcbCipherTxt = 0;
		return CTR_SUCCESS;
	}

	// 블록 크기로 나눠서 암호화할 평문의 길이와 지금 암호화 하지 않고
	// 나중에 Update나 Final에서 암호화할 부분의 길이를 구함.
	const DWORD cbNotNowPlainText = cbTotalPlainText % ARIA_BLOCK_SIZE_BYTE;
	const DWORD cbPlainTextToEncrypt = cbTotalPlainText - cbNotNowPlainText;
	const BYTE* lpbtNotNowPlainText = pbtPlainTxt + cbPlainTxt - cbNotNowPlainText;

	// 이전에 암호화 하다가 남은 평문 있으면 합쳐서 하나의 버퍼로 만듦.
	// 필요한 경우 평문을 병합할 메모리 버퍼 할당.
	BOOL bPlainTextToEncryptHasAllocated;
	BYTE* lpbtPlainTextToEncrypt;
	if(pAlgInfo->cbRemainingCipherOrPlainText)
	{
		lpbtPlainTextToEncrypt = malloc(cbPlainTextToEncrypt);
		memcpy(lpbtPlainTextToEncrypt, pAlgInfo->abtRemainingCipherOrPlainText,
			pAlgInfo->cbRemainingCipherOrPlainText);
		memcpy(lpbtPlainTextToEncrypt + pAlgInfo->cbRemainingCipherOrPlainText,
			pbtPlainTxt, cbPlainTxt - cbNotNowPlainText);
		bPlainTextToEncryptHasAllocated = TRUE;
	}
	else
	{
		lpbtPlainTextToEncrypt = pbtPlainTxt;
		bPlainTextToEncryptHasAllocated = FALSE;
	}

	// NEO_ARIA_256_CBC_Encrypt 호출
	// 참고: 이 함수의 입력 값인 *pcbCipherTxt값은 초기화 되지 않은 값임.
	// 실제 pbtCipherTxt 크기를 알 수 없지만 NEO_ARIA_256_CBC_Encrypt함수에
	// cbPlainTextToEncrypt보다 작은 n64CipherTxtSize 값을 넘겨주면 에러가
	// 발생하기 때문에 이를 피하기 위해 cbPlainTextToEncrypt로 설정 함.
	ULONGLONG n64CipherTxtSize = cbPlainTextToEncrypt;
	ULONG dwNEOError = g_lpfnNEO_ARIA_256_CBC_Encrypt(
		pAlgInfo->abtKey,
		pAlgInfo->abtChainingVar,
		lpbtPlainTextToEncrypt,
		cbPlainTextToEncrypt,
		pbtCipherTxt,
		&n64CipherTxtSize
		);
	if(NEO_SUCCESS != dwNEOError)
	{
		// TODO: 로그
		if(bPlainTextToEncryptHasAllocated)
		{
			free(lpbtPlainTextToEncrypt);
		}
		return CTR_FATAL_ERROR;
	}
	if(n64CipherTxtSize > UINT32_MAX)
	{
		if(bPlainTextToEncryptHasAllocated)
		{
			free(lpbtPlainTextToEncrypt);
		}
		return CTR_FATAL_ERROR;
	}

	// 암호화된 마지막 블록으로 ChainingVar 갱신
	*pcbCipherTxt = (DWORD) n64CipherTxtSize;
	const BYTE* lpbtChiningVar = pbtCipherTxt + *pcbCipherTxt - ARIA_BLOCK_SIZE_BYTE;
	assert(lpbtChiningVar >= pbtCipherTxt);
	memcpy(pAlgInfo->abtChainingVar, lpbtChiningVar, ARIA_BLOCK_SIZE_BYTE);

	// ARIA_BLOCK_SIZE_BYTE로 잘리지 않은 남은 평문 보관
	pAlgInfo->cbRemainingCipherOrPlainText = cbNotNowPlainText;
	if(pAlgInfo->cbRemainingCipherOrPlainText)
	{
		memcpy(pAlgInfo->abtRemainingCipherOrPlainText, lpbtNotNowPlainText, cbNotNowPlainText);
	}

	// 메모리 해제
	if(bPlainTextToEncryptHasAllocated)
	{
		free(lpbtPlainTextToEncrypt);
	}

	return CTR_SUCCESS;
}

DWORD MOCO_ARIA_EncUpdate_CTR(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				cbPlainTxt,		//	입력되는 평문의 바이트 수
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				*pcbCipherTxt)	//	출력되는 암호문의 바이트 수
{
	const DWORD cbTotalPlainText = pAlgInfo->cbRemainingCipherOrPlainText + cbPlainTxt;
	if(cbTotalPlainText <= ARIA_BLOCK_SIZE_BYTE)
	{
		// 암호화할 평문 크기가 ARIA_BLOCK_SIZE_BYTE보다 작으면 버퍼에 보관해두고 성공으로 반환.
		memcpy(&pAlgInfo->abtRemainingCipherOrPlainText[pAlgInfo->cbRemainingCipherOrPlainText],
			pbtPlainTxt, cbPlainTxt);
		pAlgInfo->cbRemainingCipherOrPlainText = cbTotalPlainText;
		*pcbCipherTxt = 0;
		return CTR_SUCCESS;
	}

	// 블록 크기로 나눠서 암호화할 평문의 길이와 지금 암호화 하지 않고
	// 나중에 Update나 Final에서 암호화할 부분의 길이를 구함.
	const DWORD cbNotNowPlainText = cbTotalPlainText % ARIA_BLOCK_SIZE_BYTE;
	const DWORD cbPlainTextToEncrypt = cbTotalPlainText - cbNotNowPlainText;
	const BYTE* lpbtNotNowPlainText = pbtPlainTxt + cbPlainTxt - cbNotNowPlainText;

	// 이전에 암호화 하다가 남은 평문 있으면 합쳐서 하나의 버퍼로 만듦.
	// 필요한 경우 평문을 병합할 메모리 버퍼 할당.
	BOOL bPlainTextToEncryptHasAllocated;
	BYTE* lpbtPlainTextToEncrypt;
	if(pAlgInfo->cbRemainingCipherOrPlainText)
	{
		lpbtPlainTextToEncrypt = malloc(cbPlainTextToEncrypt);
		memcpy(lpbtPlainTextToEncrypt, pAlgInfo->abtRemainingCipherOrPlainText,
			pAlgInfo->cbRemainingCipherOrPlainText);
		memcpy(lpbtPlainTextToEncrypt + pAlgInfo->cbRemainingCipherOrPlainText,
			pbtPlainTxt, cbPlainTxt - cbNotNowPlainText);
		bPlainTextToEncryptHasAllocated = TRUE;
	}
	else
	{
		lpbtPlainTextToEncrypt = pbtPlainTxt;
		bPlainTextToEncryptHasAllocated = FALSE;
	}

	// CTR 암호화를 위한 Nonce와 Counter 생성
	BYTE btNonce[CTR_NONCE_SIZE_BYTE];
	ULONGLONG u64Counter;
	MOCO_MakeNonceAndCounter(btNonce, &u64Counter, pAlgInfo->abtIV, pAlgInfo->n64NextBlockNumber);

	// NEO_ARIA_256_CTR_Encrypt 호출
	ULONG dwNEOError = g_lpfnNEO_ARIA_256_CTR_Encrypt(
		pAlgInfo->abtKey,
		btNonce,
		u64Counter,
		lpbtPlainTextToEncrypt,
		cbPlainTextToEncrypt,
		pbtCipherTxt
		);
	if(NEO_SUCCESS != dwNEOError)
	{
		// TODO: 로그
		if(bPlainTextToEncryptHasAllocated)
		{
			free(lpbtPlainTextToEncrypt);
		}
		return CTR_FATAL_ERROR;
	}

	// 카운터 업데이트
	*pcbCipherTxt = (DWORD) cbPlainTextToEncrypt;
	assert(0 == cbPlainTextToEncrypt % ARIA_BLOCK_SIZE_BYTE);
	pAlgInfo->n64NextBlockNumber += cbPlainTextToEncrypt / ARIA_BLOCK_SIZE_BYTE;

	// ARIA_BLOCK_SIZE_BYTE로 잘리지 않은 남은 평문 보관
	pAlgInfo->cbRemainingCipherOrPlainText = cbNotNowPlainText;
	if(pAlgInfo->cbRemainingCipherOrPlainText)
	{
		memcpy(pAlgInfo->abtRemainingCipherOrPlainText, lpbtNotNowPlainText, cbNotNowPlainText);
	}

	// 메모리 해제
	if(bPlainTextToEncryptHasAllocated)
	{
		free(lpbtPlainTextToEncrypt);
	}

	return CTR_SUCCESS;
}

DWORD MOCO_ARIA_EncFinal(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				*pcbCipherTxt)	//	출력되는 암호문의 바이트 수
{
	switch(pAlgInfo->dwModeID)
	{
	case AI_CBC:
		return MOCO_ARIA_EncFinal_CBC(pAlgInfo, pbtCipherTxt, pcbCipherTxt);
	case AI_CTR:
		return MOCO_ARIA_EncFinal_CTR(pAlgInfo, pbtCipherTxt, pcbCipherTxt);
	default:
		return CTR_FATAL_ERROR;
	}
}

DWORD MOCO_ARIA_EncFinal_CBC(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				*pcbCipherTxt)	//	출력되는 암호문의 바이트 수
{
	DWORD dwPaddBytesOrErrorCode = MOCO_PaddSet(pAlgInfo->abtRemainingCipherOrPlainText,
		pAlgInfo->cbRemainingCipherOrPlainText, ARIA_BLOCK_SIZE_BYTE, pAlgInfo->dwPadType);
	if(dwPaddBytesOrErrorCode > ARIA_BLOCK_SIZE_BYTE)
	{
		return dwPaddBytesOrErrorCode;
	}

	if(0 == dwPaddBytesOrErrorCode)
	{
		*pcbCipherTxt = 0;
		return CTR_FATAL_ERROR;
	}

	ULONGLONG n64CipherTxtSize = ARIA_BLOCK_SIZE_BYTE;
	ULONG dwNEOError = g_lpfnNEO_ARIA_256_CBC_Encrypt(
		pAlgInfo->abtKey,
		pAlgInfo->abtChainingVar,
		pAlgInfo->abtRemainingCipherOrPlainText,
		ARIA_BLOCK_SIZE_BYTE,
		pbtCipherTxt,
		&n64CipherTxtSize
		);
	if(NEO_SUCCESS != dwNEOError)
	{
		return CTR_FATAL_ERROR;
	}
	*pcbCipherTxt = (DWORD) n64CipherTxtSize;

	return CTR_SUCCESS;
}

DWORD MOCO_ARIA_EncFinal_CTR(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				*pcbCipherTxt)	//	출력되는 암호문의 바이트 수
{
	if(0 == pAlgInfo->cbRemainingCipherOrPlainText)
	{
		*pcbCipherTxt = 0;
		return CTR_SUCCESS;
	}

	// CTR 암호화를 위한 Nonce와 Counter 생성
	BYTE btNonce[CTR_NONCE_SIZE_BYTE];
	ULONGLONG u64Counter;
	MOCO_MakeNonceAndCounter(btNonce, &u64Counter, pAlgInfo->abtIV, pAlgInfo->n64NextBlockNumber);

	ULONG dwNEOError = g_lpfnNEO_ARIA_256_CTR_Encrypt(
		pAlgInfo->abtKey,
		btNonce,
		u64Counter,
		pAlgInfo->abtRemainingCipherOrPlainText,
		pAlgInfo->cbRemainingCipherOrPlainText,
		pbtCipherTxt
		);
	if(NEO_SUCCESS != dwNEOError)
	{
		return CTR_FATAL_ERROR;
	}
	*pcbCipherTxt = pAlgInfo->cbRemainingCipherOrPlainText;

	return CTR_SUCCESS;
}

DWORD MOCO_ARIA_DecInit(MOCO_ARIA_ALG_INFO *pAlgInfo)
{
	pAlgInfo->cbRemainingCipherOrPlainText = 0;
	if( pAlgInfo->dwModeID!=AI_ECB )
		memcpy(pAlgInfo->abtChainingVar, pAlgInfo->abtIV, ARIA_BLOCK_SIZE_BYTE);
	pAlgInfo->n64NextBlockNumber = 0;
	return CTR_SUCCESS;
}

DWORD MOCO_ARIA_DecUpdate(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				cbCipherTxt,	//	출력되는 암호문의 바이트 수
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				*pcbPlainTxt)	//	입력되는 평문의 바이트 수
{
	switch(pAlgInfo->dwModeID)
	{
	case AI_CBC:
		return MOCO_ARIA_DecUpdate_CBC(pAlgInfo, pbtCipherTxt, cbCipherTxt, pbtPlainTxt, pcbPlainTxt);
	case AI_CTR:
		return MOCO_ARIA_DecUpdate_CTR(pAlgInfo, pbtCipherTxt, cbCipherTxt, pbtPlainTxt, pcbPlainTxt);
	default:
		return CTR_FATAL_ERROR;
	}
}

DWORD MOCO_ARIA_DecUpdate_CBC(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				cbCipherTxt,	//	출력되는 암호문의 바이트 수
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				*pcbPlainTxt)	//	입력되는 평문의 바이트 수
{
	const DWORD cbTotalCipherText = pAlgInfo->cbRemainingCipherOrPlainText + cbCipherTxt;
	if(cbTotalCipherText <= ARIA_BLOCK_SIZE_BYTE)
	{
		// 복호화할 암호문 크기가 ARIA_BLOCK_SIZE_BYTE보다 작으면 버퍼에 보관해두고 성공으로 반환.
		memcpy(&pAlgInfo->abtRemainingCipherOrPlainText[pAlgInfo->cbRemainingCipherOrPlainText],
			pbtCipherTxt, cbCipherTxt);
		pAlgInfo->cbRemainingCipherOrPlainText = cbTotalCipherText;
		*pcbPlainTxt = 0;
		return CTR_SUCCESS;
	}

	// 블록 크기로 나눠서 복호화할 암호문의 길이와 지금 복호화 하지 않고
	// 나중에 Update나 Final에서 복호화할 부분의 길이를 구함.
	DWORD cbNotNowCipherText = cbTotalCipherText % ARIA_BLOCK_SIZE_BYTE;
	if(0 == cbNotNowCipherText)
	{
		// 마지막 블록은 패딩을 제거해야 하기 때문에 MOCO_ARIA_DecFinal_CBC에서
		// 처리하도록 보관해둔다.
		cbNotNowCipherText = ARIA_BLOCK_SIZE_BYTE;
	}
	const DWORD cbCipherTextToDecrypt = cbTotalCipherText - cbNotNowCipherText;
	const BYTE* lpbtNotNowCipherText = pbtCipherTxt + cbCipherTxt - cbNotNowCipherText;

	// 이전에 복호화 하다가 남은 암호문 있으면 합쳐서 하나의 버퍼로 만듦.
	// 필요한 경우 암호문을 병합할 메모리 버퍼 할당.
	BOOL bCipherTextToDecryptHasAllocated;
	BYTE* lpbtCipherTextToDecrypt;
	if(pAlgInfo->cbRemainingCipherOrPlainText)
	{
		lpbtCipherTextToDecrypt = malloc(cbCipherTextToDecrypt);
		memcpy(lpbtCipherTextToDecrypt, pAlgInfo->abtRemainingCipherOrPlainText,
			pAlgInfo->cbRemainingCipherOrPlainText);
		memcpy(lpbtCipherTextToDecrypt + pAlgInfo->cbRemainingCipherOrPlainText,
			pbtCipherTxt, cbCipherTxt - cbNotNowCipherText);
		bCipherTextToDecryptHasAllocated = TRUE;
	}
	else
	{
		lpbtCipherTextToDecrypt = pbtCipherTxt;
		bCipherTextToDecryptHasAllocated = FALSE;
	}

	// NEO_ARIA_256_CBC_Decrypt 호출
	ULONG dwNEOError = g_lpfnNEO_ARIA_256_CBC_Decrypt(
		pAlgInfo->abtKey,
		pAlgInfo->abtChainingVar,
		lpbtCipherTextToDecrypt,
		cbCipherTextToDecrypt,
		pbtPlainTxt
		);
	if(NEO_SUCCESS != dwNEOError)
	{
		// TODO: 로그
		if(bCipherTextToDecryptHasAllocated)
		{
			free(lpbtCipherTextToDecrypt);
		}
		return CTR_FATAL_ERROR;
	}

	// 암호화된 마지막 블록으로 ChainingVar 갱신
	*pcbPlainTxt = (DWORD) cbCipherTextToDecrypt;
	const BYTE* lpbtChiningVar = lpbtCipherTextToDecrypt + cbCipherTextToDecrypt - ARIA_BLOCK_SIZE_BYTE;
	assert(lpbtChiningVar >= lpbtCipherTextToDecrypt);
	memcpy(pAlgInfo->abtChainingVar, lpbtChiningVar, ARIA_BLOCK_SIZE_BYTE);

	// ARIA_BLOCK_SIZE_BYTE로 잘리지 않은 남은 암호문 보관
	pAlgInfo->cbRemainingCipherOrPlainText = cbNotNowCipherText;
	if(pAlgInfo->cbRemainingCipherOrPlainText)
	{
		memcpy(pAlgInfo->abtRemainingCipherOrPlainText, lpbtNotNowCipherText, cbNotNowCipherText);
	}

	// 메모리 해제
	if(bCipherTextToDecryptHasAllocated)
	{
		free(lpbtCipherTextToDecrypt);
	}

	return CTR_SUCCESS;
}

DWORD MOCO_ARIA_DecUpdate_CTR(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtCipherTxt, 	//	암호문이 출력될 pointer
	DWORD				cbCipherTxt,	//	출력되는 암호문의 바이트 수
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				*pcbPlainTxt)	//	입력되는 평문의 바이트 수
{
	return MOCO_ARIA_EncUpdate_CTR(pAlgInfo, pbtCipherTxt, cbCipherTxt, pbtPlainTxt, pcbPlainTxt);
}

// TODO: 구현 할 것.
DWORD MOCO_ARIA_DecFinal(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				*pcbPlainTxt)	//	입력되는 평문의 바이트 수
{
	switch(pAlgInfo->dwModeID)
	{
	case AI_CBC:
		return MOCO_ARIA_DecFinal_CBC(pAlgInfo, pbtPlainTxt, pcbPlainTxt);
	case AI_CTR:
		return MOCO_ARIA_DecFinal_CTR(pAlgInfo, pbtPlainTxt, pcbPlainTxt);
	default:
		return CTR_FATAL_ERROR;
	}
}

DWORD MOCO_ARIA_DecFinal_CBC(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				*pcbPlainTxt)	//	입력되는 평문의 바이트 수
{
	// 패딩 타입에 상관 없이 MOCO_ARIA_DecUpdate_CBC함수는 항상 마지막 블록의
	// 암호를 해제하지 않고 보관해 두기 때문에 abtRemainingCipherOrPlainText에는
	// 항상 유효한 데이터가 있어야 한다.
	if(ARIA_BLOCK_SIZE_BYTE != pAlgInfo->cbRemainingCipherOrPlainText)
	{
		return CTR_CIPHER_LEN_ERROR;
	}

	// 암호 해제
	ULONG dwNEOError = g_lpfnNEO_ARIA_256_CBC_Decrypt(
		pAlgInfo->abtKey,
		pAlgInfo->abtChainingVar,
		pAlgInfo->abtRemainingCipherOrPlainText,
		pAlgInfo->cbRemainingCipherOrPlainText,
		pbtPlainTxt
		);
	if(NEO_SUCCESS != dwNEOError)
	{
		return CTR_FATAL_ERROR;
	}

	// 패딩 제거
	DWORD dwPaddBytesOrErrorCode = MOCO_PaddCheck(
		pbtPlainTxt,
		pAlgInfo->cbRemainingCipherOrPlainText, pAlgInfo->dwPadType);
	if(dwPaddBytesOrErrorCode > pAlgInfo->cbRemainingCipherOrPlainText)
	{
		return dwPaddBytesOrErrorCode;
	}

	*pcbPlainTxt = pAlgInfo->cbRemainingCipherOrPlainText - dwPaddBytesOrErrorCode;

	return CTR_SUCCESS;
}

// TODO: 구현 할 것.
DWORD MOCO_ARIA_DecFinal_CTR(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	BYTE				*pbtPlainTxt,	//	입력되는 평문의 pointer
	DWORD				*pcbPlainTxt)	//	입력되는 평문의 바이트 수
{
	return MOCO_ARIA_EncFinal_CTR(pAlgInfo, pbtPlainTxt, pcbPlainTxt);
}

DWORD MOCO_ARIA_CTRUpdate(
	MOCO_ARIA_ALG_INFO	*pAlgInfo,
	LONGLONG			n64Position, 
	BYTE				*inData, 	//	입력되는 암호문의 pointer
	DWORD				inLen,		//	입력되는 암호문의 바이트 수
	BYTE				*outData,	//	평문이 출력될 pointer
	DWORD				*outLen)	//	출력되는 평문의 바이트 수
{
	const LONGLONG n64BlockNumber = n64Position / ARIA_BLOCK_SIZE_BYTE;
	const DWORD cbPrepend = n64Position % ARIA_BLOCK_SIZE_BYTE;
	const DWORD cbAppend = ARIA_BLOCK_SIZE_BYTE - ((inLen + cbPrepend) % ARIA_BLOCK_SIZE_BYTE);
	const DWORD cbToEncrypt = cbPrepend + inLen + cbAppend;

	BYTE* lpbtToEncrypt = malloc(cbToEncrypt);
	memcpy(&lpbtToEncrypt[cbPrepend], inData, inLen);
	BYTE* lpbtEncrypted = malloc(cbToEncrypt);

	// CTR 암호화를 위한 Nonce와 Counter 생성
	BYTE btNonce[CTR_NONCE_SIZE_BYTE];
	ULONGLONG u64Counter;
	MOCO_MakeNonceAndCounter(btNonce, &u64Counter, pAlgInfo->abtIV, n64BlockNumber);

	DWORD dwNEOError = g_lpfnNEO_ARIA_256_CTR_Encrypt(
		pAlgInfo->abtKey,
		btNonce,
		u64Counter,
		lpbtToEncrypt,
		cbToEncrypt,
		lpbtEncrypted
		);
	if(NEO_SUCCESS != dwNEOError)
	{
		free(lpbtToEncrypt);
		free(lpbtEncrypted);
		return CTR_FATAL_ERROR;
	}

	memcpy(outData, &lpbtEncrypted[cbPrepend], inLen);
	*outLen = inLen;

	free(lpbtToEncrypt);
	free(lpbtEncrypted);

	return CTR_SUCCESS;
}

#endif // defined(__USE_MOCOCRYPTO)
