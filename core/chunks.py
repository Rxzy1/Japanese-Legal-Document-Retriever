class Chunks:
    def __init__(self,max_size):
        self.max_size = max_size
        self.chunk=[]
    def create_chunks(self,text:list) -> list:
        temp = []
        self.chunk = []
        count = 0
        for i in range(len(text)):
            temp.append(text[i])
            count+=1
            if text[i]=='。':
                self.chunk.append("".join(temp))
                temp = []
                count=0
            elif count==self.max_size:
                for j in range(len(temp)-1,-1,-1):
                    if temp[j]=="，" or temp[j]=="、":
                        leftover = temp[j+1:]
                        temp=temp[:j+1]
                        self.chunk.append("".join(temp))
                        temp = leftover
                        count = len(temp)
                        break
                else:
                    self.chunk.append("".join(temp))
                    temp = []
                    count=0
        if temp:
            self.chunk.append("".join(temp))
        return self.chunk





