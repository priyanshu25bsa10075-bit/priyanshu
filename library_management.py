import gradio as gr

class Library:
    def __init__(self, books_list, name):
        self.booksList = books_list  # List of tuples: (title, url)
        self.name = name
        self.lendDict = {}

    def displayBooks(self):
        # Return markdown list with clickable links
        md = "\n".join(
            [f"- [{title}]({url})" for (title, url) in self.booksList]
        )
        return md

    def lendBook(self, user, book_title):
        # Check if book is in library
        titles = [t for t, _ in self.booksList]
        if book_title not in titles:
            return "Sorry, this book is not in our library."

        # Check if book is already lent out
        if book_title not in self.lendDict:
            self.lendDict[book_title] = user
            return f"Lender-Book database updated. {user} can take '{book_title}' now."
        else:
            return f"Book is already being used by {self.lendDict[book_title]}."

    def addBook(self, title, url):
        # Check if book already exists
        titles = [t for t, _ in self.booksList]
        if title in titles:
            return "This book already exists in the library."
        self.booksList.append((title, url))
        return f"Book '{title}' has been added to the library."

    def returnBook(self, book_title):
        if book_title in self.lendDict:
            self.lendDict.pop(book_title)
            return f"'{book_title}' has been returned. Thank you!"
        else:
            return "This book was not lent out."

# Initialize a large book database with real URLs
initial_books = [
    ("Discrete Mathematics", "https://en.wikipedia.org/wiki/Discrete_mathematics"),
    ("Data Structure", "https://www.geeksforgeeks.org/data-structures/"),
    ("Human Values", "https://www.scribd.com/doc/26365549/Human-Values-Character-Education"),
    ("Maths IV", "https://nptel.ac.in/courses/111104032/"),
    ("Computer System Architecture", "https://en.wikipedia.org/wiki/Computer_architecture"),
    # Add more books with URLs as needed
    ("Introduction to Algorithms", "https://mitpress.mit.edu/books/introduction-algorithms-third-edition"),
    ("Python Programming", "https://docs.python.org/3/tutorial/"),
    ("Artificial Intelligence", "https://www.aaai.org/"),
    ("Machine Learning", "https://www.coursera.org/learn/machine-learning"),
    ("Operating Systems", "https://pages.cs.wisc.edu/~remzi/OSTEP/"),
    ("Database Management Systems", "https://dbms-book.com/"),
]

lib = Library(initial_books, "Stuti's Huge Library")

def library_app(action, user, book_title, book_url):
    if action == "Display Books":
        return lib.displayBooks()
    elif action == "Lend a Book":
        if not user or not book_title:
            return "Please enter both user name and book title for lending."
        return lib.lendBook(user, book_title)
    elif action == "Add a Book":
        if not book_title or not book_url:
            return "Please enter both book title and URL to add a book."
        return lib.addBook(book_title, book_url)
    elif action == "Return a Book":
        if not book_title:
            return "Please enter the book title to return."
        return lib.returnBook(book_title)
    else:
        return "Please select a valid action."

with gr.Blocks() as demo:
    gr.Markdown("# Library Management System with Large Book Database and Real Links")

    action = gr.Radio(
        ["Display Books", "Lend a Book", "Add a Book", "Return a Book"],
        label="Select Action",
    )

    user = gr.Textbox(label="User Name (for lending books)", placeholder="Enter your name")
    book_title = gr.Textbox(label="Book Title", placeholder="Enter book title")
    book_url = gr.Textbox(label="Book URL (only for adding books)", placeholder="Enter book URL")

    output = gr.Markdown()

    def update_ui(action_choice):
        # Show/hide user and URL inputs based on action
        user.visible = action_choice == "Lend a Book"
        book_url.visible = action_choice == "Add a Book"

    action.change(update_ui, inputs=action)

    submit_btn = gr.Button("Submit")

    def on_submit(action_choice, user_name, title, url):
        return library_app(action_choice, user_name, title, url)

    submit_btn.click(
        on_submit,
        inputs=[action, user, book_title, book_url],
        outputs=output,
    )

demo.launch(share=True)
