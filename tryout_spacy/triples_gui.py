from tkinter import *
from tkinter import filedialog
from sys import exit
import spacy
from random import choice


# function for loading text from file
def open_file():
    global text_data # can it be done without global ?
    file_in = filedialog.askopenfilename(title="Select a file", # load file, some general file extensions
                                         filetypes=(("Text files", "*.txt"),
                                                    ("JSON files", "*.json"),
                                                    ("all files", "*.*")))
    if file_in: # if file is selected, person may cancel file selection
        # clear text box, load new text into the box, close file
        text_field.delete('1.0', END)
        text_file = open(file_in, "r", encoding="utf-8")
        text = text_file.read()
        text_field.insert(END, text)
        text_file.close()
        text_data = text


# function for saving data to file
def save_file():
    dots = [('json', '*.json'), ("Text file", "*.txt")]
    out_file = filedialog.asksaveasfilename(title='Save file', filetypes=dots,
                                            defaultextension='.json',initialfile ='Untitled')
    if out_file: # check if saving is canceled
        out_file = open(out_file, 'w') # create new file
        data = text_field.get('1.0', END) # take data
        out_file.write(data) # write data
        out_file.close() # close file


def run_parse(): # take the text in the text box and run POS, add all unique nous to a list, return this list
    global text_data
    if len(text_data) == 0: # get text in text box, check if it wasn't been done
        text_data = text_field.get('1.0', END)

    nlp = spacy.load("en_core_web_sm") # load spacy English small model
    doc = nlp(text_data)
    noun_set = []

    for token in doc:
        if token.pos_ == "NOUN" and token.lemma_ not in noun_set:
            noun_set.append(token.lemma_) # add nouns to list

    status_bar.config(text='Parsed')
    return noun_set


def run_triples(): # take the noun list and generate list of triples
    nouns = run_parse()
    predicate_set = ["is", "is_not", "has", "has_not"] # naive predicate set
    triples = []
    for i in range(len(nouns)): # random choice of all elements, do it once for every noun
        # may be added option for loop through every noun with every predicate and every obj
        candidate_subj = choice(nouns)
        candidate_predicate = choice(predicate_set)
        candidate_obj = choice(nouns)
        if candidate_obj != candidate_subj: # check if subj and obj are different
            triple = f"{candidate_subj} {candidate_predicate} {candidate_obj}" # make triple
            triples.append(triple) # add triple to list

    text_field.delete('1.0', END) # clear text box
    text = '\n'.join(triples)
    text_field.insert(END, text) # show triples list in text box

# initiate tkinter, add geometry
root = Tk()
root.title('Triple Generator - in English')
app_w = 1280
app_h = 720
# take screen resolution
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
# place the gui in the centre of screen
x = (screen_w // 2) - (app_w // 2)
y = (screen_h // 2) - (app_h // 2)
root.geometry(f'{app_w}x{app_h}+{x}+{y-30}')

text_data = ''

# frames
top_frame = Frame(root)
top_frame.pack(pady=5, padx=5)

# scrollbar
text_scroll = Scrollbar(root)
text_scroll.pack(side=RIGHT, fill=Y)

# text box
text_field = Text(root, font=('ariel', 16))
text_field.pack(expand=True, fill=BOTH, padx=5)
text_scroll.config(command=text_field.yview)

# status bar - changes once, doesn't change if text in text box is changed
status_bar = Label(root, text='Ready', anchor=W)
status_bar.pack(padx=5, pady=5, fill=X)

# buttons
button1 = Button(top_frame, text='Open', command=open_file)
button1.pack(side=LEFT)
button4 = Button(top_frame, text='Parse', command=run_parse)
button4.pack(side=LEFT, padx=5)
button2 = Button(top_frame, text='Generate Triples', command=run_triples)
button2.pack(side=LEFT)
button3 = Button(top_frame, text='Save', command=save_file)
button3.pack(side=LEFT, padx=5)
btn_exit = Button(top_frame, text="Close", command=exit)
btn_exit.pack(side=RIGHT, padx=20)

root.mainloop()
