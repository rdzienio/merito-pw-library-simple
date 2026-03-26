ksiazki = [
    {"tytul": "Pan Tadeusz", "autor": "Mickiewicz", "sztuk": 3},
    {"tytul": "Lalka", "autor": "Prus", "sztuk": 1},
    {"tytul": "Ferdydurke", "autor": "Gombrowicz", "sztuk": 2},
    {"tytul": "Władca Pierścieni. Powrót Króla", "autor": "Tolkien", "sztuk": 4},
    {"tytul": "Quo Vadis", "autor": "Sienkiewicz", "sztuk": 3},
    {"tytul": "Wieża jaskółki", "autor": "Sapkowski", "sztuk": 4},
    {"tytul": "Kroniki Jakuba Wędrowycza", "autor": "Pilipiuk", "sztuk": 5},
]

loginy = [
    {"login": "admin", "password": "admin", "rola": "czytelnik"},
    {"login": "dzienro", "password": "123123", "rola": "czytelnik"},
    {"login": "merito", "password": "321321", "rola": "czytelnik"},
]

wypozyczenia = {}


#logowanie - użytkownik podaje login i hasło; po 3 nieudanych próbach funkcja się kończy.
def log_in(users):
    max_attempts = 3
    attempts = 0

    print("----- LOGOWNIANIE -----")
    while attempts < max_attempts:
        login = input("Login: ").strip()    #strip do usuwania białych znaków
        password = input("Hasło: ").strip()

        #porównanie wprowadzonych danych z listą
        for user in users:
            if user["login"] == login and user["password"] == password:
                print(f"\nZalogowano: {user['login']}!")
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
    #logowanie - jesli user jest pusty to koniec programu
    user = log_in(loginy)
    if user is None:
        return
    print(f"\nWitaj w systemie biblioteki {user['login']}!")
    #pętla Menu główne
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


if __name__ == "__main__":
    main()
