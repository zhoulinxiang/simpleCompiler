from tkinter import *
'''
root=Tk()
root.title('Drawing Example')
canvas=Canvas(root,width=200,height=160,bg='white')
canvas.create_line(10,10,100,70)
canvas.create_line(10,10,40,10)
canvas.create_line(40,10,40,40)
canvas.create_line(10,40,40,40)
canvas.pack()
root.mainloop()'''

from tkinter import *
root = Tk()
# 创建一个Canvas，设置其背景色为白色
cv = Canvas(root,bg = 'white')
#cv.create_rectangle(100,200,100,200)
a=(100,100)
cv.create_bitmap(a)
for i in range(100,200,1):
    pass
    #print(i)
    #cv.create_line(i,100,i+1,100)
    #cv.create_oval((i,100,i,100))

cv.pack()
root.mainloop()