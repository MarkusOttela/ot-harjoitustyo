Functional Specification
===

## 1.1 The purpose of the application

The program supports the user in maintaining their diet by
  1. Tracking their meals, and by counting the nutritional values of each meal
  2. Informing them about the daily consumption
  3. Creating statistics about progress of the diet


## 1.1 Users

#### Normal users
  * The program has one or more `normal users`
  * The users are able to control their own information completely
  * The users are able to control shared information completely


#### Privileged users
  * The program does not have `privileged user` accounts


## 1.2.0 General Functionality

**DONE: Before login**
  * User can log in, or register a new account
  * User can edit public ingredient, recipe and mealprep databases


**DONE: User registration**
  * The user selects a username that hasn't been reserved locally yet
  * The user sets a password for their account


**DONE: Initial Survey**
  * The user enters their
    * Date of birth
    * Initial weight, height
    * Diet details
    * The system then calculates
      * The user's basal metabolic rate (calories/day if they just lied on couch)
      * User's daily calorie and macronutrient goals based on given values


**DONE: Login**
  * The user selects their username from list
  * The user enters their password
  * The user is greeted with the main menu


**DONE: The Main Menu** (indent for submenu options)
  * Daily progress
    * Listing of consumed meals and their macros
    * Daily macro goals
  * Statistics
    * Weight progress
  * Shared databases: Creation and editing of
    * Mealprep cooking
    * Single-portion recipes
    * Mealprep recipes
    * Ingredient database
* Logout button
* Exit
    * Exits the program


**DONE: Ingredient Database**
  * The system comes with pre-generated initial ingredient database
  * The user can add ingredients to their own database
  * The user can export their ingredient database (users can create content)
  * The user can user ingredients created by other local users

**DONE: Recipe Database**
    * The user can create single and mealprep recipes by specifying names and main ingredients, as well as 
      accompaniment ingredients for mealprep recipes

**DONE: Meal Creation**

1. ~~The user can add one-time meal portions where~~ 
   * ~~The ingredient weight is not known, but where~~
   * ~~The nutritional values are known (and defined during adding the meal)~~

2. The user can create recipes (templates) that use one or more ingredients in the ingredient database
   * The user can create single portions from these templates by specifying grams of each ingredient used
    * The program will calculate average nutritional values for the mealprep
   * ~~The user can add custom accompaniments for the created meal (define ingredient and grams)~~

3. The user can create a mealprep recipe that use one or more ingredients and one or more accompaniments
   * The user can create an instance of the mealprep recipe by defining grams of each ingredient
       * The program will calculate average nutritional values for the mealprep
   * The user can create meals where the user lists the grams of mealprep and each accompaniment
     * The program will calculate average nutritional values for the mealprep

4. ~~The user can also express the number of pieces of equal weight ingredients with #<integer> instead of floats that represent grams.~~
    NOTE: This will be implemented later: the per-unit grams in the ingredient database are not very useful until then. 

**Done: Automatic services**
  * The system prompts the user to enter their daily morning weight
  * ~~The system prompts the user to enter skin fold and circumference information periodically (weekly or monthly)~~

**Done: Statistics**
  * The user can view diet progress graph (IMPLEMENTED: weight)


## 1.2.1 Feature ideas

* API for importing exercises (that burn calories in addition to BMR) from e.g. Strava
* Web server and simple UI for entering information remotely
* Encrypted progress photo database
* Track sleep
* Manage weight training programs


## 1.3 Security

* All personal data is encrypted before it touches the disk
  * `Argon2id` password hashing for key generation
  * `XChaCha20-Poly1305` authenticated encryption
  * `BLAKE2b` hashing for integrity checks / generic hashing


## 1.4 Platform related constraints

* Programming language: `Python 3.10`
* Frameworks and libraries:
  * GUI
    * `pygame`
    * `pygame-menu`
  * Cryptographic libraries
    * `argon2_cffi`
    * `pynacl`
  * Data analytics
    * `matplotlib`
    * `pandas`
  * Development
    * `py.test`

* Data storage
  * Exclusively local storage
  * Ingredient database is done with SQL
  * Sensitive personal data is implemented in JSON which is encrypted before writing on disk


## 1.5 GUI wireframe designs

### Main Menu
![](https://raw.githubusercontent.com/MarkusOttela/ot-harjoitustyo/master/Documentation/Attachments/00%20-%20Main%20Menu.png)

### Add Ingredient Menu
![](https://raw.githubusercontent.com/MarkusOttela/ot-harjoitustyo/master/Documentation/Attachments/01%20-%20Add%20Ingredient%20Menu.png)
