
## Table Structure

The system uses a MySQL database with the following table structure:

```
CREATE TABLE Contacts (
    sno INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(80) NOT NULL,
    phone_num VARCHAR(120) NOT NULL,
    msg VARCHAR(120) NOT NULL UNIQUE,
    date VARCHAR(120),
    email VARCHAR(120) NOT NULL UNIQUE
);
```

## How to Run

To run this Contacts Management System:

1. Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

2. Install the required Python packages listed below:

    ```
    pip install Flask Flask-SQLAlchemy
    ```

3. Ensure you have MySQL installed and running on your system. You can download MySQL from [mysql.com](https://www.mysql.com/) and follow the installation instructions.

4. Set up a MySQL database and create the `Contacts` table using the provided SQL command.

5. Modify the database connection settings in the Flask application code to connect to your MySQL database. This typically involves setting the `SQLALCHEMY_DATABASE_URI` configuration variable in `app.py` or similar file.

6. Run the Flask application:

    ```
    python app.py
    ```

7. Access the Contacts Management System in your web browser by navigating to `http://localhost:5000`.

## Contributors

- [Shreyash Jagtap](https://github.com/shreyas5522)
