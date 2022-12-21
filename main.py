import pymysql
import hashlib
import time
import os
from datetime import datetime
import random

db =  pymysql.connect(host='127.0.0.1',password='nakshatra',user='root',db='rms')
cursor = db.cursor()

def auth():
	print("1.Existing User? Login\n2.New User? Register")
	choice= int(input("Enter choice: "))
	if choice == 1 :
		login()
	elif choice == 2:
		adduser()	
	else:
		print('Invalid Choice! Please try again')
		auth()
def login():
	global username
	username=input('Enter Username: ')
	query = f"SELECT * FROM users where username = '{username}'"
	cursor.execute(query)
	ps = cursor.fetchall()
	if ps == ():
		print('Invalid Username!')
		login()
	else:
		password=input("Enter password: ")
		hash = hashlib.sha512(password.encode('utf8')).hexdigest()
		if hash == ps[0][1]:
			cursor.execute(f"SELECT user_type from users where username = '{username}'")
			a=cursor.fetchone()
			mainloop(a[0])
		else:
			print('Wrong password!')
			login()
def adduser():
	try:
		username = input("Enter Username: ")
		password_hash = hashlib.sha512(f"{input('Enter password: ')}".encode('utf8')).hexdigest()
		user_type = input('User types: \n1) Passenger \n2) Staff \n\n Enter your user type: ')
		name = input('Enter your name: ')
		dob = int(input('Enter your date of birth (DDMMYYYY): '))
		gender = input('Enter your gender: ')
		meal_preference = input('Enter meal preference: ')
		cursor.execute(f"insert into users values('{username}','{password_hash}','{user_type}','{name}','{dob}','{gender}','{meal_preference}')")
		db.commit()
		print('User added')
	except:
		print('Username currently unavailable!!!')
def deleteuser():
	try:
		cursor.execute(f"delete from users where username = '{username}'")
		db.commit()
		print(f'User {a} deleted!')
	except:
		print('Username not found')
def addstation():
	try:
		station_code = input('Enter 3 digit station code: ')
		station_name = input('Enter station name: ')
		number_of_platform = int(input('Enter number of platform: '))
		cursor.execute(f"insert into station values('{station_code}','{station_name}','{number_of_platform}')")
		db.commit()
		print('Station added')
	except:
		print('Station Code aready exists!!')
def removestation():
	try:
		station_code = input('Enter 3 digit station code of station to remove: ')
		cursor.execute(f"delete from station where Station_code = '{station_code}'")
		db.commit()
		print(f'Station {station_code} deleted!!')
	except:
		print('Station not found!!')
def addtrain():
	try:
		train_code = int(input('Enter train code: '))
		distance  = int(input('Enter distance to be covered in KMs: '))
		train_name = input('Enter train name: ')
		station_one_end = input('Enter start station code: ')
		station_second_end = input('Enter end station code: ')
		days = input('Enter the days train operates: ')
		start_time = input('Enter start time (HH:MM:SS)')
		time_duration = int(input('Enter number of hours for total journey: '))
		number_of_coaches = int(input('Enter nunmber of coaches: '))
		number_of_seats_per_coach = int(input('Enter number of seats per coach: '))
		vacantseats = number_of_coaches * number_of_seats_per_coach
		current_status = 'idle'
		cursor.execute(f"insert into trains values('{train_code}','{distance}','{train_name}','{station_one_end}','{station_second_end}','{days}','{start_time}','{time_duration}','{number_of_coaches}','{number_of_seats_per_coach}','{vacantseats}','{current_status}')")
		db.commit()
		print('Train added')
	except:
		print('The train code might exist already or the station code entered is Invalid!! Please try again')
def removetrain():
	try:
		train_code = int(input('Enter train code to remove: '))
		cursor.execute(f"delete from trains where Train_code = '{train_code}'")
		db.commit()
		print(f'Train {train_code} deleted!!')
	except:
		print('Train not found!!')
def exit():
	print('THANK YOU FOR USING Railway Managemnt System! ☺️')
	time.sleep(4)
	os.system('exit')
def availabletrain():
	try:
		from_station = input('Enter origin station code: ')
		to_station = input('Enter destination station code: ')
		date = input('Enter date (YYYY:MM:DD): ')
		date = date.split(':')
		date = datetime(int(date[0]),int(date[1]),int(date[2]))
		day = date.strftime('%A')
		query = f"select Train_code, Train_name,station_one_end,station_second_end,Days,start_time, Time_duration from trains where station_one_end = '{from_station}' and station_second_end = '{to_station}' and vacant_seats != 0 "
		cursor.execute(query)
		a = cursor.fetchall()
		for i in a:
			for x in i:
				print(x,end = '\t\t')
			print()
	except:
		print('No trains found!!')
def mybooking():
	try:
		query = f"select * from bookings where username = '{username}'"
		cursor.execute(query)
		a = cursor.fetchall()
		for i in a:
			print(i)
	except:
		print('No current bookings')
def cancelbooking():
	try:
		pnr_num = int(input('Enter PNR number of your ticket you want to cancel: '))
		query=f"select Train_code from bookings where PNR_number = '{pnr_num}'"
		cursor.execute(query)
		traincode=cursor.fetchone()
		traincode = traincode[0]
		query  = f"select vacant_seats from trains where Train_code = {traincode}"
		cursor.execute(query)
		vacantseats=cursor.fetchone()
		vacantseats = vacantseats[0]
		query = f"delete from bookings where username = '{username}' and PNR_number = '{pnr_num}'"
		cursor.execute(query)
		db.commit()
		query = f"update trains set vacant_seats = '{vacantseats+1}' where Train_code = '{traincode}' "
		cursor.execute(query)
		print(f'Your ticket with PNR number: {pnr_num} has been deleted!')
	except:
		print('Invalid PNR_number/Username!!')
def checkfare(*train_code):
	try:
		if train_code == ():
			train_code = int(input('Enter train code: '))
		else:
			train_code = train_code[0]
			pass
		query = f"select distance from trains where Train_code = '{train_code}'"
		cursor.execute(query)
		a=cursor.fetchone()
		distance = a[0]
		fare = 0
		if distance < 100:
			fare = distance * 12
		elif distance >= 100 and distance <= 500:
			fare = distance * 10
		elif distance > 500:
			fare = distance * 8
		print(f"Fare for your journey is {fare}")
		return fare
	except:
		print('Invalid train code!')
def book():
	try:
		pnr=random.random()
		pnr=int(pnr*1000000000)
		query = f"select * from bookings where PNR_number = '{pnr}'"
		cursor.execute(query)
		a=cursor.fetchall()
		if a != ():
			book()
		train_code = int(input('Enter train code: '))
		query = f"select vacant_seats from trains where Train_code = '{train_code}'"
		cursor.execute(query)
		a=cursor.fetchone()
		if a[0] > 0:
			pass
		else:
			print('No seats available in train!!')
			book()
		from_station = input('Enter starting station code: ')
		to_station = input('Enter destination station code: ')
		date = input('Enter date (YYYY:MM:DD): ')
		date = date.split(':')
		date = datetime(int(date[0]),int(date[1]),int(date[2]))
		fare= checkfare(train_code)
		query = f"insert into bookings values('{pnr}','{username}','{train_code}','{from_station}','{to_station}','{date}','{fare}')" 
		cursor.execute(query)
		db.commit()
		query = f"update trains set vacant_seats = {a[0]-1}"
		cursor.execute(query)
		db.commit()
		print('Ticket booked!!')
	except:
		print('Your ticket cannot be booked!!')

def login_user():
	choice=int(input('''
			┌──────────────────────────┐
			│      Passenger Login     │
			├───────┬──────────────────┤
			│  S.No │      Options     │
			├───────┼──────────────────┤
			│   1   │ Delete User      │
			│   2   │ Available Train  │
			│   3   │ My Bookings      │
			│   4   │ Cancel Booking   │
			│   5   │ Check Fare       │
			│   6   │ Book Ticket      │
			│   7   │ Exit             │
			└───────┴──────────────────┘
			Enter your choice: '''))
	if choice == 1:
		deleteuser()
		os.system('cls')
		login_user()
	elif choice == 2:
		availabletrain()
		os.system('cls')
		login_user()
	elif choice == 3:
		mybooking()
		os.system('cls')
		login_user()
	elif choice == 4:
		cancelbooking()
		os.system('cls')
		login_user()
	elif choice == 5:
		checkfare()
		os.system('cls')
		login_user()
	elif choice == 6:
		book()
		os.system('cls')
		login_user()
	elif choice == 7:
		exit()
	else:
		print('Invalid Choice!')
		login_user()
def login_staff():
	choice = int(input('''
			┌──────────────────────────┐
			│       Staff Login        │
			├───────┬──────────────────┤
			│  S.No │      Options     │
			├───────┼──────────────────┤
			│   1   │ Delete User      │
			│   2   │ Available Train  │
			│   3   │ My Bookings      │
			│   4   │ Cancel Booking   │
			│   5   │ Check Fare       │
			│   6   │ Book Ticket      │
			│   7   │ Add Station      │
			│   8   │ Remove Station   │
			│   9   │ Add Train        │
			│   10  │ Remove Train     │
			│   11  │ Exit             │
			└───────┴──────────────────┘
			Enter your choice: '''))
	if choice == 1:
		deleteuser()
		os.system('cls')
		login_staff()
	elif choice == 2:
		availabletrain()
		os.system('cls')
		login_staff()
	elif choice == 3:
		mybooking()
		os.system('cls')
		login_staff()
	elif choice == 4:
		cancelbooking()
		os.system('cls')
		login_staff()
	elif choice == 5:
		checkfare()
		os.system('cls')
		login_staff()
	elif choice == 6:
		book()
		os.system('cls')
		login_staff()
	elif choice == 7:
		addstation()
		os.system('cls')
		login_staff()
	elif choice == 8:
		removestation()
		os.system('cls')
		login_staff()
	elif choice == 9:
		addtrain()
		os.system('cls')
		login_staff()
	elif choice == 10:
		removetrain()
		os.system('cls')
		login_staff()
	elif choice == 11:
		exit()
	else:
		print('Invalid Choice!')
		login_staff()
def mainloop(user_type):
	print('Welcome to the Railway Management System')
	if user_type == 'Passenger':
		login_user()
	elif user_type == 'Staff':
		login_staff()
auth()