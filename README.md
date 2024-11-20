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

### Matematyczne Objaśnienie Metody
Symulacja fali dźwiękowej opiera się na równaniu falowym, które w dwóch wymiarach można zapisać jako:

\[ \frac{\partial^2 u}{\partial t^2} = c^2 \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right) \]

gdzie:
- \( u \) to przemieszczenie fali w punkcie \((x, y)\) w czasie \( t \),
- \( c \) to prędkość fali,
- \( \frac{\partial^2 u}{\partial t^2} \) to druga pochodna przemieszczenia względem czasu,
- \( \frac{\partial^2 u}{\partial x^2} \) i \( \frac{\partial^2 u}{\partial y^2} \) to drugie pochodne przemieszczenia względem współrzędnych przestrzennych.

W symulacji numerycznej używamy metody różnic skończonych do przybliżenia tych pochodnych. Dyskretyzacja równania falowego prowadzi do następującej formuły:

\[ u_{\text{next}}[i, j] = 2u[i, j] - u_{\text{prev}}[i, j] + \left( \frac{c \cdot \Delta t}{\Delta x} \right)^2 \left( u[i+1, j] - 2u[i, j] + u[i-1, j] \right) + \left( \frac{c \cdot \Delta t}{\Delta y} \right)^2 \left( u[i, j+1] - 2u[i, j] + u[i, j-1] \right) \]

gdzie:
- \( u_{\text{next}} \) to przemieszczenie w następnym kroku czasowym,
- \( u \) to przemieszczenie w bieżącym kroku czasowym,
- \( u_{\text{prev}} \) to przemieszczenie w poprzednim kroku czasowym,
- \( \Delta t \) to krok czasowy,
- \( \Delta x \) i \( \Delta y \) to odstępy przestrzenne w siatce symulacyjnej.

Dodatkowo, w symulacji uwzględniono tłumienie fali oraz odbicia od ścian, co jest realizowane poprzez odpowiednie warunki brzegowe i współczynnik tłumienia.


## Licencja
Projekt jest dostępny na licencji MIT.