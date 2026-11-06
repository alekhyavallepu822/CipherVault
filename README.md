# CipherVault - Secure Document Sharing

## 1. Project Overview

CipherVault is a Django-based secure document-sharing web application. It allows users to upload documents, share them with selected users and control access through permissions.

The main objective is to protect documents from unauthorized access and maintain a record of access activities.

## 2. Features

- User registration and login.
- User logout.
- Secure document upload.
- Document ownership management.
- Share documents with selected users.
- Permission-based document downloads.
- Revoke previously granted access.
- View documents shared with the logged-in user.
- Audit logging for access-granted and access-denied events.
- File extension and file size validation.
- Basic PDF signature validation.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django 6.1.2 | Web framework |
| SQLite | Database |
| HTML | Web page structure |
| CSS | Web page styling |
| Git and GitHub | Version control and source code hosting |

## 4. Application Routes

| URL | Purpose | Access |
|---|---|---|
| `/` | Home page | Public |
| `/register/` | User registration | Public |
| `/login/` | User login | Public |
| `/logout/` | User logout | Authenticated user |
| `/upload/` | Upload a document | Authenticated user |
| `/my-documents/` | View owned documents | Authenticated user |
| `/share/` | Share a document | Authenticated user; owner permissions required |
| `/download/<document_id>/` | Download a document | Owner or authorized viewer |
| `/revoke/<permission_id>/` | Revoke document access | Document owner |
| `/shared-with-me/` | View shared documents | Authenticated user |

**Note:** These are Django application routes, not a REST API. The application uses HTML pages and Django views.

## 5. Security and Access Control

CipherVault includes the following security measures:

1. Authentication is required for protected document operations.
2. Document owners can share their documents with selected users.
3. Only owners or users with active viewing permission can download documents.
4. Unauthorized download requests are denied.
5. Revoked permissions prevent further downloads.
6. Only document owners can manage sharing permissions.
7. Access-granted and access-denied events are recorded in audit logs.
8. Upload validation allows PDF, TXT and CSV extensions.
9. Maximum upload size is 10 MB.
10. PDF uploads are checked using a basic file signature.

## 6. Installation and Setup

### Prerequisites

- Python
- pip
- Git

### Step 1: Clone the repository

```bash
git clone https://github.com/alekhyavallepu822/CipherVault.git
cd CipherVault
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

### Step 3: Activate the virtual environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the virtual environment Python executable directly:

```powershell
.\.venv\Scripts\python.exe
```

### Step 4: Install Django

```bash
pip install -r requirements.txt
```

### Step 5: Set the Django secret key

For Windows PowerShell:

```powershell
$env:DJANGO_SECRET_KEY = (& python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
```

Generate a new secret key for your own local environment. Never commit secret keys to GitHub.

### Step 6: Apply database migrations

```bash
python manage.py migrate
```

### Step 7: Start the development server

```bash
python manage.py runserver
```

Open the following address in your browser:

http://127.0.0.1:8000/

## 7. Automated Testing

Run the test suite using:

```bash
python manage.py test vault
```

### Test Cases

| Test Case | Expected Result |
|---|---|
| Owner downloads document | Allowed |
| Authorized viewer downloads document | Allowed |
| Unauthorized user downloads document | Denied |
| Revoked viewer downloads document | Denied |
| Invalid file extension | Rejected |
| Invalid PDF signature | Rejected |
| Valid PDF signature | Accepted by upload form |

**Latest local test result:** 7 tests passed.

## 8. Security Limitations

- The project currently uses SQLite for development.
- DEBUG is enabled in the current development configuration.
- The application has not been configured for production deployment.
- Basic file validation does not guarantee that uploaded files are safe.
- Antivirus and malware scanning are not implemented.
- Rate limiting is not implemented.
- Production deployment requires HTTPS, secure environment variables, proper host configuration and production-ready settings.

Refer to [THREATS.md](THREATS.md) for the threat model and security improvements.

## 9. AI Usage Documentation

AI assistance was used for development guidance, debugging, understanding Django concepts and preparing documentation.

Refer to [PROMPTS.md](PROMPTS.md) for the prompt summaries, AI mistakes, corrections and fixing commits.

## 10. Project Status

- Application developed and tested locally.
- Seven automated tests passed.
- Threat model and AI prompt documentation prepared.
- Live deployment: Not completed yet.

## 11. Future Enhancements

- Add antivirus and malware scanning.
- Implement rate limiting.
- Improve security monitoring.
- Configure production database and deployment.
- Improve the user interface.

## 12. Author

**Project Name:** CipherVault  
**Project Type:** Secure Document Sharing Web Application  
**Framework:** Django  
**Language:** Python