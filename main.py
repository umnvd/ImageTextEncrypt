from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo

from coder import encode
from coder import decode


def fill_file_entry():
    file_entry.delete(0, END)
    file_entry.insert(0, askopenfilename(filetypes=(('image files', '*.png  *.bmp'), ('all files', '*.*'))))


def encode_text():
    validation()
    file_name = file_entry.get()
    key = key_entry.get()
    text = text_box.get('1.0', END).strip()
    if not text:
        showerror(title='Ошибка', message='Введите текст')
        return
    encode(file_name, key, text)
    showinfo(title='Выполнено', message='Кодирование завершено')


def decode_image():
    validation()
    file_name = file_entry.get()
    key = key_entry.get()
    text = decode(file_name, key)
    text_box.delete('1.0', END)
    text_box.insert('1.0', text)
    showinfo(title='Выполнено', message='Декодирование завершено')


def validation():
    if not file_entry.get():
        showerror(title='Ошибка', message='Выберите файл')
    elif not key_entry.get():
        showerror(title='Ошибка', message='Введите ключ')


root = Tk()
root.title('T2I')
root.geometry('400x200')
root.resizable(width=False, height=False)

file_frame = Frame(master=root)
file_frame.place(width=185, x=5, y=5)
file_label = Label(master=file_frame, text='Файл')
file_label.pack(side=TOP, anchor=NW)
file_entry = Entry(master=file_frame, text='Выберите файл..')
file_entry.pack(expand=True, side=LEFT, fill=X)
browse_btn = Button(master=file_frame, text='Просмотр', command=fill_file_entry)
browse_btn.pack(side=RIGHT)

key_frame = Frame(master=root)
key_frame.place(width=185, x=5, y=60)
key_label = Label(master=key_frame, text='Ключ')
key_label.pack(side=TOP, anchor=NW)
key_entry = Entry(master=key_frame, text='Введите ключ..')
key_entry.pack(expand=True, fill=BOTH)

encode_btn = Button(master=root, text='Кодировать', command=encode_text)
encode_btn.place(width=185, x=5, y=120)
decode_btn = Button(master=root, text='Декодировать', command=decode_image)
decode_btn.place(width=185, x=5, y=160)


text_box = Text(master=root)
text_box.place(heigh=190, width=195, x=200, y=5)

root.mainloop()
