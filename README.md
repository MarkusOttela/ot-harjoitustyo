<img align="right" src="https://raw.githubusercontent.com/MarkusOttela/ot-harjoitustyo/master/logo.png" style="position: relative; top: 0; left: 0;">

# Calorinator 

The program supports the user in maintaining their diet by
  1. Tracking their meals, and by counting the nutritional values of each meal
  2. Informing them about the daily consumption in relation to their goal values
  3. Creating statistics about food and nutrient consumption, and progress of the diet

**Privacy preserving design**

* Locally hosted, all persistent data encrypted
* State-of-the-art cryptography (Argon2id, XChaCha20-Poly1305, BLAKE2b)
* Web UI that can be used via Tailscale (WireGuard) 


## Platform Support
* Linux / Python 3.10+


### Documentation

* [User Manual](https://github.com/MarkusOttela/ot-harjoitustyo/blob/master/Documentation/01%20-%20User%20Manual.md)
* [Functional Specification](https://github.com/MarkusOttela/ot-harjoitustyo/blob/master/Documentation/02%20-%20Functional%20Specification.md)
* [Program Architecture](https://github.com/MarkusOttela/ot-harjoitustyo/blob/master/Documentation/03%20-%20Architectural%20Design.md)
* [Testing](https://github.com/MarkusOttela/ot-harjoitustyo/blob/master/Documentation/04%20-%20Testing.md)
* [Hour Tracker](https://github.com/MarkusOttela/ot-harjoitustyo/blob/master/Documentation/05%20-%20Hour%20Tracker.md)
* [Changelog](https://github.com/MarkusOttela/ot-harjoitustyo/blob/master/Documentation/06%20-%20Changelog.md)


### Installation

```
sudo apt update
curl -sSL https://install.python-poetry.org | POETRY_HOME=$HOME/.local python3 -
echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> $HOME/.bashrc
/bin/bash
git clone --depth 1 https://github.com/MarkusOttela/ot-harjoitustyo.git $HOME/calorinator
cd $HOME/calorinator/
poetry install --without dev
 ```


### Launching

```
cd $HOME/calorinator/
poetry run python3 calorienator.py
```


### Development

```
sudo apt update
curl -sSL https://install.python-poetry.org | POETRY_HOME=$HOME/.local python3 -
echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> $HOME/.bashrc
/bin/bash
git clone https://github.com/MarkusOttela/ot-harjoitustyo.git $HOME/calorinator
cd $HOME/calorinator/
poetry install
 ```

---

### Viikkotehtävät

#### Viikko 1

* Tehtävä 1: Komentorivin harjoittelua
  * [komentorivi.txt](https://github.com/MarkusOttela/ot-harjoitustyo/blob/master/laskarit/viikko1/komentorivi.txt)

* Tehtävä 11: Harjoittelua
  * [gitlog.txt](https://github.com/MarkusOttela/ot-harjoitustyo/blob/master/laskarit/viikko1/gitlog.txt)

* Tehtävä 14: Lisää tiedostoja / Tyylit
  * Normaalia tekstiä
  * **Lihavoitua tekstiä**
  * _Kursivoitua tekstiä_

* Tehtävä 16: Lisää GitHubia
  * Kaivattu muutos :)

* Tehtävä 17: Paikallisen ja etärepositorion epäsynkrooni
  * Paikallinen muutos


#### Viikko 2

* Tehtävät 1..3
  * [Yksikkötestit](https://github.com/MarkusOttela/ot-harjoitustyo/blob/master/laskarit/viikko2/maksukortti/src/tests/maksukortti_test.py#L40)

* Tehtävät 6 ja 7
  * [Maksukortin yksikkötestit](https://github.com/MarkusOttela/ot-harjoitustyo/blob/master/laskarit/viikko2/unicafe/src/tests/maksukortti_test.py)

* Tehtävä 8
  * [Kassapäätteen yksikkötestit](https://github.com/MarkusOttela/ot-harjoitustyo/blob/master/laskarit/viikko2/unicafe/src/tests/kassapaate_test.py)

* Tehtävä 9
  * [Rivikattavuus-screenshot](https://github.com/MarkusOttela/ot-harjoitustyo/blob/master/laskarit/viikko2/unicafe_rivikattavuus.png)
