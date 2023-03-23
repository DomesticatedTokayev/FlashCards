import tkinter
import tkinter.ttk
from tkinter import *
import pandas
import random
import os
import json

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"

front_side = True

random_word = ""
current_card = {}
words_dic = []

remaining_questions = 0
total_questions = 0

canClick = False

# Check if save file (Words to learn exists)
def get_words_to_learn():
    global words_dic, current_language, remaining_questions, total_questions

    #1leng = {}
    data_frame = {}
    try:
        data_frame = pandas.read_csv(f"data/{current_language.lower()}_words_to_learn.csv")
    except FileNotFoundError:
        data_frame = pandas.read_csv(f"data/{current_language.lower()}_words.csv")
        data_frame.to_csv(f"data/{current_language.lower()}_words_to_learn.csv", index=False)
    else: # Not great: Find a better solution
        pass
    finally:
        lenght = pandas.read_csv(f"data/{current_language.lower()}_words.csv")
        leng = lenght.to_dict(orient="records")
        total_questions = len(leng)

        words_dic = data_frame.to_dict(orient="records")
        remaining_questions = len(words_dic)


def save_word():
    global words_dic, current_card, current_language, remaining_questions

    if remaining_questions > 0:
        try:
            words_dic.remove(current_card)
        except TypeError:
            print("Key not found")
        else:
            data = pandas.DataFrame(words_dic)
            data.to_csv(f"data/{current_language.lower()}_words_to_learn.csv", index=False)
            remaining_questions -= 1
    else:
        window.after_cancel(flip_timer)
        canvas.itemconfig(card_word, text="All questions answered, Reset to start again")


def flip_card():
    global current_card, canClick

    # Create actual values to prevent repetition
    # Ok not great: When buttons are hidden, the screen resolution also changes
    # unknown_button.grid(column=0, row=2)
    # known_button.grid(column=1, row=2)

    canClick = True
    # if front_side:
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(card_word, text=current_card["English"])
    canvas.itemconfig(card, image=back_card_img)
    canvas.itemconfig(card_title, fill="white")
    canvas.itemconfig(card_word, fill="white")


def next_card():
    global random_word, flip_timer, current_card, words_dic, current_language, canClick, remaining_questions

    canClick = False

    # unknown_button.grid_forget()
    # known_button.grid_forget()
    # Some of this code can go into its own function (There is some repetition)
    if remaining_questions == 0:
        window.after_cancel(flip_timer)

        d_frame = pandas.read_csv(f"data/{current_language.lower()}_words.csv")
        d_frame.to_csv(f"data/{current_language.lower()}_words_to_learn.csv", index=False)
        words_dic = d_frame.to_dict(orient="records")
        remaining_questions = len(words_dic)

        canvas.itemconfig(card_title, text=current_language)
        canvas.itemconfig(num_of_cards, text=f"{remaining_questions}/{total_questions}")

    current_card = random.choice(words_dic)

    canvas.itemconfig(card_title, text=current_language)
    canvas.itemconfig(card_word, text=current_card[current_language])
    canvas.itemconfig(card, image=front_card_img)
    canvas.itemconfig(num_of_cards, text=f"{remaining_questions}/{total_questions}")
    canvas.itemconfig(card_title, fill="black")
    canvas.itemconfig(card_word, fill="black")

    window.after_cancel(flip_timer)
    flip_timer = window.after(3000, func=flip_card)


def skip():
    #if canClick:
    next_card()


def correct():
    #if canClick:
    save_word()
    next_card()


def reset_language_cards():
    global current_language

    window.after_cancel(flip_timer)
    if os.path.exists(f"data/{current_language.lower()}_words_to_learn.csv") and os.path.isfile(f"data/{current_language.lower()}_words_to_learn.csv"):
        os.remove(f"data/{current_language.lower()}_words_to_learn.csv")
        get_words_to_learn()
        next_card()


def select_language(event):
    global current_language
    window.after_cancel(flip_timer)
    current_language = language_Selection.get()
    print(current_language)
    get_words_to_learn()
    next_card()

# If not, create and save words to learn on it
# If it exists, remove words from list when user names word correctly
window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

front_card_img = PhotoImage(file="images/card_front.png")
back_card_img = PhotoImage(file="images/card_back.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card = canvas.create_image(400, 263, image=front_card_img)
card_title = canvas.create_text(400, 158, text="title", fill="black", font=(FONT_NAME, 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", fill="black", font=(FONT_NAME, 60, "bold"))
num_of_cards = canvas.create_text(400, 20, text=f"{remaining_questions}/{total_questions}", fill="black", font=(FONT_NAME, 20, "italic"))
canvas.grid(column=0, row=1, columnspan=2)

n = tkinter.StringVar()
language_Selection = tkinter.ttk.Combobox(width=10, state="readonly")
language_Selection['values'] = ('French', "Italian", "Slovenian", "Spanish", "Polish")
language_Selection.current(0)
language_Selection.bind("<<ComboboxSelected>>", select_language)
language_Selection.grid(column=0, row=0, pady=10)

# Save this into json or something
current_language = language_Selection.get()

reset_button = Button(width=10, text="Reset", command=reset_language_cards)
reset_button.grid(column=1, row=0)

cross_image = PhotoImage(file="images/wrong.png", )
unknown_button = Button(image=cross_image, command=skip, highlightthickness=0)
unknown_button.grid(column=0, row=2)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, command=correct, highlightthickness=0)
known_button.grid(column=1, row=2)

get_words_to_learn()

next_card()

window.mainloop()


