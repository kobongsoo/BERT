

import json
from typing import Any

# PHP의 SESSION과 같이 global로 사용되는 변수를 활용하기 위한 클래스이다. 
# staticmethod로만 지정되어, 별도의 인스턴스화 없이 바로 사용한다.  
class MSESSION:
    conf = {"lang": "ko"};
   
    @staticmethod
    def set(name, val):
       MSESSION.conf[name] = val;
       
    @staticmethod
    def get(name):
        if name in MSESSION.conf:
            return MSESSION.conf[name];
        return None;

    @staticmethod
    def defined(name):
        if name in MSESSION.conf:
            return True;
        return False;

    @staticmethod
    def getDump():
        return json.dumps(MSESSION.conf, ensure_ascii=False);