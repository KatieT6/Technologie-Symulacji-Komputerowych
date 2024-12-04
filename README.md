# Symulacja Fali Dźwiękowej

## Autorzy:
- Marcin Mazur 242467
- Katarzyna Tyszka 242567

## Opis Projektu
Projekt symulacji fali dźwiękowej w pomieszczeniu z możliwością interakcji użytkownika. Użytkownik może generować impulsy falowe poprzez kliknięcie w obszar symulacji oraz ładować konfiguracje pomieszczenia z pliku JSON.

## Wymagania
- Python 3.11
- Pygame
- Pygame GUI
- NumPy
- Matplotlib

## Instalacja
1. Sklonuj repozytorium:
    ```sh
    git clone https://github.com/KatieT6/Technologie-Symulacji-Komputerowych.git
    cd ./Technologie-Symulacji-Komputerowych
    ```

2. Utwórz i aktywuj wirtualne środowisko:
    ```sh
    python -m venv venv
    source venv/bin/activate  # Na Windows: venv\Scripts\activate
    ```

3. Zainstaluj wymagane pakiety:
    ```sh
    pip install -r requirements.txt
    ```

## Uruchomienie
Plik EXE w katalogu ./dist
```
./dist/main.exe
```

1. Uruchom główny skrypt:
    ```sh
    python main.py
    ```

2. W oknie symulacji:
    - Kliknij przycisk "Select Room", aby wybrać plik JSON z konfiguracją pomieszczenia.
    - Wybierz z menu wyboru typ ścian pomieszczeina.
    - Kliknij w obszar symulacji, aby wygenerować impuls falowy.
    - Użyj suwaków, aby dostosować amplitudę i prędkość fali.
    - Naciśnij klawisz "r", aby zresetować symulację.

## Struktura Projektu
- `main.py`: Główny skrypt symulacji.
- `pokoj.json`: Przykładowy plik JSON z konfiguracją pomieszczenia.

## Opis Implementacji
Symulacja fali dźwiękowej została zaimplementowana w Pythonie z użyciem bibliotek Pygame i NumPy. Główne funkcje to:
- `generate_impulse_at(x_click, y_click)`: Generuje impuls falowy w miejscu kliknięcia.
- `reset_simulation()`: Resetuje stan symulacji.
- `load_room_from_json(file_path)`: Ładuje konfigurację pomieszczenia z pliku JSON.
- `update_wave()`: Aktualizuje stan symulacji fali, uwzględniając tłumienie i odbicia od ścian.
- `rescale_wave_to_colormap(u, gamma)`: Skaluje dane fali do koloru z mapy kolorów.
- `rescale_wave_to_grayscale(u, gamma)`: Skaluje dane fali do obrazu w skali szarości.


## Licencja
Projekt jest dostępny na licencji MIT.