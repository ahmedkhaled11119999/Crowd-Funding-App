import re
import ast
import json
import datetime
import copy

#####################
###-----UTILS-----###
#####################


def match_regex(user_input,pattern):
    if re.fullmatch(pattern,user_input):
        return True
    else:
        return False


def create_new_file(file_name):
    with open(file_name, "x") as file:
        pass


def append_to_file(file_name, input_dict):
    with open(file_name, "a") as file:
        file.write(input_dict + "\n")


def validate_date(date_input):
    date_arr = date_input.split("-")
    try:
        start_date = datetime.datetime(int(date_arr[0]), int(date_arr[1]), int(date_arr[2]))
        start_date_formatted = start_date.strftime("%Y-%m-%d")
        if date_input == start_date_formatted:
            return True
        return False
    except ValueError:
        return False


def print_projects(projects_list):
    for i, p_dict in enumerate(projects_list):
        p_num = i + 1
        print("Project {} Title: {}".format(p_num, p_dict["p_title"]))
        print("Project {} Details: {}".format(p_num, p_dict["p_details"]))
        print("Project {} Total Target: {}".format(p_num, p_dict["p_target"]))
        print("Project {} Start Date: {}".format(p_num, p_dict["p_start_date"]))
        print("Project {} End Date: {}".format(p_num, p_dict["p_end_date"]))
        print("########################################################")


##########################
###---USER FUNCTIONS---###
##########################


def register():
    f_name=input("Enter your first name:\n")
    l_name=input("Enter your last name:\n")
    while 1:
        email=input("Enter your email:\n")
        if match_regex(email,r".*@[a-zA-Z]+\.[a-zA-Z]+"):
            break
        else:
            print("Please enter a valid email\n")
    password=input("Enter your password:\n")
    while 1:
        conf_password = input("Confirm your password:\n")
        if conf_password == password:
            break
        else:
            print("Your password doesn't match, please re-enter\n")
    while 1:
        mobile_num = input("Enter your mobile number preceded by '+20' :\n")
        if match_regex(mobile_num,r"\+20[0-9]{10}"):
            break
        else:
            print("Please enter a valid mobile number\n")
    while 1:
        try:
            with open("reg_users","r") as file:
                users = file.read()
            if email not in users:
                user_data = {"f_name": f_name, "l_name": l_name, "email": email,
                             "password": password, "mobile_num": mobile_num, "projects": []}
                append_to_file("reg_users", json.dumps(user_data))
            else:
                print("This email is already Registered\n")
        except FileNotFoundError:
            create_new_file("reg_users")
            continue
        break


def login():
    email = input("Email: ")
    password = input("Password: ")
    with open("reg_users", "r") as file:
        users = file.readlines()
        for line_num, user in enumerate(users):
            if email in user:
                user_data = ast.literal_eval(user.strip())
                if password == user_data["password"]:
                    print("Logged in successfully\nWelcome {} !".format(user_data["f_name"]))
                    return user_data
                else:
                    print("Wrong password!, try again\n")
            if line_num == len(users) - 1:
                print("There is no registered account with this email\n")


def create_project():
    p_title = input("Enter project title:\n")
    p_details = input("Enter project details:\n")
    p_target = int(input("Enter project total target:\n"))
    while 1:
        p_start_date = input("Enter project start date (yyyy-mm-dd):\n")
        if validate_date(p_start_date):
            break
        else:
            print("Please enter a valid project start date\n")

    while 1:
        p_end_date = input("Enter project end date (yyyy-mm-dd):\n")
        if validate_date(p_end_date):
            break
        else:
            print("Please enter a valid project end date\n")

    p_data = {"p_title": p_title, "p_details": p_details, "p_target": p_target,
              "p_start_date": p_start_date, "p_end_date": p_end_date}
    append_to_file("projects", json.dumps(p_data))
    old_user_data = copy.deepcopy(logged_user)
    logged_user["projects"].append(p_title)
    with open("reg_users", "r") as file:
        users = file.readlines()
    with open("reg_users", "w") as file:
        for user in users:
            if ast.literal_eval(user.strip()) == old_user_data:
                continue
            else:
                file.write(user)
        file.write(json.dumps(logged_user))


def search_projects():
    search_method = int(input("Enter 1 to search by project title,\n2 to search by project start date\n"))
    if search_method == 1:
        search_title = input("Enter project title to search with: ")
        search_result = []
        with open("projects", "r") as f:
            projects = f.readlines()
            for project in projects:
                current_project_dict = ast.literal_eval(project.strip())
                if current_project_dict["p_title"] == search_title:
                    search_result.append(current_project_dict)
        return search_result
    elif search_method == 2:
        search_start_date = input("Enter project start date to search with (yyyy-mm-dd): ")
        if validate_date(search_start_date):
            search_result = []
            with open("projects", "r") as f:
                projects = f.readlines()
                for project in projects:
                    current_project_dict = ast.literal_eval(project.strip())
                    if current_project_dict["p_start_date"] == search_start_date:
                        search_result.append(current_project_dict)
            return search_result
        else:
            return "Please enter a valid date"
    else:
        return "Invalid input. Please enter 1 or 2 to make an action."


def view_projects():
    with open("projects", "r") as file:
        projects = file.readlines()
        for i, project in enumerate(projects):
            p_dict = ast.literal_eval(project.strip())
            p_num = i+1
            print("Project {} Title: {}".format(p_num, p_dict["p_title"]))
            print("Project {} Details: {}".format(p_num, p_dict["p_details"]))
            print("Project {} Total Target: {}".format(p_num, p_dict["p_target"]))
            print("Project {} Start Date: {}".format(p_num, p_dict["p_start_date"]))
            print("Project {} End Date: {}".format(p_num, p_dict["p_end_date"]))
            print("########################################################")


def delete_project(p_title):
    if p_title in logged_user["projects"]:
        with open("projects", "r") as file:
            projects = file.readlines()
        with open("projects", "w") as file:
            for project in projects:
                if ast.literal_eval(project.strip())["p_title"] != p_title:
                    file.write(project)
        print("Project '{}' deleted successfully".format(p_title))
    else:
        print("You can't delete a project that you didn't create")
    pass


# Main run


user_first_input = int(input("Enter 0 to register, 1 to login, or 2 to exit!\n"))

if user_first_input == 0:
    register()
elif user_first_input == 1:
    logged_user = login()
    while True:
        project_input = int(input("Enter 1 to create new project, 2 to list all projects,"
                                  "\n3 to search for a project, 4 to delete a project\nor 5 to exit\n"))
        if project_input == 1:
            create_project()
        elif project_input == 2:
            view_projects()
        elif project_input == 3:
            search_output = search_projects()
            if type(search_output) == list:
                if len(search_output) == 0:
                    print("No matches found")
                else:
                    print_projects(search_output)
            else:
                print(search_output)
        elif project_input == 4:
            p_title_del = input("Enter the title of the project you want to delete: ")
            delete_project(p_title_del)
        elif project_input == 5:
            break
        else:
            print("Invalid input. Please enter 1 or 2 or 3 or 4 to make an action.")
elif user_first_input == 2:
    exit()
else:
    print("Invalid input. Please enter 0 or 1 or 2 to make an action.")




