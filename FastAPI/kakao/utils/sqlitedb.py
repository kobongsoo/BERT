#!pip install pysqlite
import sqlite3 as sq
import pandas as pd
#--------------------------------------------------------------------------------
# 호출 예시
# from utils import sqliteDB
# db=sqliteDB('kakao.db')
# 생성
# db.execute("CREATE TABLE user_mode (id text primary key, mode integer)") 
# 추가 리스트 여러개
# query = "INSERT INTO user_mode (id, mode) VALUES (?, ?)"
# data = [("6555cbd9cb76d42cb29078a4", 1), ("6555cbd9cb76d42cb29078a6", 2)]
# db.insert_list(query, data)
# 추가 1개
#id = "6555cbd9cb76d42cb29078a4"
#query = f"INSERT INTO user_mode (id, mode) VALUES ('{id}', 1)"
#db.execute(query)
# select
# query = "SELECT * FROM user_mode"
# df = db.select(query)
# print(df)
# 삭제 
#id = "6555cbd9cb76d42cb29078a4"
#query = f"DELETE FROM user_mode WHERE id = '{id}'"
#db.execute(query)
#--------------------------------------------------------------------------------
class SqliteDB:
    def __init__(self, dbname:str):
        assert dbname, f'dbname is empty'
        
        self.dbname = dbname
        
        # 연결할 때
        self.conn = sq.connect(self.dbname)
        
        # Cursor 객체 생성
        self.c = self.conn.cursor()
        #print("생성자 호출")
        
    def __del__(self):
        #print("종료 호출")
        if self.c:
            #print("self.c.close()")
            self.c.close()
            
        if self.conn:
            #print("self.conn.close()")
            self.conn.close()
     
      # SELECT * FROM user_mode WHERE id = 'uxssxxkd' => df로 리턴함
    def select(self, dbquery:str):
        df = pd.read_sql_query(dbquery, self.conn)
        return df
    
    def insert_list(self, dbquery:str, data:list):
        assert dbquery, f'dbquery is empty'
        assert len(data) > 0, f'data is empyt'
        
        error:int = 0
        try:
            self.c.executemany(dbquery, data)
            self.conn.commit()
            return error
        except Exception as e:
            print(f'[error]insert_list=>{e}')
            error = 1002
            self.conn.rollback()
            return
      
    # UPDATE user_mode SET mode = 1 WHERE id = 'uxssxxkd'
    # DELETE FROM user_mode WHERE id = 'uxssxxkd'
    def execute(self, dbquery:str):
        assert dbquery, f'dbquery is empty'
        
        error:int = 0
        try:
            self.c.execute(dbquery)
            self.conn.commit()
        except Exception as e:
            print(f'[error]execute: {dbquery}=>{e}')
            error = 1002
            self.conn.rollback()
            return
        
    def rollback(self):
        self.conn.rollback()
        
    def close(self):
        self.c.close()
        self.conn.close()
    #----------------------------------------------
    # user_mode 관련 
    # user_mode 테이블 : id 입력 시 해당 모드 출력 
    def select_user_mode(self, user_id:str):
        assert user_id, f'user_id is empty'
        
        dbquery = f"SELECT * FROM user_mode WHERE id='{user_id}'"
        df = pd.read_sql_query(dbquery, self.conn)
        if len(df) > 0:
            return df['mode'][0]
        else:
            return -1
        
    # user_mode 테이블 :id 있으면 mode 업데이트, 없으면 추가
    def insert_user_mode(self, user_id:str, user_mode:int):
        assert user_id, f'user_id is empty'
        assert user_mode > -1, f'user_mode is wrong'
        
        try:
            res = self.select_user_mode(user_id)
            if res == -1: # 없으면 추가
                dbquery = f"INSERT INTO user_mode (id, mode) VALUES ('{user_id}', {user_mode})"
            else: # 있으면 업데이트
                dbquery = f"UPDATE user_mode SET mode = {user_mode} WHERE id = '{user_id}'"

            self.c.execute(dbquery)
            self.conn.commit()
            return 0
        except Exception as e:
            print(f'insert_user_mode=>error:{e}')
            return 1001
        
    # user_mode 테이블 :해당 id 있으면 삭제
    def delete_user_mode(self, user_id:str):
        assert user_id, f'user_id is empty'
        res = self.select_user_mode(user_id)
        
        if res > -1: # 있으면 제거
            dbquery = f"DELETE FROM user_mode WHERE id = '{user_id}'"
            self.c.execute(dbquery)
            self.conn.commit()
        
    #----------------------------------------------    
    # setting 관련 
    # setting 테이블 : id 입력 시 해당 site(naver, google) 출력 
    # userdb.execute('CREATE TABLE setting(id TEXT, site TEXT, preanswer TEXT)')  # setting 테이블 생성
    def select_setting(self, user_id:str):
        assert user_id, f'user_id is empty'
        
        dbquery = f"SELECT * FROM setting WHERE id='{user_id}'"
        df = pd.read_sql_query(dbquery, self.conn)

        if len(df) > 0:
            #print(df['site'])
            
            response:dict={}
            response['id']=df['id'][0]
            response['site']=df['site'][0]
            response['preanswer']=df['preanswer'][0]
            return response
        else:
            return -1
        
    # search_site 테이블 :id 있으면 site 업데이트, 없으면 추가
    def insert_setting(self, user_id:str, site:str, preanswer:int):
        
        assert user_id, f'user_id is empty'
        assert site, f'site is empty'
        assert preanswer >=0, f'preanswer is wrong'
        
        try:
            res = self.select_setting(user_id)
            #print(f'[insert_setting]=>res:{res}')
            
            if res == -1: # 없으면 추가
                dbquery = f"INSERT INTO setting (id, site, preanswer) VALUES ('{user_id}', '{site}', {preanswer})"
            else: # 있으면 업데이트
                dbquery = f"UPDATE setting SET site='{site}', preanswer={preanswer} WHERE id = '{user_id}'"

            print(f'[insert_setting]=>dbquery:{dbquery}')
            self.c.execute(dbquery)
            self.conn.commit()
            return 0
        except Exception as e:
            print(f'insert_setting=>error:{e}')
            return 1001
   
    # search_site 테이블 :해당 id 있으면 삭제
    def delete_setting(self, user_id:str):
        assert user_id, f'user_id is empty'
        res = self.select_setting(user_id)
        
        if res != -1: # 있으면 제거
            dbquery = f"DELETE FROM setting WHERE id = '{user_id}'"
            self.c.execute(dbquery)
            self.conn.commit()
   #----------------------------------------------           
   
    