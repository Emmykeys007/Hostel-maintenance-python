Hostel Maintenance Request System (HMRS) – Python Console Application

Project Overview

The Hostel Maintenance Request System (HMRS) is a Python console-based application that allows students to report hostel maintenance problems such as electrical faults, plumbing issues, or broken furniture, and allows the hostel administration to track and resolve these issues efficiently.

This project demonstrates the application of the Software Development Life Cycle (SDLC) using a real-life problem.

⸻

Objectives
	•	Allow students to submit maintenance requests
	•	Allow admin to view and update request status
	•	Store requests permanently using a CSV file
	•	Provide a simple and reliable menu-driven system

⸻

Software Development Life Cycle (SDLC)

1. Planning

Problem: Hostel complaints are usually reported verbally or via messages and can be forgotten.
Solution: Build a system that stores and tracks all maintenance requests.

Scope:
	•	Students can create and view requests
	•	Admin can view and update requests

⸻

2. Requirements Analysis

Functional Requirements
	•	Student can create a maintenance request
	•	Student can view their submitted requests
	•	Admin can view all requests
	•	Admin can update request status
	•	System generates unique request IDs
	•	Data persists after program closes

Non-Functional Requirements
	•	Simple user interface
	•	Reliable file storage
	•	Input validation
	•	Easy to maintain

⸻

3. System Design

Architecture
	•	Console-based menu system
	•	File-based storage using CSV (data/requests.csv)

Data Stored
	•	Request ID
	•	Student name
	•	Matric number
	•	Hostel
	•	Room
	•	Category
	•	Description
	•	Status
	•	Date created

Status Flow
Submitted → InProgress → Resolved → Closed

⸻

4. Implementation
	•	Language: Python
	•	Storage: CSV file
	•	Uses lists, functions, dataclasses, and file handling

⸻

5. Testing

Test Cases
	•	Create request → Restart program → Request still exists ✅
	•	Admin updates status → Student sees updated status ✅
	•	Invalid status change → Rejected by system ✅
6. How to Run

python main.py
Admin Login
Username: Oluwatosin Emmanuel Temitope
Password: 1234

7. Project Structure

Hostel-maintenance-python/
  main.py
  data/
    requests.csv
  README.md

  8. Future Improvements
  
	•	Assign technicians
	•	Add priority levels
	•	Add search/filter
	•	Add proper authentication
	•	Convert to GUI or web app

⸻

Author

Name: Oluwatosin Emmanuel Temitope
Project: Hostel Maintenance Request System (Python)
