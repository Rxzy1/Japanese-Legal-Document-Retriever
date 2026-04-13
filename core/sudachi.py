

from sudachipy import Dictionary,SplitMode

class Sudachi:
    def __init__(self):
        self.tokenizer_obj = Dictionary(dict="full").create()
        self.mode = SplitMode.C
    def token_words(self,text:str) -> list:
        if not text:
            return []
        tokens = self.tokenizer_obj.tokenize(text,self.mode)
        return [t.surface() for t in tokens if t.surface().strip()]

