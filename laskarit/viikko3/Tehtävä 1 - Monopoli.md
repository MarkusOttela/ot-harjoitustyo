```mermaid
classDiagram
    Monopoli    "1" --  "2"    Noppa
    Monopoli    "1" --  "2..8" Pelaaja
    Monopoli    "1" --  "1"    Pelilauta
    Pelilauta   "1" -- "40"    Ruutu
    Ruutu       "1" --  "1"    Ruutu : Seuraava ruutu
    Pelinappula "1" --  "1"    Pelaaja
    Pelinappula "1" --  "1"    Ruutu
```