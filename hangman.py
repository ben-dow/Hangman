from tkinter import *
from processword import *

class App:
    def __init__(self,master):
        '''
        Hangman Variable Initiate
        '''

        self.filestorage = Files('dictionary.txt')
        self.hangman = None
        '''
        Initiate Frame
        '''
        frame = Frame(master)
        frame.pack(padx=10,pady=10)

        '''
        Initiate Canvas
        '''
        self.hangman_canvas = Canvas(frame,width=100,height=100)
        self.hangman_canvas.grid(row=0,column=0,rowspan=10)

        '''
        Structure
        '''
        self.hangman_canvas.create_line(20,5,20,80)
        self.hangman_canvas.create_line(20,5,50,5)
        self.hangman_canvas.create_line(50,5,50,25)
        self.hangman_canvas.create_line(0,80,40,80)


        '''
        Body
        '''
        self.head = self.hangman_canvas.create_oval(40,25,60,35, state=HIDDEN)
        self.body = self.hangman_canvas.create_line(50,35,50,55, state=HIDDEN)
        self.arm_l = self.hangman_canvas.create_line(50,38,45,50, state = HIDDEN)
        self.arm_r = self.hangman_canvas.create_line(50,38,55,50, state = HIDDEN)
        self.leg_l = self.hangman_canvas.create_line(50,55,45,70, state = HIDDEN)
        self.leg_r = self.hangman_canvas.create_line(50,55,55,70, state = HIDDEN)

        '''
        Empty Letters Field
        '''
        self.wordlbl = Label(frame, text="Word:")
        self.wordlbl.grid(row=0,column=1)

        self.wordlen= Label(frame,text='( )')
        self.wordlen.grid(row=0,column=2)

        self.word = Text(frame,height = 1, width=30)
        self.word.grid(row=0,column=3)
        self.message = 'Click "Reset" to begin'
        self.word.insert(END,self.message)
        self.word.config(state=NORMAL,width=len(self.message))

        '''
        Used Letters
        '''

        self.usedlbl = Label(frame, text="Used Letters:")
        self.usedlbl.grid(row=1,column=1)

        self.used = Text(frame,height = 1,width=len(self.message), state=DISABLED)
        self.used.grid(row=1,column=3)

        '''
        Guess
        '''

        self.guess = Text(frame,height = 1, width=2)
        self.guess.grid(row=2,column=1)

        self.guessbtn = Button(
                        frame,
                        text="Guess Letter",
                        command = lambda: self.guess_process(self.guess.get(1.0))
                        )
        self.guessbtn.grid(row=2,column=3)


        '''
        Reset
        '''

        self.reset = Button(
                        frame,
                        text="Reset Game",
                        command = self.resetgame
                        )
        self.reset.grid(row=3,column=2)

        '''
        Wins and Losses
        '''
        self.wins = 0
        self.loss = 0
        self.wins_display = Label(frame,text='Wins: 0')
        self.wins_display.grid(row=3, column = 3)
        self.losses_display = Label(frame,text='Losses: 0')
        self.losses_display.grid(row=4,column=3)


    def resetgame(self):
        '''
        Resets the Game. Selects a New Word
        '''
        self.clear_display(self.used)
        self.clear_display(self.word)
        self.clear_display(self.guess)
        self.guess.config(state=NORMAL)
        self.hangman = Hangman(self.filestorage.determineWord())
        self.word.config(width=len(self.hangman.word))
        self.wordlen.config(text='(' + str(len(self.hangman.word)) + ')')
        self.hangman_canvas.itemconfig(self.head,state=HIDDEN)
        self.hangman_canvas.itemconfig(self.body,state=HIDDEN)
        self.hangman_canvas.itemconfig(self.arm_l,state=HIDDEN)
        self.hangman_canvas.itemconfig(self.arm_r,state=HIDDEN)
        self.hangman_canvas.itemconfig(self.leg_l,state=HIDDEN)
        self.hangman_canvas.itemconfig(self.leg_r,state=HIDDEN)
        print(self.hangman.word)
        print(self.hangman.wordindex)
    def guess_process(self,guess):
            if guess in self.hangman.guess_display:
                self.clear_display(self.guess)
                self.guess.config(state=NORMAL)
                return
            self.clear_display(self.guess)
            self.guess.config(state=NORMAL)
            exist = self.hangman.processGuess(guess)
            if exist == True:
                self.hangman.build_word(guess)
                self.clear_display(self.word)
                self.word.config(state=NORMAL)
                self.word.insert(END,''.join(self.hangman.word_display))
                self.word.config(state=DISABLED)

            else:
                self.used.config(state=NORMAL)
                self.used.insert(END,guess)
                self.used.config(state=DISABLED)
                if self.hangman.guesses_wrong == 1:
                    self.hangman_canvas.itemconfig(self.head,state=NORMAL)
                elif self.hangman.guesses_wrong == 2:
                    self.hangman_canvas.itemconfig(self.body,state=NORMAL)
                elif self.hangman.guesses_wrong == 3:
                    self.hangman_canvas.itemconfig(self.arm_l,state=NORMAL)
                elif self.hangman.guesses_wrong == 4:
                    self.hangman_canvas.itemconfig(self.arm_r,state=NORMAL)
                elif self.hangman.guesses_wrong == 5:
                    self.hangman_canvas.itemconfig(self.leg_l,state=NORMAL)
                elif self.hangman.guesses_wrong == 6:
                    self.hangman_canvas.itemconfig(self.leg_r,state=NORMAL)
                else:
                    self.clear_display(self.guess)
                    self.clear_display(self.used)
                    self.used.config(state=NORMAL)
                    self.used.insert(END,'You Ran Out of Guesses')
                    self.used.config(state=DISABLED)
                    self.clear_display(self.word)
                    self.word.config(state=NORMAL)
                    self.word.insert(END,self.hangman.word)
                    self.word.config(state=DISABLED)
                    self.loss += 1
                    self.losses_display.config(text='Losses: ' + str(self.loss))
            print(''.join(self.hangman.word_display).upper())
            if ''.join(self.hangman.word_display).upper() == self.hangman.word.strip().upper():
                self.clear_display(self.used)
                self.used.config(state=NORMAL)
                self.used.insert(END,'You Win!')
                self.used.config(state=DISABLED)
                self.geuss.config(state=DISABLED)
                self.wins += 1
                self.wins_display.config(text='Wins: ' + str(self.wins))
    def clear_display(self,display):
        display.config(state=NORMAL)
        display.delete(1.0,END)
        display.config(state=DISABLED)


root = Tk()
app = App(root)
root.title("Hangman")
root.mainloop()
