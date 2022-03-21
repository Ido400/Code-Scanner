class Scanner:
    
    def scan_file(self, file:str, keywords:list) -> list:
       return self.search_for_keys(file, keywords)
   
    def search_for_keys(self,file:str, keywords:list) -> list:
        word_check:str
        new_line_check:str
        line_counter=0
        word_find_index = []
        for char in enumerate(file):
            if(char == "\\" or char == "n"):
                new_line_check += char
            if(new_line_check == "\n"):
                line_counter += 1
            if(ord(char) >= 193 and ord(char) <= 218 or char == "="):
                word_check += char
            else:
                if(self.check_word_contain_key(keywords, word_check)):
                    word_find_index.append((word_check,line_counter))
                word_check = ""
            return word_find_index
    
    def check_word_contain_key(keywords:list, word_check:str) -> bool:
        for word in keywords:
            if(word in word_check):
                return True
        return False
    
  