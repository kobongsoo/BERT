
# gpu site에 대한 subclass 
# PHP의 경우 각 클래스별로 subclass를 개발하였으나,
# python의 모듈이라는 개념을 활용하여 하나의 파일에 subclass들을 모두 작성하도록 한다. 

from pympower.classes.mutility import MUtility


class GPU_MUtility(MUtility):
    
    def __init__(self, powerdb_con: "MpowerDB2" = None):
        super().__init__(powerdb_con);
        
    def subClassTest(self):
        return "Sub Class";            
