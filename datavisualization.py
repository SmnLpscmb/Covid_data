#Author: Simon Lesné

# Creating a GUI interface to visualize Covid data

from tkinter import *
import sqlite3
import numpy as np
import matplotlib.pyplot as plt 

root = Tk()
root.title('COVID-19 Data')
root.iconbitmap('D:/Simon/Python/Tkinter/basic_icon.ico')
conn = sqlite3.connect('covid-19.db')
c = conn.cursor()

top_frame = Frame(root, width=500, height=250, padx=20, pady=20)
top_frame.grid(row=0, sticky="EW", padx=20, pady=20)
bottom_frame = Frame(root, width=500, height=300, padx=20, pady=20)
bottom_frame.grid(row=1, sticky="EW", padx=20, pady=20)

title = Label(top_frame, text='Le Bilan, calmement...', pady=20, padx=40)
title.config(font=("Courier", 20))
title.grid(row=0, column=0, columnspan=5)

def add_entry():
    conn = sqlite3.connect('covid-19.db')
    c = conn.cursor()
    c.execute("SELECT total_deaths, total_cases FROM covid ORDER BY oid DESC LIMIT 1;")
    numbers = c.fetchall()
    prev_deaths, prev_cases = numbers[0][0], numbers [0][1]
    c.execute("INSERT INTO covid VALUES (:month, :day, :deaths, :tot_deaths, :cases, :tot_cases)",
            {
                'month': add_month_entry.get(),
                'day': int(add_day_entry.get()),
                'deaths': int(add_deaths_entry.get()),
                'tot_deaths': prev_deaths + int(add_deaths_entry.get()),
                'cases': int(add_cases_entry.get()),
                'tot_cases': prev_cases + int(add_cases_entry.get())
            })
    add_month_entry.delete(0, END)
    add_day_entry.delete(0, END)
    add_deaths_entry.delete(0, END)
    add_cases_entry.delete(0, END)
    conn.commit()
    conn.close()

def show(value, sec_value):    
    conn = sqlite3.connect('covid-19.db')
    c = conn.cursor()
    if sec_value == 'Deaths':
        c.execute("SELECT oid, total_deaths, new_deaths, month, date FROM covid ORDER BY oid")
        values = c.fetchall()
        subject = 'deaths'
    elif sec_value == 'Cases':
        c.execute("SELECT oid, total_cases, new_cases, month, date FROM covid ORDER BY oid")
        values = c.fetchall()
        subject = 'cases'  
    x_days = [x[3][:3]+str(x[4]) for x in values]
    if value == 'Graph':
        y_deads = [y[1] for y in values]
        plt.figure('Graph')
        plt.clf()
        plt.ylim(0, max(y_deads)*1.1)
        plt.plot(x_days, y_deads, label='Total ' + subject + ' over time')
        plt.xticks(x_days[::7])
        plt.ylabel(subject.capitalize())
        plt.xlabel('Days')
        plt.legend(loc='upper left')
        plt.title('Un joli graph')
        plt.show()
    elif value == 'Histogram':
        y_deads = [y[2] for y in values]
        plt.figure('Histogram')
        plt.clf()
        days = x_days
        deaths = y_deads
        ypos = np.arange(len(days))
        plt.xticks(ypos[::7], days[::7])
        plt.bar(ypos, deaths)
        plt.grid(True)
        plt.ylabel(subject.capitalize())
        plt.xlabel('Days')
        plt.title('Un bel histogramme')
        plt.show()
    conn.commit()
    conn.close()

def show_table():
    top = Toplevel()
    top.title("Another window")
    top.iconbitmap('D:/Simon/Python/Tkinter/basic_icon.ico')
    conn = sqlite3.connect('covid-19.db')
    c = conn.cursor()
    c.execute("SELECT * FROM covid")
    records = c.fetchall()
    months = []
    for record in records:
        months.append(record[0])
    my_set = set(months)
    counter_one = 0
    for value in my_set:
        month_label = Label(top, text='Month', padx=5, borderwidth=2, relief="solid")
        date_label = Label(top, text='Date', padx=5, borderwidth=2, relief="solid")
        deaths_label = Label(top, text='Deaths', padx=5, borderwidth=2, relief="solid")
        tot_deaths__label = Label(top, text='Total Deaths', padx=5, borderwidth=2, relief="solid")
        cases_label = Label(top, text='Cases', padx=5, borderwidth=2, relief="solid")
        tot_cases_label = Label(top, text='Total Cases', padx=5, borderwidth=2, relief="solid")
        empty_label = Label(top, text='        ', padx=5, borderwidth=2, relief="solid")
        month_label.grid(row=0, column=0+counter_one)
        date_label.grid(row=0, column=1+counter_one)
        deaths_label.grid(row=0, column=2+counter_one)
        tot_deaths__label.grid(row=0, column=3+counter_one)
        cases_label.grid(row=0, column=4+counter_one)
        tot_cases_label.grid(row=0, column=5+counter_one)
        empty_label.grid(row=0, column=6+counter_one)
        counter_one += 7
    counter_two = 1
    counter_three = 1
    counter_month = 0
    for record in records:
        month_label = Label(top, text=str(record[0]), padx=5)
        date_label = Label(top, text=str(record[1]), padx=5)
        deaths_label = Label(top, text=str(record[2]), padx=5)
        tot_deaths__label = Label(top, text=str(record[3]), padx=5)
        cases_label = Label(top, text=str(record[4]), padx=5)
        tot_cases_label = Label(top, text=str(record[5]), padx=5)
        month_label.grid(row=counter_two, column=0+counter_month)
        date_label.grid(row=counter_two, column=1+counter_month)
        deaths_label.grid(row=counter_two, column=2+counter_month)
        tot_deaths__label.grid(row=counter_two, column=3+counter_month)
        cases_label.grid(row=counter_two, column=4+counter_month)
        tot_cases_label.grid(row=counter_two, column=5+counter_month)
        if records[counter_three][0] != records[counter_three-1][0]:
            counter_month += 7
            counter_two = 0
        counter_two += 1
        counter_three += 1
    conn.commit()
    conn.close()

add_month_label = Label(top_frame, text='Month:').grid(row=1, column=0)
add_day_label = Label(top_frame, text='Day:').grid(row=2, column=0)
add_deaths_label = Label(top_frame, text='Deaths:').grid(row=3, column=0)
add_cases_label = Label(top_frame, text='Cases:').grid(row=4, column=0)
add_month_entry = Entry(top_frame, width=30)
add_month_entry.grid(row=1, column=1)
add_day_entry = Entry(top_frame, width=30)
add_day_entry.grid(row=2, column=1)
add_deaths_entry = Entry(top_frame, width=30)
add_deaths_entry.grid(row=3, column=1)
add_cases_entry = Entry(top_frame, width=30)
add_cases_entry.grid(row=4, column=1)

add_data_btn = Button(top_frame, text='Add new entry', command=add_entry, pady=10, padx=10)
add_data_btn.grid(row=3, column=2, rowspan=2)

table_btn = Button(top_frame, text="Show all data", command=show_table, padx=13, pady=10)
table_btn.grid(row=1, column=2, rowspan=2)

choice = StringVar()
choice.set("Histogram")
sec_choice = StringVar()
sec_choice.set('Deaths')

histogram_btn = Radiobutton(bottom_frame, text='Per day', variable=choice, value='Histogram')
histogram_btn.grid(row=0, sticky='W')
graph_btn = Radiobutton(bottom_frame, text='Total over time', variable=choice, value='Graph')
graph_btn.grid(row=1, sticky='W')

deaths_btn = Radiobutton(bottom_frame, text='Deaths', variable=sec_choice, value='Deaths')
deaths_btn.grid(row=0, column=2, sticky='W')
cases_btn = Radiobutton(bottom_frame, text='Cases', variable=sec_choice, value='Cases')
cases_btn.grid(row=1, column=2, sticky='W')

show_graph_btn = Button(bottom_frame, text='Show', command=lambda: show(choice.get(), sec_choice.get()))
show_graph_btn.grid(row=2, column=1, padx=100, sticky='S')

conn.commit()
conn.close()
root.mainloop()