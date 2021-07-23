from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.pyplot import *
from tkinter import *
import apriori as ap
import mplcursors


class Dashboard:

    def __init__(self, combination, min_support, min_confidence, from_date, to_date):
        self.combination = combination
        self.min_support = float(min_support)
        self.min_confidence = float(min_confidence)
        self.from_date = str(from_date)
        self.to_date = str(to_date)
        self.screen = Tk()
        self.sales_date = list()
        self.sales_total = list()
        self.sales_chart_data = None
        self.database = None
        self.dict_database = dict()

    def database_product_value(self):
        for i in self.database:
            self.dict_database[i[0]] = [i[2], i[3]]


    def apriori(self):
        for i in self.screen.winfo_children():
            if str(i) != '.!frame':
                i.destroy()

        s = Scrollbar(self.screen)
        window = Text(self.screen, height = 580, width=1050)
        s.pack(side=RIGHT, fill=Y)
        window.pack()
        s.config(command=window.yview)
        window.config(yscrollcommand=s.set)

        temp = ap.Apriori()
        temp.from_to(self.from_date, self.to_date)
        temp.aprioriiteration(self.combination, self.min_support, self.min_confidence)
        self.database = temp.database_file
        self.database_product_value()
        temp1 = temp.int_to_string()
        self.sales_chart_data = temp.goods_sale_with_date
        window.insert(END,temp1)

    def profit_chart(self):
        for i in self.screen.winfo_children():
            if str(i) != '.!frame':
                i.destroy()

        temp = dict()
        for i in self.sales_chart_data:
            if i[0] in temp:
                temp[i[0]].extend([self.dict_database[int(j)][0] for j in i[1:]])
            else:
                temp[i[0]] = [self.dict_database[int(j)][0] for j in i[1:]]
        for i in temp.keys():
            temp[i] = sum(temp[i])
        window1 = self.screen
        fig = Figure(figsize = (15, 5), dpi = 100)
        fig.suptitle('From {} TO {}'.format(self.from_date, self.to_date))
        plot1 = fig.add_subplot(111)
        # list(temp.keys())
        plot1.plot(list(temp.values()), 'o-')
        canvas = FigureCanvasTkAgg(fig,master = window1)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas,  window1)
        toolbar.update()
        canvas.get_tk_widget().pack()

    def pie_chart(self):
        for i in self.screen.winfo_children():
            if str(i) != '.!frame':
                i.destroy()
        temp = dict()
        for i in self.sales_chart_data:
            for j in i[1:]:
                if 1 <= int(j) <=5:
                    if 'Food' in temp:
                        temp['Food'] += int(j)
                    else:
                        temp['Food'] = int(j)

                if 6 <= int(j) <=10:
                    if 'Drinks' in temp:
                        temp['Drinks'] += int(j)
                    else:
                        temp['Drinks'] = int(j)

                if 11 <= int(j) <=15:
                    if 'Chocolates' in temp:
                        temp['Chocolates'] += int(j)
                    else:
                        temp['Chocolates'] = int(j)

                if 16 <= int(j) <=21:
                    if 'Cleaning' in temp:
                        temp['Cleaning'] += int(j)
                    else:
                        temp['Cleaning'] = int(j)


        fig = matplotlib.figure.Figure(figsize=(15, 5))
        fig.suptitle('From {} TO {}'.format(self.from_date, self.to_date))
        ax = fig.add_subplot(111)
        ax.pie(list(temp.values()))
        ax.legend(list(temp.keys()))

        circle=matplotlib.patches.Circle( (0,0), 0.6, color='white')
        ax.add_artist(circle)

        window= self.screen
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().pack()
        canvas.draw()
        window.mainloop()

    def sales_chart(self):
        for i in self.screen.winfo_children():
            if str(i) != '.!frame':
                i.destroy()

        temp = dict()
        for i in self.sales_chart_data:
            if i[0] in temp:
                temp[i[0]].extend([self.dict_database[int(j)][1] for j in i[1:]])
            else:
                temp[i[0]] = [self.dict_database[int(j)][1] for j in i[1:]]

        for i in temp.keys():
            temp[i] = sum(temp[i])

        window1 = self.screen
        fig = Figure(figsize = (15, 5), dpi = 100)
        fig.suptitle('From {} TO {}'.format(self.from_date, self.to_date))
        plot1 = fig.add_subplot(111)
        # list(temp.keys()),
        plot1.plot(list(temp.values()), 'o-')
        mplcursors.cursor(plot1)

        canvas = FigureCanvasTkAgg(fig,master = window1)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas,  window1)
        toolbar.update()
        canvas.get_tk_widget().pack()

    def main_screen(self):
        self.screen.title('Dashboard')
        self.screen.geometry('1050x580')
        self.screen.config(background='snow')
        main = Frame(self.screen)
        main.pack(side='left', fill='both')
        main.config(background="#358597")

        Button(main, text='Product Recommendation', width=23, bg='snow', command=self.apriori).grid(padx=10, pady=10)
        Button(main, text='Sales Chart', width=23, bg='snow', command=self.sales_chart).grid(padx=10, pady=10)
        Button(main, text='Profit Chart', width=23, bg='snow', command=self.profit_chart).grid(padx=10, pady=10)
        Button(main, text='Predict Sales Chart', width=23, bg='snow').grid(padx=10, pady=10)
        Button(main, text='Pie Chart', width=23, bg='snow',command=self.pie_chart).grid(padx=10, pady=10)

        self.screen.mainloop()


if __name__ == '__main__':
    d = Dashboard(3, 6, 25, '1/02/2020', '4/02/2020')
    d.main_screen()