__author__ = 'zhou'

"""Token_Type = [
    'ORIGIN', 'SCALE', 'ROT', 'IS', 'TO',  # 保留字
    'STEP', 'DRAW', 'FOR', 'FROM',  # 保留字
    'T',  # 参数
    'SEMICO', 'L_BRACKET', 'R_BRACKET', 'COMMA',  # 分隔符号
    'PLUS', 'MINUS', 'MUL', 'DIV', 'POWER',  # 运算符
    'FUNC',  # 函数
    'CONST_ID',  # 常数
    'NONTOKEN',  # 空记号
    'ERRTOKEN'
]"""
# print(Token_Type[1])

class Token:
	def __init__(self, type, lexeme, value, func):
		self.type = type
		self.lexeme = lexeme
		self.value = value
		self.func = func


PI = Token('CONST_ID', "PI", 3.1415926, "")
E = Token('CONST_ID', "E", 2.71828, "")
T = Token('T', "T", 0.0, "")
SIN = Token('FUNC', "SIN", 0.0, 'sin')
COS = Token('FUNC', "COS", 0.0, 'cos')
TAN = Token('FUNC', "TAN", 0.0, 'tan')
LN = Token('FUNC', "LN", 0.0, 'log')
EXP = Token('FUNC', "EXP", 0.0, 'exp')
SQRT = Token('FUNC', "SQRT", 0.0, 'sqrt')
ORIGIN = Token('ORIGIN', "ORIGIN", 0.0, "")
SCALE = Token('SCALE', "SCALE", 0.0, "")
ROT = Token('ROT', "ROT", 0.0, "")
IS = Token('IS', "IS", 0.0, "")
FOR = Token('FOR', "FOR", 0.0, "")
FROM = Token('FROM', "FROM", 0.0, "")
TO = Token('TO', "TO", 0.0, "")
STEP = Token('STEP', "STEP", 0.0, "")
DRAW = Token('DRAW', "DRAW", 0.0, "")

Token_Tab = [PI, E, T, SIN, COS, TAN, LN, EXP, SQRT, ORIGIN, SCALE, ROT,IS,FOR, FROM, TO, STEP, DRAW]

'''for i in Token_Tab:
	print(i.type,i.lexeme,i.value,i.func)
'''
'''TokenTab=[
	['CONST_ID',"PI",	3.1415926,""],
	['CONST_ID',"E",2.71828,""]
	['T',"T",0.0,""],
	['FUNC',		"SINz",		0.0,		'sin'],
	['FUNC',		"COS",		0.0,		'cos'],
	['FUNC',		"TAN",		0.0,		'tan'],
	['FUNC',		"LN",		0.0,		'log'],
	['FUNC',		"EXP",		0.0,		'exp'],
	['FUNC',		"SQRT",		0.0,		'sqrt'],
	['ORIGIN',	"ORIGIN",	0.0,		""],
	['SCALE',		"SCALE",	0.0,		""],
	['ROT',		"ROT",		0.0,		""],
	['IS',		"IS",		0.0,		""],
	['FOR',		"FOR",		0.0,		""],
	['FROM',		"FROM",		0.0,		""],
	['TO',		"TO",		0.0,		""],
	['STEP',		"STEP",		0.0,		""],
	['DRAW',		"DRAW",		0.0,		""]
	]
'''

LineNo = 0
TOKEN_LEN = 100
#f = open(file_name,'r')
str=""
str_buffer = []
str_i = 0
f=None
def test(now,char):
	global LineNo,str,str_buffer,str_i
	print('local:',now,'char:',char,'str:',str,' len(str):',len(str),' str_buffer:',str_buffer,' str_i:',str_i)


def InitScanner(file_name):
	try:
		global f
		f=open(file_name, 'r')
		global str
		str=f.read()
		global str_i
		str_i=0
		global LineNo
		LineNo=0
		return 1
	except:
		print('Open error!')
		raise
def CloseScanner():
	global f
	f.close()
def GetChar():
	global str_i
	global str
	#print('len:',len(str))
	#print(str_i)
	if str_i<len(str):
		char= str[str_i]
		#print(str[str_i])
	else :
		char=''
	str_i += 1
	#if str_i>len(str):
	#	return ''
	#print("char:",char)
	return char
def BackChar():
	global str_i
	str_i -= 1
def AddCharTokenString(char):
	global str_buffer
	str_buffer.append(char)
def EmptyTokenString():
	global str_buffer
	str_buffer.clear()
def JudgeKeyToken(IDstring):
	for i in range(len(Token_Tab)):
		#print("ID:",IDstring,'TOKEN:',Token_Tab[i].lexeme)
		if IDstring.upper()==Token_Tab[i].lexeme:
			return Token_Tab[i]
	errorToken=Token('ERRORTOKEN',''.join(str_buffer),0,"")
	return errorToken
def GetToken():
	EmptyTokenString();
	token_lexeme=''.join(str_buffer)
	while True:
		char=GetChar()
		#test('1',char)
		if(char==''):
			#print('nontoken')
			token_type='NONTOKEN'
			token=Token(token_type,token_type,0,'')
			#print(token)
			return token
		elif char=='\n':
			#print('huiche')
			global LineNo
			LineNo+=1
		elif char!=' ':
			#print("back ")
			break
	AddCharTokenString(char)
	#print(str_buffer)
	if(char.isalpha()):
		#print('isalpha')
		while True:
			char=GetChar()
			#test('2',char)

			global str_i
			#print(str_i)
			#print(char)
			if char.isalnum():
				AddCharTokenString(char)
				#print(str_buffer)
			else :
				break
		BackChar()
		token_lexeme=''.join(str_buffer)
		token=JudgeKeyToken(token_lexeme)
		#print(token)
		return token
	elif char.isdigit():
		while True:
			char=GetChar()
			#test('3',char)
			#print('char:',char)
			if char=='.':
				AddCharTokenString(char)
			elif char.isdigit():
				AddCharTokenString(char)
				#print(str_buffer)
			else :
				break
		BackChar()
		token_lexeme="".join(str_buffer)
		#print(token_lexeme)
		import string
		token_value=float(token_lexeme)
		#print(token_value)
		token=Token('CONST_ID',token_lexeme,token_value,'')
		return token
	else:

		if  char==';':
			token=Token('SEMICO',';',0,'')
			return token
		elif char=='(':
			token=Token('L_BRACKET',char,0,'')
			return token
		elif char==')':
			token=Token('R_BRACKET',char,0,'')
			return token
		elif char==',':
			token=Token('COMMA',char,0,'')
			return token
		elif char=='+':
			token=Token('PLUS',char,0,'')
			return token
		elif char=='-':
			char = 	GetChar()
			if char=='-':
				while char!='\n' and char!='':
					char=GetChar()
				BackChar()
				return GetToken()
			else:
				BackChar()
				token=Token('MINUS','-',0,'')
				return token
		elif char=='/':
			char = 	GetChar()
			if char=='-':
				while char!='\n' and char!='':
					char=GetChar()
				BackChar()
				return GetToken()
			else:
				BackChar()
				token=Token('DIV','/',0,'')
				return token
		elif char=='*':
			char=GetChar()
			if char=='*':
				token=Token('POWER','**',0,'')
				return token
			else:
				BackChar();
				token=Token('MUL','*',0,'')
				return token
		else:
			token=Token('ERRORTOKEN',''.join(str_buffer),0,'')
			return token

def main():
	InitScanner('test.txt')
	CloseScanner()
	print('-'*50)
	print("   记号类别     字符串     常数值       函数指针")
	while True:
		token=GetToken()
		if token.type!=	'NONTOKEN':
			print("%10s"%token.type,"%10s"%token.lexeme,"%10s"%token.value,"%10s"%token.func)
			print('hanghao:',LineNo)
		else:
			break
	print('-'*50)

#main()

#print(str)
'''print(len(str))
for i in range(len(str)):
	AddCharTokenString(GetChar())
print(str_buffer)
string="".join(str_buffer)
print(string)
EmptyTokenString()
print(str_buffer)
'''

'''for i in range(len(str)):
	AddCharTokenString(GetChar())
print(str_buffer)
string="".join(str_buffer)
print(string)
class2=JudgeKeyToken(string)
print(class2.type,class2.lexeme,class2.value,class2.func)'''

'''class1=GetToken()
print(class1.type,class1.lexeme,class1.value,class1.func)
class2=GetToken()
print(class2.type,class2.lexeme,class2.value,class2.func)
class3=GetToken()
print(class3.type,class3.lexeme,class3.value,class3.func)
class3=GetToken()
print(class3.type,class3.lexeme,class3.value,class3.func)'''
















