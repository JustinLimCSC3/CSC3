import tkinter as tk
from tkinter import font, messagebox
import random

class CountryQuizApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Country Quiz")
        self.state("zoomed")  # Start maximized

        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="Gaegu", size=12)

        self.user_age = None  # Initialize user age

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.current_question = 0

        # Define and create frames for different pages
        for F in (AgePage, MainPage, QuizPage, ResultsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(AgePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def set_user_age(self, age):
        self.user_age = age

    def show_results(self, correct_answers, total_questions):
        self.frames[ResultsPage].update_results(correct_answers, total_questions)
        self.show_frame(ResultsPage)

# AgePage: Get user's age
class AgePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title_font = font.Font(family="Gaegu", size=20, weight="bold")
        title_label = tk.Label(self, text="Welcome to Country Quiz!", font=title_font)
        title_label.pack(pady=30)

        label_font = font.Font(family="Gaegu", size=16)
        self.age_label = tk.Label(self, text="Please enter your age:", font=label_font)
        self.age_label.pack(pady=10)

        self.age_entry = tk.Entry(self, font=label_font)
        self.age_entry.pack(pady=10)

        button_font = font.Font(family="Gaegu", size=14)
        self.continue_button = tk.Button(self, text="Continue", font=button_font, command=self.check_age)
        self.continue_button.pack(pady=20)

    def check_age(self):
        try:
            age = int(self.age_entry.get())
            if 0 <= age <= 100:
                self.controller.set_user_age(age)
                self.controller.show_frame(MainPage)
            else:
                messagebox.showerror("Invalid Age", "Please enter an age between 0 and 100.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid age.")

# MainPage: Start the quiz
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title_font = font.Font(family="Gaegu", size=20, weight="bold")
        title_label = tk.Label(self, text="Country Quiz", font=title_font)
        title_label.pack(pady=30)

        button_font = font.Font(family="Gaegu", size=16)
        self.start_button = tk.Button(self, text="Start Quiz", command=self.start_quiz, font=button_font, padx=20, pady=15, bd=2, highlightbackground="black")
        self.start_button.pack(pady=20)

        self.exit_button = tk.Button(self, text="Exit", command=self.controller.quit, font=button_font, padx=20, pady=15, bd=2, highlightbackground="black")
        self.exit_button.pack(pady=10)

    def start_quiz(self):
        self.controller.show_frame(QuizPage)

# ResultsPage: Display quiz results
class ResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title_font = font.Font(family="Gaegu", size=18, weight="bold")
        self.title_label = tk.Label(self, text="Results", font=title_font)
        self.title_label.pack(pady=30)

        self.result_label = tk.Label(self, text="", font=("Gaegu", 14))
        self.result_label.pack(pady=10)

        self.back_button = tk.Button(self, text="Back to Main Menu", font=("Gaegu", 14), command=self.back_to_main_menu)
        self.back_button.pack(pady=10)

        self.exit_button = tk.Button(self, text="Exit", font=("Gaegu", 14), command=self.controller.quit)
        self.exit_button.pack(pady=10)

    def update_results(self, correct_answers, total_questions):
        self.result_label.config(text=f"You got {correct_answers} out of {total_questions} questions correct.")

    def back_to_main_menu(self):
        self.controller.current_question = 0  # Reset question index
        self.controller.show_frame(MainPage)

# QuizPage: Display and manage quiz questions
class QuizPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title_font = font.Font(family="Gaegu", size=18, weight="bold")
        title_label = tk.Label(self, text="Quiz", font=title_font)
        title_label.pack(pady=30)

        self.questions = [
            {"question": "What is the largest continent?", "answers": ["Asia", "Africa", "Europe", "Oceania"], "correct": "Asia"},
            {"question": "What is the smallest continent?", "answers": ["Oceania", "Africa", "North America", "Antarctica"], "correct": "Oceania"},
            {"question": "What continent has the most countries?", "answers": ["Africa", "South America", "Europe", "Asia"], "correct": "Africa"},
            {"question": "This country is known for its ancient pyramids", "answers": ["Egypt", "Brazil", "India", "Russia"], "correct": "Egypt"},
            {"question": "This 'boot-shaped' country is known for its Colosseum and leaning tower.", "answers": ["Italy", "France", "Spain", "China"], "correct": "Italy"},
            {"question": "With the highest population in the world, this country is known for its Great Wall.", "answers": ["China", "USA", "Japan", "Mexico"], "correct": "China"}
        ]

        self.correct_answers = 0
        self.current_question_idx = -1
        self.total_questions = len(self.questions)

        self.question_label = tk.Label(self, text="", font=("Gaegu", 16))
        self.question_label.pack()

        self.answer_buttons = [tk.Button(self, text="", font=("Gaegu", 14), command=lambda idx=i: self.check_answer(idx)) for i in range(4)]
        self.button_indices = [0, 1, 2, 3]
        self.shuffle_buttons()

        self.next_button = tk.Button(self, text="Next", font=("Gaegu", 14), command=self.next_question, state=tk.DISABLED)

        self.show_question(0)

    def shuffle_buttons(self):
        random.shuffle(self.button_indices)

    def show_question(self, question_idx):
        self.current_question_idx = question_idx
        question_number = question_idx + 1
        question = self.questions[question_idx]

        self.question_label.config(text=f"Question {question_number}: {question['question']}")
        self.shuffle_buttons()

        for i, button_index in enumerate(self.button_indices):
            answer = question["answers"][button_index]
            self.answer_buttons[i].config(text=answer)
            self.answer_buttons[i].pack(pady=5)

        self.next_button.pack_forget()

    def check_answer(self, answer_idx):
        question = self.questions[self.current_question_idx]
        selected_answer = question["answers"][self.button_indices[answer_idx]]
        if selected_answer == question["correct"]:
            self.correct_answers += 1
        self.next_question()

    def next_question(self):
        self.controller.current_question += 1
        if self.controller.current_question < self.total_questions:
            self.show_question(self.controller.current_question)
        else:
            self.controller.show_results(self.correct_answers, self.total_questions)

if __name__ == "__main__":
    app = CountryQuizApp()
    app.mainloop()
