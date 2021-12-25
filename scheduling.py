import datetime as dt
from datetime import date, timedelta, datetime
import sys
today = date.today()

def get_date_list(day, f_con = "none"):

    import sys

    for x in "-/ ":
        date = (str(day)).split(x)
        if date[0] != str(day):
            break

    while "" in date:
        date.remove("")
    while " " in date:
        date.remove(" ")
    date = list(map(lambda x: x.replace(" ",""), date))

    ymd = {"year": 2, "month": 0, "day": 1}

    if ((len(date) == 3) and ("".join(date).isdigit()) and (date[ymd["year"]].replace("0", "").isdigit() and len(date[ymd["year"]]) <= 4) and (int(date[ymd["month"]]) - 1 in range(12)) and (int(date[ymd["day"]]) - 1 in range([30, 31][((int(date[ymd["month"]])) % 2)] - (2 * int(int(date[ymd["month"]]) == 2))))):
        date = [date[ymd["year"]], date[ymd["month"]], date[ymd["day"]]]
        for count, x in enumerate(date):
            date[count] = int(x)
        return date
    else:
        if f_con == "error":
            print("\n\t|get_date_list - Invalidity Error|")
            sys.exit()
        elif f_con == "true":
            return True
        elif f_con == "false":
            return False
        elif f_con == "none":
            return None

#takes the due date inputs from the user and determines if they are valid dates
def due_date_split(entry, breaker):
    new_date = entry.split('-')

    if len(new_date) == 3:
        check_digit = ''
        for value in new_date:
            check_digit += value

        if check_digit.isdigit() and len(new_date[0]) <= 2 and len(new_date[1]) <= 2 and len(new_date[2]) <= 4:
            pass
        else:
            print('Invalid Date Entry!')
            breaker = 'F'
            return [breaker]
    else:
        print('Invalid Date Entry!')
        breaker = 'F'
        return [breaker]

    m = int(new_date[0])
    d = int(new_date[1])
    y = int(new_date[2])
    return [breaker,m,d,y]

#takes the list of weekends and weekdays and sorts them into seperate lists
def sort_days(all_days_list):
    all_days = []
    weekends_list = []
    weekdays_list = []
    is_weekend = ['Sat','Sun']
    for day1 in all_days_list:
        if day1.strftime('%a') in is_weekend: #sees if day is a weekend
            weekends_list.append(day1)
        else:
            weekdays_list.append(day1)
    all_days.append(weekends_list)
    all_days.append(weekdays_list)
    return all_days

#function asks the user what weekdays they want off (specific dates)
def weekdays_off(weekdays_list, weekends_list): #sees which weekdays will be taken off
    dayoff = None
    days_off = []
    used = []
    count_1 = 1
    print("How many weekdays off do you need?")
    days_off_total=input("> ")
    if days_off_total == '0':
        return []
    while days_off_total.isdigit() == False:
        print("Please enter only digits")
        print("How many weekdays off do you need?")
        days_off_total=input("> ")
    days_off_total = int(days_off_total)
    days_off_total_2 = days_off_total
    while int(days_off_total) > int(len(weekdays_list)):
        print("You have asked for too many days off, please ask for less")
        print("How many weekdays off do you need?")
        days_off_total=input("> ")
    while days_off_total > 0:
        while True:
            print(f"What day would you like off(mm-dd-yyyy), Day {int(count)} of {days_off_total_2}")
            dayoff_input = input("> ")
            for temp in used:
                if dayoff_input == temp:
                    print("You have already entered that date, please enter a different one")
                    break
            count = 0
            dayoff_list = dayoff_input.split("-")
            for x in dayoff_list:
                if x.isdigit() == False:
                    print("Please enter that again as a date with numbers")
                    break
                else:
                    dayoff_list[count] = int(x)
                count += 1
            if dayoff_list[0] in range(1,13) and dayoff_list[1] in range(1,32): #if day is a usable date
                pass
            else:
                print("Please enter a valid date")
                break
            used.append(dayoff_input)
            #print(used)
            dayoff = date(day = int(dayoff_list[1]), month = int(dayoff_list[0]), year = int(dayoff_list[2]))

            if dayoff in weekdays_list: #makes sure it's a weekday
                days_off_total -= 1
                days_off.append(dayoff)
                break
            elif dayoff in weekends_list:
                print('That date is a weekend, please enter a different date')
            else:
                print("Please enter that again")
    return days_off

#asks the user if they want weekends off
day_dict = {'M':'Monday',
            'TU':'Tuesday',
            'W':'Wednesday',
            'TH':'Thursday',
            'F':'Friday',
            'SA':'Saturday',
            'SU':'Sunday'}
def weekends_off(weekends_list): #checks if user wants weekends off
    daysOfWeek_off = []
    while True:
        print("\nWould you like a specific day of the week off?\nEx: Mondays, Thursdays, Saturdays, etc. (Y/N)")
        weekends_input = input("> ")
        if weekends_input.upper().startswith("N"):
            return daysOfWeek_off
        elif weekends_input.upper().startswith("Y"):
            while True:
                print("\nWhich day would you like off? Enter a day (M, Tu, W, Th, F, Sa, Su)")
                weekday_off = input("> ").upper()
                if weekday_off in day_dict.keys():
                    for day in weekends_list:
                        if day.strftime("%A") == day_dict[weekday_off]:
                            daysOfWeek_off.append(day)
                print('Would you like to take off another weekday?')
                weekday_again = input('> ').upper()
                if weekday_again == 'Y':
                    pass
                else:
                    break
            return daysOfWeek_off

print('Today\'s Date:',date.today().strftime('%b %-d, %Y'))


timeline_items = [] #final list of all information
while True: #main program loop
    print('What is the name of the assignment?')
    assign_name = input('> ')

    while True: #asks user for when the assignment is due (loop)
        loop_break = 'T'
        print(f'\nWhen is \'{assign_name.title()}\' due?\nPlease format as mm-dd-yyyy in all digits')
        date_input = input("> ")
        date_list = get_date_list(date_input, "true")

        while date_list == True:
            date_input = input("> ")
            date_list = get_date_list(date_input, "true")

        due_date = date(month = int(date_list[1]), day = int(date_list[2]), year = int(date_list[0]))
        delta = (due_date - date.today()).days
        print(f'\'{assign_name.title()}\' is due in {delta} days')
        break

    while True: #asks user how many hours of work they need (loop)
        print(f'\nHow many hours of work will you need on \'{assign_name.title()}\'?')
        assign_hours = input('> ')
        if assign_hours.isdigit():
            assign_hours = int(assign_hours)
            break
        else:
            print('Invalid Hour Entry!')

    #[name of assignment, hours of work needed for assignment, days until assignment is due, date when assignment is due]
    timeline_items.append([assign_name, assign_hours, delta, due_date])

    #asks if user would like to add another assignment, if yes, loop, if not, breaks loop
    print('\nWould you like to add another assignment? (Y/N)')
    new_assign = input('> ')
    if new_assign.upper() == 'Y':
        pass
    else:
        break

total_hours = 0
for item in timeline_items: #calculates total hours of work
    total_hours += item[1]

sorted_due_dates = []
for item in timeline_items: #sorts due dates from closest to furthest
    sorted_due_dates.append(item[2])
    sorted_due_dates.sort()

#calculates length of timeline (furthest due date from today (important to algorithm))
#sorted_due_dates[-1] is the furthest due date from today
delta1 = today + timedelta(days = sorted_due_dates[-1])


count = 1
all_days_list = [] #list of every day from today to the furthest due date (end of timeline)
print("Your timeline is set up so you will be working from", today.strftime("%b %-d, %Y"), "to", delta1.strftime("%b %-d, %Y")+'\n')
all_days = sorted_due_dates[-1]
for x in range(int(all_days)):
    current_day = today + timedelta(days = count)
    all_days_list.append(current_day)
    count += 1

#calls function that splits weekdays and weekends into seperate lists (important for calculating days off)
sorted_days = sort_days(all_days_list)
weekends = sorted_days[0]
weekdays = sorted_days[1]
weekends_off_list = weekends_off(weekends)
weekdays_off_list = weekdays_off(weekdays, weekends)

spec_days_off = [] #specific days off, or and days the user specifically inputted to have off
#create an entire list of dates off
if len(weekends_off_list) > 0 and len(weekdays_off_list) > 0:
    all_days_off = weekends_off_list + weekdays_off_list  #add every date to this list
elif len(weekdays_off_list) == 0:
    all_days_off = weekends_off_list
elif len(weekends_off_list) == 0:
    all_days_off = weekdays_off_list
else:
    all_days_off = []

#ALGORITHM
count = 0
new_timeline_items = [] #updated list of everything important

#for reference:
#timeline_items = [name of assignment, hours of work needed for assignment, days until assignment is due, date when assignment is due]
while True:
    if count > len(sorted_due_dates):
        break
    else:
        for item in timeline_items:
            if sorted_due_dates[count] == item[2]:
                timeline_items.remove(item)
                new_timeline_items.append(item)
                break
    count += 1

timeline_items = new_timeline_items

hours_per_day = total_hours / (sorted_due_dates[-1]- len(all_days_off)) #sorted days[-1] is the maximum length of the timeline, or the total days

#next, iterate through each number in sorted_due_dates[-1] (total days)

due_count = 0  #sorted days counter (sorted_due_dates[0], sorted_due_dates[1], etc.)
day_count = 1  #day counter (day 1, day 2, etc.)
timeline_layout = [] #final list
unfortunate_msg = ''

for item in range(sorted_due_dates[-1]): #iterates through each day
    date2 = timedelta(days = day_count)
    delta = date.today() + date2

    hours_remaining = hours_per_day #hours of work allowed for one day
    one_day = [['Day '+str(day_count), delta]]
    sorted_due_dates = []
    for item in timeline_items:
        sorted_due_dates.append(item[2])
        sorted_due_dates.sort()

    for assignment in timeline_items:
        if delta in all_days_off: #if the current day being created is a day off, pass (no work today)
            one_day.append(['DAY OFF - No work today'])
            break
        elif hours_remaining <= 0:
            break
        elif assignment[1] == 0 or assignment[2] == 0: #assignment has been completely planned
            due_count += 1
        elif sorted_due_dates[due_count] == assignment[2]: #starts with the closest due date
            work_for_day = assignment[1] / assignment[2]
            if hours_remaining <= 0: #hours of work per day limit has been reached or exceeded
                due_count += 1
                break
            elif assignment[2] == 1 and assignment[1] > hours_remaining: #1 day remaining for assignment and assignment requires more hours than allowed
                one_day.append([assignment[0],assignment[1]])
                assignment[1] -= work_for_day
                hours_remaining = 0
                due_count += 1
                unfortunate_msg = '\n\nUnfortunately, on some days the hours per day limit has been exceeded due to an excess amount of work due in a short amount of time'
            elif work_for_day > hours_remaining: #limit for work per day has been reached
                one_day.append([assignment[0],hours_remaining])
                assignment[1] -= hours_remaining
                hours_remaining = 0
                due_count += 1
            elif work_for_day <= hours_remaining: #perfect scenario: work per day is less than hours remaining
                one_day.append([assignment[0],work_for_day])
                hours_remaining -= work_for_day
                assignment[1] -= work_for_day
                due_count += 1


    for assignment in timeline_items:
        assignment[2] -= 1

    timeline_layout.append(one_day)
    day_count += 1
    due_count = 0

#below creates the final schedule and converts all hours into hours + minutes (ex: 1.75 hours -> 1 hour 45 min):
hours = 0
mins = 0
counter_day = -1
for day in timeline_layout:
    if day[1][0] == 'DAY OFF - No work today':
        counter_day += 1
        counter_value = 0
    else:
        counter_day += 1
        counter_value = 0
        for value in day[1:]:
            counter_value += 1
            convert = str(value[1])
            convert_list = convert.split('.')

            decimal = '0.'+convert[-1]
            mins = float(decimal) * 60
            mins = int(mins)
            hours = int(convert_list[0])

            if hours == 1:
                if mins == 0:
                    timeline_layout[counter_day][counter_value][1] = str(hours)+' hour'
                else:
                    timeline_layout[counter_day][counter_value][1] = str(hours)+' hour, '+str(mins)+' minutes'
            elif hours > 1:
                if mins == 0:
                    timeline_layout[counter_day][counter_value][1] = str(hours)+' hours'
                else:
                    timeline_layout[counter_day][counter_value][1] = str(hours)+' hours, '+str(mins)+' minutes'
            else:
                timeline_layout[counter_day][counter_value][1] = str(mins)+' minutes'

hpd_convert = str(hours_per_day)
hpd_convert_list = hpd_convert.split('.')
hpd_decimal = '0.'+hpd_convert[2]
hpd_mins = float(hpd_decimal) * 60
hpd_mins = int(hpd_mins)
hpd_hours = int(hpd_convert_list[0])
if hpd_hours == 1:
    hpd_convert = '('+str(hpd_hours)+' hour, '+str(hpd_mins)+' minutes)'
elif hpd_hours > 1:
    hpd_convert = '('+str(hpd_hours)+' hours, '+str(hpd_mins)+' minutes)'
else:
    hpd_convert = '('+str(hpd_mins)+' minutes)'

timeline = open('timeline.txt','w')
line1 = str(f'Hours of work per day: {hours_per_day} {hpd_convert} \nKeep in mind you may have more or less work each day depending on your due dates and days off\nHere is the timeline we made for you:')
timeline.write(line1)
for line in timeline_layout:
    line2 = str(f'\n\n{line[0][0]}: {line[0][1].strftime("%b %-d, %Y")}\n')
    timeline.write(line2)
    for value in line[1:]:
        if value[0] == 'DAY OFF - No work today':
            line3 = str(value[0])
        else:
            line3 = str(f'{value[1]} of \'{value[0].title()}\'. ')
        timeline.write(line3)
