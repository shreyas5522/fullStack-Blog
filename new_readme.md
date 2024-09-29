
### Full-Stack Flask Blog Application

The Full-Stack Blog Application is a web platform built with Flask and MySQL, designed for users to create, manage, and share blog posts seamlessly. This application features a user-friendly interface with HTML templates, allowing users to easily navigate through various blog posts and manage their content.

Key features include:
- **User Registration and Authentication:** Users can sign up, log in, and manage their profiles securely.
- **Create and Manage Posts:** Users can write, edit, and delete blog posts with rich content, including titles, subtitles, and images.
- **Responsive Design:** The application is designed to be responsive and user-friendly, ensuring a smooth experience across devices.

This project serves as a comprehensive solution for blogging and contact management, showcasing the power of Flask as a full-stack web framework.
---
### Step 1: Install MySQL Server

1. **Download and Install MySQL:**
   - Visit [MySQL Downloads](https://dev.mysql.com/downloads/mysql/).
   - Choose your operating system and follow the installation instructions.

2. **Start MySQL Server:**
   - On Windows, you can start MySQL from the Services application.
   - On macOS or Linux, use the terminal:
     ```bash
     sudo service mysql start
     ```

3. **Access MySQL Command Line:**
   ```bash
   mysql -u root -p
   ```
   - Enter your MySQL root password when prompted.

### Step 2: Create the Database and Tables

1. **Create a Database:**
   ```sql
   CREATE DATABASE contacts_management;
   USE contacts_management;
   ```

2. **Create Tables:**
   ```sql
   CREATE TABLE Contacts (
       sno INTEGER PRIMARY KEY AUTO_INCREMENT,
       name VARCHAR(80) NOT NULL,
       phone_num VARCHAR(120) NOT NULL,
       msg VARCHAR(120) NOT NULL UNIQUE,
       date VARCHAR(120),
       email VARCHAR(120) NOT NULL UNIQUE
   );

   CREATE TABLE posts (
       sno INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
       title VARCHAR(80) NOT NULL,
       slug VARCHAR(25) NOT NULL,
       content VARCHAR(2500) NOT NULL,
       subtitle VARCHAR(50),
       author VARCHAR(12) NOT NULL DEFAULT 'Shreyas',
       img_file VARCHAR(12),
       date VARCHAR(120)
   );

   CREATE TABLE user (
       id INTEGER NOT NULL AUTO_INCREMENT,
       username VARCHAR(80) NOT NULL UNIQUE,
       password VARCHAR(80) NOT NULL,
       PRIMARY KEY (id)
   );
   ```

### Step 3: Install Python and Required Packages

1. **Download and Install Python:**
   - Go to [Python Downloads](https://www.python.org/downloads/) and install the latest version.

2. **Install Required Python Packages:**
   Open your terminal or command prompt and run:
   ```bash
   pip install Flask Flask-SQLAlchemy mysqlclient
   ```

### Step 4: Run the Flask Application

1. **Run the Application:**
   In your terminal, navigate to the directory containing `app.py` and run:
   ```bash
   python app.py
   ```

2. **Access the System:**
   Open your web browser and go to:
   ```
   http://localhost:5000
   ```
---
