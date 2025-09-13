#<a href="https://studenttracker-vd0h.onrender.com/">Student Performance Tracker</a>

A Flask web application that manages students, subjects, and grades with a clean interface, simple data model, and a small JSON statistics endpoint. It demonstrates routing, server side templating, validated forms, client side filtering and sorting, and a print friendly student report.

## Overview

This project allows registration of students, entry and update of subject grades, viewing of averages with performance labels, and exploration of the roster through search, filters, and two viewing modes. A statistics modal retrieves summary counts and the overall average from a JSON endpoint to support review and demo scenarios.

## Screenshots

Add images by updating the src attribute values below after uploading screenshots to the repository or an image host

<p align="center">
  <img src="\screenshots\Home_Page.png" alt="Home page overview" width="900">
</p>

<br><br>

<p align="center">
  <img src="\screenshots\All_student_list.png" alt="All students list with search and filters" width="900">
</p>

<br><br>

<p align="center">
  <img src="\screenshots\add_new_student.png" alt="Add new students" width="900">
</p>

<p align="center">
  <img src="\screenshots\add_grade.png" alt="Add Grade" width="900">
</p>

<p align="center">
  <img src="\screenshots\stats.png" alt="Stats" width="900">
</p>

## Features

1. Register students with validation for name and unique roll number  
2. Add and update grades per subject with numeric range checks  
3. Compute averages and show performance labels and visual indicators  
4. Explore the roster in table or card layout with client side search and filters  
5. Sort by name, roll number, subjects count, or average in table view  
6. Display summary statistics in a modal backed by a JSON endpoint  
7. Print a concise student summary for quick sharing  
8. External stylesheet and script for caching and maintainability  
9. Optional timed refresh to help during live demos

## Technology

Application  
Flask for routing and server side rendering  
SQLite for persistence  
JSON endpoint for statistics

Interface  
Bootstrap for layout and components  
Bootstrap Icons for visuals  
Custom stylesheet and script for behavior such as filters, sorting, validation, statistics modal, and print support

## Getting Started

Prerequisites  
Python version 3.9 or newer is recommended  
A virtual environment tool of choice

Setup  
Create and activate a virtual environment  
Install project dependencies using the standard Python package manager  
Start the development server  
Open the local address in a browser

Configuration  
Define a strong secret key through an environment variable for production deployments  
Optionally set a custom port and enable or disable debug mode with environment variables

## Data Model

Students include name and roll number fields  
Grades link a roll number to a subject and a numeric grade  
Indexes are created for efficient lookups and updates on roll numbers

## Endpoints

Pages  
GET slash shows the home page with quick actions  
GET or POST slash add underscore student processes student creation  
GET or POST slash add underscore grade processes grade creation and updates  
GET slash view underscore student slash roll number shows the student detail page  
GET slash view underscore all underscore students lists all students with search and filters

API  
GET slash api slash statistics returns total students, total grades, and overall average as JSON

## User Experience

Roster exploration  
Search by name or roll number, filter by performance levels, and toggle between table and card views

Validation and feedback  
Forms provide client side validation hints and visual feedback  
Submission disables buttons and shows progress indicators

Statistics and printing  
A modal fetches statistics through the JSON endpoint  
A print action renders a concise and readable report for a student

## Deployment

Run the application behind a production grade WSGI server  
Set environment variables for secret key, port, and debug mode as appropriate for the target platform  
Use a persistent volume or move to a hosted database service if horizontal scaling is required

## Customization

Branding  
Update name, email, and professional links in the navigation area

Visual style  
Adjust colors, spacing, and animations through the stylesheet

Behavior  
Modify filters, sorting, modal content, refresh behavior, validation rules, and print logic in the script

Screenshots  
Replace the empty src attributes in the screenshots section with the uploaded image links to showcase the application

## Troubleshooting

Styling or scripts not applied  
Confirm the layout template references the external stylesheet and script  
Use a hard reload and verify in browser developer tools that assets load successfully

Template rendering issues  
Verify that each template extends the base layout and defines the expected content blocks  
Check server logs for template name mismatches or syntax errors

Data issues  
Ensure the application has write access to the local database file  
If the schema is corrupted during development, remove the file and restart to reinitialize tables

Routes  
Ensure the student detail route includes the roll number segment in the URL and links are constructed correctly
