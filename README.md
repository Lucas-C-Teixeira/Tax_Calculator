# Tax_Calculator
Tax calculator in C for IRPF and IRPJ, developed as a CS50 final project. Modular structure using header files and separate implementations.

# Brazilian Fiscal Engine & Web Interface

![C](https://img.shields.io/badge/language-C-00599C.svg) ![Python](https://img.shields.io/badge/framework-Flask-000000.svg) ![CS50](https://img.shields.io/badge/course-CS50x-7b68ee.svg)

A high-performance fiscal calculator designed to navigate the multi-layered complexities of the Brazilian tax system. This project features a **hybrid architecture**: a robust core engine written in **C** for mathematical precision, paired with a **Python/Flask** web interface for modern accessibility.

##  Project Overview

The Brazilian tax landscape is globally recognized for its complexity. This project provides a modular and scalable solution to calculate essential taxes like **IRPF** (Individual Income Tax) and **IRPJ** (Corporate Income Tax). By implementing the logic in C, the system ensures strict fiscal accuracy, handling progressive brackets and deductions with sub-millisecond performance.

##  Technical Highlights

* **Hybrid Integration**: Demonstrates advanced architecture by decoupling heavy fiscal logic (C) from the presentation layer (Python).
* **Progressive Tax Modeling**: Accurate implementation of the Brazilian "Tabela Progressiva," including automated INSS deductions.
* **Smart Deduction Logic**: The engine automatically evaluates and selects the most advantageous deduction for the user (Simplified vs. Dependent-based).
* **Corporate Regime Support**: Handles both **Real Profit** (*Lucro Real*) and **Presumed Profit** (*Lucro Presumido*), including automated surcharge calculations for high revenues.
* **Automated Build System**: Full lifecycle management via a smart `Makefile` with pattern substitution and automated directory handling.
* **Robust Memory Safety**: Strict use of headers, custom structs, and error codes (`SUCCESS`, `ERR_NULL_POINTER`, etc.) to ensure system stability.

##  Repository Structure

```text
.
├── src/                # C Source files (Tax logic modules)
├── bin/                # Compiled object files (.o)
├── tests/              # Test suites and main entry point
├── web/                # Flask application (Templates & Static)
├── Makefile            # Automated build script
└── app.py              # Web-to-C Bridge


---

## 🚀 How to Run

### 1. Clone the repository
git clone https://github.com/your-username/tax-calculator.git
cd tax-calculator

### 3. Run the Flask app
pip install flask
python app.py


---

##  Features

- Multi-tax calculation (IRPF, IRPJ, IOF)  
- Modular architecture in C  
- Integration with Python (Flask)  
- Expandable structure  

---

##  Project Status

In development — core logic implemented, improvements ongoing.

---

##  Future Improvements

- Web interface (UI)  
- API endpoints  
- More accurate tax rules  
- Input validation  
- Automated tests  

---

##  Educational Purpose

Developed as part of CS50 to demonstrate:
- Systems programming in C  
- Cross-language integration  
- Real-world financial logic  

---

##  License

Open-source for educational use.
