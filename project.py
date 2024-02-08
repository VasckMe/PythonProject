from pip._vendor import requests
from functions.input_data import wprowadz_dane_faktury, wprowadz_dane_platnosci
from functions.save_data import zapisz_faktury_do_pliku, zapisz_platnosc_do_pliku, zapisz_wynik_platnosci_do_pliku
from functions.calculate_data import oblicz_roznice

# Pobiera kurs waluty metoda "GET" z NBP API
def pobierz_kurs_waluty(kod_waluty, data):
    url = f'http://api.nbp.pl/api/exchangerates/rates/A/{kod_waluty}/{data}/?format=json'
    response = requests.get(url)
    match response.status_code:
        case 200:
            kurs_waluty = response.json()['rates'][0]['mid']
            return kurs_waluty
        case 404:
            print(f'404 Błąd podczas pobierania kursu dla {kod_waluty} na dzień {data}')
        case _:
            print(f'{response.status_code} Błąd podczas pobierania kursu dla {kod_waluty} na dzień {data}')

    return None

def main():
    kwota_faktury, data_faktury, kod_waluty_faktury = wprowadz_dane_faktury()
    kwota_platnosci, data_platnosci, kod_waluty_platnosci = wprowadz_dane_platnosci()

    zapisz_faktury_do_pliku(kwota_faktury, data_faktury, kod_waluty_faktury)
    zapisz_platnosc_do_pliku(kwota_platnosci, data_platnosci, kod_waluty_platnosci)
        
    kurs_waluty_faktury = pobierz_kurs_waluty(kod_waluty_faktury, data_faktury)
    kurs_waluty_platnosci = pobierz_kurs_waluty(kod_waluty_platnosci, data_platnosci)

    if kurs_waluty_faktury is not None and kurs_waluty_platnosci is not None:
        wynik, roznica = oblicz_roznice(kwota_faktury*kurs_waluty_faktury, kwota_platnosci*kurs_waluty_platnosci)
        zapisz_wynik_platnosci_do_pliku(wynik, roznica)
    else:
        print("Error appeared, kurs_waluty_faktury or kurs_waluty_platnosci is None")

if __name__ == "__main__":
    main()