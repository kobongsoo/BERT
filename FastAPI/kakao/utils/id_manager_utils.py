class IdManager:
    
    def __init__(self):
        self.id_list = []

    def add(self,user_id, user_mode):
        new_id = {'user_mode': user_mode, 'user_id': user_id}
        self.id_list.append(new_id)
        # print(f"ID {new_id} has been added.")

    def remove_id_all(self, user_id):  
        self.id_list = [item for item in self.id_list if item['user_id'] != user_id]

    def display_all(self):
        return self.id_list

    def check_id_exists(self, user_id): 
        return any(item['user_id'] == user_id for item in self.id_list)

    def get_user_mode(self, user_id):
        for item in self.id_list:
            if item['user_id'] == user_id:
                return item['user_mode']
        return None  # 해당 user_id에 대응하는 user_mode가 없을 경우 None 반환
    
    def update_user_mode(self, user_id, new_user_mode):
        for item in self.id_list:
            if item['user_id'] == user_id:
                item['user_mode'] = new_user_mode
                break  # 이미 찾았으니 더 이상 반복할 필요가 없음
        else:
            # for 문이 break 없이 종료됐을 경우 (즉, 해당 user_id를 찾지 못했을 경우)
            self.add(user_id, new_user_mode)
        