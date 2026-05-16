class Book:

    def __init__(self, title, author, total_copies):
        self.title = title
        self.author = author
        self._total_copies = total_copies          # hermetyzacja
        self._available_copies = total_copies

    @property
    def available(self):
        return self._available_copies > 0

    def borrow(self):
        if not self.available:
            raise ValueError(f"Brak egzemplarzy: {self.title}")
        self._available_copies -= 1

    def return_copy(self):
        if self._available_copies < self._total_copies:
            self._available_copies += 1

    def __str__(self):
        return f"{self.title} — {self.author} (dostępne: {self._available_copies})"

class User:

    def __init__(self, login, password, role):
        self.login = login
        self._password = password
        self.role = role

    def authenticate(self, password):
        return self._password == password

    def menu(self):
        raise NotImplementedError("Klasy pochodne muszą zaimplementować menu()")

    def __str__(self):
        return f"{self.login}"


class Reader(User):

    def __init__(self, login, password):
        super().__init__(login, password, "Czytelnik")
        self.borrowed = []
        self.extension_requests = []

    def menu(self):
        print(f"Menu czytelnika ({self.login}):")
        print("  1. Przeglądaj katalog")
        print("  2. Wypożycz")
        print("  3. Moje wypożyczenia")
        print("  4. pPośba o przedłużenie")


class Librarian(User):

    def __init__(self, login, password):
        super().__init__(login, password, "Bibliotekarz")

    def menu(self):
        print(f"Menu bibliotekarza ({self.login}):")
        print("  1. Lista wszystkich wypożyczeń")
        print("  2. Prośby o przedłużenie")

class Library:

    def __init__(self):
        self.books = []
        self.users = []
        self.extension_requests = []

    def add_book(self, book):
        self.books.append(book)

    def add_user(self, user):
        self.users.append(user)

    def show_books(self):
        print("\nKatalog książek:")
        for index, book in enumerate(self.books):
            print(f"{index + 1}. {book}")

    def borrow_book(self, reader, book_index):
        book = self.books[book_index]

        if book.available_copies > 0:
            book.borrow()
            reader.borrowed_books.append(book)
            print(f"{reader.login} wypożyczył: {book.title}")
        else:
            print("Książka niedostępna")

    def show_borrowings(self):
        print("\nAktualne wypożyczenia:")

        for user in self.users:
            if isinstance(user, Reader):
                for book in user.borrowed:
                    print(f"{user.login} -> {book.title}")

    def handle_requests(self):
        print("\nProśby o przedłużenie:")

        for index, request in enumerate(self.extension_requests):
            reader, book = request

            print(f"{index + 1}. {reader.login} -> {book.title}")

            decision = input("Akceptuj? (t/n): ")

            if decision.lower() == "t":
                print("Prośba zaakceptowana")
            else:
                print("Prośba odrzucona")

        self.extension_requests.clear()

    # logowanie - użytkownik podaje login i hasło; po 3 nieudanych próbach funkcja się kończy.
    def log_in(self):
        max_attempts = 3
        attempts = 0

        print("----- LOGOWNIANIE -----")
        while attempts < max_attempts:
            login = input("Login: ").strip()  # strip do usuwania białych znaków
            password = input("Hasło: ").strip()

            # uzycie autentykacji
            for user in self.users:
                if user.login == login and user.authenticate(password):
                    print(f"\nZalogowano: {user}!")
                    return user
            attempts += 1
            print(f"Błędny login lub hasło! Próba {attempts}/{max_attempts}\n")

        print("Przekroczono liczbę prób! Do widzenia.")
        return None




#Przeglądanie katalogu
def print_books(books):
    print("\nKatalog dostepnych tytułów")
    print("-----------------------------")
    for book in books:
        print(f"{book['tytul']} — {book['autor']} (dostępne: {book['sztuk']})")

#szukanie ksiązki po tytule
def find_book_by_title(books, title):
    title = title.strip().lower()   #lower do ignorowania wielkości liter
    for book in books:
        if book["tytul"].strip().lower() == title:
            return book
    return None

#Wypożyczenie książki
def borrow_book(books, borrows, user_login):
    title = input("Podaj tytuł książki do wypożyczenia: ")
    book = find_book_by_title(books, title) #metoda do szukania ksiązki po tytule
    if book is None:
        print("Nie znaleziono książki o podanym tytule!")
        return

    if book["sztuk"] <= 0:
        print("Tytuł nie jest obecnie dostępny do wypożyczenia!")
        return

    # zmniejszamy ilość sztuk
    book["sztuk"] -= 1

    # dodanie tytułu do wypożyczeń czytalnika
    if user_login not in borrows:
        borrows[user_login] = []
    borrows[user_login].append({"tytul": book["tytul"], "autor": book["autor"]})
    print(f"Wypożyczono: {book['tytul']} — {book['autor']}")

#Moje wypożyczenia
def print_user_borrows(borrows, user_login):
    user_borrows = borrows.get(user_login, []) #pobranie listy posiadanych tytułów, ograniczonej do loginu czytelnika

    if not user_borrows:
        print("Brak wypożyczonych książek!")
        return

    print("Moje wypożyczenia:") #wyświetlenie listy wypożyczeń
    for borrow in user_borrows:
        print(f"{borrow['tytul']} — {borrow['autor']}")


#Wyswietl Menu główne
def print_main_menu():
    print("\n----------------------------")
    print("1) Przeglądaj katalog książek")
    print("2) Wypożycz książkę")
    print("3) Moje wypożyczenia")
    print("0) Wyloguj")

def main():
    library = Library()

    library.add_book(Book("Lalka", "Prus", 1))
    library.add_book(Book("Pan Tadeusz", "Mickiewicz", 3))
    library.add_book(Book("Ferdydurke", "Gombrowicz", 2))
    library.add_book(Book("Władca Pierścieni. Powrót Króla", "Tolkien", 4))
    library.add_book(Book("Quo Vadis", "Sienkiewicz", 3))
    library.add_book(Book("Wieża jaskółki", "Sapkowski", 4))
    library.add_book(Book("Kroniki Jakuba Wędrowycza", "Pilipiuk", 5))

    library.add_user(Librarian("admin", "admin"))
    library.add_user(Librarian("merito", "321321"))
    library.add_user(Reader("dzienro", "123123"))
    library.add_user(Reader("kowalski", "abc123"))

    #logowanie - jesli user jest pusty to koniec programu
    user = library.log_in()
    if user is None:
        return
    print(f"\nWitaj w systemie biblioteki {user}!")
    #pętla Menu główne
    """
    while True:
        print_main_menu()
        choice = input("> ").strip()
        if choice == "1": #opcja Przeglądanie katalogu
            print_books(ksiazki)
        elif choice == "2": #opcja Wypożyczenie książki
            borrow_book(ksiazki, wypozyczenia, user["login"])
        elif choice == "3": #opcja Moje wypożyczenia
            print_user_borrows(wypozyczenia, user["login"])
        elif choice == "0": #opcja Wylogowanie
            print("Wylogowano!")
            return
        else:
            print("Nieznana opcja, spróbuj ponownie.")
            continue
    """

if __name__ == "__main__":
    main()
