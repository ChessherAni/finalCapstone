# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password


#=========== IMPORTING LIBRARIES ===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"


#=========== DEFINING FUNCTIONS ===========
def clear_screen():
    os.system("clear||cls")


def reg_user():
    '''Add a new user to the user.txt file'''

    # Request input of new username & check if it already exists
    new_username = input("New Username: ")
    while True:
        if new_username in username_password.keys():
            print("Username already taken")
            new_username = input("Please try a different username: ")
        else:
            break
            
    # Request password and confirmed password
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    # Check if the new password and confirmed password are the same.
    while True:
        if new_password == confirm_password:
            # If they are the same, add them to the user.txt file,
            username_password[new_username] = new_password
            
            with open("user.txt", "w") as out_file:
                user_data = []
                for i in username_password:
                    user_data.append(f"{i};{username_password[i]}")
                out_file.write("\n".join(user_data))

            clear_screen()
            print("New user added!")

            break
        # Otherwise present a relevant message.
        else:
            confirm_password = input("Passwords do not match, please reconfirm password: ")


def add_task():
    '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to
             - A title of a task
             - A description of the task 
             - The due date of the task.'''
    
    # Request username and check if username exists
    task_username = input("Name of person assigned to task: ").lower()
    while True:
        if task_username in username_password.keys():
            break
        else:    
            task_username = input("User does not exist. Please enter a valid username: ")

    # Request title and description of task
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")


    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    
    # Add to task_list
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)

    # Write task_list to tasks.txt
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    
    clear_screen()
    print("Task successfully added.")


def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)'''

    for t in task_list:
        print("_"*50 + "\n")
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Completed?  {"Yes" if t['completed'] else "No"}\n"
        disp_str += f"Task Description: \n {t['description']}"
        print(disp_str)
    print("_"*50 + "\n")


def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)'''

    # Variable to tally if user hasn't been assigned any tasks yet
    no_tasks = 0

    # Accessing tasks by number
    task_num = 0

    print()
    print("All the tasks assigned to you")
    for t in task_list:
        if t['username'] != curr_user:
            no_tasks += 1
            t['number'] = 0

        # Print out all tasks assigned to user
        # Add task's number to task_list
        else:
            task_num += 1
            t['number'] = task_num
            print("_"*50 + "\n")
            disp_str = f"Task Number: \t {t['number']}\n"
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Completed?  {"Yes" if t['completed'] else "No"}\n"
            disp_str += f"Task Description: \n {t['description']}"
            print(disp_str)
    print("_"*50 + "\n")


    # If no tasks have been assigned, print out relevant message   
    if len(task_list) == no_tasks:
        print(f"No tasks have been assigned to you yet")
        print("_"*50 + "\n")
        
    else:
        # Editing tasks
        task_choice = input("Enter the number of a task to edit it, or enter -1 to return to menu: ")

        # Error handling
        while True:
            # Return to menu if user enters -1
            if task_choice == "-1":
                clear_screen()
                break
            elif not task_choice.isnumeric() or int(task_choice) > task_num:
                task_choice = input("Please enter the number of a task, or -1: ")
            elif int(task_choice) < -1 or int(task_choice) == 0:
                task_choice = input("Please enter the number of a task, or -1: ")
            else:
                break

        # Logic for editing tasks    
        # Remind user which task they're editing
        completed_check = False
        for t in task_list:
            if task_choice != "-1" and int(task_choice) == t['number']:
                clear_screen()
                print(f"You are editing task '{t['title'].capitalize()}'")
                print()
                
                # If task is already complete, return to menu
                if t['completed']:
                    clear_screen()
                    print("Cannot edit completed tasks. Returning to menu")
                    completed_check = True
                    break

        if task_choice != "-1" and not completed_check:
            # Ask user which task they want to edit
            edit_choice = input("""There are three editing options:
        1. Mark this task as complete
        2. Edit the user assigned to this task
        3. Edit the due date of this task\nEnter option number: """)
                    
            # Error handling
            while True:
                if not edit_choice.isdigit() or int(edit_choice) > 3 or int(edit_choice) == 0:
                    edit_choice = input("Invalid answer. Enter 1, 2 or 3: ")
                else:
                    break
                
            # Marking a task as complete
            if edit_choice == "1":
                for t in task_list:
                    if int(task_choice) != t['number']:
                        continue
                    else:
                        # Change to completed
                        t['completed'] = True

                        # Success message
                        clear_screen()
                        print(f"Task '{t['title'].capitalize()}' marked as complete")

                        # Write changes to tasks.txt
                        with open("tasks.txt", "w") as task_file:
                            task_list_to_write = []
                            for t in task_list:
                                str_attrs = [
                                    t['username'],
                                    t['title'],
                                    t['description'],
                                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                    "Yes" if t['completed'] else "No"
                                ]
                                task_list_to_write.append(";".join(str_attrs))
                            task_file.write("\n".join(task_list_to_write))

            # Editing a task's username
            elif edit_choice == "2":
                for t in task_list:
                    if int(task_choice) != t['number']:
                        continue
                    else:
                        new_task_username = input("This task is now assigned to: ")
                        # Error handling
                        while True:
                            if new_task_username in username_password.keys():
                                break
                            else:
                                new_task_username = input("Please enter a valid username: ")

                        # Change task's username
                        t['username'] = new_task_username

                        # Success message
                        clear_screen()
                        print(f"Task '{t['title'].capitalize()}' now assigned to '{t['username']}'")

                        # Write changes to tasks.txt
                        with open("tasks.txt", "w") as task_file:
                            task_list_to_write = []
                            for t in task_list:
                                str_attrs = [
                                    t['username'],
                                    t['title'],
                                    t['description'],
                                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                    "Yes" if t['completed'] else "No"
                                ]
                                task_list_to_write.append(";".join(str_attrs))
                            task_file.write("\n".join(task_list_to_write))

            # Edit a task's due date
            elif edit_choice == "3":
                for t in task_list:
                    if int(task_choice) != t['number']:
                        continue
                    else:                
                        # Error handling
                        while True:
                            try:
                                new_task_duedate = input("New task due date (YYYY-MM-DD): ")
                                new_datetime = datetime.strptime(new_task_duedate, DATETIME_STRING_FORMAT)
                                break

                            except ValueError:
                                print("Invalid datetime format. Please use the format specified")
                        
                        # Change task's due date
                        t['due_date'] = new_datetime

                        # Success message
                        clear_screen()
                        print(f"Task '{t['title'].capitalize()}' due date changed to {new_datetime}")

                        # Write changes to tasks.txt
                        with open("tasks.txt", "w") as task_file:
                            task_list_to_write = []
                            for t in task_list:
                                str_attrs = [
                                    t['username'],
                                    t['title'],
                                    t['description'],
                                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                    "Yes" if t['completed'] else "No"
                                ]
                                task_list_to_write.append(";".join(str_attrs))
                            task_file.write("\n".join(task_list_to_write))

def generate_report():
    """If the user is an admin they can generate statistics about number of users
    and tasks"""

    # ==== Tasks overview ==== 
    # Variables for calculations
    num_tasks = 0
    num_uncomplete = 0
    num_overdue = 0

    # Find out how many tasks in total
    for t in task_list:
        num_tasks += 1
        # How many tasks are uncomplete
        if not t['completed']:
            num_uncomplete += 1
            # Of these, how many are overdue
            if t['due_date'] < datetime.today():
                num_overdue += 1
    
    # Calculate number of incomplete tasks
    num_completed = num_tasks - num_uncomplete

    # Percentage calculations
    perc_complete = (num_completed / num_tasks) * 100
    perc_uncomplete = (num_uncomplete / num_tasks) * 100

    # Construct string that will write to file
    overview_tasks = "="*18 + " Tasks Overview " + "="*18
    overview_tasks += f"""\nGenerated & tracked tasks: {num_tasks}
Completed tasks: {num_completed}
Uncompleted tasks: {num_uncomplete}
Overdue tasks: {num_overdue}

{perc_complete}% of all tasks have been completed
{perc_uncomplete}% are still incomplete"""

    # Write data to file
    with open("task_overview.txt", 'w') as file:
        file.write(overview_tasks)

    print("Task overview completed!")

    # ==== User Overview ====
    # Variables for calculations
    num_users = 0
    overview_ulist = []

    # Find out how many users in total
    for u in username_password.keys():
        overview_udict = {}
        num_users += 1

        user_overdue = 0
        user_uncomplete = 0
        # How many tasks each user has
        user_task = 0
        for t in task_list:
            if u == t['username']:
                user_task += 1

                # How many of their tasks are incomplete
                if not t['completed']:
                    user_uncomplete += 1
                    # Of these, how many are overdue
                    if t['due_date'] < datetime.today():
                        user_overdue += 1

        # Percentage calculations
        perc_assigned = (user_task / num_tasks) * 100
        try: 
            perc_user_complete = ((user_task - user_uncomplete) / user_task) * 100
            perc_user_incomplete = (user_uncomplete / user_task) * 100
            perc_user_overdue = (user_overdue / user_task) * 100
        except ZeroDivisionError:
            perc_user_complete = 0
            perc_user_incomplete = 0
            perc_user_overdue = 0

        # Convert to dictionary & append to list
        overview_udict['username'] = u
        overview_udict['tasks'] = user_task
        overview_udict['assigned'] = perc_assigned
        overview_udict['complete'] = perc_user_complete
        overview_udict['incomplete'] = perc_user_incomplete
        overview_udict['overdue'] = perc_user_overdue
        
        overview_ulist.append(overview_udict)


    # Constructing the string to write to file
    overview_users = "="*17 + " All Users Overview " + "="*17
    overview_users += f"""\nNumber of users: {num_users}\nGenerated & tracked tasks: {num_tasks}\n\n"""
    # User specific information
    for u in overview_ulist:
        overview_users += f"User '{u['username'].capitalize()}' Overview\n"
        overview_users += f"\t{u['tasks']} tasks have been assigned to '{u['username'].capitalize()}'\n"
        # Skip this info if no tasks have been assigned to the user
        if u['tasks'] != 0:
            overview_users += f"\tThey have been assigned {u['assigned']}% of all tasks\n"
            overview_users += f"\tThey have completed {u['complete']}% of their tasks\n"
            overview_users += f"\tThey still need to complete {u['incomplete']}% of their tasks\n"
            overview_users += f"\t{u['overdue']}% of their tasks are overdue\n"
        else:
            pass
        overview_users += "\n"

    # Write data to file
    with open("user_overview.txt", 'w') as file:
        file.write(overview_users)

    print("User overview completed!")


def display_statistics():
    '''If the user is an admin they can display statistics about number of users
    and tasks.'''

    # Call generate_report if the files do not exist yet
    if not os.path.exists("task_overview.txt"):
        generate_report()
    if not os.path.exists("user_overview.txt"):
        generate_report()

    # Reading in task_overview.txt
    with open("task_overview.txt", 'r') as file:
        t_overview_data = file.read().split('\n')

    # Displaying overview of tasks
    print()
    for t in t_overview_data:
        print(t)
    print()

    # Reading in user_overview.txt
    with open("user_overview.txt", 'r') as file:
        u_overview_data = file.read().split('\n')
        # u_overview_data = [t for t in t_overview_data if t != ""]

    # Displaying overview of users
    for u in u_overview_data:
        print(u)
    print("_"*50 + "\n")


#=========== MAIN CODE ===========
# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    while True:
        if curr_user in username_password.keys():
            break
        else:
            print("User does not exist")
            curr_user = input("Please try again: ")

    curr_pass = input("Password: ")
    while True:
        if username_password[curr_user] == curr_pass:
            break
        else:
            print("Wrong password")
            curr_pass = input("Please try again: ")

    clear_screen()
    print("Login Successful!")
    logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    if curr_user == "admin":
        menu = input('''Select one of the following options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()
    else:
        menu = input('''Select one of the following options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
e - Exit
: ''').lower()

    if menu == 'r':
        clear_screen()
        reg_user()

    elif menu == 'a':
        clear_screen()
        add_task()

    elif menu == 'va':
        clear_screen()
        view_all()

    elif menu == 'vm':
        clear_screen()
        view_mine()
    
    elif menu == 'gr' and curr_user == 'admin':
        clear_screen()        
        generate_report()
        
    elif menu == 'ds' and curr_user == 'admin':
        clear_screen()
        display_statistics()

    elif menu == 'e':
        print('Goodbye!')
        exit()

    else:
        clear_screen()
        print("You have made a wrong choice, please try again")