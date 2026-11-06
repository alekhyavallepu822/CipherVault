# CipherVault - Threat Model

## 1. Project Overview

CipherVault is a Django-based secure document-sharing application. It allows document owners to upload documents, share them with selected users, and control download permissions.

## 2. Identified Threats and Mitigations

| Threat | Mitigation |
|---|---|
| Unauthorized document access | Login is required before accessing protected document features. |
| Unauthorized downloads | Only the document owner or a user with active viewing permission can download a document. |
| Access after permission revocation | Revoked users cannot download the document. |
| Unauthorized sharing | Only the document owner can share their documents. |
| Unauthorized permission revocation | Only the document owner can revoke access. |
| Invalid file uploads | File extension and file size are validated. Only PDF, TXT and CSV files are accepted. |
| Fake PDF files | A basic PDF file signature check is performed. |
| Missing security visibility | Access granted and access denied events are recorded in audit logs. |
| Direct public file access | Uploaded files are not intentionally exposed through a public media URL. |

## 3. Security Testing

The following automated tests are implemented:

1. Owner can download their document.
2. Authorized viewer can download a shared document.
3. Unauthorized user cannot download a document.
4. Revoked viewer cannot download a document.
5. Invalid file extensions are rejected.
6. Invalid PDF signatures are rejected.
7. Valid PDF files are accepted by the upload form.

All 7 tests passed during local testing.

## 4. Accepted Risks and Limitations

- The application currently uses SQLite for local development.
- The development configuration has DEBUG enabled and is not suitable for production deployment.
- File validation checks extensions, file size and a basic PDF signature. It does not guarantee that files are safe.
- Antivirus scanning and malware detection are not implemented.
- Rate limiting and advanced security monitoring are not implemented.
- Production deployment requires secure environment variables, HTTPS, proper ALLOWED_HOSTS configuration and production-ready settings.

## 5. Future Improvements

- Add antivirus or malware scanning.
- Implement rate limiting for login and upload operations.
- Use a production database.
- Configure HTTPS and secure deployment settings.
- Improve audit logging and security monitoring.

## 6. Conclusion

CipherVault implements basic document access control, file validation and audit logging. Further security improvements are required before production use.
