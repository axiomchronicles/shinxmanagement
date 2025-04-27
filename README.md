
# ShinxManagement

**ShinxManagement** is a modern and secure banking application that allows users to manage their personal finances, access their accounts, and interact with banking services. The app provides a seamless user experience through account setup, login functionality, and a simple, intuitive interface for managing financial activities.

## Features

- **Account Setup**: Users can create a secure account, set a password, and agree to terms & conditions.
- **Login & Authentication**: Secure login using Customer ID or Email.
- **Password Strength Validation**: Ensures that users create strong passwords during account setup.
- **Two-Factor Authentication (2FA)**: Option to enable 2FA for additional security.
- **Terms and Conditions**: Users must agree to T&C during account setup.
- **Alert Notifications**: Users can opt to receive SMS/Email alerts for transactions or account updates.

## Technologies Used

- **Frontend**:
  - HTML, CSS (TailwindCSS)
  - JavaScript (Vanilla)
- **Backend**:
  - **Aquilify** (ASGI Python Web Server)
- **Databases**:
  - **SQLite** (Relational Database)
  - **Electrus** (NoSQL In-memory Database, Hyper Fast)

## Getting Started

### Prerequisites

1. **Aquilify**: Aquilify is an ASGI web server. Install it using the following:
   ```bash
   pip install aquilify
   ```

2. **SQLite**: SQLite is used as the relational database for storing user data.
   
3. **Electrus**: Electrus is a NoSQL memory-based database used for fast, real-time interactions. Install it using:
   ```bash
   pip install electrus
   ```

4. **Python**: Python 3.x is required for running the backend.
   
### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/ShinxManagement.git
   ```

2. Navigate to the project directory:
   ```bash
   cd ShinxManagement
   ```

3. Install required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the SQLite database by running the following command:
   ```bash
   python setup_db.py
   ```

5. Run the Aquilify ASGI server:
   ```bash
   aquilify run app:app
   ```

   The app will be accessible at `http://localhost:8000/` (or your specified port).

### Frontend

The frontend of the application is built using pure **HTML**, **CSS** (with **TailwindCSS**), and **JavaScript**. It is a responsive, user-friendly interface designed to work across devices.

### Backend

The backend is powered by **Aquilify**, an ASGI web server. It handles user authentication, account management, and interacts with two databases:

- **SQLite**: Stores user data, passwords, and transactional information.
- **Electrus**: Used for fast, memory-based storage of temporary data for quick processing.

## Screenshots

Here are some screenshots of the application:

1. **Account Setup Screen:**
   ![Account Setup](assets/account-setup.png)

2. **Login Screen:**
   ![Login Screen](assets/login-screen.png)

## Contributing

Contributions are welcome! To contribute to this project, follow these steps:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **TailwindCSS** for the utility-first CSS framework.
- **Aquilify** for the ASGI server.
- **SQLite** for relational database management.
- **Electrus** for high-speed, in-memory NoSQL database management.
