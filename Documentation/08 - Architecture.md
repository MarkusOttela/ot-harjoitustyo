
# Class diagram


```mermaid
classDiagram
    
    IngredientDatabase "1" -- "*" Ingredient
    Main               "1" -- "*" User
    Main               "1" -- "1" GUI
    Main               "1" -- "1" IngredientDatabase
    User               "1" -- "1" UserCredentials
```
