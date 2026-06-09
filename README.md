# YOUR PROJECT TITLE
#### Video Demo:  <URL HERE>
#### Description: CS50 Final Project: A modular tax calculation system combining Flask, SQLite, and a C-based calculation engine to estimate Brazilian individual and corporate income taxes.



---

# Overview

Tax Calculator is a web application designed to calculate Brazilian income taxes for both individuals and companies.

The project was developed as the final project for Harvard University's CS50: Introduction to Computer Science and combines multiple technologies, including C, Python, Flask, SQLite, HTML, and CSS.

Rather than implementing all calculations directly in Python, I chose to build a dedicated tax calculation engine in C and integrate it into the web application using Python's `ctypes` library. This design separates the business logic from the presentation layer and demonstrates interoperability between low-level and high-level programming languages.

The application allows users to register accounts, perform tax calculations, and store calculation history in a relational database.

The primary goal of this project was not only to create a functional tax calculator but also to explore software engineering concepts such as modular architecture, database design, authentication systems, and language integration.

---

# Understanding the Brazilian Tax System

Before discussing the implementation, it is important to understand the problem this project aims to solve.

Brazil has one of the most complex tax systems in the world. Individuals and businesses are subject to different taxation rules, calculation methods, and reporting requirements.

## IRPF – Individual Income Tax

IRPF stands for *Imposto de Renda da Pessoa Física* (Individual Income Tax). Taxpayers may reduce their taxable income through legally allowed deductions such as dependents and deductible expenses.

## IRPJ – Corporate Income Tax

IRPJ stands for *Imposto de Renda da Pessoa Jurídica* (Corporate Income Tax).

This project supports:

### Real Profit (Lucro Real)

Taxes are calculated using the company's actual profit:

Profit = Revenue - Expenses

### Presumed Profit (Lucro Presumido)

The government assumes a predefined profit margin and calculates taxes based on that presumed profit instead of actual profit.

---

# Project Objectives

- Build a complete web application
- Create a reusable tax calculation engine in C
- Integrate Python and C
- Implement user authentication
- Design a relational database
- Apply software engineering principles
- Solve a real-world problem

---

# Main Features

## User Authentication

- User registration
- Secure login
- Password hashing
- Session management
- Logout functionality

## Individual Tax Calculation (IRPF)

- Income analysis
- Dependent deductions
- Taxable income calculation
- Tax estimation

## Corporate Tax Calculation (IRPJ)

- Revenue analysis
- Expense analysis
- Profit calculation
- Tax regime validation
- Tax estimation

## Calculation History

All calculations are stored and can be reviewed later.

---

# System Architecture

```text
User
  ↓
HTML Interface
  ↓
Flask Application
  ↓
Python Bridge (ctypes)
  ↓
C Tax Engine
  ↓
SQLite Database
```

Each layer has a clearly defined responsibility.

---

# Python–C Integration

One of the most important technical aspects of this project is the integration between Python and C.

The bridge layer uses Python's `ctypes` module to:

- Load the compiled library
- Define compatible structures
- Configure function signatures
- Pass data between languages
- Handle results safely

---

# Database Design

The database stores:

- User accounts
- Individual taxpayers
- Companies
- Tax regimes
- Tax calculation history

CPF is the Brazilian taxpayer identification number for individuals.

CNPJ is the Brazilian taxpayer identification number for businesses.

---

# Technologies Used

## Programming Languages

- C
- Python
- SQL
- HTML
- CSS

## Frameworks and Libraries

- Flask
- ctypes
- SQLite
- Werkzeug

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/yourusername/Tax_Calculator.git
cd Tax_Calculator
```

## Create a Virtual Environment

```bash
python -m venv .venv
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Initialize the Database

```bash
python database/setup_db.py
```

## Run the Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# Design Decisions

## Why C?

The calculations could have been implemented entirely in Python. However, implementing the tax engine in C provided:

- Better separation of responsibilities
- Reusable business logic
- Exposure to systems programming
- Demonstration of language interoperability

## Why Flask?

Flask was chosen because it is lightweight, flexible, and ideal for educational projects.

## Why SQLite?

SQLite requires no separate server, is easy to deploy, and is perfectly suitable for a project of this scale.

---

# Challenges Encountered

The most significant challenge was integrating Python and C.

Both languages use different data representations and memory models, requiring careful handling of structures, data types, and function interfaces.

Another challenge was translating Brazilian tax rules into deterministic algorithms while maintaining code readability and modularity.

---

# Future Improvements

- Additional Brazilian taxes
- PDF reports
- REST API
- Docker deployment
- Cloud hosting
- Email verification
- Password recovery
- Automated testing suite

---

# Lessons Learned

This project brought together many concepts learned throughout CS50, including:

- Software architecture
- Database design
- Authentication systems
- Web development
- Systems programming
- Python–C interoperability

More importantly, it demonstrated how multiple technologies can work together to solve a real-world problem.

---

# Author

Lucas Teixeira

Final Project for CS50: Introduction to Computer Science

Harvard University
