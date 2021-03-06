#!/usr/bin/python3
from Author import Author
from tkinter import *
from citation_parser import ParserScholar

class Parser_GUI ():


 fields = 'Name', 'Surname'

def fetch(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()
      print('%s: "%s"' % (field, text))

def makeform(root, fields):
   entries = []
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries
root = Tk()
ents = makeform(root, Parser_GUI.fields)
root.bind('<Return>', (lambda event, e=ents: fetch(e)))
text = Text(root)
text.pack()
b1 = Button(root, text='Is Upgrade',
command=(lambda e=ents: fetch(e)))
#scholar=ParserScholar('Ecir Uğur','Küçüksille')
b1.pack(side=LEFT, padx=5, pady=5)
b2 = Button(root, text='Show Quotes', command=text.insert(INSERT,scholar.get_quotes))
b2.pack(side=LEFT, padx=5, pady=5)
b3 = Button(root, text='Show Writers', command=text.insert(INSERT,scholar.get_author_writers))
b3.pack(side=LEFT, padx=5, pady=5)
b4 = Button(root, text='Show Writings', command=text.insert(INSERT,scholar.get_author_writings))
b4.pack(side=LEFT, padx=5, pady=5)
b5 = Button(root, text='Show Author Bibliography', command=text.insert(INSERT,scholar.get_parsed_bib_text_data_author))
b5.pack(side=LEFT, padx=5, pady=5)
b6 = Button(root, text='Exit Program', command=root.quit)
b6.pack(side=LEFT, padx=5, pady=5)
root.mainloop()
#quotes_list= scholar.get_quotes()


root.mainloop()

