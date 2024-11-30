import random
import os

FILENAME = "users.txt"

def initialize_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as file:
            pass

# reading user data 
def read_users():
    users = {}
    try:
        with open(FILENAME, "r") as file:
            for line in file:
                username, password, score = line.strip().split(",")
                users[username] = {"password": password, "score": int(score)}
    except Exception as e:
        print(f"Error reading user file: {e}")
    return users

# adding new user's data
def write_user(username, password, score=0):
    try:
        with open(FILENAME, "a") as file:
            file.write(f"{username},{password},{score}\n")
    except Exception as e:
        print(f"Error writing to user file: {e}")

#updating score of the user
def update_user_score(username, score):
    users = read_users()
    if username in users:
        
        users[username]["score"] = score

        with open(FILENAME, "w") as file:
            for user, data in users.items():
                file.write(f"{user},{data['password']},{data['score']}\n")
    else:
        print(f"User {username} not found!")

# Signup process
def signup():
    print("________ Signup ________")
    users = read_users()
    while True:
        username = input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty.")
            continue

        if username in users:
            print("Username already taken. Please try a different one.")
            continue

        password = input("Enter password: ").strip()
        if not password:
            print("Password cannot be empty.")
            continue

        write_user(username, password)
        print("Signup successful! You can now log in.")
        break

# Login process
def login():
    print("_________ Login _________")
    users = read_users()
    while True:
        username = input("Enter your username: ").strip()
        if not username:
            print("Username cannot be empty.")
            continue

        password = input("Enter your password: ").strip()
        if not password:
            print("Password cannot be empty.")
            continue

        if username in users and users[username]["password"] == password:
            print(f"Welcome, {username}!")
            return tiousername
        else:
            print("Invalid credentials. Would you like to sign up? (yes/no)")
            choice = input().strip().lower()
            if choice == "yes":
                signup()
                return username
            elif choice == "no":
                continue
            else:
                print("Invalid choice!")

#importing questions from the questions.txt file 
def load_questions(filename):
    questions = {"Python": [], "Java": [], "C++": []}
    category = None

    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                
                if line.startswith("# Category:"):
                    category = line.split(":")[1].strip()
                elif line.startswith("Q:") and category:
                    question_data = {"question": line[3:].strip(), "options": [], "correct": None, "explanation": ""}
                elif line.startswith("A:") or line.startswith("B:") or line.startswith("C:") or line.startswith("D:"):
                    question_data["options"].append(line[3:].strip())
                elif line.startswith("Correct:"):
                    question_data["correct"] = int(line.split(":")[1].strip()) - 1
                elif line.startswith("Explanation:"):
                    question_data["explanation"] = line[12:].strip()
                    
                    questions[category].append(question_data)

        return questions
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# quiz
def run_quiz(category, questions, username):
    print(f"\nStarting {category} Quiz!")
    selected_questions = random.sample(questions[category], 5)
    score = 0

    for idx, question_data in enumerate(selected_questions, 1):
        print(f"\nQuestion {idx}: {question_data['question']}")
        for i, option in enumerate(question_data["options"], 1):
            print(f"{i}. {option}")
        answer = input("Your answer (1-4): ").strip()

        if answer.isdigit() and 1 <= int(answer) <= 4:
            chosen_option = int(answer) - 1
            if chosen_option == question_data["correct"]:
                print("Correct!")
                score += 1
            else:
                correct_option = question_data["correct"] + 1
                print(f"Wrong! Correct answer: {correct_option}. {question_data['options'][question_data['correct']]}")

            print(f"Explanation: {question_data['explanation']}")
        else:
            print("Invalid input. Skipping question.")

    print(f"\nQuiz Complete! You scored {score} out of 5.")
    if score < 3:
        print("Don't worry! Keep practicing to improve your skills.")
    update_user_score(username, score)

# Main function
def main():
    initialize_file()  
    questions_file = "questions.txt"
    questions = load_questions(questions_file)
    if not questions:
        return

    print("=== Welcome to the Quiz App ===")

    # Login 
    username = login()
    while True:
        print("\nSelect a category:")
        print("1. Python")
        print("2. Java")
        print("3. C++")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()
        if choice == "1":
            run_quiz("Python", questions, username)
        elif choice == "2":
            run_quiz("Java", questions, username)
        elif choice == "3":
            run_quiz("C++", questions, username)
        elif choice == "4":
            print(f"Goodbye, {username}!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
