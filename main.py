from tkinter import *
from tkcalendar import *
import dashboard as db


class Main:

    def __init__(self):
        self.screen = Tk()
        self.from_data = StringVar()
        self.to_data = StringVar()
        self.combination = IntVar()
        self.min_support = StringVar()
        self.min_confidence = StringVar()

    def nextwindow(self):
        self.screen.destroy()
        temp = db.Dashboard(self.combination.get(), self.min_support.get(), self.min_confidence.get(), self.from_data.get(), self.to_data.get())
        temp.main_screen()

    def calender_window(self, text):
        screen2 = Toplevel(self.screen)
        screen2.geometry('230x130')
        Label(screen2, text='').pack()
        Label(screen2, text='Select Date').pack()
        data = DateEntry(screen2, date_pattern='dd/mm/yyyy')
        data.pack()

        def setvalue():
            if text == 'first':
                self.from_data.set(data.get())
                self.from_date = data.get()
                screen2.destroy()
            else:
                self.to_data.set(data.get())
                self.to_date = data.get()
                screen2.destroy()

        Label(screen2, text='').pack()
        Button(screen2, text='Change', width=10, command=setvalue).pack()

    def main_screen(self):
        self.screen.geometry('500x350')
        self.screen.title('Smart profitable solutions using Recommendation Framework')
        self.screen.config(bg='white smoke')

        Label(self.screen, width='500', text='Please enter details below', bg='#358597', fg='snow').pack()
        Label(self.screen, text='From :', width='10', bg='white smoke').place(x=50, y=40)
        Entry(self.screen, textvariable=self.from_data).place(x=150, y=40)
        Button(text='Select date', height='0', bg='grey99', fg='black', command=lambda: self.calender_window('first')).place(x=320, y=35)

        Label(self.screen, text='TO :', height='1', width='10', bg='white smoke').place(x=50, y=90)
        Entry(self.screen, textvariable=self.to_data).place(x=150, y=90)
        Button(text='Select date', bg='grey99', fg='black', command=lambda: self.calender_window('second')).place(x=320, y=85)

        Label(self.screen, text='Combination :', height='1', width='10', bg='white smoke').place(x=50, y=140)
        Entry(self.screen, textvariable=self.combination).place(x=150, y=140)

        Label(self.screen, text='Minsupport :', height='1', width='10', bg='white smoke').place(x=50, y=190)
        Entry(self.screen, textvariable=self.min_support).place(x=150, y=190)

        Label(self.screen, text='Minconfidence :', height='1', width='12', bg='white smoke').place(x=50, y=240)
        Entry(self.screen, textvariable=self.min_confidence).place(x=150, y=240)

        Button(text='Next', height='1', width='15', bg='grey99', fg='black', command=self.nextwindow).place(x=180, y=300)

        self.screen.mainloop()


if __name__ == '__main__':
    t = Main()
    t.main_screen()


