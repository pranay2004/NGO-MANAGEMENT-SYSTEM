import customtkinter , tkinter as tk , admin_auth , random , sqlite3 , os , datetime , re, pandas as pd
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox

customtkinter.set_appearance_mode("black")  
customtkinter.set_default_color_theme("dark-blue")

def save_employee_data(user_id, password, firstname, lastname, dob,  email, phone, alt_phone, education, skills, experience, address1, address2, district, pin):
    conn = sqlite3.connect('employee_database.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS employees (
                userid INTEGER PRIMARY KEY,
                password VARCHAR(255),
                firstname TEXT,
                lastname TEXT,
                dob VARCHAR(10),
                email VARCHAR(100),
                phone INTEGER,
                alt_phone INTEGER,
                education VARCHAR(200),
                skills VARCHAR(200),
                experience TEXT,
                address1 VARCHAR(200),
                address2 VARCHAR(200),
                district TEXT,
                pin INTEGER(6)
                )""")
    c.execute(f"""CREATE TABLE IF NOT EXISTS user_{user_id} (
                date TIMESTAMP NOT NULL,
                present INTEGER(1),
                absent INTEGER(1),
                leave INTEGER(1)
              )""")

    c.execute("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)",
              (user_id, password, firstname, lastname, dob, email, phone, alt_phone, education, skills, experience, address1, address2, district, pin))

    conn.commit()
    conn.close()

def main():

    def forward_to_login_page():
        app.destroy()
        app.update()
        login_page()

    def forward_to_admin_page():
        app.destroy()
        app.update()
        admin_page()

    app = customtkinter.CTk()
    app.geometry("720x480")
    app.title("welcome")
    app.resizable(False, False)

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x_coordinate = (screen_width / 2) - (400 / 2)
    y_coordinate = (screen_height / 2) - (480 / 2)

    app.geometry(f"{720}x{480}+{int(x_coordinate)}+{int(y_coordinate)}")

    title = customtkinter.CTkLabel(app, text="CHOOSE AN OPTION BELOW", font=("Arial",32), text_color="steelblue4")
    title.pack(padx= 5, pady=60)

    login_img = Image.open('user_icon.png')
    login_image = customtkinter.CTkImage(light_image=login_img, size=(125, 120))
    login_img_label = customtkinter.CTkLabel(app, text="", image=login_image)
    login_img_label.place(relx=0.3, rely=0.45, anchor=tk.CENTER)

    login_btn = customtkinter.CTkButton(app, text="USER LOGIN", width=200, height=50, font=("bold", 24), cursor = "hand2", command=forward_to_login_page)
    login_btn.place(relx=0.3, rely=0.65, anchor=tk.CENTER)

    admin_img = Image.open('admin.png')
    admin_image = customtkinter.CTkImage(light_image=admin_img, size=(130, 130))
    admin_img_label = customtkinter.CTkLabel(app, text="", image=admin_image)
    admin_img_label.place(relx=0.7, rely=0.46, anchor=tk.CENTER)

    admin_btn = customtkinter.CTkButton(app, text="ADMIN LOGIN", width=200, height=50, font=("bold", 24), cursor = "hand2", command=forward_to_admin_page)
    admin_btn.place(relx=0.7, rely=0.65, anchor=tk.CENTER)

    note_text = f"*NOTE: 1. If you are an EMPLOYEE then click USER LOGIN option. \n     2. If you are an ADMIN then click ADMIN LOGIN option."
    note = customtkinter.CTkLabel(app, text=note_text, font=("italic",12), text_color="gray")
    note.place(relx=0.02, rely=0.93, anchor=tk.W)

    trade_mark = customtkinter.CTkLabel(app, text="@PC", font=("italic",12), text_color="dimgray")
    trade_mark.place(relx=0.95, rely=0.95, anchor=tk.CENTER)

    app.mainloop()

def login_page():

    def forward_to_main_page():
        app.destroy()
        app.update()
        main()

    def toggle_show_password():
        if show_password_var.get():
            pwd_box.configure(show="")
        else:
            pwd_box.configure(show="#")

    def validate_input_userid(input_text):
        return len(input_text) <= 10 
    
    def validate_input_pwd(input_text):
        return len(input_text) <= 25

    app = customtkinter.CTk()
    app.geometry("400x480")
    app.title("LOGIN PAGE")
    app.resizable(False, False)

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x_coordinate = (screen_width / 2) - (400 / 2)
    y_coordinate = (screen_height / 2) - (480 / 2)

    app.geometry(f"{400}x{480}+{int(x_coordinate)}+{int(y_coordinate)}")


    login_img = Image.open('user_icon.png')
    login_image = customtkinter.CTkImage(light_image=login_img, size=(125, 120))
    login_img_label = customtkinter.CTkLabel(app, text="", image=login_image)
    login_img_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    userid_box_text = customtkinter.CTkLabel(app, text="USER ID/Phone Number:-", font=("Arial",14), text_color="medium sea green")
    userid_box_text.place(relx=0.21, rely=0.4)
    userid_box = customtkinter.CTkEntry(app, width=250, height=30, validate="key", validatecommand=(app.register(validate_input_userid), "%P")) 
    userid_box.place(relx=0.2, rely=0.45)

    pwd_box_text = customtkinter.CTkLabel(app, text="PASSWORD:-", font=("Arial",14), text_color="medium sea green")
    pwd_box_text.place(relx=0.21, rely=0.55)
    pwd_box = customtkinter.CTkEntry(app, width=250, height=30, show="#", validate="key", validatecommand=(app.register(validate_input_pwd), "%P"))
    pwd_box.place(relx=0.2, rely=0.6)
    

    show_password_var = tk.BooleanVar()
    show_password_check = customtkinter.CTkCheckBox(app, text="Show Password", variable=show_password_var,onvalue=True, 
                                                    offvalue=False,command=toggle_show_password, font=("arial",16))
    show_password_check.place(relx=0.22, rely=0.68)

    trade_mark = customtkinter.CTkLabel(app, text="@PC", font=("italic",10), text_color="dimgray")
    trade_mark.place(relx=0.95, rely=0.97, anchor=tk.CENTER)

    def access():
        global userid_login_page,pwd_login_page
        userid_login_page = userid_box.get()
        pwd_login_page = pwd_box.get()
        try:
            conn = sqlite3.connect('employee_database.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT password FROM employees WHERE userid = ?", (userid_login_page,))
            pwd = cursor.fetchone()
            if pwd:
                if pwd[0] == pwd_login_page:
                    app.destroy()
                    app.update()
                    user_panel()
                else:
                    messagebox.showerror("ERROR", "Invalid password")
            else:
                messagebox.showerror("ERROR", "Invalid user ID")
        except sqlite3.Error as e:
            messagebox.showerror("ERROR", str(e))
        finally:
            conn.close()
    
    login_btn = customtkinter.CTkButton(app, text="LOGIN", width=200, height=40, font=("bold", 24), cursor = "hand2", command=access)
    login_btn.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
    login_btn.bind("<Return>", lambda event: access())

    back_img = Image.open('back.png')
    back_image = customtkinter.CTkImage(light_image=back_img, size=(50, 50))
    back_img_btn = customtkinter.CTkButton(app, text="", image=back_image, cursor="hand2", fg_color="transparent", hover_color="grey10",width=50,height=50, command=forward_to_main_page)
    back_img_btn.place(relx=0.1, rely=0.08, anchor=tk.CENTER)

    app.mainloop()

incorrect_attempts = 0
def admin_page():
    def forward_to_main_page():
        app.destroy()
        app.update()
        main()

    def toggle_show_password():
        if show_password_var.get():
            pwd_box.configure(show="")
        else:
            pwd_box.configure(show="#")

    def validate_input_userid(input_text):
        return len(input_text) <= 10
    
    def validate_input_pwd(input_text):
        return len(input_text) <= 25
    
    def admin_panel_access():
            adminid_box_text = adminid_box.get()
            pwd_box_text = pwd_box.get()

            if adminid_box_text == "adim" and pwd_box_text == "admin":
                app.destroy()
                app.update()
                admin_panel()
            
            elif adminid_box_text!= "adim" or pwd_box_text!= "admin":
                error_message_text = f"Invalid ID or password"
                error_message = customtkinter.CTkLabel(app, text=error_message_text, font=("Arial", 12), text_color="red")
                error_message.place(relx=0.5, rely=0.82, anchor=tk.CENTER)

            else:
                admin_panel_access()

    app = customtkinter.CTk()
    app.geometry("400x480")
    app.title("ADMIN PAGE")
    app.resizable(False, False)

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x_coordinate = (screen_width / 2) - (400 / 2)
    y_coordinate = (screen_height / 2) - (480 / 2)

    app.geometry(f"{400}x{480}+{int(x_coordinate)}+{int(y_coordinate)}")


    admin_img = Image.open('admin.png')
    admin_image = customtkinter.CTkImage(light_image=admin_img, size=(125, 120))
    admin_img_label = customtkinter.CTkLabel(app, text="", image=admin_image)
    admin_img_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    adminid_box_text = customtkinter.CTkLabel(app, text="ADMIN ID:-", font=("Arial",14), text_color="medium sea green")
    adminid_box_text.place(relx=0.21, rely=0.35)
    adminid_box = customtkinter.CTkEntry(app, width=250, height=30, validate="key", validatecommand=(app.register(validate_input_userid), "%P")) 
    adminid_box.place(relx=0.2, rely=0.4)

    pwd_box_text = customtkinter.CTkLabel(app, text="PASSWORD:-", font=("Arial",14), text_color="medium sea green")
    pwd_box_text.place(relx=0.21, rely=0.5)
    pwd_box = customtkinter.CTkEntry(app, width=250, height=30, show="#", validate="key", validatecommand=(app.register(validate_input_pwd), "%P"))
    pwd_box.place(relx=0.2, rely=0.55)

    show_password_var = tk.BooleanVar()
    show_password_check = customtkinter.CTkCheckBox(app, text="Show Password", variable=show_password_var,onvalue=True, 
                                                    offvalue=False,command=toggle_show_password, font=("arial",16))
    show_password_check.place(relx=0.22, rely=0.64)

    trade_mark = customtkinter.CTkLabel(app, text="@PC", font=("italic",10), text_color="dimgray")
    trade_mark.place(relx=0.95, rely=0.97, anchor=tk.CENTER)

    login_btn = customtkinter.CTkButton(app, text="LOGIN", width=200, height=40, font=("bold", 24), cursor = "hand2", command=admin_panel_access)
    login_btn.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
    login_btn.bind("<Return>", lambda event: admin_panel_access())

    back_img = Image.open('back.png')
    back_image = customtkinter.CTkImage(light_image=back_img, size=(50, 50))
    back_img_btn = customtkinter.CTkButton(app, text="", image=back_image, cursor="hand2", fg_color="transparent", hover_color="grey10",width=50,height=50, command=forward_to_main_page)
    back_img_btn.place(relx=0.1, rely=0.08, anchor=tk.CENTER)

    note_text = f"*NOTE: Please remember the credentials. You will not be able to reset \n password without loging in."
    note = customtkinter.CTkLabel(app, text=note_text, font=("italic",12), text_color="gray")
    note.place(relx=0.03, rely=0.9, anchor=tk.W)

    app.mainloop()



###########################################-----ADMIN PANEL FUNCTIONS -----#################################################

def admin_panel():

    def forward_to_main_page():
        app.destroy()
        app.update()
        main()
    
    def forward_to_add_employee_page():
        app.destroy()
        app.update()
        add_employee()

    def forward_to_attendence_page():
        app.destroy()
        app.update()
        attendence()

    def forward_to_download_record_page():
        app.destroy()
        app.update()
        download_record()

    def forward_to_edit_record_page():
        app.destroy()
        app.update()
        edit_record()    

    
    app = customtkinter.CTk()
    app.geometry("720x500")
    app.title("ADMIN PANEL")
    app.resizable(False, False)

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x_coordinate = (screen_width / 2) - (400 / 2)
    y_coordinate = (screen_height / 2) - (480 / 2)

    app.geometry(f"{720}x{500}+{int(x_coordinate)}+{int(y_coordinate)}")

    back_img = Image.open('back.png')
    back_image = customtkinter.CTkImage(light_image=back_img, size=(50, 50))
    back_img_btn = customtkinter.CTkButton(app, text="", image=back_image, cursor="hand2", fg_color="transparent", hover_color="grey10",width=50,height=50, command=forward_to_main_page)
    back_img_btn.place(relx=0.06, rely=0.08, anchor=tk.CENTER)

    admin_lable = customtkinter.CTkLabel(app, text=("WELCOME ADMIN "), font=("Arial", 42), text_color="steelblue4")
    admin_lable.place(relx=0.5, rely=0.08, anchor=tk.CENTER)

    add_employee_img = Image.open('add_employee.png')
    add_employee_image = customtkinter.CTkImage(light_image=add_employee_img, size=(100, 100))
    add_employee_img_label = customtkinter.CTkLabel(app, text="", image=add_employee_image)
    add_employee_img_label.place(relx=0.3, rely=0.34, anchor=tk.CENTER)
    add_employee_btn = customtkinter.CTkButton(app, text="Add Employee", width=200, height=40, font=("bold", 24), cursor = "hand2", command=forward_to_add_employee_page)
    add_employee_btn.place(relx=0.3, rely=0.48, anchor=tk.CENTER)

    attendence_img = Image.open('attendence.png')
    attendence_image = customtkinter.CTkImage(light_image=attendence_img, size=(100, 100))
    attendence_img_label = customtkinter.CTkLabel(app, text="", image=attendence_image)
    attendence_img_label.place(relx=0.7, rely=0.34, anchor=tk.CENTER)
    attendence_btn = customtkinter.CTkButton(app, text="Attendence", width=200, height=40, font=("bold", 24), cursor = "hand2", command=forward_to_attendence_page)
    attendence_btn.place(relx=0.7, rely=0.48, anchor=tk.CENTER)

    download_record_img = Image.open('download_record.png')
    download_record_image = customtkinter.CTkImage(light_image=download_record_img, size=(100, 100))
    download_record_img_label = customtkinter.CTkLabel(app, text="", image=download_record_image)
    download_record_img_label.place(relx=0.3, rely=0.66, anchor=tk.CENTER)
    download_record_btn = customtkinter.CTkButton(app, text="Download Record", width=200, height=40, font=("bold", 24), cursor = "hand2", command=forward_to_download_record_page)
    download_record_btn.place(relx=0.3, rely=0.80, anchor=tk.CENTER)

    edit_record_img = Image.open('edit_record.png')
    edit_record_image = customtkinter.CTkImage(light_image=edit_record_img, size=(90, 90))
    edit_record_img_label = customtkinter.CTkLabel(app, text="", image=edit_record_image)
    edit_record_img_label.place(relx=0.7, rely=0.66, anchor=tk.CENTER)
    edit_record_btn = customtkinter.CTkButton(app, text="Edit Record", width=200, height=40, font=("bold", 24), cursor = "hand2", command=forward_to_edit_record_page)
    edit_record_btn.place(relx=0.7, rely=0.80, anchor=tk.CENTER)

    trade_mark = customtkinter.CTkLabel(app, text="@PC", font=("italic",10), text_color="dimgray")
    trade_mark.place(relx=0.97, rely=0.97, anchor=tk.CENTER)

    app.mainloop()



def add_employee():

    def generate_unique_number():
        number = str(random.randint(100000,999999))

        conn = sqlite3.connect('employee_database.db')
        cursor = conn.cursor()
        search = cursor.execute("SELECT userid FROM employees")

        if number != search:
            return  number

    def forward_to_admin_panel():
        app.destroy()
        app.update()
        admin_panel()

    def upload_picture():
        global file_path
        file_path = filedialog.askopenfilename(initialdir="/", title="Select Image", filetypes=(("Image Files", "*.jpg;*.png"), ("All Files", "*.*")))
        if file_path:
            global user_image
            user_image = ImageTk.PhotoImage(Image.open(file_path).resize((200,200)))
            user_img_btn.configure(image=user_image)
            global userid
            userid = userid_box.get()
    
    def validate_email(email):
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(pattern, email):
                return True
            else:
                return False

    def validate_phone_number(phone):
        pattern = r'^[0-9]{10}$'
        if re.match(pattern, phone):
            return True
        else:
            return False

    def validate_pin_code(pin_code):
        pattern = r'^[0-9]{6}$'
        if re.match(pattern, pin_code):
            return True
        else:
            return False

    
    def add_employee_data():

        user_id = userid_box.get()
        password = "password"
        firstname = firstname_box.get()
        lastname = lastname_box.get()
        dob = dob_box.get()
        email = email_box.get()
        phone = phone_box.get()
        alt_phone = alt_phone_box.get()
        education = education_box.get()
        skills = skills_box.get()
        experience = experience_var.get()
        address_1 = address1.get()
        address_2 = address2.get()
        district_name = district.get()
        pin_code = pin.get()

        image_name = f"{userid}.jpg"
        image_path = os.path.join("images", image_name)
        if os.path.exists(image_path):
            os.remove(image_path)
        Image.open(file_path).resize((200, 200)).save(image_path)

        if not user_id or not firstname or not lastname or not email or not phone or not alt_phone or not education or not skills or not experience or not address_1 or not address_2 or not district_name or not pin_code:
            messagebox.showerror("Error", "Please fill in all the required fields.")
            return False

        if not validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return False

        if not validate_phone_number(phone) or not validate_phone_number(alt_phone):
            messagebox.showerror("Error", "Please enter a valid phone number.")
            return False

        if not validate_pin_code(pin_code):
            messagebox.showerror("Error", "Please enter a valid pin code.")
            return False

        save_employee_data(user_id, password, firstname, lastname, dob, email, phone, alt_phone, education, skills, experience, address_1, address_2, district_name, pin_code)
        app.update()
        app.destroy()
        add_employee()

    def validate_input_number(input_text):
        if len(input_text) <= 10 and input_text.isdigit():
            return True
        else:
            return False
    
    def validate_input_pincode(input_text):
        if len(input_text) <= 6 and input_text.isdigit():
            return True
        else:
            return False

    app = customtkinter.CTk()
    app.geometry("900x750")
    app.title("ADD EMPLOYEE")
    app.resizable(False, False)

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x_coordinate = (screen_width / 2) - (750 / 2)
    y_coordinate = (screen_height / 2) - (800 / 2)

    app.geometry(f"{900}x{750}+{int(x_coordinate)}+{int(y_coordinate)}")

    back_img = Image.open('back.png')
    back_image = customtkinter.CTkImage(light_image=back_img, size=(50, 50))
    back_img_btn = customtkinter.CTkButton(app, text="", image=back_image, cursor="hand2", fg_color="transparent", hover_color="grey10",width=50,height=50, command=forward_to_admin_panel)
    back_img_btn.place(relx=0.04, rely=0.05, anchor=tk.CENTER)

    title = customtkinter.CTkLabel(app, text="ADD EMPLOYEE:-", font=("Arial",32), text_color="orangered")
    title.place(relx=0.25, rely=0.05, anchor=tk.CENTER)

    userid_label = customtkinter.CTkLabel(app, text=f"User ID:", font=("Arial", 18), text_color="orange")
    userid_label.place(relx=0.8, rely=0.2, anchor=customtkinter.CENTER)
    userid_box = customtkinter.CTkEntry(app, width=75, height=35, font=("Arial",18))
    userid_box.insert(0, generate_unique_number())
    userid_box.configure(state = "readonly")
    userid_box.place(relx=0.9, rely=0.2, anchor=customtkinter.CENTER)

    user_img = Image.open('user.png')
    user_image = customtkinter.CTkImage(light_image=user_img, size=(200, 200))
    user_img_btn = customtkinter.CTkButton(app, text="", image=user_image, cursor="hand2", fg_color="transparent", hover_color="grey10",width=50,height=50, command=upload_picture)
    user_img_btn.place(relx=0.855, rely=0.4, anchor=tk.CENTER)

    user_img_text = customtkinter.CTkLabel(app, text="Click to upload the \n picture of the employee.", font=("Arial",16), text_color="orange")
    user_img_text.place(relx=0.76, rely=0.54)

    note = customtkinter.CTkLabel(app, text="NOTE:- The default password for the \n     employee is 'password'.", font=("Arial",14), text_color="grey")
    note.place(relx=0.15, rely=0.95, anchor=tk.CENTER)

    firstname_box_text = customtkinter.CTkLabel(app, text="First Name:-", font=("Arial",18), text_color="medium sea green")
    firstname_box_text.place(relx=0.054, rely=0.15)
    firstname_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    firstname_box.place(relx=0.05, rely=0.185)

    lastname_box_text = customtkinter.CTkLabel(app, text="Last Name:-", font=("Arial",18), text_color="medium sea green")
    lastname_box_text.place(relx=0.054, rely=0.25)
    lastname_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    lastname_box.place(relx=0.05, rely=0.285)

    dob_box_text = customtkinter.CTkLabel(app, text="Date of Birth:-    (dd/mm/yy)", font=("Arial",18), text_color="medium sea green")
    dob_box_text.place(relx=0.054, rely=0.35)
    dob_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    dob_box.place(relx=0.05, rely=0.385)

    email_box_text = customtkinter.CTkLabel(app, text="Email ID:-", font=("Arial",18), text_color="medium sea green")
    email_box_text.place(relx=0.054, rely=0.5)
    email_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    email_box.place(relx=0.05, rely=0.535)

    phone_box_text = customtkinter.CTkLabel(app, text="Phone Number:-", font=("Arial",18), text_color="medium sea green")
    phone_box_text.place(relx=0.054, rely=0.6)
    phone_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18), validate="key", validatecommand=(app.register(validate_input_number), "%P"))
    phone_box.place(relx=0.05, rely=0.635)

    alt_phone_box_text = customtkinter.CTkLabel(app, text="Alternate Phone Number:-", font=("Arial",18), text_color="medium sea green")
    alt_phone_box_text.place(relx=0.054, rely=0.7)
    alt_phone_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18), validate="key", validatecommand=(app.register(validate_input_number), "%P"))
    alt_phone_box.place(relx=0.05, rely=0.735)

    education_box_text = customtkinter.CTkLabel(app, text="Education Details:-", font=("Arial",18), text_color="medium sea green")
    education_box_text.place(relx=0.404, rely=0.15)
    education_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    education_box.place(relx=0.4, rely=0.185)

    skills_box_text = customtkinter.CTkLabel(app, text="Skills:-", font=("Arial",18), text_color="medium sea green")
    skills_box_text.place(relx=0.404, rely=0.25)
    skills_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    skills_box.place(relx=0.40, rely=0.285)

    experience_box_text = customtkinter.CTkLabel(app, text="Experience Level:-", font=("Arial",18), text_color="medium sea green")
    experience_box_text.place(relx=0.404, rely=0.35)
    experience_options = ["Fresher", "1 Year", "2 Year", "3 Year", "+3 Year"]
    experience_var = tk.StringVar()
    experience_var.set(experience_options[0])  
    experience_box = customtkinter.CTkComboBox(app, values=experience_options, width=280, height=35, font=("Arial",18))
    experience_box.configure(state = "readonly")
    experience_box.place(relx=0.40, rely=0.385)

    address1_text = customtkinter.CTkLabel(app, text="Address 1:-", font=("Arial",18), text_color="medium sea green")
    address1_text.place(relx=0.404, rely=0.5)
    address1 = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    address1.place(relx=0.40, rely=0.535)

    address2_text = customtkinter.CTkLabel(app, text="Address 2:-", font=("Arial",18), text_color="medium sea green")
    address2_text.place(relx=0.404, rely=0.6)
    address2 = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    address2.place(relx=0.40, rely=0.635)

    district_text = customtkinter.CTkLabel(app, text="District:-", font=("Arial",18), text_color="medium sea green")
    district_text.place(relx=0.404, rely=0.7)
    district = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    district.place(relx=0.40, rely=0.735)

    pin_text = customtkinter.CTkLabel(app, text="Pin Code:-", font=("Arial",18), text_color="medium sea green")
    pin_text.place(relx=0.404, rely=0.8)
    pin = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18), validate="key", validatecommand=(app.register(validate_input_pincode), "%P"))
    pin.place(relx=0.40, rely=0.835)    

    submit_btn = customtkinter.CTkButton(app, text="SUBMIT", width=200, height=40, font=("bold", 24), cursor = "hand2", command=add_employee_data)
    submit_btn.place(relx=0.52, rely=0.95, anchor=tk.CENTER)

    trade_mark = customtkinter.CTkLabel(app, text="@PC", font=("italic",10), text_color="dimgray")
    trade_mark.place(relx=0.97, rely=0.97, anchor=tk.CENTER)

    app.mainloop()

def attendence():

    def forward_to_admin_panel():
        app.destroy()
        app.update()
        admin_panel()
    
    def search():
        user_id = userid_box.get()
        
        conn = sqlite3.connect('employee_database.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT firstname, lastname, email, phone FROM employees WHERE userid=?", (user_id,))
        user_details = cursor.fetchone()
        
        if user_details:
            firstname, lastname, email, phone, = user_details
            
            firstname_box.configure(state = "normal")
            firstname_box.delete(0, tk.END)
            firstname_box.insert(0, firstname)
            firstname_box.configure(state = "readonly")

            lastname_box.delete(0, tk.END)
            lastname_box.configure(state = "normal")
            lastname_box.insert(0, lastname)
            lastname_box.configure(state = "readonly")

            email_box.delete(0, tk.END)
            email_box.configure(state = "normal")
            email_box.insert(0, email)
            email_box.configure(state = "readonly")

            phone_box.delete(0, tk.END)
            phone_box.configure(state = "normal")
            phone_box.insert(0, phone)
            phone_box.configure(state = "readonly")

            image_path = f"./images/{user_id}.jpg"
            if os.path.exists(image_path):
                try:
                    user_image = Image.open(image_path)
                    #user_image = user_image.resize((200, 200))
                    user_image = ImageTk.PhotoImage(user_image)
                    user_img_lable.configure(image=user_image)
                    user_img_lable.image = user_image
                except IOError:
                    messagebox.showerror("ERROR", "Failed to load image")
            else:
                messagebox.showerror("ERROR", "Image file not found")
        else:
            messagebox.showerror("ERROR","User ID not found in the database")

        conn.close()

    def validate_input_userid(input_text):
        if len(input_text) <= 6:
            return True
        else:
            return False 
    
    def present():
        user_id = userid_box.get()
        date = date_box.get()

        conn = sqlite3.connect('employee_database.db')
        c = conn.cursor()

        table_id = f"user_{user_id}"

        c.execute(f"""INSERT INTO {table_id} (date,present,absent,leave)
                  values(?,?,?,?)""",(date,1,0,0))

        conn.commit()
        conn.close()
        app.update()
        app.destroy()
        attendence()
    
    def absent():
        user_id = userid_box.get()
        date = date_box.get()

        conn = sqlite3.connect('employee_database.db')
        c = conn.cursor()

        table_id = f"user_{user_id}"

        c.execute(f"""INSERT INTO {table_id} (date,present,absent,leave)
                  values(?,?,?,?)""",(date,0,1,0))
        
        conn.commit()
        conn.close()
        app.update()
        app.destroy()
        attendence()
    
    def leave():
        user_id = userid_box.get()
        date = date_box.get()

        conn = sqlite3.connect('employee_database.db')
        c = conn.cursor()

        table_id = f"user_{user_id}"

        c.execute(f"""INSERT INTO {table_id} (date,present,absent,leave)
                  values(?,?,?,?)""",(date,0,0,1))
        
        conn.commit()
        conn.close()
        app.update()
        app.destroy()
        attendence()

    app = customtkinter.CTk()
    app.geometry("800x550")
    app.title("ATTENDENCE")
    app.resizable(False, False)

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x_coordinate = (screen_width / 2) - (500 / 2)
    y_coordinate = (screen_height / 2) - (600 / 2)

    app.geometry(f"{800}x{550}+{int(x_coordinate)}+{int(y_coordinate)}")

    back_img = Image.open('back.png')
    back_image = customtkinter.CTkImage(light_image=back_img, size=(50, 50))
    back_img_btn = customtkinter.CTkButton(app, text="", image=back_image, cursor="hand2", fg_color="transparent", hover_color="grey10",width=50,height=50, command=forward_to_admin_panel)
    back_img_btn.place(relx=0.045, rely=0.06, anchor=tk.CENTER)

    title = customtkinter.CTkLabel(app, text="ATTENDENCE:-", font=("Arial",32), text_color="orangered")
    title.place(relx=0.25, rely=0.06, anchor=tk.CENTER)

    date_box = customtkinter.CTkEntry(app, width=104, height=35, font=("Arial",18))
    date_box.insert(0, datetime.date.today())
    date_box.configure(state = "readonly")
    date_box.place(relx=0.8, rely=0.06, anchor=customtkinter.CENTER)

    userid_label = customtkinter.CTkLabel(app, text=f"User ID:", font=("Arial", 18), text_color="orange")
    userid_label.place(relx=0.32, rely=0.2, anchor=customtkinter.CENTER)
    userid_box = customtkinter.CTkEntry(app, width=200, height=35, font=("Arial",18), validate="key", validatecommand=(app.register(validate_input_userid), "%P"))
    userid_box.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)
    userid_search_btn = customtkinter.CTkButton(app, text="SEARCH", cursor="hand2", width=80, height=30, command=search)
    userid_search_btn.place(relx=0.7, rely=0.2, anchor=tk.CENTER)
    userid_box.bind("<Return>", lambda event: search())

    user_img = Image.open('user.png')
    user_image = customtkinter.CTkImage(light_image=user_img, size=(200, 200))
    user_img_lable = customtkinter.CTkLabel(app, text="", image=user_image)
    user_img_lable.place(relx=0.2, rely=0.5, anchor=tk.CENTER)

    firstname_box_text = customtkinter.CTkLabel(app, text="First Name :", font=("Arial",18), text_color="medium sea green")
    firstname_box_text.place(relx=0.32, rely=0.33)
    firstname_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    firstname_box.configure(state = "readonly")
    firstname_box.place(relx=0.45, rely=0.33)

    lastname_box_text = customtkinter.CTkLabel(app, text="Last Name :", font=("Arial",18), text_color="medium sea green")
    lastname_box_text.place(relx=0.32, rely=0.43)
    lastname_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    lastname_box.configure(state = "readonly")
    lastname_box.place(relx=0.45, rely=0.43)

    email_box_text = customtkinter.CTkLabel(app, text="Email ID     :", font=("Arial",18), text_color="medium sea green")
    email_box_text.place(relx=0.32, rely=0.53)
    email_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    email_box.configure(state = "readonly")
    email_box.place(relx=0.45, rely=0.533)

    phone_box_text = customtkinter.CTkLabel(app, text="Phone No.  :", font=("Arial",18), text_color="medium sea green")
    phone_box_text.place(relx=0.32, rely=0.63)
    phone_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    phone_box.configure(state = "readonly")
    phone_box.place(relx=0.45, rely=0.63)

    present_btn = customtkinter.CTkButton(app, text="PRESENT", width=200, height=40, font=("bold", 24), cursor = "hand2", fg_color="green3", hover_color="green4", command=present)
    present_btn.place(relx=0.2, rely=0.85, anchor=tk.CENTER)

    absent_btn = customtkinter.CTkButton(app, text="ABSENT", width=200, height=40, font=("bold", 24), cursor = "hand2", fg_color="red2", hover_color="red3", command=absent)
    absent_btn.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

    leave_btn = customtkinter.CTkButton(app, text="LEAVE", width=200, height=40, font=("bold", 24), cursor = "hand2", fg_color="yellow3", hover_color="yellow4", command=leave)
    leave_btn.place(relx=0.8, rely=0.85, anchor=tk.CENTER)

    trade_mark = customtkinter.CTkLabel(app, text="@PC", font=("italic",10), text_color="dimgray")
    trade_mark.place(relx=0.97, rely=0.97, anchor=tk.CENTER)

    app.mainloop()

def download_record():
    def forward_to_admin_panel():
        app.destroy()
        app.update()
        admin_panel()

    def search():
        user_id = userid_box.get()
        
        conn = sqlite3.connect('employee_database.db')
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT firstname, lastname, email, phone FROM employees WHERE userid={user_id}")
        user_details = cursor.fetchone()
        
        if user_details:
            firstname, lastname = user_details[:2]
            
            firstname_box.configure(state = "normal")
            firstname_box.delete(0, tk.END)
            firstname_box.insert(0, firstname)
            firstname_box.configure(state = "readonly")

            lastname_box.delete(0, tk.END)
            lastname_box.configure(state = "normal")
            lastname_box.insert(0, lastname)
            lastname_box.configure(state = "readonly")

            image_path = f"./images/{user_id}.jpg"
            if os.path.exists(image_path):
                try:
                    user_image = Image.open(image_path)
                    user_image = ImageTk.PhotoImage(user_image)
                    user_img_lable.configure(image=user_image)
                    user_img_lable.image = user_image
                except IOError:
                    messagebox.showerror("ERROR", "Failed to load image")
            else:
                messagebox.showerror("ERROR", "Image file not found")
        else:
            messagebox.showerror("ERROR","User ID not found in the database")

        year = year_box.get()
        month = month_box.get()

        if month == "JANUARY":
            present = cursor.execute(f"SELECT sum(present) FROM user_{user_id} WHERE date LIKE '{year}-01%'").fetchone()[0]
            absent = cursor.execute(f"SELECT sum(absent) FROM user_{user_id} WHERE date LIKE '{year}-01%'").fetchone()[0]
            leave = cursor.execute(f"SELECT sum(leave) FROM user_{user_id} WHERE date LIKE '{year}-01%'").fetchone()[0]

            present_box.configure(state = "normal")
            present_box.delete(0, tk.END)
            present_box.insert(0, present)
            present_box.configure(state = "readonly")

            absent_box.configure(state = "normal")
            absent_box.delete(0, tk.END)
            absent_box.insert(0, absent)
            absent_box.configure(state = "readonly")

            leave_box.configure(state = "normal")
            leave_box.delete(0, tk.END)
            leave_box.insert(0, leave)
            leave_box.configure(state = "readonly")
            
        elif month == "FEBRUARY":
            present = cursor.execute(f"SELECT sum(present) FROM user_{user_id} WHERE date LIKE '{year}-02%'").fetchone()[0]
            absent = cursor.execute(f"SELECT sum(absent) FROM user_{user_id} WHERE date LIKE '{year}-02%'").fetchone()[0]
            leave = cursor.execute(f"SELECT sum(leave) FROM user_{user_id} WHERE date LIKE '{year}-02%'").fetchone()[0]

            present_box.configure(state = "normal")
            present_box.delete(0, tk.END)
            present_box.insert(0, present)
            present_box.configure(state = "readonly")

            absent_box.delete(0, tk.END)
            absent_box.configure(state = "normal")
            absent_box.insert(0, absent)
            absent_box.configure(state = "readonly")

            leave_box.delete(0, tk.END)
            leave_box.configure(state = "normal")
            leave_box.insert(0, leave)
            leave_box.configure(state = "readonly")

        elif month == "MARCH":
            present = cursor.execute(f"SELECT sum(present) FROM user_{user_id} WHERE date LIKE '{year}-03%'").fetchone()[0]
            absent = cursor.execute(f"SELECT sum(absent) FROM user_{user_id} WHERE date LIKE '{year}-03%'").fetchone()[0]
            leave = cursor.execute(f"SELECT sum(leave) FROM user_{user_id} WHERE date LIKE '{year}-03%'").fetchone()[0]

            present_box.configure(state = "normal")
            present_box.delete(0, tk.END)
            present_box.insert(0, present)
            present_box.configure(state = "readonly")

            absent_box.delete(0, tk.END)
            absent_box.configure(state = "normal")
            absent_box.insert(0, absent)
            absent_box.configure(state = "readonly")

            leave_box.delete(0, tk.END)
            leave_box.configure(state = "normal")
            leave_box.insert(0, leave)
            leave_box.configure(state = "readonly")

        elif month == "APRIL":
            present = cursor.execute(f"SELECT sum(present) FROM user_{user_id} WHERE date LIKE '{year}-04%'").fetchone()[0]
            absent = cursor.execute(f"SELECT sum(absent) FROM user_{user_id} WHERE date LIKE '{year}-04%'").fetchone()[0]
            leave = cursor.execute(f"SELECT sum(leave) FROM user_{user_id} WHERE date LIKE '{year}-04%'").fetchone()[0]

            present_box.configure(state = "normal")
            present_box.delete(0, tk.END)
            present_box.insert(0, present)
            present_box.configure(state = "readonly")

            absent_box.delete(0, tk.END)
            absent_box.configure(state = "normal")
            absent_box.insert(0, absent)
            absent_box.configure(state = "readonly")

            leave_box.delete(0, tk.END)
            leave_box.configure(state = "normal")
            leave_box.insert(0, leave)
            leave_box.configure(state = "readonly")

        elif month == "MAY":
            present = cursor.execute(f"SELECT sum(present) FROM user_{user_id} WHERE date LIKE '{year}-05%'").fetchone()[0]
            absent = cursor.execute(f"SELECT sum(absent) FROM user_{user_id} WHERE date LIKE '{year}-05%'").fetchone()[0]
            leave = cursor.execute(f"SELECT sum(leave) FROM user_{user_id} WHERE date LIKE '{year}-05%'").fetchone()[0]

            present_box.configure(state = "normal")
            present_box.delete(0, tk.END)
            present_box.insert(0, present)
            present_box.configure(state = "readonly")

            absent_box.delete(0, tk.END)
            absent_box.configure(state = "normal")
            absent_box.insert(0, absent)
            absent_box.configure(state = "readonly")

            leave_box.delete(0, tk.END)
            leave_box.configure(state = "normal")
            leave_box.insert(0, leave)
            leave_box.configure(state = "readonly")

        elif month == "JUNE":
            present = cursor.execute(f"SELECT sum(present) FROM user_{user_id} WHERE date LIKE '{year}-06%'").fetchone()[0]
            absent = cursor.execute(f"SELECT sum(absent) FROM user_{user_id} WHERE date LIKE '{year}-06%'").fetchone()[0]
            leave = cursor.execute(f"SELECT sum(leave) FROM user_{user_id} WHERE date LIKE '{year}-06%'").fetchone()[0]

            present_box.configure(state = "normal")
            present_box.delete(0, tk.END)
            present_box.insert(0, present)
            present_box.configure(state = "readonly")

            absent_box.delete(0, tk.END)
            absent_box.configure(state = "normal")
            absent_box.insert(0, absent)
            absent_box.configure(state = "readonly")

            leave_box.delete(0, tk.END)
            leave_box.configure(state = "normal")
            leave_box.insert(0, leave)
            leave_box.configure(state = "readonly")

        elif month == "JULY":
            present = cursor.execute(f"SELECT sum(present) FROM user_{user_id} WHERE date LIKE '{year}-07%'").fetchone()[0]
            absent = cursor.execute(f"SELECT sum(absent) FROM user_{user_id} WHERE date LIKE '{year}-07%'").fetchone()[0]
            leave = cursor.execute(f"SELECT sum(leave) FROM user_{user_id} WHERE date LIKE '{year}-07%'").fetchone()[0]

            present_box.configure(state = "normal")
            present_box.delete(0, tk.END)
            present_box.insert(0, present)
            present_box.configure(state = "readonly")

            absent_box.delete(0, tk.END)
            absent_box.configure(state = "normal")
            absent_box.insert(0, absent)
            absent_box.configure(state = "readonly")

            leave_box.delete(0, tk.END)
            leave_box.configure(state = "normal")
            leave_box.insert(0, leave)
            leave_box.configure(state = "readonly")

        elif month == "AUGUST":
            present = cursor.execute(f"SELECT sum(present) FROM user_{user_id} WHERE date LIKE '{year}-08%'").fetchone()[0]
            absent = cursor.execute(f"SELECT sum(absent) FROM user_{user_id} WHERE date LIKE '{year}-08%'").fetchone()[0]
            leave = cursor.execute(f"SELECT sum(leave) FROM user_{user_id} WHERE date LIKE '{year}-08%'").fetchone()[0]

            present_box.configure(state = "normal")
            present_box.delete(0, tk.END)
            present_box.insert(0, present)
            present_box.configure(state = "readonly")

            absent_box.delete(0, tk.END)
            absent_box.configure(state = "normal")
            absent_box.insert(0, absent)
            absent_box.configure(state = "readonly")

            leave_box.delete(0, tk.END)
            leave_box.configure(state = "normal")
            leave_box.insert(0, leave)
            leave_box.configure(state = "readonly")

        elif month == "SEPTEMBER":
            present = cursor.execute(f"SELECT sum(present) FROM user_{user_id} WHERE date LIKE '{year}-09%'").fetchone()[0]
            absent = cursor.execute(f"SELECT sum(absent) FROM user_{user_id} WHERE date LIKE '{year}-09%'").fetchone()[0]
            leave = cursor.execute(f"SELECT sum(leave) FROM user_{user_id} WHERE date LIKE '{year}-09%'").fetchone()[0]

            present_box.configure(state = "normal")
            present_box.delete(0, tk.END)
            present_box.insert(0, present)
            present_box.configure(state = "readonly")

            absent_box.delete(0, tk.END)
            absent_box.configure(state = "normal")
            absent_box.insert(0, absent)
            absent_box.configure(state = "readonly")

            leave_box.delete(0, tk.END)
            leave_box.configure(state = "normal")
            leave_box.insert(0, leave)
            leave_box.configure(state = "readonly")

        elif month == "OCTOBER":
            present = cursor.execute(f"SELECT sum(present) FROM user_{user_id} WHERE date LIKE '{year}-10%'").fetchone()[0]
            absent = cursor.execute(f"SELECT sum(absent) FROM user_{user_id} WHERE date LIKE '{year}-10%'").fetchone()[0]
            leave = cursor.execute(f"SELECT sum(leave) FROM user_{user_id} WHERE date LIKE '{year}-10%'").fetchone()[0]

            present_box.configure(state = "normal")
            present_box.delete(0, tk.END)
            present_box.insert(0, present)
            present_box.configure(state = "readonly")

            absent_box.delete(0, tk.END)
            absent_box.configure(state = "normal")
            absent_box.insert(0, absent)
            absent_box.configure(state = "readonly")

            leave_box.delete(0, tk.END)
            leave_box.configure(state = "normal")
            leave_box.insert(0, leave)
            leave_box.configure(state = "readonly")

        elif month == "NOVEMBER":
            present = cursor.execute(f"SELECT sum(present) FROM user_{user_id} WHERE date LIKE '{year}-11%'").fetchone()[0]
            absent = cursor.execute(f"SELECT sum(absent) FROM user_{user_id} WHERE date LIKE '{year}-11%'").fetchone()[0]
            leave = cursor.execute(f"SELECT sum(leave) FROM user_{user_id} WHERE date LIKE '{year}-11%'").fetchone()[0]

            present_box.configure(state = "normal")
            present_box.delete(0, tk.END)
            present_box.insert(0, present)
            present_box.configure(state = "readonly")

            absent_box.delete(0, tk.END)
            absent_box.configure(state = "normal")
            absent_box.insert(0, absent)
            absent_box.configure(state = "readonly")

            leave_box.delete(0, tk.END)
            leave_box.configure(state = "normal")
            leave_box.insert(0, leave)
            leave_box.configure(state = "readonly")

        elif month == "DECEMBER":
            present = cursor.execute(f"SELECT sum(present) FROM user_{user_id} WHERE date LIKE '{year}-12%'").fetchone()[0]
            absent = cursor.execute(f"SELECT sum(absent) FROM user_{user_id} WHERE date LIKE '{year}-12%'").fetchone()[0]
            leave = cursor.execute(f"SELECT sum(leave) FROM user_{user_id} WHERE date LIKE '{year}-12%'").fetchone()[0]

            present_box.configure(state = "normal")
            present_box.delete(0, tk.END)
            present_box.insert(0, present)
            present_box.configure(state = "readonly")

            absent_box.delete(0, tk.END)
            absent_box.configure(state = "normal")
            absent_box.insert(0, absent)
            absent_box.configure(state = "readonly")

            leave_box.delete(0, tk.END)
            leave_box.configure(state = "normal")
            leave_box.insert(0, leave)
            leave_box.configure(state = "readonly")

        conn.close()

    def validate_input_userid(input_text):
        if len(input_text) <= 6:
            return True
        else:
            return False 

    def download_record_in_excelsheet():

        conn = sqlite3.connect("employee_database.db")
        cursor = conn.cursor()

        user_id = userid_box.get()
        year = year_box.get()
        month = month_box.get()

        if month == "JANUARY":

            query = f"""
                SELECT  date, present, absent, leave
                FROM user_{user_id}
                WHERE strftime('%Y-%m', date) = '{year}-01'
            """
            data = pd.read_sql_query(query, conn)

            writer = pd.ExcelWriter(f'{user_id} {month}.xlsx', engine='xlsxwriter')

            data.to_excel(writer, sheet_name='Sheet1', index=False)

            writer._save()
        
        elif month == "FEBRUARY":

            query = f"""
                SELECT  present, absent, leave
                FROM user_{user_id}
                WHERE strftime('%Y-%m', date) = '{year}-02'
            """
            data = pd.read_sql_query(query, conn)

            writer = pd.ExcelWriter(f'records/{user_id} {month}.xlsx', engine='xlsxwriter')

            data.to_excel(writer, sheet_name='Sheet1', index=False)

            writer._save()
        
        elif month == "MARCH":

            query = f"""
                SELECT  present, absent, leave
                FROM user_{user_id}
                WHERE strftime('%Y-%m', date) = '{year}-03'
            """
            data = pd.read_sql_query(query, conn)

            writer = pd.ExcelWriter(f'records/{user_id} {month}.xlsx', engine='xlsxwriter')

            data.to_excel(writer, sheet_name='Sheet1', index=False)

            writer._save()
        
        elif month == "APRIL":

            query = f"""
                SELECT  present, absent, leave
                FROM user_{user_id}
                WHERE strftime('%Y-%m', date) = '{year}-04'
            """
            data = pd.read_sql_query(query, conn)

            writer = pd.ExcelWriter(f'records/{user_id} {month}.xlsx', engine='xlsxwriter')

            data.to_excel(writer, sheet_name='Sheet1', index=False)

            writer._save()

        elif month == "MAY":

            query = f"""
                SELECT  present, absent, leave
                FROM user_{user_id}
                WHERE strftime('%Y-%m', date) = '{year}-05'
            """
            data = pd.read_sql_query(query, conn)

            writer = pd.ExcelWriter(f'records/{user_id} {month}.xlsx', engine='xlsxwriter')

            data.to_excel(writer, sheet_name='Sheet1', index=False)

            writer._save()
        
        elif month == "JUNE":

            query = f"""
                SELECT  present, absent, leave
                FROM user_{user_id}
                WHERE strftime('%Y-%m', date) = '{year}-06'
            """
            data = pd.read_sql_query(query, conn)

            writer = pd.ExcelWriter(f'records/{user_id} {month}.xlsx', engine='xlsxwriter')

            data.to_excel(writer, sheet_name='Sheet1', index=False)

            writer._save()

        elif month == "JULY":

            query = f"""
                SELECT  present, absent, leave
                FROM user_{user_id}
                WHERE strftime('%Y-%m', date) = '{year}-07'
            """
            data = pd.read_sql_query(query, conn)

            writer = pd.ExcelWriter(f'records/{user_id} {month}.xlsx', engine='xlsxwriter')

            data.to_excel(writer, sheet_name='Sheet1', index=False)

            writer._save()

        elif month == "AUGUST":

            query = f"""
                SELECT  present, absent, leave
                FROM user_{user_id}
                WHERE strftime('%Y-%m', date) = '{year}-08'
            """
            data = pd.read_sql_query(query, conn)

            writer = pd.ExcelWriter(f'records/{user_id} {month}.xlsx', engine='xlsxwriter')

            data.to_excel(writer, sheet_name='Sheet1', index=False)

            writer._save()

        elif month == "SEPTEMBER":

            query = f"""
                SELECT  present, absent, leave
                FROM user_{user_id}
                WHERE strftime('%Y-%m', date) = '{year}-09'
            """
            data = pd.read_sql_query(query, conn)

            writer = pd.ExcelWriter(f'records/{user_id} {month}.xlsx', engine='xlsxwriter')

            data.to_excel(writer, sheet_name='Sheet1', index=False)

            writer._save()
        
        elif month == "OCTOBER":

            query = f"""
                SELECT  present, absent, leave
                FROM user_{user_id}
                WHERE strftime('%Y-%m', date) = '{year}-10'
            """
            data = pd.read_sql_query(query, conn)

            writer = pd.ExcelWriter(f'records/{user_id} {month}.xlsx', engine='xlsxwriter')

            data.to_excel(writer, sheet_name='Sheet1', index=False)

            writer._save()

        elif month == "NOVEMBER":

            query = f"""
                SELECT  present, absent, leave
                FROM user_{user_id}
                WHERE strftime('%Y-%m', date) = '{year}-11'
            """
            data = pd.read_sql_query(query, conn)

            writer = pd.ExcelWriter(f'records/{user_id} {month}.xlsx', engine='xlsxwriter')

            data.to_excel(writer, sheet_name='Sheet1', index=False)

            writer._save()

        elif month == "DECEMBER":

            query = f"""
                SELECT  present, absent, leave
                FROM user_{user_id}
                WHERE strftime('%Y-%m', date) = '{year}-12'
            """
            data = pd.read_sql_query(query, conn)

            writer = pd.ExcelWriter(f'records/{user_id} {month}.xlsx', engine='xlsxwriter')

            data.to_excel(writer, sheet_name='Sheet1', index=False)

            writer._save()

        conn.close()
        app.destroy()
        app.update()
        download_record()

    app = customtkinter.CTk()
    app.geometry("600x780")
    app.title("ATTENDENCE")
    app.resizable(False, False)

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x_coordinate = (screen_width / 2) - (300 / 2)
    y_coordinate = (screen_height / 2) - (850 / 2)

    app.geometry(f"{600}x{780}+{int(x_coordinate)}+{int(y_coordinate)}")

    back_img = Image.open('back.png')
    back_image = customtkinter.CTkImage(light_image=back_img, size=(50, 50))
    back_img_btn = customtkinter.CTkButton(app, text="", image=back_image, cursor="hand2", fg_color="transparent", hover_color="grey10",width=50,height=50, command=forward_to_admin_panel)
    back_img_btn.place(relx=0.055, rely=0.045, anchor=tk.CENTER)

    title = customtkinter.CTkLabel(app, text="DOWNLOAD RECORD:-", font=("Arial",32), text_color="orangered")
    title.place(relx=0.42, rely=0.045, anchor=tk.CENTER)

    userid_label = customtkinter.CTkLabel(app, text=f"User ID", font=("Arial", 18), text_color="orange")
    userid_label.place(relx=0.2, rely=0.14, anchor=customtkinter.CENTER)
    userid_box = customtkinter.CTkEntry(app, width=120, height=35, font=("Arial",18), validate="key", validatecommand=(app.register(validate_input_userid), "%P"))
    userid_box.place(relx=0.2, rely=0.18, anchor=customtkinter.CENTER)

    year_box_text = customtkinter.CTkLabel(app, text="Year", font=("Arial",18), text_color="orange")
    year_box_text.place(relx=0.4, rely=0.14, anchor=customtkinter.CENTER)
    year_options = [str(year) for year in range(datetime.datetime.now().year, datetime.datetime.now().year - 10, -1)]
    year_var = tk.StringVar()
    year_var.set(year_options[0])  
    year_box = customtkinter.CTkComboBox(app, values=year_options, width=100, height=35, font=("Arial",18))
    year_box.configure(state = "readonly")
    year_box.place(relx=0.4, rely=0.18, anchor=customtkinter.CENTER)

    month_box_text = customtkinter.CTkLabel(app, text="Month", font=("Arial",18), text_color="orange")
    month_box_text.place(relx=0.63, rely=0.14, anchor=customtkinter.CENTER)
    month_options = ["JANUARY", "FEBRUARY" , "MARCH" , "APRIL" , "MAY" , "JUNE", "JULY" , "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER" , "DECEMBER"]
    month_var = tk.StringVar()
    month_var.set(month_options[0])  
    month_box = customtkinter.CTkComboBox(app, values=month_options, width=150, height=35, font=("Arial",18))
    month_box.configure(state = "readonly")
    month_box.place(relx=0.625, rely=0.18, anchor=customtkinter.CENTER)

    userid_search_btn = customtkinter.CTkButton(app, text="SEARCH", cursor="hand2", width=80, height=35, command=search, font = ("Arial", 16))
    userid_search_btn.place(relx=0.84, rely=0.18, anchor=tk.CENTER)
    userid_box.bind("<Return>", lambda event: search())

    user_img = Image.open('user.png')
    user_image = customtkinter.CTkImage(light_image=user_img, size=(200, 200))
    user_img_lable = customtkinter.CTkLabel(app, text="", image=user_image)
    user_img_lable.place(relx=0.5, rely=0.38, anchor=tk.CENTER)

    firstname_box_text = customtkinter.CTkLabel(app, text="First Name :", font=("Arial",18), text_color="medium sea green")
    firstname_box_text.place(relx=0.29, rely=0.545)
    firstname_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    firstname_box.configure(state = "readonly")
    firstname_box.place(relx=0.28, rely=0.58)

    lastname_box_text = customtkinter.CTkLabel(app, text="Last Name :", font=("Arial",18), text_color="medium sea green")
    lastname_box_text.place(relx=0.29, rely=0.645)
    lastname_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    lastname_box.configure(state = "readonly")
    lastname_box.place(relx=0.28, rely=0.68)

    present_box_text = customtkinter.CTkLabel(app, text="PRESENT", font=("Arial",18), text_color="medium sea green")
    present_box_text.place(relx=0.18, rely=0.75)
    present_box = customtkinter.CTkEntry(app, width=150, height=35, font=("Arial",18))
    present_box.configure(state = "readonly")
    present_box.place(relx=0.12, rely=0.78)
    
    absent_box_text = customtkinter.CTkLabel(app, text="ABSENT", font=("Arial",18), text_color="medium sea green")
    absent_box_text.place(relx=0.44, rely=0.75)
    absent_box = customtkinter.CTkEntry(app, width=150, height=35, font=("Arial",18))
    absent_box.configure(state = "readonly")
    absent_box.place(relx=0.37, rely=0.78)

    leave_box_text = customtkinter.CTkLabel(app, text="LEAVE", font=("Arial",18), text_color="medium sea green")
    leave_box_text.place(relx=0.68, rely=0.75)
    leave_box = customtkinter.CTkEntry(app, width=150, height=35, font=("Arial",18))
    leave_box.configure(state = "readonly")
    leave_box.place(relx=0.621, rely=0.78)

    download_record_btn = customtkinter.CTkButton(app, text="DOWNLOAD RECORD", width=200, height=40, font=("bold", 22), cursor = "hand2", command=download_record_in_excelsheet)
    download_record_btn.place(relx=0.5, rely=0.92, anchor=tk.CENTER)

    trade_mark = customtkinter.CTkLabel(app, text="@PC", font=("italic",10), text_color="dimgray")
    trade_mark.place(relx=0.97, rely=0.98, anchor=tk.CENTER)

    app.mainloop()

def edit_record():

    def forward_to_admin_panel():
        app.destroy()
        app.update()
        admin_panel()
    
    def validate_input_userid(input_text):
        if len(input_text) <= 6:
            return True
        else:
            return False 
        
    def upload_picture():
        user_id = userid_box.get()
        if user_id != "":
            file_path = filedialog.askopenfilename(initialdir="/", title="Select Image", filetypes=(("Image Files", "*.jpg;*.png"), ("All Files", "*.*")))
            if file_path:
                global user_image
                user_image = ImageTk.PhotoImage(Image.open(file_path).resize((200,200)))
                user_img_btn.configure(image=user_image)
                user_id = userid_box.get()
                image_path = f"./images/{user_id}.jpg"
                if os.path.exists(image_path):
                    os.remove(image_path)
                Image.open(file_path).save(image_path)
        elif user_id == "":
            messagebox.showerror("ERROR", "Please fill the USER ID box.")
        
    def search():
        user_id = userid_box.get()
        
        conn = sqlite3.connect('employee_database.db')
        cursor = conn.cursor()
        
        cursor.execute(f"""SELECT firstname, lastname, dob, email, phone, alt_phone, education, skills, experience, address1, address2, district, pin
                        FROM employees WHERE userid={user_id}""")
        user_details = cursor.fetchone()
        
        if user_details:
            firstname, lastname, dob, email, phone, alt_phone, education, skills, experience, address1, address2, district, pin = user_details[:13]
            
            firstname_box.delete(0, tk.END)
            firstname_box.insert(0, firstname)

            lastname_box.delete(0, tk.END)
            lastname_box.insert(0, lastname)

            dob_box.delete(0, tk.END)
            dob_box.insert(0, dob)

            email_box.delete(0, tk.END)
            email_box.insert(0, email)

            phone_box.delete(0, tk.END)
            phone_box.insert(0, phone)

            alt_phone_box.delete(0, tk.END)
            alt_phone_box.insert(0, alt_phone)

            education_box.delete(0, tk.END)
            education_box.insert(0, education)

            skills_box.delete(0, tk.END)
            skills_box.insert(0, skills)

            experience_box.delete(0, tk.END)
            experience_box.insert(0, experience)

            address1_box.delete(0, tk.END)
            address1_box.insert(0, address1)

            address2_box.delete(0, tk.END)
            address2_box.insert(0, address2)

            district_box.delete(0, tk.END)
            district_box.insert(0, district)

            pin_box.delete(0, tk.END)
            pin_box.insert(0, pin)            

            image_path = f"./images/{user_id}.jpg"
            if os.path.exists(image_path):
                try:
                    user_image = Image.open(image_path)
                    #user_image = user_image.resize((200, 200))
                    user_image = ImageTk.PhotoImage(user_image)
                    user_img_btn.configure(image=user_image)
                    user_img_btn.image = user_image
                except IOError:
                    messagebox.showerror("ERROR", "Failed to load image")
            else:
                messagebox.showerror("ERROR", "Image file not found")
        else:
            messagebox.showerror("ERROR","User ID not found in the database")

    def delete_record():
        user_id = userid_box.get()
        if user_id != "":
            message = messagebox.askyesno("CONFIRMATION", "Are you sure you want to delete this record?")
            if message == True:
                delete_box()
        elif user_id == "":
                messagebox.showerror("ERROR", "Please fill the USER ID box.")

        def delete_box():       
                conn = sqlite3.connect('employee_database.db')
                cursor = conn.cursor()
                cursor.execute(f"""DELETE FROM employees WHERE userid={user_id}""")
                cursor.execute(f"DROP TABLE {user_id}")
                conn.commit()
                conn.close()
                messagebox.showinfo("SUCCESS", "Record deleted successfully")

    def update_data():
        message = messagebox.askyesno("CONFIRMATION", "Are you sure you want to edit this record?")
        if message == True:
            user_id = userid_box.get()
            conn = sqlite3.connect('employee_database.db')
            cursor = conn.cursor()

            firstname = firstname_box.get()
            lastname = lastname_box.get()
            dob = dob_box.get()
            email = email_box.get()
            phone = phone_box.get()
            alt_phone = alt_phone_box.get()
            education = education_box.get()
            skills = skills_box.get()
            experience = experience_box.get()
            address1 = address1_box.get()
            address2 = address2_box.get()
            district = district_box.get()
            pin = pin_box.get()

            cursor.execute(f"""UPDATE employees SET firstname='{firstname}', lastname='{lastname}', dob='{dob}', email='{email}', phone='{phone}', alt_phone='{alt_phone}', education='{education}', skills='{skills}', experience='{experience}', address1='{address1}', address2='{address2}', district='{district}', pin='{pin}' WHERE userid={user_id}""")
            conn.commit()
            conn.close()

            messagebox.showinfo("SUCCESS", "Record updated successfully")
    
    app = customtkinter.CTk()
    app.geometry("900x750")
    app.title("EDIT RECORD")
    app.resizable(False, False)

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x_coordinate = (screen_width / 2) - (750 / 2)
    y_coordinate = (screen_height / 2) - (800 / 2)

    app.geometry(f"{900}x{750}+{int(x_coordinate)}+{int(y_coordinate)}")

    back_img = Image.open('back.png')
    back_image = customtkinter.CTkImage(light_image=back_img, size=(50, 50))
    back_img_btn = customtkinter.CTkButton(app, text="", image=back_image, cursor="hand2", fg_color="transparent", hover_color="grey10",width=50,height=50, command=forward_to_admin_panel)
    back_img_btn.place(relx=0.04, rely=0.05, anchor=tk.CENTER)

    title = customtkinter.CTkLabel(app, text="EDIT RECORD:-", font=("Arial",32), text_color="orangered")
    title.place(relx=0.25, rely=0.05, anchor=tk.CENTER)

    userid_label = customtkinter.CTkLabel(app, text=f"User ID:", font=("Arial", 18), text_color="orange")
    userid_label.place(relx=0.8, rely=0.2, anchor=customtkinter.CENTER)
    userid_box = customtkinter.CTkEntry(app, width=100, height=35, font=("Arial",18), validate="key", validatecommand=(app.register(validate_input_userid), "%P"))
    userid_box.place(relx=0.9, rely=0.2, anchor=customtkinter.CENTER)

    userid_search_btn = customtkinter.CTkButton(app, text="SEARCH", cursor="hand2", width=100, height=35, command=search, font = ("Arial", 16))
    userid_search_btn.place(relx=0.86, rely=0.27, anchor=tk.CENTER)
    userid_box.bind("<Return>", lambda event: search())

    user_img = Image.open('user.png')
    user_image = customtkinter.CTkImage(light_image=user_img, size=(200, 200))
    user_img_btn = customtkinter.CTkButton(app, text="", image=user_image, cursor="hand2", fg_color="transparent", hover_color="grey10",width=50,height=50, command=upload_picture)
    user_img_btn.place(relx=0.87, rely=0.5, anchor=tk.CENTER)

    firstname_box_text = customtkinter.CTkLabel(app, text="First Name:-", font=("Arial",18), text_color="medium sea green")
    firstname_box_text.place(relx=0.054, rely=0.15)
    firstname_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    firstname_box.place(relx=0.05, rely=0.185)

    lastname_box_text = customtkinter.CTkLabel(app, text="Last Name:-", font=("Arial",18), text_color="medium sea green")
    lastname_box_text.place(relx=0.054, rely=0.25)
    lastname_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    lastname_box.place(relx=0.05, rely=0.285)

    dob_box_text = customtkinter.CTkLabel(app, text="Date of Birth:-    (dd/mm/yy)", font=("Arial",18), text_color="medium sea green")
    dob_box_text.place(relx=0.054, rely=0.35)
    dob_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    dob_box.place(relx=0.05, rely=0.385)

    email_box_text = customtkinter.CTkLabel(app, text="Email ID:-", font=("Arial",18), text_color="medium sea green")
    email_box_text.place(relx=0.054, rely=0.5)
    email_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    email_box.place(relx=0.05, rely=0.535)

    phone_box_text = customtkinter.CTkLabel(app, text="Phone Number:-", font=("Arial",18), text_color="medium sea green")
    phone_box_text.place(relx=0.054, rely=0.6)
    phone_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    phone_box.place(relx=0.05, rely=0.635)

    alt_phone_box_text = customtkinter.CTkLabel(app, text="Alternate Phone Number:-", font=("Arial",18), text_color="medium sea green")
    alt_phone_box_text.place(relx=0.054, rely=0.7)
    alt_phone_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    alt_phone_box.place(relx=0.05, rely=0.735)

    education_box_text = customtkinter.CTkLabel(app, text="Education Details:-", font=("Arial",18), text_color="medium sea green")
    education_box_text.place(relx=0.404, rely=0.15)
    education_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    education_box.place(relx=0.4, rely=0.185)

    skills_box_text = customtkinter.CTkLabel(app, text="Skills:-", font=("Arial",18), text_color="medium sea green")
    skills_box_text.place(relx=0.404, rely=0.25)
    skills_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    skills_box.place(relx=0.40, rely=0.285)

    experience_box_text = customtkinter.CTkLabel(app, text="Experience Level:-", font=("Arial",18), text_color="medium sea green")
    experience_box_text.place(relx=0.404, rely=0.35) 
    experience_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    experience_box.place(relx=0.40, rely=0.385)

    address1_text = customtkinter.CTkLabel(app, text="Address 1:-", font=("Arial",18), text_color="medium sea green")
    address1_text.place(relx=0.404, rely=0.5)
    address1_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    address1_box.place(relx=0.40, rely=0.535)

    address2_text = customtkinter.CTkLabel(app, text="Address 2:-", font=("Arial",18), text_color="medium sea green")
    address2_text.place(relx=0.404, rely=0.6)
    address2_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    address2_box.place(relx=0.40, rely=0.635)

    district_text = customtkinter.CTkLabel(app, text="District:-", font=("Arial",18), text_color="medium sea green")
    district_text.place(relx=0.404, rely=0.7)
    district_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    district_box.place(relx=0.40, rely=0.735)

    pin_text = customtkinter.CTkLabel(app, text="Pin Code:-", font=("Arial",18), text_color="medium sea green")
    pin_text.place(relx=0.404, rely=0.8)
    pin_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    pin_box.place(relx=0.40, rely=0.835)    

    delete_btn = customtkinter.CTkButton(app, text="DELETE", width=200, height=40, font=("bold", 24), cursor = "hand2", fg_color="red2", hover_color="red3", command=delete_record)
    delete_btn.place(relx=0.32, rely=0.95, anchor=tk.CENTER)

    update_btn = customtkinter.CTkButton(app, text="UPDATE", width=200, height=40, font=("bold", 24), cursor = "hand2", fg_color="green3", hover_color="green4",command=update_data)
    update_btn.place(relx=0.62, rely=0.95, anchor=tk.CENTER)

    trade_mark = customtkinter.CTkLabel(app, text="@PC", font=("italic",10), text_color="dimgray")
    trade_mark.place(relx=0.97, rely=0.97, anchor=tk.CENTER)

    app.mainloop()

##############################################---------------------USER PANEL FUNCTION-------------------------################################################

def user_panel():
    def forward_to_login_page():
        app.destroy()
        app.update()
        login_page()

    def download_record_in_excelsheet():
        conn = sqlite3.connect('employee_database.db')
        c = conn.cursor()

        query = f"""
                SELECT  date, present, absent, leave
                FROM user_{userid_login_page}
            """
        data = pd.read_sql_query(query, conn)

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Workbook", "*.xlsx")])

        if file_path:
            writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
            data.to_excel(writer, sheet_name='Sheet1', index=False)
            writer._save()
            messagebox.showinfo("SUCCESS", "Record downloaded successfully")
        else:
            messagebox.showinfo("CANCEL", "Download cancelled")

        conn.commit()
        conn.close()

    def change_password():

        def update_password():
            conn = sqlite3.connect('employee_database.db')
            cursor = conn.cursor()
            cursor.execute(f"""UPDATE employees SET password = '{new_pwd_box.get()}' WHERE userid == {userid_login_page}""")
            conn.commit()
            conn.close()
            messagebox.showinfo("SUCCESS", "Password updated successfully")

        app = customtkinter.CTk()
        app.geometry("400x200")
        app.title("USER PANEL")
        app.resizable(False, False)
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()

        new_pwd_box_text = customtkinter.CTkLabel(app, text="Enter Your New Password:-", font=("Arial",18), text_color="medium sea green")
        new_pwd_box_text.place(relx=0.19, rely=0.08)
        new_pwd_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
        new_pwd_box.place(relx=0.17, rely=0.3)

        change_btn = customtkinter.CTkButton(app, text="CHANGE", width=200, height=40, font=("bold", 20), cursor = "hand2", command=update_password)
        change_btn.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        x_coordinate = (screen_width / 2) - (200 / 2)
        y_coordinate = (screen_height / 2) - (200 / 2)

        app.geometry(f"{400}x{200}+{int(x_coordinate)}+{int(y_coordinate)}")

        app.mainloop()
        app.update()
        app.destroy()

    
    app = customtkinter.CTk()
    app.geometry("900x750")
    app.title("USER PANEL")
    app.resizable(False, False)

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x_coordinate = (screen_width / 2) - (750 / 2)
    y_coordinate = (screen_height / 2) - (800 / 2)

    app.geometry(f"{900}x{750}+{int(x_coordinate)}+{int(y_coordinate)}")

    back_img = Image.open('back.png')
    back_image = customtkinter.CTkImage(light_image=back_img, size=(50, 50))
    back_img_btn = customtkinter.CTkButton(app, text="", image=back_image, cursor="hand2", fg_color="transparent", hover_color="grey10",width=50,height=50, command=forward_to_login_page)
    back_img_btn.place(relx=0.04, rely=0.05, anchor=tk.CENTER)

    title = customtkinter.CTkLabel(app, text="USER PANEL:-", font=("Arial",32), text_color="orangered")
    title.place(relx=0.25, rely=0.05, anchor=tk.CENTER)
        
    firstname_box_text = customtkinter.CTkLabel(app, text="First Name :", font=("Arial",18), text_color="medium sea green")
    firstname_box_text.place(relx=0.054, rely=0.15)
    firstname_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    firstname_box.place(relx=0.17, rely=0.15)

    lastname_box_text = customtkinter.CTkLabel(app, text="Last Name :", font=("Arial",18), text_color="medium sea green")
    lastname_box_text.place(relx=0.054, rely=0.23)
    lastname_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    lastname_box.place(relx=0.17, rely=0.23)
    
    userid_box_text = customtkinter.CTkLabel(app, text="User ID      :", font=("Arial",18), text_color="medium sea green")
    userid_box_text.place(relx=0.054, rely=0.31)
    userid_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    userid_box.place(relx=0.17, rely=0.31)

    image_path = f"./images/{userid_login_page}.jpg"
    if os.path.exists(image_path):
        try:
            user_image = Image.open(image_path)
            user_image = customtkinter.CTkImage(light_image=user_image, size=(250, 250))
            user_img_lable = customtkinter.CTkLabel(app, text="", image=user_image)
            user_img_lable.place(relx=0.75, rely=0.28, anchor=tk.CENTER)
        except IOError:
            messagebox.showerror("ERROR", "Failed to load image")
    else:
        user_img = Image.open('user.png')
        user_image = customtkinter.CTkImage(light_image=user_img, size=(250, 250))
        user_img_lable = customtkinter.CTkLabel(app, text="", image=user_image)
        user_img_lable.place(relx=0.75, rely=0.28, anchor=tk.CENTER)

    dob_box_text = customtkinter.CTkLabel(app, text="Last Name :", font=("Arial",18), text_color="medium sea green")
    dob_box_text.place(relx=0.054, rely=0.39)
    dob_box = customtkinter.CTkEntry(app, width=280, height=35, font=("Arial",18))
    dob_box.place(relx=0.17, rely=0.39)

    address_box_text = customtkinter.CTkLabel(app, text="Address     :", font=("Arial",18), text_color="medium sea green")
    address_box_text.place(relx=0.054, rely=0.47)
    address_box = customtkinter.CTkTextbox(app, width=400, height=80, font=("Arial",18))
    address_box.place(relx=0.17, rely=0.47)

    present_box_text = customtkinter.CTkLabel(app, text="PRESENT", font=("Arial",18), text_color="medium sea green")
    present_box_text.place(relx=0.18, rely=0.7)
    present_box = customtkinter.CTkEntry(app, width=200, height=45, font=("Arial",20))
    present_box.place(relx=0.12, rely=0.73)
        
    absent_box_text = customtkinter.CTkLabel(app, text="ABSENT", font=("Arial",18), text_color="medium sea green")
    absent_box_text.place(relx=0.44, rely=0.7)
    absent_box = customtkinter.CTkEntry(app, width=200, height=45, font=("Arial",20))
    absent_box.place(relx=0.37, rely=0.73)

    leave_box_text = customtkinter.CTkLabel(app, text="LEAVE", font=("Arial",18), text_color="medium sea green")
    leave_box_text.place(relx=0.69, rely=0.7)
    leave_box = customtkinter.CTkEntry(app, width=200, height=45, font=("Arial",20))

    leave_box.place(relx=0.621, rely=0.73)

    download_record_btn = customtkinter.CTkButton(app, text="DOWNLOAD RECORD", width=200, height=40, font=("bold", 20), cursor = "hand2", command=download_record_in_excelsheet)
    download_record_btn.place(relx=0.285, rely=0.88, anchor=tk.CENTER)

    change_password_btn = customtkinter.CTkButton(app, text="CHANGE PASSWORD", width=200, height=40, font=("bold", 20), cursor = "hand2", command=change_password)
    change_password_btn.place(relx=0.685, rely=0.88, anchor=tk.CENTER)

    conn = sqlite3.connect('employee_database.db')
    cursor = conn.cursor()
        
    cursor.execute("SELECT firstname, lastname, userid, dob, address1, address2, district, pin FROM employees WHERE userid=?", (userid_login_page,))
    user_details = cursor.fetchone()
        
    if user_details:
        firstname, lastname, userid, dob, address1, address2, district, pin= user_details
            
        firstname_box.delete(0, tk.END)
        firstname_box.insert(0, firstname)

        lastname_box.delete(0, tk.END)
        lastname_box.insert(0, lastname)

        userid_box.delete(0, tk.END)
        userid_box.insert(0, str(userid))

        dob_box.delete(0, tk.END)
        dob_box.insert(0, str(dob))

        address_box.delete(1.0, tk.END)
        address_box.insert(1.0, str(address1) + "," + str(address2) + "," + str(district) + "," + str(pin))

    else:
        messagebox.showerror("ERROR","User ID not found in the database")

    current_month = datetime.datetime.now().month

    present = cursor.execute(f"SELECT sum(present) FROM user_{userid_login_page} WHERE date LIKE '____-{current_month}%'").fetchone()[0]
    absent = cursor.execute(f"SELECT sum(absent) FROM user_{userid_login_page} WHERE date LIKE '____-{current_month}%'").fetchone()[0]
    leave = cursor.execute(f"SELECT sum(leave) FROM user_{userid_login_page} WHERE date LIKE '____-{current_month}%'").fetchone()[0]

    present_box.configure(state = "normal")
    present_box.delete(0, tk.END)
    present_box.insert(0, str(present))
    present_box.configure(state = "readonly")

    absent_box.configure(state = "normal")
    absent_box.delete(0, tk.END)
    absent_box.insert(0, str(absent))
    absent_box.configure(state = "readonly")

    leave_box.configure(state = "normal")
    leave_box.delete(0, tk.END)
    leave_box.insert(0, str(leave))
    leave_box.configure(state = "readonly")

    conn.close()

    app.mainloop()

main()