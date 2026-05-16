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

    def menu(self, library):
        raise NotImplementedError("Klasy pochodne muszą zaimplementować menu()")

    def __str__(self):
        return f"{self.login}"


class Reader(User):

    def __init__(self, login, password):
        super().__init__(login, password, "Czytelnik")
        self.borrowed = []
        self.extension_requests = []

    def menu(self, library):
       while True:

            print(f"Menu czytelnika ({self.login}):")
            print("  1. Przeglądaj katalog")
            print("  2. Wypożycz")
            print("  3. Moje wypożyczenia")
            print("  4. Przedłuż wypożyczenie")
            print("  0. Wyloguj")

            choice = input("> ").strip()
            if choice == "1":
                library.show_books()
            elif choice == "2":
                library.borrow_book(self)
            elif choice == "3":
                library.show_user_borrowings(self)
            elif choice == "4":
                library.send_request(self)
            elif choice == "0":
                print("Wylogowano!\n")
                return
            else:
                print("Nieznana opcja, spróbuj ponownie.\n")

                continue


class Librarian(User):

    def __init__(self, login, password):
        super().__init__(login, password, "Bibliotekarz")

    def menu(self, library):
        while True:

            print(f"Menu bibliotekarza ({self.login}):")
            print("  1. Lista wszystkich wypożyczeń")
            print("  2. Prośby o przedłużenie")
            print("  0. Wyloguj")
            choice = input("> ").strip()
            if choice == "0": #opcja Wylogowanie
                print("Wylogowano!\n")
                return
            else:
                print("Nieznana opcja, spróbuj ponownie.\n")
                continue

class Library:

    def __init__(self):
        self.books = []
        self.users = []
        self.extension_requests = []

    def add_book(self, book):
        self.books.append(book)

    def add_user(self, user):
        self.users.append(user)

    # Przeglądanie katalogu
    def show_books(self):
        print("\nKatalog książek:")
        for index, book in enumerate(self.books):
            print(f"{index + 1}. {book}")

    # szukanie ksiązki po tytule
    def find_book_by_title(self):
        title = input("Podaj tytuł książki do wypożyczenia: ")
        title = title.strip().lower()  # lower do ignorowania wielkości liter
        for book in self.books:
            if book.title.strip().lower() == title:
                return book
        return None

    # Wypożyczenie ksiązki
    def borrow_book(self, reader):
        book = self.find_book_by_title()

        if book is None:
            print("Nie znaleziono tytułu!\n")
            return

        if book:
            book.borrow()
            reader.borrowed.append(book)
            print(f"{reader.login} wypożyczył: {book.title} - {book.author}\n")
        else:
            print("Książka niedostępna!\n")

    # Wypożyczenia czytelnika
    def show_user_borrowings(self, reader):
        print(f"Aktualne wypozyczenia: {reader.login}")

        if not reader.borrowed:
            print("Lista jest pusta!\n")
        for index, book in enumerate(reader.borrowed):
            print(f"{index + 1}. {book}")

    # Wszystkie wypożyczenia
    def show_borrowings(self):
        print("\nAktualne wypożyczenia:")

        for user in self.users:
            if isinstance(user, Reader):
                for book in user.borrowed:
                    print(f"{user} -> {book.title} {book.author}")

    # Wyslij przedłużenie
    def send_request(self, reader):
        self.show_user_borrowings(reader)
        book_idx = int(input(" > "))
        book_idx -=1
        try:
            book = reader.borrowed[book_idx]

            if book is None:
                print("Nie znaleziono wypożyczenia!\n")
                return
            elif book in reader.extension_requests:
                print("Prośba została już wysłana!\n")
            else:
                reader.extension_requests.append(book)
                print(f"Wysłano prośbę o przedłużenie! {book.title} {book.author}\n")
        except IndexError:
            print("Nieprawidłowy nr wypożyczenia!\n")
        except ValueError as e:
            print(e)
        return


    # Obsługa przedłużeń
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
                book.return_copy()
                reader.borrowed_books.remove(book)

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
    user.menu(library)

if __name__ == "__main__":
    main()
