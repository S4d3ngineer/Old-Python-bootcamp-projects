from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"
SCORE_FONT = ("Arial", 12)
QUESTION_FONT = ("Arial", 20, "italic")


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)
        self.window.title("Quizzler")

        self.label = Label(text=f"Score:", bg=THEME_COLOR, fg='white', font=SCORE_FONT)
        self.label.grid(column=1, row=0)

        self.canvas = Canvas(width=300, height=250, bg="white", highlightthickness=0)
        self.question_text = self.canvas.create_text(
            150,
            125,
            width=280,
            text="PLACEHOLDER",
            font=QUESTION_FONT
        )
        self.canvas.grid(column=0, row=1, columnspan=2, pady=50)

        self.green_button_img = PhotoImage(file="images/true.png")
        self.green_button = Button(image=self.green_button_img, highlightthickness=0, command=self.answer_yes)
        self.green_button.grid(column=0, row=2)

        self.red_button_img = PhotoImage(file="images/false.png")
        self.red_button = Button(image=self.red_button_img, highlightthickness=0, command=self.answer_no)
        self.red_button.grid(column=1, row=2)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            self.label.config(text=f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz!")
            self.green_button.config(state="disabled")
            self.red_button.config(state="disabled")

    def answer_yes(self):
        is_right = self.quiz.check_answer(user_answer="true")
        self.give_feedback(is_right)

    def answer_no(self):
        is_right = self.quiz.check_answer(user_answer="false")
        self.give_feedback(is_right)

    def give_feedback(self, is_right):
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000, func=self.get_next_question)
