class token:

    def __init__(self,text,type,line):
        self.text = text
        self.type = type
        self.line = line
    
    def __str__(self):
        return str(self.type) + ":" + str(self.text)

class tokenizer:

    def __init__(self,text):
        self.queu = list(text)
        self.queu.reverse()
        self.state = "null"
        self.line = 0
        self.tokens = []
        self.nxt_chr = ""

    def tokenize(self):
        self.state_unknown(self.nxt())
        while(self.state != None):
            if self.state == "var":
                self.var(self.nxt_chr)
            if self.state == "ws":
                self.whitespace(self.nxt_chr)
            if self.state == "comment":
                self.comment(self.nxt_chr)
            if self.state == "str":
                self.string(self.nxt_chr)
        tokenList = []
        prev_newline = False
        for t in self.tokens:
            if prev_newline:
                if t.type != "nl":
                    prev_newline = False
                    tokenList.append(t)
            else:
                tokenList.append(t)
                if t.type == "nl":
                    prev_newline = True
        tokenList.append(token("EOF","EOF",self.line))
        return tokenList

    def nxt(self):
        if len(self.queu) == 0:return None
        next_char = self.queu.pop()
        if next_char == '\n':
            self.line += 1
        return next_char
    
    def state_unknown(self,next_char):
        self.nxt_chr = next_char
        if next_char == None:
            self.state = None
        elif next_char.isspace():
            self.state = "ws"
        elif next_char == "#":
            self.state = "comment"
        elif next_char == "\"":
            self.state = "str"
        else:
            self.state = "var"
        
    def whitespace(self,next_char):
        txt = []
        while next_char.isspace():
            txt.append(next_char)
            next_char = self.nxt()
            if(next_char == None):
                self.state_unknown(next_char)
                return
        if '\n' in txt:
            self.new_token("newline","nl")
        self.state_unknown(next_char)

    def comment(self,next_char):
        while next_char != '\n':
            next_char = self.nxt()
            if(next_char == None):
                self.state_unknown(next_char)
                return
        self.state_unknown(next_char)

    def string(self,next_char):
        next_char = self.nxt()
        is_escape = False
        escape_lookup = {'"':'"',"\\":"\\","n":"\n","t":"\t","b":"\b"}
        txt = []
        while True:
            if next_char == None:
                break
            if is_escape:
                if next_char in escape_lookup.keys():
                    txt.append(escape_lookup[next_char])
                is_escape = False
            else:
                if next_char == "\\":
                    is_escape = True
                elif next_char == "\"":
                    break
                else:
                    txt.append(next_char)
            next_char = self.nxt()
        self.new_token("".join(txt),"str")
        self.state_unknown(self.nxt())

    def new_token(self,text,type):
        if type != "str":
            text = text.upper()
        if type != "var":
            self.tokens.append(token(text,type,self.line))
        elif text != "":
            if (text[0].isdigit()) or (text[0] == '-'):
                self.tokens.append(token(text,"int",self.line))
            elif text[0] == ".":
                self.tokens.append(token(text,"l_addr",self.line))
            elif text[0] == "@":
                self.tokens.append(token(text,"g_addr",self.line))
            elif text[0] == "$":
                self.tokens.append(token(text,"var",self.line))
            else:
                self.tokens.append(token(text,"ins",self.line))

    def var(self,next_char):
        txt = []
        while True:
            if next_char == ",":
                if txt != []:
                    self.new_token("".join(txt),"var")
                self.new_token(",","comma")
                self.state_unknown(self.nxt())
                break
            elif next_char == None:
                if txt != []:
                    self.new_token("".join(txt),"var")
                self.state_unknown(next_char)
                break
            elif (next_char == "#") or next_char.isspace() or (next_char == "\""):
                if next_char == "\n":
                    self.line -=1
                if txt != []:
                    self.new_token("".join(txt),"var")
                if next_char == "\n":
                    self.line += 1
                self.state_unknown(next_char)
                break
            else:
                txt.append(next_char)
                next_char = self.nxt()

if __name__ == "__main__":
    with open("test.s",'r') as F:
        t = tokenizer(F.read())
        for tok in t.tokenize():
            print(tok)
