from csv import excel

from sudachipy import Dictionary,SplitMode

class Sudachi:
    def __init__(self):
        self.tokenizer_obj = Dictionary(dict="full").create()
        self.mode = SplitMode.C
        self.text = ""
    def token_words(self, text: str) -> list:
        if not text:
            return []
            # Split into manageable segments by newline/paragraph
        segments = [s for s in text.split('\n') if s.strip()]
        all_tokens = []
        for segment in segments:
        # Sudachi's hard limit is ~49149 chars, stay safe
          for i in range(0, len(segment), 40000):
            chunk = segment[i:i+40000]
            tokens = self.tokenizer_obj.tokenize(chunk, self.mode)
            all_tokens.extend([t.surface() for t in tokens if t.surface().strip()])
        return all_tokens

