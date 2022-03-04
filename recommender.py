#coding:utf8

"""
This script works as intended as long as the original .txt files left untouched.
If somehow the program is shut down unexpectedly, files might corrupt (lines might shift)
which disrupts the way this program works. In that case, please try running the program
with the original .txt files.
"""

import sys
import os
import random

book_database = open(os.path.join(sys.path[0], "books.txt"), "r")     # opens "books.txt" and assigns it to a variable named "book_database"
books = book_database.read().strip().split("\n")                      # using split() method we seperate lines and add them to a list named "books"
books_by_author = []                                                  # books_by_author is another list in which the name of the book and the author is seperated    
for book in books:                                                    
    books_by_author.append(book.split(","))                         
    
user_rating_database = open(os.path.join(sys.path[0], "ratings.txt"), "r+")       # opens "ratings.txt"
ratings = {}                                                                      # a dictionary to store ratings to use and manipulate ratings data easier is created
for line in user_rating_database:                                                 # using next() function usernames are seperated from ratings
    ratings[line.strip()] = (next(user_rating_database, '').strip().split())
    
if not os.path.exists(os.path.join(sys.path[0], "passwords.txt")):                         # checks whether there's a file named "passwords.txt" in the directory
    with open(os.path.join(sys.path[0], "passwords.txt"), "w") as passwords:               # if doesn't exists creates one  
        for user in ratings.keys():                                                        # this loop is to give old users passwords
            passwords.write(user + "\n")                                                         
            passwords.write(str(user.replace(" ", "") + str(random.randint(0, 999))) + "\n")

with open(os.path.join(sys.path[0], "passwords.txt"), "r") as passwords:        
    # A dictionary for passwords is created for better access to data
    pass_dict = {}                                  
    for line in passwords:
        pass_dict[line.strip()] = (next(passwords).strip())

def update_database(entered_username, entered_password):
    """
    This function gives default values of ratings for the new registered user and writes that to ratings.txt.
    The function is also used to update passwords.txt and ratings.txt with new data.
    """
    # Set all ratings of new user to 0.
    ratings[entered_username] = ['0'] * len(books)

    with open(os.path.join(sys.path[0], "ratings.txt"), "w") as user_rating_database:
        # Write the new user's name to user_rating_database.
        user_rating_database.write(entered_username + "\n")

    with open(os.path.join(sys.path[0], "passwords.txt"), "a") as passwords:
        # Write the new user's username to password.txt, then the new password.
        passwords.write(entered_username + "\n")      
        passwords.write(entered_password + "\n")
        pass_dict[entered_username] = entered_password

    with open(os.path.join(sys.path[0], "ratings.txt"), "w") as user_rating_database:
        for i in range(len(ratings.keys())):
            # Rewrite the ratings.txt with the new data.
            user_rating_database.write(list(ratings.keys())[i] + "\n" + " ".join(list(ratings.values())[i]) + "\n")  

def password_reset(entered_username):
    """
    This function resets user password. It's called in 2 cases.
    1-) If the user entered his/her passwords wrong multiple times and accepted to reset password.
    2-) If the user chose to reset his/her passwords through account settings
    """
    while True:
        new_password = input("Please enter your new password: ")
        # If password is empty or whitespace      
        if new_password == "" or new_password.isspace():              
            print("Password can't be empty.\n")                       
            continue
        verify_password = input("Verify new password: ")
        # If password is empty or whitespace         
        if verify_password == "" or verify_password.isspace():     
            print("Password can't be empty.\n")                  
            continue
        elif new_password == verify_password: 
            # Replace the password of logged user in pass_dict dictionary with new password.                 
            pass_dict[entered_username] = new_password               
            break
        else:
            print("Passwords do not match. Try again.\n")          
            continue
    with open(os.path.join(sys.path[0], "passwords.txt"), "w") as passwords:     
        for i in range(len(pass_dict.keys())):
            # Rewrite the password.txt with new password data.
            passwords.write(list(pass_dict.keys())[i] + "\n" + (list(pass_dict.values())[i]) + "\n")    
    print("Password reset is complete. Now you can log in.\n")
    # Restart the program.
    main()     

def signup(entered_username):
    """
    This function is called if a new user wants to register.
    After registering and logging in, ten_random_books() function is called.
    """
    while True:
        entered_password = input("Create a password: ")
        # If password is empty or whitespace            
        if entered_password == "" or entered_password.isspace():      
                print("Password can't be empty.\n")                 
                continue
        verify_password = input("Please verify your password: ")
        # If password is empty or whitespace     
        if verify_password == "" or entered_password.isspace():    
                print("Password can't be empty.\n")          
                continue
        elif verify_password == entered_password:           
            update_database(entered_username, entered_password)
            break
        else:
            print("Passwords don not match.\n")          
    print("Sign-up is complete. You can log in now\n")
    
    while True:
        for failed_try in range(3):
            print("Username: " + entered_username)
            entered_password = input("Password: ")
            # If password is empty or whitespace
            if entered_password == "" or entered_password.isspace():        
                print("Password can't be empty.\n")
                break
            # If wrong password is entered 3 times
            elif failed_try == 2:
                while True:
                    want_reset = input("Too many failed attempts. Do you want to reset your password? [Y/N]")
                    if want_reset == "Y" or want_reset == "y":              
                        password_reset(entered_username)      
                        break
                    elif want_reset == "N" or want_reset == "n":      
                        main()
                    else:
                        print("You've made an invalid request. Please try again.\n")    
                        continue 
            # If the password is correct after signing up, ten_random_books() function is called   
            elif entered_password == pass_dict[entered_username]:     
                print("Log in successful.\n")
                ten_random_books(entered_username)
                break
            else:
                print("Wrong password. Try again.\n")
                continue        
        break

def login(entered_username):
    """
    This function is used for logging in. If entered username doesn't exist
    in the database, it assumes it's a new user and asks whether he/she wants
    to register. If accepted, signup() function is called.
    """
    while True:
        for failed_try in range(4):
            # If wrong password is entered 3 times
            if failed_try == 3:
                while True:
                    want_reset = input("Too many failed attempts. Do you want to reset your password? [Y/N]")
                    if want_reset == "Y" or want_reset == "y":       
                        password_reset(entered_username)
                        break
                    elif want_reset == "N" or want_reset == "n":    
                        main()
                    else:
                        print("You've made an invalid request. Please try again.\n")
                        continue    
            elif entered_username in ratings.keys():
                if failed_try != 0:
                    print("Username: " + entered_username)
                entered_password = input("Password: ")
                # If password is empty or whitespace
                if entered_password == "" or entered_password.isspace():       
                    print("Password can't be empty.")
                    login(entered_username) 
                elif entered_password == pass_dict[entered_username]:
                    print("Log in successful. Welcome back " + entered_username + ".", end = "\n\n")
                    break
                else:
                    print("Wrong password. Please try again.\n")
            else:
                want_new_account = input("No users found. Do you want to sign up with this username? [Y/N] : ")    
                if want_new_account == "Y" or want_new_account == "y":
                    signup(entered_username)
                    break
                elif want_new_account == "N" or want_new_account == "n":
                    main()
                else:
                    print("You've made an invalid request. Please try again.\n")
                    login(entered_username)
                    break
        break

def change_username(entered_username):
    """
    This function is used to change username if the user chooses that option
    in the account settings.
    """
    while True:
        entered_password = input("Please enter your password to proceed: ")     
        if entered_password == "" or entered_password.isspace():
            print("Password can't be empty.\n")
        elif entered_password == pass_dict[entered_username]:
            new_username = input("Please enter your new username: ")
            # If password is empty or whitespace 
            if new_username == "" or entered_password.isspace():     
                print("Username can't be empty.\n")
                continue

            # Replace the username with new username in password dictionary.
            pass_dict[new_username] = pass_dict[entered_username]    
            # Delete the old username from dictionary.
            del pass_dict[entered_username] 
            # Replace the username with new username in ratings dictionary.                    
            ratings[new_username] = ratings[entered_username]
            # Delete the old username from ratings dictionary        
            del ratings[entered_username]  

            with open(os.path.join(sys.path[0], "passwords.txt"), "w") as passwords:
                for i in range(len(pass_dict.keys())):
                    # Rewrite the passwords.txt with new data
                    passwords.write(list(pass_dict.keys())[i] + "\n" + (list(pass_dict.values())[i]) + "\n")  

            with open(os.path.join(sys.path[0], "ratings.txt"), "w") as user_rating_database:
                for i in range(len(ratings.keys())):
                    # Rewrite the ratings.txt with new data
                    user_rating_database.write(list(ratings.keys())[i] + "\n" + " ".join(list(ratings.values())[i]) + "\n")  
            break
        else:
            print("Wrong password. Please try again.\n")
    
def delete_account(entered_username):
    """
    This function is used to delete user account if user chooses
    that from the account options.
    """
    while True:
        entered_password = input("Please enter your password to proceed: ")
        # If password is empty or whitespace       
        if entered_password == "" or entered_password.isspace():       
            print("Password can't be empty.\n")
        elif entered_password == pass_dict[entered_username]:
            # Delete the user from pass_dict.
            del pass_dict[entered_username]
            # Delete the user in ratings dictionary.                         
            del ratings[entered_username]

            with open(os.path.join(sys.path[0], "passwords.txt"), "w") as passwords:
                for i in range(len(pass_dict.keys())):
                    # Rewrite the passwords.txt with new data
                    passwords.write(list(pass_dict.keys())[i] + "\n" + (list(pass_dict.values())[i]) + "\n")

            with open(os.path.join(sys.path[0], "ratings.txt"), "w") as user_rating_database:
                for i in range(len(ratings.keys())):
                    # Rewrite the ratings.txt with new data
                    user_rating_database.write(list(ratings.keys())[i] + "\n" + " ".join(list(ratings.values())[i]) + "\n")

            print("Your account " + entered_username + " has been successfully deleted.\n")
            main()
            break        
        else:
            print("Wrong password. Please try again.\n")

def get_rated_books(entered_username):
    """
    This function is used to find which books the user has already rated before.
    """
    ratedBooks = [books[i].split(",") for i in range(len(books)) if int(ratings[entered_username][i]) != 0]
    return ratedBooks
       
def ten_random_books(entered_username):
    """
    This function is used to display 10 random books from book database for the user to rate.
    The ratings are then used for recommending new books to the user.
    """
    print("--------------------------------------------------------")
    print('''Before I can recommend some new books for you to read,
you need to tell me your opinion on a few books.
If you haven’t read the book, answer 0 but otherwise use 
this scale:

            -5: Hated it!
            -3: Didn ’t like it.
             1: OK
             3: Liked it.
             5: Really liked it.
                                ''')
    print("--------------------------------------------------------")
    # A counter to know when the user has rated 10 books.
    new_user_ratings = 0     
    # This list contains books that have been showed to the user.
    index_of_shown_books = []   
    while new_user_ratings != 10: 
        while True:
            # book_index is a random integer to get a random book.
            book_index = random.randint(0, len(books) - 1)
            # If this book is not shown before    
            if book_index not in index_of_shown_books:   
                while True:
                    print(books_by_author[book_index][1] + " by " + books_by_author[book_index][0])
                    rating = input("Your rating of this book: ")
                    if not rating in ['-5', '-3', '0', '1', '3', '5']:
                        print("You can rate the books by only using the scale above.\n")
                        continue
                    else:
                        break
                if int(rating) != 0:
                    # Add the rating to the ratings dictionary.
                    ratings[entered_username][book_index] = rating    
                    index_of_shown_books.append(book_index)
                    new_user_ratings += 1
                    break
                elif int(rating) == 0:
                    index_of_shown_books.append(book_index)
                    continue       
        
    with open(os.path.join(sys.path[0], "ratings.txt"), "w") as user_rating_database:
        for i in range(len(ratings.keys())):
            # Rewrite the ratings.txt with new data
            user_rating_database.write(list(ratings.keys())[i] + "\n" + " ".join(list(ratings.values())[i]) + "\n")  

def rating_system(entered_username, book_number):
    """
    This function is used to enable each user to change their previous ratings.
    """
    # If the selected book hasn't been rated by the user before
    if ratings[entered_username][book_number - 1] == '0':     
        print("You haven't rated " + books_by_author[book_number - 1][1] + " by " + books_by_author[book_number - 1][0] + " yet.")
        new_rating = input("What is your rate for " + books_by_author[book_number-1][1] + " by " + books_by_author[book_number-1][0] + "? ")
        # Check if the rating is valid or not
        if new_rating not in ['-5', '-3', '1', '3', '5']:      
            print("You can only rate the books using the scale above.")
            rating_system(entered_username, book_number)
        # Change the rating of selected book.
        ratings[entered_username][book_number - 1] = new_rating     
        print("Rating is successful.")
        
    elif ratings[entered_username][book_number - 1] != '0':
        while True:
            print("Your previous rating for " + books_by_author[book_number-1][1] + " by " + books_by_author[book_number-1][0] + " was " + ratings[entered_username][book_number - 1])
            new_rating = input('''What is your new rate? (Please rate according to the scale below. ) 
            -5: Hated it!
            -3: Didn’t like it.
            1: OK
            3: Liked it.
            5: Really liked it.
            ''')
            if new_rating not in ['-5', '-3', '1', '3', '5']:
                print("You can rate the books by only using the scale above.\n")
                continue
            else:
                ratings[entered_username][book_number - 1] = new_rating
                print("Rating is successful.\n")
                break
        else:
            print("You've made an invalid request. Please try again.\n")
            rating_system(entered_username, book_number)
    
    with open(os.path.join(sys.path[0], "ratings.txt"), "w") as user_rating_database:
        for i in range(len(ratings.keys())):
            # Rewrite the ratings.txt with new data
            user_rating_database.write(list(ratings.keys())[i] + "\n" + " ".join(list(ratings.values())[i]) + "\n")       
            
def algorithm_A(entered_username):
    """
    Recommends user 10 highest rated books.
    """
    # Find how many times a certain book has been rated to later use that value in averaging.
    number_of_ratings = [0] * len(books)    
    
    for i in range(len(books)):
        for j in list(ratings.values()):
            # If rating is not 0, which means it's not rated by a certain user
            if int(j[i]) != 0:            
                number_of_ratings[i] += 1
    
    for i in range(len(number_of_ratings)):
        # If the number of ratings of a certain book is 0:
        if number_of_ratings[i] == 0:    
            # Set it to 1. (This is to prevent getting ZeroDivisionError when averaging)
            number_of_ratings[i] = 1     
    
    ratings2 = list(ratings.values())
    ratings2 = list([map(int,i) for i in ratings2])
    # Calculate the averages of ratings of each books.                 
    avg_of_ratings = [sum(x)/number for x,number in zip(zip(*ratings2), number_of_ratings)]   
    
    most_rated_books = []   # A blank list that will contain books from avg_of_ratings.
    for i in range(len(books)):
        # Add the highest rated books to list.
        most_rated_books.append(books_by_author[avg_of_ratings.index(max(avg_of_ratings))])   
        # Set it to 0. (This is to get other highest rated book after the current highest rated book.)
        avg_of_ratings[avg_of_ratings.index(max(avg_of_ratings))] = 0  
    # Sort the list from highest to lowest.
    most_rated_books.sort(reverse = True)   

   
    print("Recommended Books:")
    print("------------------------------------------------")
    recommended_book_count = 0   
    for book in most_rated_books:
        # Print the book if the user hasn't read it yet, then stop after 10 books.
        if book not in get_rated_books(entered_username) and recommended_book_count < 10:  
            print(book[1] + " by " + book[0])
            recommended_book_count += 1   
    print("------------------------------------------------")
           
def algorithm_B(entered_username):
    
    """
    Recommends user 10 highest rated books from the most similar user.
    """
    # Copy the ratings dictionary so the original one won't be affected.
    users = ratings.copy()
    # Delete the current user to prevent comparing to him/herself.      
    del users[entered_username]
    # A dictionary to store similarity rates. (Key: compared user, Value: similarity value)    
    comparison = {}
    # Compare current user with every other user and add the similarity value to comparison dictionary.
    for i in range(len(users.keys())):
        comparison[list(users.keys())[i]] = sum([int(x)*int(y) for x,y in zip(ratings[entered_username],list(users.values())[i])])
    
    # Get the most similar user to current user.
    most_similar = max(comparison, key=comparison.get)

    ratings_of_most_similar = []
    for rating in list(ratings[most_similar]):
        ratings_of_most_similar.append(int(rating))

    highest_of_most_similar = []
    for i in range(len(books)):
        # Add the book by checking the index of the highest rating of most similar user.
        highest_of_most_similar.append(books_by_author[ratings_of_most_similar.index(max(ratings_of_most_similar))])
        # We set the value to -999 so the same book won't be added to the list  
        ratings_of_most_similar[ratings_of_most_similar.index(max(ratings_of_most_similar))] = -999
    
    print("Recommended Books:")
    print("------------------------------------------------")
    recommended_book_count = 0
    for book in highest_of_most_similar:
        # Print the book if the user hasn't read it yet, then stop after 10 books.
        if book not in get_rated_books(entered_username):   
            print(book[1] + " by " + book[0])
            recommended_book_count += 1
            if recommended_book_count == 10:
                break     
    print("------------------------------------------------")
    
def algorithm_C(entered_username):
    """
    Recommends the user 10 books by first comparing the user with other users and getting a similarity value
    for each user, then summing the products of ratings and similarity values and finally getting the 10 highest from
    the results.
    """
    # Copy the ratings dictionary so the original one won't be affected.
    users = ratings.copy()     
    # Delete the current user to prevent comparing to him/herself.
    del users[entered_username]
    # A dictionary to store similarity rates. (Key: compared user, Value: similarity value)    
    comparison = {}
    # Compare current user with every other user and add the similarity value to comparison dictionary.
    for i in range(len(users.keys())):
        comparison[list(users.keys())[i]] = sum([int(x)*int(y) for x,y in zip(ratings[entered_username],list(users.values())[i])])
    # A dictionary containing each user's ratings multiplied by their similarity values.    
    new_ratings = {}
    for i in range(len(list(users.keys()))):
        new_ratings[list(users.keys())[i]] = [int(x)*int(y) for x,y in zip(list(ratings.values())[i], list(comparison.values()))]
    # Get the sum of new ratings and add them to a list    
    sum_of_new_ratings = [sum(x) for x in zip(*list(new_ratings.values()))]
    
    most_rated_books = []
    # Find the books with highest values and add to list.
    for i in range(len(books)):
        most_rated_books.append(books_by_author[sum_of_new_ratings.index(max(sum_of_new_ratings))])
        # After adding each book, set its value to -999999999 so it won't be added multiple times.
        sum_of_new_ratings[sum_of_new_ratings.index(max(sum_of_new_ratings))] = -999999999
    
    print("Recommended Books:")
    print("------------------------------------------------")
    recommended_book_count = 0
    for book in most_rated_books:
        if book not in get_rated_books(entered_username):
            print(book[1] + " by " + book[0])
            recommended_book_count += 1
            if recommended_book_count == 10:
                break      
    print("------------------------------------------------")

def main():
    while True:
        print("\n" + "   Welcome to the Book Recommender System™")
        print("--------------------------------------------")
        entered_username = input("Username: ")
        # If username is empty or whitespace
        if entered_username == "" or entered_username.isspace():
            print("Username can't be empty.\n")
            main()
        login(entered_username)
        while True:
            option = input("What would you like to do now "  + entered_username + '? ' + "(Please enter the number of your desired choice.)\n" 
            '''
            1-) I want to rate a new book or change an old rating.
            2-) I want to get new book recommendations.
            3-) I want to log out.
            4-) I want to go to account settings.
            5-) Who made this program?
            ''')

            if option == "1":
                while True:
                    print("--------------------------------------------")
                    for i in range(len(books)):
                        print(str(i+1) + "-) " + books[i])
                    print("--------------------------------------------")
                    book_number = int(input("Please enter the number of book that you wish to rate or change the rating of.\n"))
                    if book_number in range(0, len(books) + 1):
                        break
                    else:
                        print("You've made an invalid request. Please try again.\n")
                rating_system(entered_username, book_number)
                        
            elif option == "2":
                while True:
                    which_algorithm = input('I can make recommendations based on 3 different algorithms. Which algorithm would you prefer? A, B or C? : ')
                    if which_algorithm == 'A' or which_algorithm == 'a':
                        algorithm_A(entered_username)
                        break
                    elif which_algorithm == 'B' or which_algorithm == 'b':
                        algorithm_B(entered_username)
                        break
                    elif which_algorithm == 'C' or which_algorithm == 'c':
                        algorithm_C(entered_username)  
                        break
                    else:
                        print("You've made an invalid request. Please try again.\n")
                        continue
            elif option == "3":
                print('Log out successful.', end="\n\n")   
                break

            elif option == "4":
                while True:
                    account_option = input("What would you like to with yout account " + entered_username + " ? (Please enter the number of your desired choice.)\n"
                    '''
                    1-) I want to change my username.
                    2-) I want to change my password.
                    3-) I want to terminate my account.
                    4-) I want to go back to main menu.
                    ''')

                    if account_option == "1":
                        change_username(entered_username)
                    elif account_option == "2":
                        password_reset(entered_username)
                    elif account_option == "3":
                        sure_delete = input("Are you sure about deleting your account? (This action cannot be reverted.) [Y/N]: ")
                        if sure_delete == "Y" or sure_delete == "y":
                            delete_account(entered_username)
                            main()
                        elif sure_delete == "N" or sure_delete == "n":
                            break
                        else:
                            print("You've made an invalid request. Please try again.\n")  
                    elif account_option == "4":
                        break
                    else:
                        print("You've made an invalid request. Please try again.\n")
            elif option == "5":
                print("""
                This program has been created by:

                Mert Yağmur and Serkan Büyükcoşkun

                as a project for CE140.
                """)          
            else:
                print("You've made an invalid request. Please try again.\n") 
                continue

if __name__ == "__main__":
    main()