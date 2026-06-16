*** MEDKON - obróbka XMLa ***

Poniższa insrukcja do odfiltrowania produktów z wyjściowego XMLa, do XML zawierającego tylko produkty,
które mają znaleźć się na stronie Ceneo.

W pierwszej kolejoności należy pobrać najświeższy plik XML z aktualną ofertą Medkon. Należy zapisać ten
plik jako "oferta_medkon.xml". Aby dokonać filtrowania, należy również utwozyć plik .txt z listą ID produktów,
które mają znaleźć się w ofercie. Każdy ID powinien być w osobnym wierszu.

Aby utworzyć plik z IDs produktów, które zawierają wskazaną frazę w nazwie produktu albo w nazwie producenta,
należy użyć skryptu "ids_select.py". Skrypt przyjmuje najpierw pole filtrowania, a potem jedną lub kilka fraz:
python ids_select.py name fraza1 fraza2 fraza3
python ids_select.py producer fraza1 fraza2 fraza3

Tryb "name" wyszukuje frazy w nazwie produktu, np. python ids_select.py name "avene spf".
Tryb "producer" wyszukuje frazy w nazwie producenta, np. python ids_select.py producer boiron.
Można też użyć polskiego aliasu "producent", np. python ids_select.py producent boiron.

Dla zgodności ze starszym użyciem można nadal pominąć pole filtrowania - wtedy skrypt domyślnie filtruje po nazwie produktu,
np. python ids_select.py "avene sun". Można też mieszać pojedyncze słowa i frazy, np. python ids_select.py name avene "la roche".
Jeżeli chcesz wyszukać dwa lub więcej słów występujących obok siebie, wpisz je w cudzysłowie.

Po wyselekcjonowaniu właściwych IDs należy uruchomić skrypt filter_xml.py aby utworzyć nowy plik XML z wybranymi 
produktami o IDs podanymi w pliku lub w kilku plikach. Aby uruchomić ten skrypt należy:
- w jednym folderze trzymać plik filter_xml.py, plik oferta_medkon.xml oraz wybrane listy IDs, np. ids_basic.txt i ids_avene_sun_09_06_2026.txt
- otworzyć skrypt filter_xml
- w terminalu wpisać: python filter_xml.py ids_basic.txt ids_avene_sun_09_06_2026.txt

Skrypt filter_xml.py automatycznie scala ID z podanych plików, usuwa duplikaty i na końcu pokazuje podsumowanie:
ile ID wczytano, ile było unikalnych, ile produktów zapisano do XML oraz ile ID nie występuje już w aktualnym pliku oferta_medkon.xml.

Po uruchimieniu skrytpu w ten sposób generowany jest plik "oferta_filtered_<aktualna-data>". 
Plik ten należy załadować na github, otworzyć go w wersji RAW i adres URL tej wersji należy załadować do Ceneo.


*** Dodawanie nowej apteki do strony - edycja przez panel PrestaShop ***

Aby dodać nową aptekę do systemu, w panelu głównym przejdź do zakładki:Preferencje > Kontakt > Sklepy i kliknij przycisk Dodaj nowy sklep.
Poniżej znajdziesz wyjaśnienie, jak poprawnie wypełnić poszczególne pola formularza.

1. Pola standardowe (wypełnij normalnie)
Te pola uzupełniamy rzeczywistymi danymi apteki:
Nazwa: Wpisz nazwę apteki.
Adres: Wpisz główny adres. (Uwaga: na podstawie tego, co tu wpiszesz, system automatycznie utworzy link podstrony dla tej apteki).
Kod pocztowy, Miasto, Kraj
Szerokość i Długość geograficzna
Telefon oraz Adres e-mail

2. Pola specjalne (wymagają odpowiedniego formatowania)
Niektóre pola w systemie służą do integracji z portalem GdziePoLek lub wyświetlania dodatkowych informacji. Wypełnij je zgodnie z poniższymi wskazówkami:
Adres (2) — Przycisk "Zamów do tej apteki"W tym polu wklejamy tylko końcówkę linku z portalu GdziePoLek, bez początkowej części adresu https://www.gdziepolek.pl/apteki/.
Przykład:Pełny link: https://www.gdziepolek.pl/apteki/w-gnieznie/186/apteka-medkon-ul-dworcowa-9aDo pola wpisz tylko: w-gnieznie/186/apteka-medkon-ul-dworcowa-9a
Fax — Znacznik na mapie GdziePoLekW tym polu wpisujemy wyłącznie numer ID apteki, który znajduje się na samym końcu linku do mapy.
Przykład:Pełny link: https://www.gdziepolek.pl/partner/apteki-medkon?pharmacyId=12102Do pola wpisz tylko: 12102
Notatka — "Informacje o lokalizacji" oraz "Oferta apteki"To pole odpowiada za dwa różne teksty na stronie. Aby system wiedział, co jest czym, musisz rozdzielić oba teksty pionową kreską: | (znak ten znajdziesz na klawiaturze najczęściej nad klawiszem Enter, używając Shift + ).
Tekst przed znakiem | to Informacje o lokalizacji.
Tekst po znaku | to Oferta apteki.

3. Godziny otwarcia (Ważne!)
Ze względu na ustawienia systemu, godziny otwarcia wypełniamy w specyficzny sposób:
Poniedziałek: Wpisz tutaj godziny otwarcia dla dni od poniedziałku do piątku. System automatycznie skopiuje te godziny na resztę tygodnia roboczego.
Wtorek, Środa, Czwartek, Piątek: Zostaw puste.
Sobota i Niedziela: Wypełnij normalnie, zgodnie z faktycznymi godzinami pracy w weekendy.

4. Zakończenie
Zdjęcie: Wgraj zdjęcie apteki w standardowy sposób.
Status (Włączone): Upewnij się, że opcja jest zaznaczona na "Tak", aby apteka była widoczna na stronie. Zapisz zmiany.
