class Book:

    def __init__(self, title, author, total_copies):
        self.title = title
        self.author = author
        self._total_copies = total_copies          # hermetyzacja
        self._available_copies = total_copies
        self.reservations = []

    @property
    def available(self):
        return self._available_copies > 0
    
    @property
    def borrowed_count(self):
        return self._total_copies - self._available_copies

    def borrow(self):
        if not self.available:
            raise ValueError(f"Brak egzemplarzy: {self.title}")
        self._available_copies -= 1

    def return_copy(self):
        if self._available_copies < self._total_copies:
            self._available_copies += 1

    def reserve(self, reader):
        if reader not in self.reservations:
            self.reservations.append(reader)
            return True
        else:
            return False

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
            print("  2. Filtruj katalog")
            print("  3. Sortuj katalog")
            print("  4. Wypożycz")
            print("  5. Zarezerwuj książkę")
            print("  6. Moje wypożyczenia")
            print("  7. Przedłuż wypożyczenie")
            print("  0. Wyloguj")

            choice = input("> ").strip()
            if choice == "1":
                library.show_books()
            elif choice == "2":
                library.filter_books_menu()
            elif choice == "3":
                library.sort_books_menu()
            elif choice == "4":
                library.borrow_book(self)
            elif choice == "5":
                library.reserve_book(self)
            elif choice == "6":
                library.show_user_borrowings(self)
            elif choice == "7":
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
            print("  3. Filtruj katalog")
            print("  4. Sortuj katalog")
            print("  5. Statystyki")
            print("  0. Wyloguj")
            choice = input("> ").strip()
            if choice == "1":
                library.show_borrowings()
            elif choice == "2":
                library.handle_requests()
            elif choice == "3":
                library.filter_books_menu()
            elif choice == "4":
                library.sort_books_menu()
            elif choice == "5":
                library.show_statistics()
            elif choice == "0": #opcja Wylogowanie
                print("Wylogowano!\n")
                return
            else:
                print("Nieznana opcja, spróbuj ponownie.\n")
                continue


# funkcja wyższego rzędu do filtrowania i wyświetlania wyników uzywajaca predykatu            
def display_filtered(collection, predicate, label="Wyniki"):
    results = list(filter(predicate, collection))
    print(f"\n{label} ({len(results)} pozycji):")
    if not results:
        print("Brak wyników!")
    for index, item in enumerate(results, 1):
        print(f"{index}. {item}")
    return results
    

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

    # fancy filtrowanie katalogu - uzycie funkcji wyższego rzędu
    def filter_books_menu(self):
        print("\nFiltrowanie katalogu:")
        print(" 1. Po frazie w tytule")
        print(" 2. Po frazie w autorze")
        print(" 3. Tylko dostępne (niezajęte)")
        choice = input("> ").strip()

        if choice == "1": #lambda + filter
            phrase = input("Podaj frazę do wyszukania w tytule: ").strip().lower()
            display_filtered(self.books, lambda b: phrase in b.title.lower(), f"Książki z '{phrase}' w tytule")
        elif choice == "2": #lambda + filter
            phrase = input("Podaj frazę do wyszukania w autorze: ").strip().lower()
            display_filtered(self.books, lambda b: phrase in b.author.lower(), f"Książki z '{phrase}' w autorze")
        elif choice == "3": #comprehension
            available = [b for b in self.books if b._available_copies > 0]
            print(f"\nDostępne książki ({len(available)} pozycji):")
            for i, b in enumerate(available, 1):
                print(f"  {i}. {b}")
        else:
            print("Nieznana opcja, spróbuj ponownie.\n")

    # fancy sortowanie katalogu - uzycie sorted + lambda
    def sort_books_menu(self):
        print("\nSortowanie katalogu:")
        print(" 1. Po tytule (A-Z)")
        print(" 2. Po autorze (A-Z)")
        print(" 3. Po liczbie dostępnych egzemplarzy (malejąco)")
        choice = input("> ").strip()
        if choice == "1":
            sorted_books = sorted(self.books, key=lambda b: b.title.lower())
            label = "Książki posortowane po tytule (A-Z)"
        elif choice == "2":
            sorted_books = sorted(self.books, key=lambda b: b.author.lower())
            label = "Książki posortowane po autorze (A-Z)"
        elif choice == "3":
            sorted_books = sorted(self.books, key=lambda b: -b._available_copies)
            label = "Książki posortowane po liczbie dostępnych egzemplarzy (malejąco)"
        else:
            print("Nieznana opcja, spróbuj ponownie.\n")
            return
        print(f"\n{label}:")
        for index, book in enumerate(sorted_books, 1):
            print(f"{index}. {book}")

    # Szukanie ksiązki po tytule
    def find_book_by_title(self):
        title = input("Podaj tytuł książki do wypożyczenia: ")
        title = title.strip().lower()  # lower do ignorowania wielkości liter
        return next((b for b in self.books if b.title.strip().lower() == title), None)

    # Wypożyczenie ksiązki
    def borrow_book(self, reader):
        book = self.find_book_by_title()

        if book is None:
            print("Nie znaleziono tytułu!\n")
            return

        if book.available:
            book.borrow()
            reader.borrowed.append(book)
            print(f"{reader.login} wypożyczył: {book.title} - {book.author}\n")
        else:
            print("Książka niedostępna!\n")

    # Rezerwacja książki
    def reserve_book(self, reader):
        unavailable_books = [b for b in self.books if not b.available]
        if not unavailable_books:
            print("Wszystkie książki są dostępne, nie ma czego rezerwować!\n")
            return
        print("\nNiedostępne książki:")
        for index, book in enumerate(unavailable_books, 1):
            print(f"{index}. {book}")

        try:
            choice = int(input("Wybierz nr: ")) - 1
            book_to_reserve = unavailable_books[choice]
            if book_to_reserve.reserve(reader):
                print(f"Złożono prośbę o rezerwację: {book_to_reserve.title} - {book_to_reserve.author}\n")
            else:
                print("Już złożyłeś prośbę o rezerwację tej książki!\n")
        except (ValueError, IndexError):
            print("Nieprawidłowy wybór!\n")


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

        readers = [u for u in self.users if isinstance(u, Reader)]
        for reader in readers:
            requests_copy = reader.extension_requests.copy()
            for book in requests_copy:
                has_reservation = len(book.reservations) > 0
                reservation_info = " Na tę ksiązkę są rezerwacje!" if has_reservation else ""
                print(f"\n  {reader.login} -> {book.title}{reservation_info}")
                decision = input("  Akceptuj? (t/n): ")
                if decision.lower() == "t":
                    print("  Prośba zaakceptowana")
                else:
                    print("  Prośba odrzucona")
                reader.extension_requests.remove(book)

    def show_statistics(self):
        print("\n=== Statystyki ===")
        readers = [u for u in self.users if isinstance(u, Reader)]

        # łączna liczba wypożyczeń - sum + comprehension
        total_borrowed = sum(len(r.borrowed) for r in readers)
        print(f"Łączna liczba wypożyczeń: {total_borrowed}")

        # max + lambda
        if self.books:
            most_popular = max(self.books, key=lambda b: b.borrowed_count)
            print(f"\nNajczęściej wypożyczana książka: {most_popular.title} - {most_popular.author} "
                  f"(wypożyczona {most_popular.borrowed_count} razy)")
            
        # ranking czytelników - sorted + lambda
        ranked_readers = sorted(readers, key=lambda r: -len(r.borrowed))
        print(f"\nRanking czytelników:")
                # map do formatowania wierszy
        rows = list(map(
            lambda r: f"  {r.login}: {len(r.borrowed)} wypożyczeń",
            ranked_readers
        ))
        print("\n".join(rows) if rows else "  Brak czytelników.")
 
        print("======================\n")

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
    library.add_book(Book("Władca Pierścieni. Drużyna Pierścienia", "Tolkien", 5))
    library.add_book(Book("Władca Pierścieni. Dwie Wieże", "Tolkien", 3))
    library.add_book(Book("Quo Vadis", "Sienkiewicz", 3))
    library.add_book(Book("Wieża jaskółki. Wiedźmin. Tom 6", "Sapkowski", 4))
    library.add_book(Book("Chrzest ognia. Wiedźmin. Tom 5", "Sapkowski", 4))
    library.add_book(Book("Kroniki Jakuba Wędrowycza", "Pilipiuk", 5))

    library.add_user(Librarian("admin", "admin"))
    library.add_user(Librarian("merito", "321321"))
    library.add_user(Reader("dzienro", "123123"))
    library.add_user(Reader("kowalski", "abc123"))

    while True:
        print(f"\nWitaj w systemie biblioteki!")
        print("1. Zaloguj")
        print("0. Wyjście")
        choice = input("> ")
        if choice == "1":
            #logowanie - jesli user jest pusty to koniec programu
            user = library.log_in()
            if user is None:
                return
            user.menu(library)

        elif choice == "0":
            print("Do widzenia")
            break
        else:
            print("Nieprawidłowa opcja")

if __name__ == "__main__":
    main()
