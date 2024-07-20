# FC24 Pack Tracker

## Overview

FC24 Pack Tracker is a Chrome extension and backend system designed to track and record when a pack or player pick is opened on the FC24 web app. The extension scrapes relevant data and stores it in a PostgreSQL database using a FastAPI backend with SQLAlchemy for database management.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
    - [Chrome Extension](#chrome-extension)
    - [Backend](#backend)
3. [Usage](#usage)
    - [Chrome Extension Usage](#chrome-extension-usage)
    - [Backend Usage](#backend-usage)
4. [API Endpoints](#api-endpoints)


## Features

- **Chrome Extension**: Monitors and scrapes pack and player pick data when opened on the FC24 web app.
- **Backend**: A FastAPI application to handle incoming data from the extension and store it in a PostgreSQL database.
- **Database**: SQLAlchemy integration for ORM and PostgreSQL database to manage and query the stored data.

## Installation

### Chrome Extension

1. **Clone the repository**:
    ```bash
    git clone https://github.com/stefanosilva94/eafc_analysis.git
    ```

2. **Load the extension**:
    - Open Chrome and navigate to `chrome://extensions/`.
    - Enable "Developer mode" by toggling the switch on the top right corner.
    - Click on "Load unpacked" and select the `extension` directory from this repository.

### Backend

1. **Clone the repository (If not already done)**:
    ```bash
    git clone https://github.com/stefanosilva94/eafc_analysis.git
    ```

2. **Set up a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the environment variables**:
    Create a `.env` file in the `backend` directory and add the following:
    ```
    DATABASE_URL=postgresql+psycopg://user:password@localhost/dbname
    ```

5. **Run the backend server**:
    ```bash
    uvicorn main:app --reload
    ```

## Usage

### Chrome Extension Usage

1. Navigate to the FC24 web app and open a pack or player pick.
2. The extension will automatically scrape the relevant data and send it to the backend.

### Backend Usage

1. Ensure the backend server is running (`uvicorn main:app --reload`).
2. The backend will receive data from the Chrome extension and store it in the PostgreSQL database.

## API Endpoints

- **GET /packs**: Retrieve all pack data.
- **GET /packs/{id}**: Retrieve a specific pack by ID.
- **POST /packs**: Add new pack data.
- **GET /packed_items**: Retrieve all packed item data.
- **GET /packed_items/{id}**: Retrieve a specific packed item by ID.
- **POST /packed_items**: Add new packed item data.


