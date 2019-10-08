import os
import pickle


class Employeemanager:

    total_employees = 0
    employee_list = []
    default_pay = 20000

    def __init__(self, restore=True, filename="employeelist.db"):
        if restore is True and os.path.exists(filename):
            print("found existing database file")
            with open(filename, "rb") as db:
                Employeemanager.employee_list = pickle.load(db)
        else:
            print("database file was not found. creating a new one")
            with open(filename, "xb") as db:
                pickle.dump(Employeemanager.employee_list, db)

    @classmethod
    def save_db(cls):
        with open("employeelist.db", "wb") as db:
            pickle.dump(cls.employee_list, db)

    @classmethod
    def create_employee(cls, fname="", lname="", position="", pay=None):
        if position.title() == "Manager":
            emp = cls.Manager()
        elif position.title() == "Superhero":
            emp = cls.Superhero()
        elif position.title() == "Intern":
            emp = cls.Intern()
        elif position.title() == "Ceo":
            emp = cls.Ceo()
        else:
            emp = cls.Employee()
            emp.position = "{} ({})".format(position.title(), emp.position.title())
        emp.fname = fname.title()
        emp.lname = lname.title()
        if pay is None:
            emp.pay = cls.default_pay
        else:
            emp.pay = pay
        emp_exists = False
        for cur_emp in cls.employee_list:
            if cur_emp.fname == emp.fname and cur_emp.lname == emp.lname:
                emp_exists = True
        if emp_exists is False:
            cls.employee_list.append(emp)
            cls.total_employees = len(cls.employee_list)
            print("created {}: {} {}".format(emp.position, emp.fname, emp.lname))
        else:
            print("Employee with name {} {} already exists".format(emp.fname, emp.lname))

    @classmethod
    def create_employees_from_list(cls, emp_list):
        for emps in emp_list:
            if len(emps) > 3:
                Employeemanager.create_employee(emps[0], emps[1], emps[2], emps[3])
            else:
                Employeemanager.create_employee(emps[0], emps[1], emps[2])

    @classmethod
    def remove_employee_by_name(cls, fname, lname):
        fname = fname.title()
        lname = lname.title()
        emp_to_remove = -1
        for i, emp in enumerate(cls.employee_list):
            if fname == emp.fname and lname == emp.lname:
                emp_to_remove = i
        if emp_to_remove > -1:
            cls.employee_list[emp_to_remove].show_details()
            print("remove this employee? (type 'yes' and hit enter to remove. anything else will cancel)")
            user_resp = input()
            if user_resp == "yes":
                del cls.employee_list[emp_to_remove]
                print("removed", fname, lname)
                cls.total_employees = len(cls.employee_list)
            else:
                print("remove is cancelled")
        else:
            print("No employee found with that name")

    @classmethod
    def list_all(cls, dept=None):
        list_total = 0
        print("listing all", end=" ")
        if dept is not None:
            dept = dept.lower()
            print("in dept", dept)
        else:
            print("")
        for emp in cls.employee_list:
            if dept is None or emp.position.lower().find(dept) >= 0:
                emp.show_details()
                list_total += 1
        print("listed ", list_total, "/", len(cls.employee_list), " employee(s)", sep="")

    @staticmethod
    def calculate_percent(first, second):
        result = (second / first) * 100 - 100
        tail = "% increase" if result >= 0 else "% decrease"
        result = -result if result < 0 else result
        return str(round(result, 1)) + tail

    class Employee:
        """Base employee class"""
        def __init__(self):
            self.fname = "None"
            self.lname = "None"
            self.position = "Generic"
            self.pay = 0

        @staticmethod
        def add_string_padding(string="", target_length=10):
            pad = " "
            pad_count = int(target_length - len(string))
            if pad_count > 0:
                string += pad*pad_count
            return string

        def show_details(self):
            name_string = self.add_string_padding("Name: " + self.fname + " " + self.lname, target_length=25)
            position_string = self.add_string_padding("Position: " + self.position, target_length=34)
            pay_string = self.add_string_padding("Pay: " + str(self.pay), target_length=15)
            increase_string = Employeemanager.calculate_percent(Employeemanager.default_pay, self.pay)

            print(name_string + position_string + pay_string + increase_string)

    class Manager(Employee):

        def __init__(self):
            super().__init__()
            self.position = "Manager"
            self.managed_employees = []

    class Superhero(Employee):

        def __init__(self):
            super().__init__()
            self.position = "Superhero"
            self.people_saved = 0

    class Intern(Employee):

        def __init__(self):
            super().__init__()
            self.position = "Intern"
            self.people_annoyed = 0

    class Ceo(Employee):

        def __init__(self):
            super().__init__()
            self.position = "Ceo"
            self.people_fired = 0

    @staticmethod
    def display_menu():
        print("")
        print("1) List all Employees")
        print("2) List all employees in dept")
        print("3) Add employee")
        print("4) Remove employee")
        print("5) Save current employees")
        print("6) Exit")
        print("")
        user_resp = input("Choose an option: ")
        print("")
        return user_resp


class Config:
    config_order = []
    config = {"users_allowed": "5", "desc_string": "configs", "verbose": "0",
              "server_ip": "192.168.0.1", "random_option": "1"}

    @classmethod
    def load_config(cls):
        try:
            with open("config.cfg", "r") as cfg_file:
                config_order = []
                for line in cfg_file:
                    entry = line.split(sep="=")
                    param = entry[0].strip()
                    value = entry[1].strip()
                    cls.config[param] = value
                    config_order.append(param)
                cls.config_order = config_order
                print("found existing config file")
        except IOError as error:
            print("config file error:", error)
            print("using default config")

    @classmethod
    def show_config(cls):
        print("")
        print("****config file settings****")
        for i in cls.config_order:
            if i in cls.config.keys():
                print("{} = {}".format(i, cls.config[i]))
        has_unconfigured_settings = False
        for i in cls.config:
            if i not in cls.config_order:
                has_unconfigured_settings = True
                break
        else:
            print("")
            print("no unconfigured settings")
        if has_unconfigured_settings:
            print("")
            print("****unconfigured settings****")
            for i in cls.config:
                if i not in cls.config_order:
                    print("{} = {}".format(i, cls.config[i]))


empdb = Employeemanager()
config = Config()
config.load_config()
config.show_config()

while True:
    u_resp = empdb.display_menu()
    if u_resp == "1":
        empdb.list_all()
    elif u_resp == "2":
        u_dept = input("Dept to list: ")
        empdb.list_all(u_dept)
    elif u_resp == "3":
        u_fname = input("First Name: ")
        u_lname = input("Last Name: ")
        u_position = input("Position: ")
        u_pay = input("Yearly Salary (blank for default): ")
        if u_pay == "":
            u_pay = None
        else:
            u_pay = int(u_pay)
        empdb.create_employee(u_fname, u_lname, u_position, u_pay)
    elif u_resp == "4":
        u_fname = input("First Name: ")
        u_lname = input("Last Name: ")
        empdb.remove_employee_by_name(u_fname, u_lname)
    elif u_resp == "5":
        empdb.save_db()
        print("saved {} records".format(empdb.total_employees))
    elif u_resp == "6":
        empdb.save_db()
        print("Goodbye!")
        exit()
