from tokens import *

class Lexer:
    def __init__(self, source):
        self.tokens = []
        self.source = source
        self.start = 0
        self.curr = 0
        self.line = 1

    def advance(self):
        ch = self.source[self.curr]
        self.curr = self.curr + 1
        return ch
    
    def peek(self):
        if self.curr >= len(self.source):
            return "\0"
        return self.source[self.curr]
    
    def lookahead(self, n=1):
        if self.curr >= len(self.source):
            return "\0"
        return self.source[self.curr + n]
    
    def match(self, expected):
        if self.curr >= len(self.source):
            return False
        if self.source[self.curr] != expected:
            return False
        self.curr = self.curr + 1 #consumes that char
        return True

    def handle_number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == "." and self.lookahead().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
            self.add_token(TOK_FLOAT)
        else:
            self.add_token(TOK_INTEGER)

    def handle_string(self, start_quote):
        while self.peek() != start_quote and self.curr < len(self.source):
            self.advance()
        if self.curr >= len(self.source):
            raise SystemError(f"[Line {self.line}] Unterminated string")
        self.advance()
        self.add_token(TOK_STRING)

    def handle_identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        text = self.source[self.start:self.curr]
        keyword_type = keywords.get(text)

        if keyword_type == None:
            self.add_token(TOK_IDENTIFIER)
        
        else:
            self.add_token(keyword_type)


    
    def add_token(self, token_type):
        self.tokens.append(Token(token_type, self.source[self.start:self.curr], self.line))

    def tokenize(self):
        while self.curr < len(self.source):
            self.start = self.curr
            ch = self.advance()

            if ch == "\n": self.line = self.line + 1
            elif ch == "\ ": pass
            elif ch == "\t": pass
            elif ch == "\r": pass
            
            elif ch == "(": self.add_token(TOK_LPAREN)
            elif ch == ")": self.add_token(TOK_RPAREN)
            elif ch == "{": self.add_token(TOK_LCURLY)
            elif ch == "}": self.add_token(TOK_RCURLY)
            elif ch == "[": self.add_token(TOK_LSQUAR)
            elif ch == "]": self.add_token(TOK_RCURLY)
            elif ch == ".": self.add_token(TOK_DOT)
            elif ch == ",": self.add_token(TOK_COMMA)
            elif ch == "+": self.add_token(TOK_PLUS)
            elif ch == "-":
                if self.match("-"):
                    while self.peek() != "\n" and self.curr < len(self.source):
                        self.advance()
                else:
                    self.add_token(TOK_MINUS)
            elif ch == "*": self.add_token(TOK_STAR)
            elif ch == "^": self.add_token(TOK_PLUS)
            elif ch == "/": self.add_token(TOK_SLASH)
            elif ch == ";": self.add_token(TOK_SEMICOLON)
            elif ch == "?": self.add_token(TOK_QUESTION)
            elif ch == "%": self.add_token(TOK_MOD)
            # two chat tokens
            elif ch == "=":
                if self.match("="):
                    self.add_token(TOK_EQ)
            elif ch == "~":
                if self.match("="):
                    self.add_token(TOK_NE)
                else:
                    self.add_token(TOK_NOT)

            elif ch == "<":
                if self.match("="):
                    self.add_token(TOK_LE)
                else:
                    self.add_token(TOK_LT)
            elif ch == ">":
                if self.match("="):
                    self.add_token(TOK_GE)
                else:
                    self.add_token(TOK_GT)
            elif ch == ":":
                if self.match("="):
                    self.add_token(TOK_ASSIGN)
                else:
                    self.add_token(TOK_COLON)
            elif ch == '"' or ch == '\'':
                self.handle_string(ch)
            elif ch.isdigit():
                self.handle_number()
            elif ch.isalpha() or ch == '_':
                self.handle_identifier()
            else:
                raise SyntaxError(f"[Line {self.line}] Error at {ch}: unexpected character.")
            
                
        return self.tokens
        