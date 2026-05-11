-- database/schema.sql
PRAGMA foreign_keys = ON;

-- 1. ACCOUNT / LOGIN TABLE (The "Who" - Authentication)
CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_guid TEXT NOT NULL UNIQUE, 
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    account_status TEXT CHECK(account_status IN ('ACTIVE', 'LOCKED')) DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. PERSONS TABLE (Individual / PF)
CREATE TABLE persons (
    person_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL, -- Link to Login
    full_name TEXT NOT NULL,
    cpf_number TEXT NOT NULL UNIQUE,
    birth_date DATE,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
);

-- 3. COMPANIES TABLE (Legal Entity / PJ)
CREATE TABLE companies (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL, -- Link to Login
    regime_id INTEGER NOT NULL,  -- Link to tax_regimes
    trade_name TEXT NOT NULL,
    legal_name TEXT NOT NULL,
    cnpj_number TEXT NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (regime_id) REFERENCES tax_regimes(regime_id)
);

-- 4. TAX REGIMES (Lookup table)
CREATE TABLE tax_regimes (
    regime_id INTEGER PRIMARY KEY AUTOINCREMENT,
    regime_code TEXT NOT NULL UNIQUE,
    regime_name TEXT NOT NULL
);

-- 5. CALCULATIONS (Fact table)
-- Linked to either person or company depending on your business logic
-- Here, linked to company as per your original editing service idea
CREATE TABLE tax_calculations (
    calculation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER, -- Optional if it's a person calculation
    person_id INTEGER,  -- Optional if it's a company calculation
    revenue_cents INTEGER NOT NULL,
    tax_amount_cents INTEGER NOT NULL,
    fiscal_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    FOREIGN KEY (person_id) REFERENCES persons(person_id)
);


-- Inserindo os regimes apenas com as colunas existentes
INSERT INTO tax_regimes (regime_code, regime_name) VALUES 
('REAL', 'Lucro Real'),
('PRESUMED', 'Lucro Presumido'),
('SIMPLES', 'Simples Nacional');