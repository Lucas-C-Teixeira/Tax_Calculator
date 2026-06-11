# TaxCalculator
#### Video Demo:  <[URL HERE](https://youtu.be/tFD_F664FVs)>
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

Before discussing the implementation details, it is important to understand the taxes calculated by this system.

Brazil has one of the most complex tax systems in the world, with different rules for individuals and businesses. This project focuses on two major federal taxes: IRPF (Individual Income Tax) and IRPJ (Corporate Income Tax).

## IRPF – Individual Income Tax

IRPF (Imposto de Renda da Pessoa Física) is a progressive tax applied to an individual's annual income. The amount of tax owed depends on the taxpayer's taxable income after deductions.

In this system, the user provides:

Annual gross income
Number of dependents
Deductible expenses

The application first calculates the taxable income:

Taxable Income = Gross Income − Deductions

After determining the taxable income, the system applies the official progressive tax brackets. Each portion of income is taxed according to its corresponding bracket, rather than applying a single rate to the entire income.

This approach reproduces the way the Brazilian Federal Revenue Service calculates income tax. The final result includes:

Taxable income
Effective tax rate
Total tax due

## IRPJ – Corporate Income Tax

IRPJ (Imposto de Renda da Pessoa Jurídica) is the corporate income tax applied to businesses operating in Brazil.

The application supports two taxation regimes:

Real Profit (Lucro Real)

Under the Real Profit regime, taxes are calculated based on the company's actual profit.

The system receives:

Total revenue
Total expenses

The profit is calculated as:

Profit = Revenue − Expenses

If the company generates a profit, the IRPJ is calculated by applying the corresponding tax rate to that amount. Because the calculation uses the company's real financial results, this regime is generally more accurate but also more complex.

### Real Profit (Lucro Real)

Taxes are calculated using the company's actual profit:

Profit = Revenue - Expenses

### Presumed Profit (Lucro Presumido)

In the Presumed Profit regime, the government assumes that a fixed percentage of the company's revenue represents profit.

Instead of analyzing actual expenses, the system calculates a presumed profit:

Presumed Profit = Revenue × Presumed Margin

The IRPJ is then calculated based on this presumed profit value.

This regime simplifies tax calculations because companies do not need to demonstrate their actual profitability for tax purposes.

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
git clone https://github.com/Lucas-C-Teixeira/Tax_Calculator.git
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
