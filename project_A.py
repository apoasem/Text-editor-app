import tkinter.messagebox as messageBox
import  tkinter.colorchooser as colorChooser
from tkinter import *
from tkinter import filedialog
from tkinter import font
import codecs
import os
import re

mywindow = Tk()

mywindow.geometry("400x380")

mywindow.title("My Text Editor")

buttonframe = Frame()       # make frame

customFont = font.Font(family="Helvetica", size=8)

mytext = Text(mywindow, width=400, height=380, bd = 2, font= customFont)


buttonframe.pack(side="top", fill="x")

mytext.pack()


#################################################### main menu functions ##################################################################################

def encode_runlength(string):
    r = ""
    l = len(string)
    if l == 0:
        return ""
    if l == 1:
        return string + str(1)
    count = 1
    i = 1
    while i < l:
        if string[i] == string[i - 1]:
            count += 1
        else:
            r = r + string[i - 1] + str(count)
            count = 1
        i += 1
    r = r + string[i - 1] + str(count)
    return r



def new():
    ans = messageBox.askquestion(title="save file", message="would you like to save file")
    if ans == 'yes':
            save()
            delete_all()
    else:
        delete_all()


def delete_all():
    mytext.delete(1.0, END)




def decode_runlength(lst):
    q = ""
    for character, count in lst:
        q += character * count
    return q



############################################# huffman encode functions ######################################################

#text = 'abdfbcbedbabcfefbdddedbbfababc'

def build_huffman_tree(text):
	f = {}

	for char in text:
		if char in f:
			f[char] = f[char] + 1
		else:
			f[char] = 1

	ht = []
	for item in f.items():
		ht.append((item[0], item[1]))

	while len(ht) > 1:
		ht.sort(key=lambda item: item[1])
		new_node = (ht[0][0] + ht[1][0], ht[0][1] + ht[1][1], ht[0], ht[1])

		ht.pop(0)
		ht[0] = new_node
	return ht[0]


def encode_symbol(char, tree, code = []):
	if len(tree[0]) > 1:
		if char in tree[2][0]:
			code.append('0')
			return encode_symbol(char, tree[2], code)
		else:
			code.append('1')
			return encode_symbol(char, tree[3], code)
	elif tree[0] == char:
		return code
	else:
		raise Exception("Symbol '%c' is not in the tree" % char)

def encode_alphabet(alphabet, tree):
	encoding = {}
	for char in alphabet:
		encoding[char] = encode_symbol(char, tree, [])
	return encoding


def encode_message(text, table):
	code = []
	for char in text:
		code.extend(table[char])
	return ''.join(code)

############################################ huffman decode function #####################################################################



def decode_message(code,tree):
	tree_iter = tree
	message = ''
	for bit in code:
		tree_iter = tree_iter[2 if bit == '0' else 3]
		if len(tree_iter[0]) == 1:
			message = message + tree_iter[0]
			tree_iter = tree
	return message

#----------------------------------------------------------------------

def open():
    x = mytext.get('1.0', END + '-1c')
    if x != "":
        ans = messageBox.askquestion(title="save file", message="would you like to save file")
        if ans == 'yes':
            save_as()
            delete_all()
            pass
        else:
            delete_all()
            pass
    else:
        pass


    extensions = [('All files','*'),  ('Runlength files','*.rltxt'), ('Huffman files','*.huf'), ('text files','*.txt')]


    opmyfile = filedialog.askopenfile(parent=mywindow, mode='rb', title='Select a file', filetypes=extensions )
    if opmyfile != None:
        myfile_path = os.path.abspath(opmyfile.name)
        myfile = codecs.open(myfile_path,"rb", encoding="utf-8")

        if myfile != None:
            exe = myfile.name
            ex = exe.split(".")[-1]
            if ex == "RLTXT" or "rltxt":
                contents = myfile.read()
                vava = [(x[0],int(x[1])) for x in re.findall(r'(?:(\w+?)(\d+))+?',contents)] # read list of tuples from file
                mycontent = decode_runlength(vava)
                mytext.insert('1.0', mycontent)
                myfile.close()
            elif ex == "HUf" or "huf":
                # not working

                tree = build_huffman_tree("abdfbcbedbabcfefbdddedbbfababc")
                y = decode_message(myfile.read(),tree)
                mytext.insert('1.0', y)
                myfile.close()

            elif ex == "txt":
                contents = myfile.read()
                mytext.insert('1.0', contents)
            else:
                contents = myfile.read()
                mytext.insert('1.0', contents)



#--------------------------------------------------------


def save():
    extensions = [('Text files', '*.txt')]

    opmyfile = filedialog.asksaveasfile(mode='w', filetypes= extensions, defaultextension=".txt")
    if opmyfile != None:
        myfile_path = os.path.abspath(opmyfile.name)
        myfile = codecs.open(myfile_path,"w", encoding="utf-8")
        x = mytext.get('1.0', END + '-1c')

        myfile.write(x)
        myfile.close()



def save_as():
    extensions = [('txt files', '*.txt'), ('All files', '*')]
    opmyfile = filedialog.asksaveasfile(mode="w", title='please type file extension otherwise file will be saved as txt file', filetypes= extensions,defaultextension=".txt")
    if opmyfile != None:
        myfile_path = os.path.abspath(opmyfile.name)
        myfile = codecs.open(myfile_path, "rb", encoding="utf-8")

        if myfile != None:
            exe = myfile.name
            myfile_path = os.path.abspath(opmyfile.name)
            myfile = codecs.open(myfile_path, "w", encoding="utf-8")
            ex = exe.split(".")[-1]
            if ex == "rltxt":
                print("rltxt")
                myfile.write(encode_runlength(mytext.get('1.0', END + '-1c')))

            elif ex == "huf":
                print("HUF")
                tree = build_huffman_tree(mytext.get('1.0', END + '-1c'))
                table = encode_alphabet(tree[0], tree)
                code = encode_message(mytext.get('1.0', END + '-1c'), table)
                myfile.write(code)

            elif ex == "txt":
                print("txt")
                myfile.write((mytext.get('1.0', END + '-1c')))
            else:
                myfile.write((mytext.get('1.0', END + '-1c')))


def close():
    x = ""
    x = mytext.get('1.0', END + '-1c')
    if x != "":
        ans = messageBox.askquestion(title="save file", message="would you like to save file")
        if ans == 'yes':
                save()
                mywindow.quit()
        else:
            mywindow.quit()
    else:
        mywindow.quit()


#################################################### edit menu functions ##################################################################################

def choose_color():
    colorlist = colorChooser.askcolor()
    color_name = colorlist[1]  # to pick up the color name
    mytext.configure(fg=color_name)

def change_font_size(x):
    customFont.configure(size=x)

def change_font_style(x):
    customFont.configure(family=x)


def underline():
    customFont.configure(underline=True)

def font_bold():
    customFont.configure(weight='bold')

def italic_font():
    customFont.configure(slant='italic')

def normal():
    customFont.configure(slant='roman')
    customFont.configure(weight='normal')
    customFont.configure(underline=0)

############################################################ GUI of main menu ##############################################################################


# main menu bar
mymenu = Menu(mywindow)
mywindow.config(menu = mymenu)


#file menu
file_menu = Menu(mymenu)
file_menu=Menu(mymenu,tearoff=0)
mymenu.add_cascade(label="File", menu = file_menu)
file_menu.add_command(label="New", command=new)
file_menu.add_command(label="Open", command=open)
file_menu.add_separator()
file_menu.add_command(label="Save", command=save)
file_menu.add_command(label="Save As..",command=save_as)
file_menu.add_command(label="Close", command=close)






########################################################## GUI of edit menu #################################################################################

edit_menu = Menu(mymenu)

edit_menu=Menu(mymenu,tearoff=0)
mymenu.add_cascade(label="Edit", menu= edit_menu)

edit_menu.add_command(label="Choose color", command=choose_color)
edit_menu.add_command(label="delete all", command=delete_all)



# font size menu #

size_menu = Menu(mymenu)
size_menu=Menu(mymenu,tearoff=0)
mymenu.add_cascade(label="font size", menu = size_menu)

size_menu.add_command(label=10, command=lambda: change_font_size(10))
size_menu.add_command(label= 20, command=lambda:change_font_size(20))
size_menu.add_command(label= 30, command=lambda:change_font_size(30))
size_menu.add_command(label= 40, command=lambda:change_font_size(40))
size_menu.add_command(label= 50, command=lambda:change_font_size(50))
size_menu.add_command(label= 60, command=lambda:change_font_size(60))
size_menu.add_command(label= 70, command=lambda:change_font_size(70))
size_menu.add_command(label= 80, command=lambda:change_font_size(80))
size_menu.add_command(label= 90, command=lambda:change_font_size(90))
size_menu.add_command(label= 100,command=lambda:change_font_size(100))



# font style menu


font_menu = Menu(mymenu)
font_menu=Menu(mymenu,tearoff=0)
mymenu.add_cascade(label="font style", menu = font_menu)


font_menu.add_command(label= "Arial", command=lambda:change_font_style("Arial"))
font_menu.add_command(label= "CENTURY", command=lambda:change_font_style("CENTURY"))
font_menu.add_command(label= "Corbel", command=lambda:change_font_style("Corbel"))
font_menu.add_command(label= "Consolas", command=lambda:change_font_style("Consolas"))
font_menu.add_command(label= "Tahoma", command=lambda:change_font_style("Tahoma"))
font_menu.add_command(label= "MTCORSVA", command=lambda:change_font_style("MTCORSVA"))

font_menu.add_separator()

font_menu.add_command(label= "aldhabi", command=lambda:change_font_style("aldhabi"))
font_menu.add_command(label= "andlso", command=lambda:change_font_style("andlso"))




bold = Button(mywindow, text ="bold", command = font_bold)

bold.pack( in_=buttonframe ,side = "right")
italic = Button(mywindow, text ="Italic", command = italic_font)

italic.pack( in_=buttonframe ,side = "right")
under_line = Button(mywindow, text ="underline", command = underline)

under_line.pack( in_=buttonframe ,side = "right")
under_line = Button(mywindow, text ="Normal", command = normal)

under_line.pack( in_=buttonframe ,side = "right")

#---------------------------------


mywindow.mainloop()