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
#logowanie - użytkownik podaje login i hasło; po 3 nieudanych próbach funkcja się kończy.
def log_in(loginy):
    max_attempts = 3
    attempts = 0

    print("----- LOGOWNIANIE -----")
    while attempts < max_attempts:
        login = input("Login: ").strip()
        password = input("Hasło: ").strip()

        for user in loginy:
            if user["login"] == login and user["password"] == password:
                print(f"\nZalogowano: {user['login']}!")
                return user
        attempts += 1
        print(f"Błędny login lub hasło! Próba {attempts}/{max_attempts}\n")

    print("Przekroczono liczbę prób! Do widzenia.")
    return None

def print_books():
    for ksiazka in ksiazki:
        print(f"{ksiazka['tytul']} — {ksiazka['autor']} (dostępne: {ksiazka['sztuk']})")

def print_main_menu():
    print("\n----------------------------")
    print("1) Przeglądaj książki")
    print("0) Wyloguj")

def main():
    # logowanie - jesli user jest pusty to koniec programu
    user = log_in(loginy)
    if user is None:
        return
    print(f"\nWitaj w systemie biblioteki {user['login']}!")
    while True:
        print_main_menu()
        choice = input("> ").strip()
        if choice == "1":
            print_books()
        elif choice == "0":
            print("Wylogowano!")
            return
        else:
            print("Nieznana opcja, spróbuj ponownie.")
            continue


if __name__ == "__main__":
    main()
