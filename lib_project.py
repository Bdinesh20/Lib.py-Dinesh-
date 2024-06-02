import datetime
import json
import getpass

# Initialize global variables
books = []
members = []
member_counter = 1
Password = "Pooja$kmce123"  # Set default password

def load_data():
    global books, members, member_counter, Password
    try:
        with open("savedata.json", "r") as f:
            data = f.read()
            if data.strip():
                data = json.loads(data)
                books = data.get("books", [])
                members = data.get("members", [])
                member_counter = data.get("member_counter", 1)
                Password = data.get("Password", "Pooja$kmce123")
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        print("Error: The data file is corrupted or empty. Using default data.")

def save_data():
    global books, members, member_counter, Password
    with open("savedata.json", "w") as f:
        data = {
            "books": books,
            "members": members,
            "member_counter": member_counter,
            "Password": Password
        }
        json.dump(data, f, indent=4)

def main_menu():
    print("\n==== Library Management System ====")
    print("1. Search for a book")
    print("2. Add a new book")
    print("3. Update book information")
    print("4. Delete a book")
    print("5. View all books")
    print("6. Borrow a book")
    print("7. Return a book")
    print("8. Renew book")
    print("9. Manage members")
    print("10. Generate reports")
    print("11. ADMIN")
    print("12. Exit")

def search_menu():
    print("\n==== Search Menu ====")
    print("1. Search by title")
    print("2. Search by author")
    print("3. Search by ISBN")
    print("4. Return to main menu")

def update_menu():
    print("\n==== Update Book Menu ====")
    print("1. Update title")
    print("2. Update author")
    print("3. Update ISBN")
    print("4. Update availability")
    print("5. Return to main menu")

def member_menu():
    print("\n==== Member Management Menu ====")
    print("1. Add a new member")
    print("2. Update member information")
    print("3. Delete a member")
    print("4. View all members")
    print("5. Return to main menu")

def report_menu():
    print("\n==== Generate Reports Menu ====")
    print("1. Generate book inventory report")
    print("2. Generate member borrowing history report")
    print("3. Return to main menu")

def admin_block():
    print("\nAdmin Portal")
    print("1. Admin Attendance Check In")
    print("2. Admin Attendance Check Out")
    print("3. Update Password")

def search_by_title():
    title = input("Enter the title of the book: ")
    found_books = [book for book in books if book["title"].lower() == title.lower()]
    if found_books:
        for book in found_books:
            print_book(book)
    else:
        print("No books found with that title.")

def search_by_author():
    author = input("Enter the book author: ")
    found_books = [book for book in books if book["author"].lower() == author.lower()]
    if found_books:
        for book in found_books:
            print_book(book)
    else:
        print("No books found by that author.")

def search_by_isbn():
    isbn = input("Enter the book ISBN: ")
    found_books = [book for book in books if book["isbn"] == isbn]
    if found_books:
        for book in found_books:
            print_book(book)
    else:
        print("No books found with that ISBN.")

def add_book():
    title = input("Enter the book title: ")
    author = input("Enter the book author: ")
    isbn = input("Enter the book ISBN: ")
    quantity = int(input("Enter the quantity of the book: "))
    book = {
        "title": title,
        "author": author,
        "isbn": isbn,
        "availability": quantity > 0,
        "quantity": quantity
    }
    books.append(book)
    save_data()
    print("New book added to library")

def update_title(book):
    new_title = input("Enter the new title of the book: ")
    book["title"] = new_title
    print("Title has been updated")
    save_data()

def update_author(book):
    new_author = input("Enter the new name of the author: ")
    book["author"] = new_author
    print("Author has been updated")
    save_data()

def update_isbn(book):
    new_isbn = input("Enter the updated ISBN number: ")
    book["isbn"] = new_isbn
    print("ISBN has been updated")
    save_data()

def update_availability(book):
    availability = input("Enter availability (True/False): ")
    book["availability"] = availability.lower() == 'true'
    print("Availability updated successfully.")
    save_data()

def update_book():
    isbn = input("Enter the ISBN of the book to update: ")
    for book in books:
        if book["isbn"] == isbn:
            update_menu()
            update_choice = input("\nEnter your update option: ")
            if update_choice == "1":
                update_title(book)
            elif update_choice == "2":
                update_author(book)
            elif update_choice == "3":
                update_isbn(book)
            elif update_choice == "4":
                update_availability(book)
            elif update_choice == "5":
                return
            else:
                print("Invalid choice.")
            break
    else:
        print("Book not found.")

def delete_book():
    isbn = input("Enter the ISBN of the book to delete: ")
    global books
    book_to_delete = None
    for book in books:
        if book["isbn"] == isbn:
            book_to_delete = book
            break
    if book_to_delete:
        books.remove(book_to_delete)
        save_data()
        print("Book deleted successfully.")
    else:
        print("Book not found.")

def view_books():
    if books:
        for book in books:
            print_book(book)
    else:
        print("No books available.")
def borrow_book():
    is_member = input("Are you a member? (yes/no): ")
    if is_member == "no":
        name = input("Enter your name: ")
        add_member(name)  # Add the new member
        member = members[-1]
    else:
        member_id = int(input("Enter your member ID: "))
        member = find_member_by_id(member_id)
        if not member:
            print("Member not found.")
            return

    isbn = input("Enter the ISBN of the book to borrow: ")
    book = next((book for book in books if book["isbn"] == isbn), None)
    
    if book is None:
        print(f"No book found with ISBN {isbn}")
        return
    
    if book["availability"] and book["quantity"] > 0:
        borrow_date = datetime.datetime.now()
        due_date = borrow_date + datetime.timedelta(days=30)
        book["quantity"] -= 1
        if book["quantity"] == 0:
            book["availability"] = False
        member["borrowed_books"].append({
            "isbn": book["isbn"], 
            "borrow_date": str(borrow_date), 
            "due_date": str(due_date)
        })
        save_data()
        print(f"Book borrowed successfully. Due date for return is {due_date}.")
    else:
        print("Book is currently unavailable.")

def return_book():
    member_id = int(input("Enter your member ID: "))
    member = find_member_by_id(member_id)
    if not member:
        print("Member not found.")
        return
    
    isbn = input("Enter the ISBN of the book to return: ")
    for book in books:
        if book["isbn"] == isbn:
            if book["quantity"] == 0:
                book["availability"] = True
            book["quantity"] += 1
            borrowed_books = member["borrowed_books"]
            for borrowed_book in borrowed_books:
                if borrowed_book["isbn"] == isbn:
                    if datetime.datetime.now() > datetime.datetime.fromisoformat(borrowed_book["due_date"]):
                        member["remark"] = "B"
                        member["remark_date"] = str(datetime.datetime.now())
                        print("Book returned late. You cannot borrow books for the next 15 days.")
                    borrowed_books.remove(borrowed_book)
                    save_data()
                    print("Book returned successfully.")
                    break
            break
    else:
        print("Book not found.")
def add_member(name):
    global member_counter
    member = {
        "member_id": member_counter,
        "name": name,
        "borrowed_books": [],
        "remark": "",
        "remark_date": None
    }
    members.append(member)
    member_counter += 1
    save_data()

def find_member_by_id(member_id):
    for member in members:
        if member["member_id"] == member_id:
            return member
    return None

def update_member():
    member_id = int(input("Enter the member ID to update: "))
    for member in members:
        if member["member_id"] == member_id:
            new_name = input("Enter the new name: ")
            member["name"] = new_name
            save_data()
            print("Member information updated successfully.")
            break
    else:
        print("Member not found.")

def delete_member():
    member_id = int(input("Enter the member ID to delete: "))
    global members
    for member in members:
        if member["member_id"] == member_id:
            members.remove(member)
            save_data()
            print("Member deleted successfully.")
            return
    print("Member not found.")

def view_members():
    if members:
        for member in members:
            print_member(member)
            print("-" * 30)  # Separator line between members
    else:
        print("No members found.")

def generate_book_inventory_report():
    print("\n" + "="*30)
    print("==== Book Inventory Report ====")
    print("="*30)
    if books:
        for book in books:
            print_book(book)
            print("-" * 30)  # Separator line between books
    else:
        print("No books available.")

def generate_member_borrowing_history_report():
    print("\n" + "="*30)
    print("==== Member Borrowing History Report ====")
    print("="*30)
    if members:
        for member in members:
            print_member(member)
            if member["borrowed_books"]:
                for borrowed_book in member["borrowed_books"]:
                    print(f"Borrowed ISBN: {borrowed_book['isbn']}, Borrow Date: {borrowed_book['borrow_date']}, Due Date: {borrowed_book['due_date']}")
                print("-" * 30)  # Separator line between borrowed books
            else:
                print("No borrowed books.")
                print("-" * 30)  # Separator line between members
    else:
        print("No members found.")

def admin_check_in():
    current_time = datetime.datetime.now()
    attendance_in = input("Enter 'check in' to mark attendance: ")
    if attendance_in.lower() == "check in":
        print(f"Check-in time: {current_time}. Attendance check-in successful.")

def admin_check_out():
    current_time = datetime.datetime.now()
    attendance_out = input("Enter 'check out' to mark attendance: ")
    if attendance_out.lower() == "check out":
        print(f"Check-out time: {current_time}. Attendance check-out successful.")

def update_password():
    global Password
    current_password = input("Enter your current password: ")
    if current_password == Password:
        while True:
            new_password = input("Enter your new password: ")
            confirm_password = input("Confirm your new password: ")
            if new_password == confirm_password:
                Password = new_password  # Update the global variable
                save_data()  # Save the updated password
                print("Password updated successfully.")
                break
            else:
                print("Passwords do not match. Please try again.")
    else:
        print("Incorrect current password.")

def print_book(book):
    print(f"Title: {book['title']}")
    print(f"Author: {book['author']}")
    print(f"ISBN: {book['isbn']}")
    print(f"Availability: {book['availability']}")
    

def print_member(member):
    print(f"Member ID: {member['member_id']}")
    print(f"Name: {member['name']}")
    print(f"Borrowed Books: {member['borrowed_books']}")
    print(f"Remark: {member['remark']}")
    print(f"Remark Date: {member['remark_date']}")

def find_member_by_id(member_id):
    for member in members:
        if member["member_id"] == member_id:
            return member
    return None

def renew_book():
    member_id = int(input("Enter your member ID: "))
    member = find_member_by_id(member_id)
    if not member:
        print("Member not found.")
        return
    
    isbn = input("Enter the ISBN of the book to renew: ")
    for borrowed_book in member["borrowed_books"]:
        if borrowed_book["isbn"] == isbn:
            borrowed_book["due_date"] = str(datetime.datetime.fromisoformat(borrowed_book["due_date"]) + datetime.timedelta(days=30))
            save_data()
            print(f"Book renewed successfully. New due date is {borrowed_book['due_date']}.")
            break
    else:
        print("Book not found in your borrowed list.")

def main():
    load_data()  # Load data at the start
    global user_name, Password
    user_name = input("Enter user name: ")
    password_attempt = input("Enter password: ")
    
    if user_name == "Pooja@kmce.com" and password_attempt == Password:
        print("Logged in")
    else:
        print("Incorrect login credentials")
        return

    while True:
        main_menu()
        choice = input("\nEnter your choice (1-12): ")

        if choice == "1":
            search_menu()
            search_choice = input("\nEnter your search option: ")
            if search_choice == "1":
                search_by_title()
            elif search_choice == "2":
                search_by_author()
            elif search_choice == "3":
                search_by_isbn()
            elif search_choice == "4":
                continue
            else:
                print("Invalid choice.")
        elif choice == "2":
            add_book()
        elif choice == "3":
            update_book()
        elif choice == "4":
            delete_book()
        elif choice == "5":
            view_books()
        elif choice == "6":
            borrow_book()
        elif choice == "7":
            return_book()
        elif choice == "8":
            renew_book()    
        elif choice == "9":
            member_menu()
            member_choice = input("\nEnter your member management option: ")
            if member_choice == "1":
                name = input("Enter the member name: ")
                add_member(name)
            elif member_choice == "2":
                update_member()
            elif member_choice == "3":
                delete_member()
            elif member_choice == "4":
                view_members()
            elif member_choice == "5":
                continue
            else:
                print("Invalid choice.")
        elif choice == "10":
            report_menu()
            report_choice = input("\nEnter your report generation option: ")
            if report_choice == "1":
                generate_book_inventory_report()
            elif report_choice == "2":
                generate_member_borrowing_history_report()
            elif report_choice == "3":
                continue
            else:
                print("Invalid choice.")
        elif choice == "11":
            if user_name == "Pooja@kmce.com":
                password_attempt = input("Enter password: ")
                if password_attempt == Password:
                    admin_block()
                    admin_choice = input("\nEnter your admin choice (1-3): ")
                    if admin_choice == "1":
                        admin_check_in()
                    elif admin_choice == "2":
                        admin_check_out()
                    elif admin_choice == "3":
                        update_password()
                else:
                    print("Access denied. Incorrect admin password.")
        elif choice == "12":
            print("Exiting the system.")
            save_data()  # Save data before exiting
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
