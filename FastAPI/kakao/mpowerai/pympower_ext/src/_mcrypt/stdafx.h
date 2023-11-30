#pragma once

#include <stdint.h>

#if defined(__USE_MOCOCRYPTO_KISACRYPTO_MIXING)
#if !defined(__USE_MOCOCRYPTO)
#error "전처리 상수 __USE_MOCOCRYPTO_KISACRYPTO_MIXING를 선언하면 __USE_MOCOCRYPTO도 선언해야 합니다."
#endif // !defined(__USE_MOCOCRYPTO)
#endif // defined(__USE_MOCOCRYPTO_KISACRYPTO_MIXING)
