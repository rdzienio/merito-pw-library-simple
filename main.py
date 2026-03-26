ksiazki = [
    {"tytul": "Pan Tadeusz", "autor": "Mickiewicz", "sztuk": 3},
    {"tytul": "Lalka", "autor": "Prus", "sztuk": 1},
    {"tytul": "Ferdydurke", "autor": "Gombrowicz", "sztuk": 2},
    {"tytul": "Wladca Pierścieni. Powrot Krola", "autor": "Tolkien", "sztuk": 4},
    {"tytul": "Quo Vadis", "autor": "Sienkiewicz", "sztuk": 3},
    {"tytul": "Wieza jaskolki", "autor": "Sapkowski", "sztuk": 4},
    {"tytul": "Kroniki Jakuba Wedrowycza", "autor": "Pilipiuk", "sztuk": 5},
]

loginy = [
    {"login": "admin", "password": "admin", "rola": "czytelnik"},
    {"login": "dzienro", "password": "123123", "rola": "czytelnik"},
    {"login": "merito", "password": "321321", "rola": "czytelnik"},
]

def main():
    for ksiazka in ksiazki:
        print(f"{ksiazka['tytul']} — {ksiazka['autor']} (dostępne: {ksiazka['sztuk']})")


if __name__ == "__main__":
    main()
