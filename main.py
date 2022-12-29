import csv
import os
from tkinter import *
from tkinter import ttk
from numpy import size

#global variables
root = Tk()
mainframe = Frame(root)
title = Label(root,text="Atlantic hotel", font = ("times roman",30))
name = Label(root,text='Name :')
nameEntry = Entry(root,width=30)
age = Label(root,text='Age :')
ageEntry = Entry(root,width=30)
room_number = Label(root,text='Room number :')
roomEntry = Entry(root,width=30)
medical_issues = Label(root,text='Medical issues :')
medicalEntry = Entry(root,width=30)
guest_name_reminder = "Please type your name here"
spacer = Label(root,text='')
event_name = ""
subevent1 = Label(root,text=event_name,font=('bold',25))
event_listbox = Listbox(root, exportselection=False)
guests_listbox = Listbox(root)

#collects guest data
def get_guest_info():
    get_name = nameEntry.get()
    get_age = ageEntry.get()
    get_room = roomEntry.get()
    get_medical = medicalEntry.get()
    add_guest(get_name,get_age,get_room,get_medical)
    
add_guest_button=Button(root,text='Add Guest',command=get_guest_info)

def guest_entry():
    title.grid(column = 2, row = 0)
    name.grid(column = 1, row = 2)
    nameEntry.grid(column = 2, row = 2)
    age.grid(column = 1, row = 3)
    ageEntry.grid(column = 2, row = 3)
    room_number.grid(column = 1, row = 4)
    roomEntry.grid(column = 2, row = 4)
    medical_issues.grid(column = 1, row = 5)
    medicalEntry.grid(column = 2, row = 5)
    add_guest_button.grid(column=2, row=6)
    spacer.grid(column = 1, row = 7)

def event_info(event_name):
    event_info = scan_file("events.csv",event_name)
    return event_info

def get_events(file_name):
    names = []
    with open(file_name, mode ='r') as file:
        csv_read = csv.reader(file)
        for name in csv_read:
            if size(name)>0:
                names.append(name[0])
        file.close()
        return names

def event_list():
    event_list = get_events("events.csv")
    return event_list

#changes events when you click on the list
def change_event(more):
    try:
        i = event_listbox.curselection()[0]
        text = event_listbox.get(i)
        event_name = text
        show_event(text)
    except IndexError:
        print("")

def show_events():
    subevent1=Label(root,text='Events',font=('bold',25))
    subevent1.grid(column = 2, row = 8)
    events = event_list()
    event_listbox.grid(column=2,row=9)
    spacer2=Label(root,text='')
    spacer2.grid(column = 1, row = 10)
    for element in events:
        event_listbox.insert(END,element)
    event_listbox.bind("<<ListboxSelect>>", change_event)

def show_event(event_name):
    if len(event_name)<1:
        event_name = str(event_list()[0])
    subevent1=Label(root,text='                                         ',font=('bold',25))
    subevent1.grid(column = 2, row = 11)
    subevent1=Label(root,text=event_name,font=('bold',25))
    subevent1.grid(column = 2, row = 11)
    event_data = event_info(event_name)
    event_max_guests = "Maximum capacity: " + event_data[1]
    subevent2=Label(root,text='                                           ')
    subevent2.grid(column = 2, row = 12)
    subevent2=Label(root,text=event_max_guests)
    subevent2.grid(column = 2, row = 12)
    subevent3=Label(root,text="Registered Guests",font=('bold'))
    subevent3.grid(column = 2, row = 13)
    guests_listbox.delete(0, "end")
    event_guests = (event_data[2:])
    for guest in event_guests:
        guests_listbox.insert(END,guest)
    guests_listbox.grid(column=2,row=14)
    sign_up_button(event_name)

#if event fills up then wont add guest
def check_event_space(event_name):
    space_left = False
    if len(event_name) > 1:
        event_data = event_info(event_name)
        event_max_guests = int(event_data[1])
        event_count_guests = size(event_data[2:])
        slots_left = event_max_guests - event_count_guests
        if (slots_left>0):
            space_left = True
    return space_left

#adds guest to the selected event or disables button if event is full
def sign_up_button(event_name):
    if check_event_space(event_name):
        registerbutton=Button(root,text='Sign me up!',command=lambda: add_name_to_event(event_name))
    else:
        registerbutton=Button(root,text='  Event Full ',fg="#000",state="disabled")
    registerbutton.grid(column=2,row=15)

def scan_file(file_name, key):
    with open(file_name, mode ='r') as file:
        csv_read = csv.reader(file)
        for lines in csv_read:
            if lines[0] == key:
                file.close()
                return lines

def add_name_to_event(event_name):
    guest_name = nameEntry.get()
    if guest_name==guest_name_reminder:
        guest_name = ""
    event = scan_file("events.csv",event_name)
    event_guests = event[2:]
    if guest_name not in event_guests:
        if (len(guest_name)>0):
            add_guest_to_event(guest_name,event_name)
        else:
            nameEntry.delete(0, "end")
            nameEntry.insert(0,guest_name_reminder)

def get_file(file_name):
    with open(file_name, mode ='r') as file:
        all_lines = []
        csv_read = csv.reader(file)
        for line in csv_read:
            all_lines.append(line)
        file.close()
        return all_lines

#reads all guest information
def guest_info(guest_name):
    guest_info = scan_file("guests.csv",guest_name)
    return guest_info

def guests_at_event(event_name):
    all_guests = (scan_file("events.csv",event_name))[2:]
    return all_guests

#adds guest into event list file
def add_guest_to_event(guest_name,event_name):
    event = scan_file("events.csv",event_name)
    event_guests = event[2:]
    if (len(guest_name)>0) and guest_name not in event_guests:
        all_lines = ""
        with open("events.csv", mode ='r') as file:
            csv_read = csv.reader(file)
            for count,lines in enumerate(csv_read):
                if (lines[0] == event_name):
                    max_guests = int(lines[1])
                    current_guests = lines[2:]
                    count_guests = len(current_guests)
                    if (count_guests < max_guests):
                        lines.append(guest_name)
                all_lines += ",".join(lines) + "\n"
            file.close()
        with open('events.csv', 'w') as file:
            file.write(all_lines)
            file.close()
    show_event(event_name)

#adds guest to the registry
def add_guest(guest_name, guest_age, guest_room, guest_medical):
    new_guest = [guest_name, guest_age, guest_room, guest_medical]
    existing_guest = False
    all_guests = get_file("guests.csv")
    new_guest_list = ""
    if (len(guest_name)>0 and guest_name!=guest_name_reminder):
        for guest in all_guests:
            if (guest[0] == guest_name):
                new_guest_list += ",".join(new_guest) + "\n"
                existing_guest = True
            else:
                new_guest_list += ",".join(guest) + "\n"
        if not existing_guest:
            new_guest_list = new_guest_list + ",".join(new_guest)
        with open('guests.csv', 'w') as file:
            file.write(new_guest_list)
            file.close()
    else:
        nameEntry.delete(0, "end")
        nameEntry.insert(0,guest_name_reminder)

def main():
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    guest_entry()
    show_events()
    show_event("")
    root.mainloop()

if __name__=="__main__":
    main()
