#include "stdafx.h"
#include "kisa-crypto.h"
// 2019년 3월 8일 박규영
// BIG_ENDIAN을 undef하기 위해 필요.
#include "kisa-seed.h"

///////////////////////////////////////////////////////////
// skchoi. 2014.11.28 CTR 모드 추가 
#ifdef WIN32
unsigned __int64 SEED_SwapEndian(unsigned __int64 host_longlong)
#else
uint64_t SEED_SwapEndian(uint64_t host_longlong)
#endif
{
#ifdef BIG_ENDIAN
	host_longlong = (host_longlong >> 56) |
		((host_longlong << 40) & 0x00FF000000000000) |
		((host_longlong << 24) & 0x0000FF0000000000) |
		((host_longlong << 8) & 0x000000FF00000000) |
		((host_longlong >> 8) & 0x00000000FF000000) |
		((host_longlong >> 24) & 0x0000000000FF0000) |
		((host_longlong >> 40) & 0x000000000000FF00) |
		(host_longlong << 56);
	return host_longlong;
#else
	return host_longlong;
#endif
	/*
	x = (x>>24) |
	((x<<8) & 0x00FF0000) |
	((x>>8) & 0x0000FF00) |
	(x<<24);
	*/

	/*
	int x = 1;

	// little endian
	if(*(char *)&x == 1)
	return ((((unsigned __int64)htonl((unsigned long)host_longlong)) << 32) + (unsigned __int64)htonl((unsigned long)(host_longlong >> 32)));

	// big endian
	else
	return host_longlong;
	*/
}
/*
unsigned __int64 SEED_ntohll(unsigned __int64 host_longlong)
{
int x = 1;

//  little endian
if(*(char *)&x == 1)
return ((((unsigned __int64)ntohl((unsigned long)host_longlong)) << 32) + (unsigned __int64)ntohl((unsigned long)(host_longlong >> 32)));

//  big endian
else
return host_longlong;
}
*/
