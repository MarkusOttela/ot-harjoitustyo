
# Program class hierarchy


```mermaid
classDiagram
    
    IngredientDatabase "1" -- "*" Ingredient
    Main               "1" -- "*" User
    Main               "1" -- "1" GUI
    Main               "1" -- "1" IngredientDatabase
    User               "1" -- "1" UserCredentials
```

# Program exception hierarchy

```mermaid
classDiagram
    
    Exception            <|-- CalorinatorException
    CalorinatorException <|-- DatabaseException 
    DatabaseException    <|-- IngredientNotFound
    CalorinatorException <|-- ValidationError 
    CalorinatorException <|-- ConversionError 
    CalorinatorException <|-- IncompleteConversion 
    CalorinatorException <|-- IncorrectPassword 
    CalorinatorException <|-- AbortMenuOperation 
    CalorinatorException <|-- SecurityException 
```

# Sequence diagram of creating new user

Note that this is high-level description of the process. Library calls and details are omitted. 

```mermaid

sequenceDiagram
    main_menu->>create_new_user: call(gui)
    
    create_new_user->>register_credentials: call(gui)
    register_credentials-->>create_new_user: username, salt
    
    create_new_user->>derive_database_key: call(password)
    derive_database_key-->>create_new_user: salt, database_key

    create_new_user->>UserCredentials: UserCredentials(username, salt, database_key)
    UserCredentials-->>create_new_user: user_credentials
    
    create_new_user->>User: User(user_credentials)
    User-->>create_new_user: user

    create_new_user-->>main_menu: user
```
