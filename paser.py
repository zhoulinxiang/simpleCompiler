__author__ = 'zhou'
import scanner
from math import *
token=None
Parameter=0
Origin_x,Origin_y=0,0
Scale_x,Scale_y=1,1
Rot_angle=0

from tkinter import *
root = Tk()
# 创建一个Canvas，设置其背景色为白色
cv = Canvas(root,bg = 'white', height=500, width=800)

class ExprNode:
    def __init__(self,type,first=None,second=None,third=None,fourth=None):
        self.type=type
        if type=='PLUS' or type=='MINUS' or type=='MUL' or type=='DIV' or type=='POWER':
            self.left=first
            self.right=second
        elif type=='FUNC':
            self.child=first
            self.func=second
        elif type=='CONST_ID':
            self.caseconst=first
        elif type=='T':
            self.t=first
def MakeExprNode(type,first=None,second=None):
    if type=='PLUS' or type=='MINUS' or type=='MUL' or type=='DIV' or type=='POWER':
        node=ExprNode(type,first,second)
    elif type=='FUNC':
        node=ExprNode(type,first,second)
    elif type=='CONST_ID':
        node=ExprNode(type,first)
    elif type=='T':
        node=ExprNode(type,first)
    return node
def PrintSyntaxTree(root,indent):
    pass
    for temp in range(indent-1):
        print('\t',end='')
    #print(root.type)
    if root.type=='PLUS':
        print("+")
    elif root.type=='MINUS':
        print('-')
    elif root.type=='MUL':
        print('*')
    elif root.type=='DIV':
        print('/')
    elif root.type=='POWER':
        print('**')
    elif root.type=='FUNC':
        print(root.func)
    elif root.type=='CONST_ID':
        print(root.caseconst)
    elif root.type=='T':
        print('T')
    else:
        print('Error Tree Node!')
        exit()
    if root.type=='CONST_ID' or root.type=='T':
        return
    if root.type=='FUNC':
        PrintSyntaxTree(root.child,indent+1)
    else:
        PrintSyntaxTree(root.left,indent+1)
        PrintSyntaxTree(root.right,indent+1)
def Tree_trace(x):
    PrintSyntaxTree(x,1)
def enter(x):
    pass
    #print('enter in: ',x)
def back(x):
    pass
    #print('exit in: ',x)
def call_match(x):
    pass
   # print('matchtoken: ',x)
def ErrorMessage(line,descripe,string):
    pass
def SyntaxError(error):
    if error==1:
        global token
        print('第',scanner.LineNo+1,"行错误记号:",token.lexeme)
    elif error==2:
        print('第',scanner.LineNo+1,"行不是预期符号:",token.lexeme)
def FetchToken():
    global token
    token=scanner.GetToken()
    #print('toke.type token.value:',token.type,' ',token.value)
    if token.type=="ERRORTOKEN":
        SyntaxError(1)
def MatchToken(token_type):
    global token
    if token.type!=token_type:
        SyntaxError(2)
    FetchToken()
def Program():
    enter("Program")
    while(token.type!='NONTOKEN'):
        Statement();
        MatchToken('SEMICO')
    back('program')
def Statement():
    enter('Statement')
    if token.type=='ORIGIN':
        OriginStatement()
    elif token.type=='SCALE':
        ScaleStatement()
    elif token.type=='ROT':
        RotStatement()
    elif token.type=='FOR':
        ForStatement()
    else:SyntaxError(2)
    back("Statement")
def OriginStatement():
    enter("OriginStatement")
    MatchToken('ORIGIN')
    MatchToken('IS')
    MatchToken('L_BRACKET')
    tmp=Expression()
    global Origin_x
    Origin_x=GetExprValue(tmp)
    MatchToken('COMMA')
    tmp=Expression()
    global Origin_y
    Origin_y=GetExprValue(tmp)
    MatchToken('R_BRACKET')
    back('OriginStatement')
def ScaleStatement():
    enter('ScaleStatement')
    MatchToken("SCALE")
    MatchToken("IS")
    MatchToken("L_BRACKET")
    tmp=Expression()
    global Scale_x
    Scale_x=GetExprValue(tmp)
    MatchToken('COMMA')
    tmp=Expression()
    global Scale_y
    Scale_y=GetExprValue(tmp)
    MatchToken('R_BRACKET')
    back('ScaleStatement')
def RotStatement():
    enter('RotStatement')
    MatchToken('ROT')
    MatchToken("IS")
    tmp=Expression()
    global Rot_angle
    Rot_angle=GetExprValue(tmp)
    back('RotStatement')
def ForStatement():
    enter('ForStatement')
    MatchToken('FOR')
    call_match('FOR')
    MatchToken('T')
    call_match("T")
    MatchToken('FROM')
    call_match('FROM')
    start_ptr=Expression()
    start=GetExprValue(start_ptr)
    #print('start:',start)
    MatchToken('TO')
    call_match("TO")
    end_ptr=Expression()
    end=GetExprValue(end_ptr)
    #print('end;',end)
    MatchToken("STEP")
    call_match("STEP")
    step_ptr=Expression()
    step=GetExprValue(step_ptr)
    #print('step:',step)
    MatchToken("DRAW")
    call_match("DRAW")
    MatchToken('L_BRACKET')
    call_match('(')
    x_ptr=Expression()
    MatchToken('COMMA')
    call_match(',')
    y_ptr=Expression()
    MatchToken('R_BRACKET')
    call_match(')')
    DrawLoop(start,end,step,x_ptr,y_ptr)
    back('FORSTATEMENT')
def Expression():
    enter("Expression")
    left=Term()
    while  token.type=='PLUS' or token.type=='MINUS':
        token_tem=token.type
        MatchToken(token_tem)
        right=Term()
        left=MakeExprNode(token_tem,left,right)
    #print(left)
    if left.type!='T':
        Tree_trace(left)
    back('Expression')
    return left
def Term():
    enter('Term')
    left=Factor()
    #global token
    #print(token.type)
    while token.type=='MUL' or token.type=='DIV':
        token_tmp=token.type
        MatchToken(token_tmp)
        right=Factor()
        left=MakeExprNode(token_tmp,left,right)
    back('Term')
   # print('term:',left)
    return left
def Factor():
    enter('Factor')
    #print('factor;',token.type)
    if token.type=='PLUS':
        MatchToken('PLUS')
        right=Factor()
    elif token.type=='MINUS':
        MatchToken('MINUS')
        right=Factor()
        left=ExprNode('CONST_ID',0)
        right=MakeExprNode('MINUS',left,right)
    else:
        right=Component()
    back('Factor')
    #print('factor:',right)
    return right
def Component():
    enter('Component')
    left=Atom()
    if token.type=='POWER':
        MatchToken('POWER')
        right=Component()
        left=MakeExprNode('POWER',left,right)
    back('Component')
    #print('component:',left)
    return left
def Atom():
    enter('Atom')
    t=token
    #print('atom:',token.type)
    if token.type=='CONST_ID':
        #print(token.type,token.value)
        MatchToken("CONST_ID")
        #print(t.type,t.value)
        address=MakeExprNode('CONST_ID',t.value)
        #print('atom,if,address:',address)
    elif token.type=='T':
        MatchToken('T')
        address=MakeExprNode('T',Parameter)
    elif token.type=='FUNC':
        MatchToken('FUNC')
        MatchToken('L_BRACKET')
        tmp=Expression()
        #print(tmp,'+',t.value,t.type,t.lexeme)
        address=MakeExprNode('FUNC',tmp,t.lexeme)
        MatchToken('R_BRACKET')
    elif token.type=='L_BRACKET':
        MatchToken('L_BRACKET')
        address=Expression()
        MatchToken('R_BRACKET')
    else:
        SyntaxError(2)
    back('Atom')
    #print('Atom:',address)
    return address
def Paser(SrcFile):
    enter('Paser')
    if scanner.InitScanner(SrcFile)!=1:
        print('Open file Error')
        return ;
    FetchToken()
    Program()
    scanner.CloseScanner()
    back('Parser')
def DrawPixel(x,y):
    cv.create_line(x,x,y,y)
def GetExprValue(root):
    #print('root:',root)
    #print('root.type',root.type)


    if root.type==None:
        #print('root.value','none')
        return 0
    if root.type=='PLUS':
        return  GetExprValue(root.left)+GetExprValue(root.right)
    elif root.type=='MINUS':
        return GetExprValue(root.left)-GetExprValue(root.right)
    elif root.type=='MUL':
        return GetExprValue(root.left)*GetExprValue(root.right)
    elif root.type=='DIV':
        return GetExprValue(root.left)/GetExprValue(root.right)
    elif root.type=='POWER':
        return GetExprValue(root.left)**GetExprValue(root.right)
    elif root.type=='FUNC':
        if root.func=='SIN':
            return  sin(GetExprValue(root.child))
        elif root.func=='COS':
            return  cos(GetExprValue(root.child))
        elif root.func=='SQRT':
            return sqrt(GetExprValue(root.child))
        elif root.func=='EXP':
            return exp(GetExprValue(root.child))
        elif root.func=='LN':
            pass
            #print('child:',GetExprValue(root.child))
            #return log(GetExprValue(root.child))

    elif root.type=='T':
        #print('root.value.t',Parameter)
        return Parameter
    elif root.type=='CONST_ID':
        #print('root.value.const;',root.caseconst)
        return root.caseconst
    else:return 0
def DrawLoop(start,end,step,horptr,verptr):
    #print('start end step:',start,' ',end,' ',step )
    global Parameter
    Parameter=start
    #for Parameter in range(float(start),float(end),float(step)):
    while(Parameter<=end):
        #print('Parameter:',Parameter)
        x=CalcCoord(horptr,verptr,0,0)[0]
        y=CalcCoord(horptr,verptr,0,0)[1]
        #print('x,y;',x,y)
        cv.create_line(x,y,x+1,y)
        Parameter+=step
def CalcCoord(hor_exp,ver_exp,hor_x,hor_y):
    #print('hor_exp:',hor_exp)
    horcord=GetExprValue(hor_exp)
   #print('horcord:',horcord)
    vercord=GetExprValue(ver_exp)
    global Scale_x
    horcord*=Scale_x
    vercord*=Scale_y
    hor_tem=horcord*cos(Rot_angle)+vercord*sin(Rot_angle)
    vercord=vercord*cos(Rot_angle)-horcord*sin(Rot_angle)
    horcord=hor_tem
    horcord+=Origin_x
    vercord+=Origin_y
    hor_x=horcord
    hor_y=vercord
    #print('hor_x,hor_y;',hor_x,hor_y)
    return[hor_x,hor_y]



Paser('test.txt')
cv.pack()
root.mainloop()

