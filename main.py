from os.path import exists
from tkinter import *
import pandas


BACKGROUND_COLOR = "#B1DDC6"
CARD_COLOR = "#91C2AF"

if exists("data/wrong_words.csv"):
    words_data = pandas.read_csv("data/wrong_words.csv")
else:
    words_data = pandas.read_csv("data/french_words.csv")
    with open("data/wrong_words.csv", "w") as file:
        df = pandas.DataFrame(columns=["French","English"])
        df.to_csv(file, index=False)

fr_word = "word"


def gen_word():
    global fr_word
    rand_row = words_data.sample()
    fr_word = rand_row.French.to_string(index=False)
    word.itemconfig(word_text, text=fr_word)


def flip_fr():
    gen_word()
    global fr_word
    card.itemconfig(card_image, image=card_front_img)
    word.itemconfig(word_text, text=fr_word, fill="black")
    word.config(bg="white")
    title.itemconfig(title_text, text="French", fill="black")
    title.config(bg="white")


def flip_eng():
    global fr_word
    card.itemconfig(card_image, image=card_back_img)
    row = words_data[words_data.French == fr_word]
    eng_word = row.English.to_string(index=False)
    word.itemconfig(word_text, text=eng_word, fill="white")
    word.config(bg=CARD_COLOR)
    title.itemconfig(title_text, text="English", fill="white")
    title.config(bg=CARD_COLOR)


def right_click():
    global words_data
    index = words_data.index[words_data.French == fr_word].to_list()
    words_data = words_data.drop(index=index)
    if len(words_data) > 0:
        flip_fr()
        window.after(3000, func=flip_eng)
    else:
        end_print()

def wrong_click():
    global words_data
    with open("data/wrong_words.csv", "a") as file:
        df = words_data[words_data.French == fr_word]
        df.to_csv(file, index=False, header=False)
    index = words_data.index[words_data.French == fr_word].to_list()
    words_data = words_data.drop(index=index)
    if len(words_data) > 0:
        flip_fr()
        window.after(3000, func=flip_eng)
    else:
        end_print()

def end_print():
    card.itemconfig(card_image, image=card_front_img)
    word.itemconfig(word_text, text="No more cards", fill="black")
    word.config(bg="white")
    title.itemconfig(title_text, text="", fill="black")
    title.config(bg="white")
    right_button.config(command="")
    wrong_button.config(command="")




window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

card = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_image = card.create_image(400, 263, image=card_front_img)
card.grid(column=0, row=0, columnspan=2, rowspan=4)

right_img = PhotoImage(file="images/right.png")

right_button = Button(image=right_img, width=100, height=100, compound="c",highlightthickness=0, borderwidth=0, command=right_click)
right_button.grid(column=0,row=5)

wrong_img= PhotoImage(file="images/wrong.png")

wrong_button = Button(image=wrong_img, width=100, height=99, compound="c",highlightthickness=0, borderwidth=0, command=wrong_click)
wrong_button.grid(column=1,row=5)

title = Canvas(width=600, height=100, bg="white", highlightthickness=0)
title_text = title.create_text(300, 50, text="", font=("Tahoma", 40, "italic"), anchor="center", fill="black")
title.grid(column=0, row=0, columnspan=2)

word = Canvas(width=600, height=100, bg="white", highlightthickness=0)
word_text = word.create_text(300, 50, text="Start", font=("Tahoma", 60, "bold"),anchor="center", fill="black")
word.grid(column=0, row=1, columnspan=2)

window.mainloop()