# FireApp

FireApp is a web-based application that displays fire stations and fire incidents on interactive maps using Leaflet and OpenStreetMap. The project uses Django as the backend framework.

## Features

- Display fire stations on a map.
- Display fire incidents on a map.
- Filter fire incidents by city.
- Responsive map integration using Leaflet.

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv env
   env\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   Copy and paste (or press `Ctrl+Click`) the provided link after running the development server.

## Project Structure

- **projectsite/templates/**  
  Contains Django templates for the maps and base layout.
  
- **fire/**  
  Contains the Django views, models, and URL configurations.

- **static/**  
  Contains static files such as images and CSS files.

## Notes

- This README focuses on the mapping functionality. Other features such as the charts have been temporarily disregarded.
- Ensure that the required static assets (like `fireincident.png` and `firetruck.png`) are available in the appropriate `static/img` directory.