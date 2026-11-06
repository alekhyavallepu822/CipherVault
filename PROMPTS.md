# CipherVault - AI Prompt and Correction Log

**Project:** CipherVault - Secure Document Sharing  
**AI Tool Used:** ChatGPT  
**Development Period:** November 2026

> Note: The prompt descriptions below summarize the actual development interactions. They are not claimed to be exact verbatim prompts.

## Entry 1 - Django Project Setup and Authentication

**Date:** November 2, 2026

**Prompt / Task Summary:**  
Asked AI to help build a beginner-friendly Django application for secure document sharing, including registration, login and logout.

**AI Output:**  
AI provided Django project structure, authentication views, URL configuration and template guidance.

**What AI Got Wrong:**  
Some setup and URL configuration details needed adjustment to match the existing project structure.

**Correction Made:**  
Reviewed the Django URLs and views, corrected the configuration and tested registration and login locally.

**Fixing Commit:** `a61005b` - Implement secure document sharing with access control and audit logs.

## Entry 2 - Document Permissions and Access Control

**Date:** November 3, 2026

**Prompt / Task Summary:**  
Asked AI to implement secure document sharing so that owners could share documents with selected users and control download permissions.

**AI Output:**  
AI suggested a DocumentPermission model and permission checks for document downloads.

**What AI Got Wrong:**  
The suggested implementation needed to be checked against the actual permission records and owner/viewer roles.

**Correction Made:**  
Tested owner access, authorized viewer access and unauthorized access. Verified that users without active permission were denied downloads.

**Fixing Commit:** `a61005b` - Implement secure document sharing with access control and audit logs.

## Entry 3 - Audit Logging

**Date:** November 4, 2026

**Prompt / Task Summary:**  
Asked AI to add audit logging to record document access decisions.

**AI Output:**  
AI suggested an AuditLog model and recording access-granted and access-denied events.

**What AI Got Wrong:**  
The audit log implementation required database migration and admin registration before the records could be inspected.

**Correction Made:**  
Created and applied the migration, registered AuditLog in Django admin and verified the access events.

**Fixing Commit:** `a61005b` - Implement secure document sharing with access control and audit logs.

## Entry 4 - File Upload Validation

**Date:** November 6, 2026

**Prompt / Task Summary:**  
Asked AI to improve document upload security by validating file extensions, file size and PDF signatures.

**AI Output:**  
AI provided form validation for PDF, TXT and CSV files, a 10 MB size limit and a basic PDF signature check.

**What AI Got Wrong:**  
The first test-file editing attempt caused an indentation problem and an import issue because test imports were placed in the wrong file.

**Correction Made:**  
Corrected the imports, organized the test file and verified that the Django system check passed.

**Fixing Commit:** `65e95a9` - Add file validation and access control tests.

## Entry 5 - Correcting the Download URL in Automated Tests

**Date:** November 6, 2026

**Prompt / Task Summary:**  
Asked AI to resolve failures in the automated document access tests.

**AI Output:**  
AI initially suggested an incorrect URL name in the test code.

**What AI Got Wrong:**  
The test used an incorrect URL name such as `download_document_document`, which caused Django's `NoReverseMatch` error.

**Correction Made:**  
Checked the actual URL pattern in the project and corrected the test to use `download_document`. Re-ran the test suite successfully.

**Verification Result:**  
All 7 automated tests passed.

**Fixing Commit:** `65e95a9` - Add file validation and access control tests.

## Conclusion

AI was used as a development assistant for understanding Django, implementing features, debugging errors and preparing documentation. Its suggestions were reviewed and tested rather than accepted blindly. Incorrect suggestions were corrected by checking the actual project code and running Django checks and automated tests.
