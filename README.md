# Job Application Tracker (CustomTkinter)

A **GUI-based job application tracker** built with Python and CustomTkinter. Designed to help you organize, search, and manage job applications efficiently in one place.

## Features

* Add, edit, and delete job applications
* Search applications by **company name**
* Filter by **application date** and **status**
* Select individual rows or **select all**
* Export applications to **CSV**
* Clean, modern UI with sidebar navigation
* Graphs tab included as a placeholder for future analytics

## Application Fields

Each application stores:

* Company
* Role
* Location
* Date Applied
* Status (Applied, Interview, Rejected, Offer)
* Follow-up Notes

## How to Run

1. Install dependencies:

```bash
pip install customtkinter
```

2. Run the app:

```bash
python3 job_application_tracker.py
```

## Notes

* Exported CSV file is saved as `applications_export.csv`
* Graphs tab is a placeholder for future visualization features
* Window size is fixed for consistent layout
* Navigate to Settings from Menu to export to CSV

## Screenshots
### Application Menu
![image alt](https://github.com/LaytonL24/Job-Application-Tracker/blob/b5e6af15288170300f422e3bd4c602a75b60489b/Application%20Menu.png)

### Add Application
![image alt](https://github.com/LaytonL24/Job-Application-Tracker/blob/d01a618736294a66193a0c66f606eb8f70963411/Add%20Application.png)

