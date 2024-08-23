# Nginx Log Parser

## tl;dr

1. **Start the project**:
   ```bash
   make up
2. **Parse the log file**
    ```bash
    make parse_log url=YOUR_URL_HERE
3. **Access the admin panel**
    ```bash
    Username: admin
    Password: admin
    http://127.0.0.1:8000/admin/
## Overview

This project is a Django application designed to parse and aggregate Nginx log files. It includes a management command for processing log files from a remote URL (currently implemented only for google drive based resources), parsing the data, and saving it to a database. The application provides a Django admin interface and a DRF API for viewing and managing the parsed logs.

## Features

- **Django Management Command**: Parses and saves Nginx logs from a remote URL.
- **Django Admin Interface**: Manage and filter log entries.
- **DRF API**: View, filter, and paginate log entries. Swagger documentation included.
- **Docker Integration**: The project is containerized using Docker and Docker Compose.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- GNU Make

### Setup and run
> **Note:** All commands provided in this documentation should be executed from the root directory of the project, where the `Makefile` is located. This ensures that all `docker-compose` and `Makefile` commands function correctly.

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <project-directory>
2. **Build and start the containers(two):**
    ```bash 
    make up
3. **Parse Nginx remote logs (curently implemented only for google drive based resources):**
    ```bash 
    make parse_log url=[your url here]
4. **Stop all Docker containers:**
    ```bash 
    make down