import json

class ZarzadcaCennika:
    def __init__(self, plik):
        self.sciezka = plik
        self.dane = self.wczytaj_cennik()

    def wczytaj_cennik(self):
        try:
            with open(self.sciezka, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Błąd: Nie znaleziono pliku cennik.json!")
            return None

class Koszyk:
    def __init__(self):
        self.bilety = []

    def wyswietl_koszyk(self):
        if not self.bilety:
            print("\nKoszyk jest pusty.")
            return 0
        suma = 0
        print("\n--- TWÓJ KOSZYK ---")
        for bilet in self.bilety:
            print(f"- {bilet['nazwa']}: {bilet['cena']:.2f} PLN")
            suma += bilet['cena']
        print(f"RAZEM: {suma:.2f} PLN")
        return suma

    def dodaj_bilet(self, nazwa, cena):
        self.bilety.append({"nazwa": nazwa, "cena": cena})

    def wyczysc(self):
        self.bilety = []

class AutomatBiletowy:
    def __init__(self):
        self.cennik_obj = ZarzadcaCennika('cennik.json')
        self.koszyk = Koszyk()
        self.sciezka_wyboru = []

    def pobierz_znak(self, komunikat):
        while True:
            wejscie = input(komunikat).strip().lower()
            if len(wejscie) == 1:
                return wejscie
            print("Błąd: Wpisz tylko jeden znak!")

    def proces_platnosci(self, suma):
        print(f"\nDo zapłaty: {suma:.2f} PLN")
        while True:
            try:
                wplata = float(input("Wrzuć pieniądze (podaj kwotę): "))
                if wplata < suma:
                    print(f"Niewystarczająca kwota. Brakuje {(suma - wplata):.2f} PLN")
                    suma -= wplata
                else:
                    reszta = wplata - suma
                    print(f"Dziękujemy! Wydaję resztę: {reszta:.2f} PLN")
                    print("Bilety zostały wydrukowane.")
                    break
            except ValueError:
                print("Błąd: Podaj poprawną liczbę!")

    def uruchom(self):
        cennik = self.cennik_obj.dane
        if not cennik: return
        
        while True:
            poziom = cennik
            for klucz in self.sciezka_wyboru:
                poziom = poziom[klucz]

            print(f"\n--- MENU: {' / '.join(self.sciezka_wyboru).upper() if self.sciezka_wyboru else 'START'} ---")
            
            opcje = list(poziom.keys())
            mapa_wyboru = {}
            for i, opcja in enumerate(opcje):
                klawisz = str(i + 1)
                mapa_wyboru[klawisz] = opcja
                cena = f"({poziom[opcja]} PLN)" if isinstance(poziom[opcja], (int, float)) else ""
                print(f"[{klawisz}] {opcja} {cena}")

            print("[K] Zobacz koszyk i zapłać")
            print("[R] Resetuj wybór")
            print("[X] Wyjdź")

            znak = self.pobierz_znak("Wybór: ")

            if znak == 'x': break
            elif znak == 'r': self.sciezka_wyboru = []
            elif znak == 'k':
                suma = self.koszyk.wyswietl_koszyk()
                if suma > 0:
                    if self.pobierz_znak("Czy chcesz zapłacić? (t/n): ") == 't':
                        self.proces_platnosci(suma)
                        self.koszyk.wyczysc()
                        self.sciezka_wyboru = []
            elif znak in mapa_wyboru:
                wybrany_klucz = mapa_wyboru[znak]
                if isinstance(poziom[wybrany_klucz], dict):
                    self.sciezka_wyboru.append(wybrany_klucz)
                else:
                    self.koszyk.dodaj_bilet(f"{' '.join(self.sciezka_wyboru)} {wybrany_klucz}", poziom[wybrany_klucz])
                    print(f"DODANO: {wybrany_klucz}")
                    self.sciezka_wyboru = []

if __name__ == "__main__":
    automat = AutomatBiletowy()
    automat.uruchom()