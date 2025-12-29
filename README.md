# URL Shortener with Flask and SQLite

## Overview

This project is a simple URL shortener built using Python and Flask. It allows users to convert long URLs into short, shareable links. Each short link redirects the user to the original URL when accessed. The project is designed to be minimal, easy to understand, and suitable for learning backend fundamentals such as routing, databases, and encoding techniques.

The application uses SQLite as the database, making it lightweight and easy to run locally without any external setup.

## Features

This application provides URL shortening using a Base62 encoding technique. It stores URLs persistently using SQLite so that shortened links continue to work across server restarts. The project also includes basic error handling and a simple web interface for user interaction.

An additional feature of this project is failure simulation. Database failures and delays can be simulated using configuration flags, which helps in understanding how real-world systems behave under faulty conditions.

## Tech Stack

The backend is written in Python using the Flask web framework. SQLite is used as the database for storing URLs. HTML is used for rendering templates, and CSS can be added for styling through the static directory.

## How It Works

When a user submits a URL through the web interface, the application first checks whether the URL already exists in the database. If it exists, the existing ID is reused. If not, the URL is inserted into the database, and a unique auto-incremented ID is generated.

This numeric ID is then converted into a Base62 encoded string, which becomes the short URL. When a user accesses the short URL, the application decodes the Base62 string back into the original ID, retrieves the corresponding URL from the database, and redirects the user.

## Project Structure

The main application logic is in `app.py`.  
Database initialization logic is in `init_db.py`.  
Failure simulation configuration is in `failures.py`.  
HTML templates are stored in the `templates` directory.  
Static files such as CSS are stored in the `static` directory.

## Setup Instructions

1. Clone the repository to your local machine.
2. Install the required dependency by installing Flask.
3. Run the database initialization script to create the SQLite database and required table.
4. Start the Flask application by running `app.py`.

Once the server starts, open your browser and visit http://127.0.0.1:5000 to use the application.

## Failure Simulation

The application includes a failure configuration file that allows you to simulate database downtime or artificial delays. This is useful for learning how backend systems handle errors and service unavailability.

You can modify the values in `failures.py` to enable or disable these simulated failures.

## Limitations

This project is intended for learning and local usage. It does not include authentication, rate limiting, or advanced security features. SQLite is used as a local database and is not suitable for high-traffic production environments.

## Future Improvements

Possible enhancements include adding URL expiration, custom short aliases, analytics for link usage, improved UI styling, and migrating the database to a cloud-based solution for multi-device access.

## License

This project is open for learning and personal use. You are free to modify and extend it as needed.
