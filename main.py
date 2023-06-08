from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
timer = None
current_card = {}
to_learn = {}


def new_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(canvas_img, image=card_img)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=current_card["French"], fill="black")
    print(current_card["French"])
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_img, image=card_back)


def is_know():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    new_word()


# grabbing info from the CSV and putting it to lists
try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

window = Tk()
window.title("Flash Card Project")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

# Lists to store the right and wrong answers
words_known = []
words_unknown = []

# ----------------------UI Set up----------------------------#

# Create canvas for the flash card and text
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_img = PhotoImage(file="./images/card_front.png")
canvas_img = canvas.create_image(400, 263, image=card_img)
title_text = canvas.create_text(400, 150, text="Title", font=("ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="Word", font=("ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# save images
right_img = PhotoImage(file="./images/right.png")
wrong_img = PhotoImage(file="./images/wrong.png")
card_back = PhotoImage(file="./images/card_back.png")
card_front = PhotoImage(file="./images/card_front.png")

# Buttons
right_button = Button(text="Right", image=right_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=is_know)
right_button.grid(column=1, row=1)

wrong_button = Button(text="Wrong", image=wrong_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=new_word)
wrong_button.grid(column=0, row=1)

new_word()

window.mainloop()
