# Real-Time Secure File Sharing System

A real-time file sharing system built with Django, which enables users to upload and download files securely with encryption, expiring links, and one-time download functionality.

## Features

- Secure file uploads with AES encryption
- Automatic file decryption on download
- Expiring download links
- One-time download access
- File versioning support
- Virus/malware scanning using ClamAV
- Admin dashboard to manage files and users
- Drag-and-drop file upload interface

## Technologies Used

- Python 3
- Django
- SQLite (for development)
- JavaScript (for frontend upload interface)
- ClamAV (for virus scanning)
- HTML/CSS (basic templates)

## How to Use

1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies using `pip install -r requirements.txt`
4. Run migrations using `python manage.py migrate`
5. Start the development server: `python manage.py runserver`
6. Upload files from the frontend or Postman
7. Download files using the `/download/<file_id>/` URL

## Admin Panel

- Access via `/admin/`
- Role-based user access
- Manage encrypted files and versions
- Add file expiry time and control downloads




