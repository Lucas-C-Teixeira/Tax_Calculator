#include "irpf.h"
#include <stdio.h>

// DEPENDENT DEDUCTION
#define DEPENDENT_DEDUCTION 189.59

// SIMPLIFIED DEDUCTION
#define SIMPLIFIED_RATE 0.20
#define SIMPLIFIED_LIMIT 528.00


// ---------------- INSS ----------------

static double calculate_inss(double salary)
{
    double inss = 0.0;

    if (salary <= 1412.00)
        return salary * 0.075;

    inss += 1412.00 * 0.075;

    if (salary <= 2666.68)
        return inss + (salary - 1412.00) * 0.09;

    inss += (2666.68 - 1412.00) * 0.09;

    if (salary <= 4000.03)
        return inss + (salary - 2666.68) * 0.12;

    inss += (4000.03 - 2666.68) * 0.12;

    if (salary <= 7786.02)
        return inss + (salary - 4000.03) * 0.14;

    inss += (7786.02 - 4000.03) * 0.14;

    return inss;
}


// ---------------- IRPF ----------------

int calculate_irpf(Person p, double *irpf)
{
    if (irpf == NULL)
        return ERR_NULL_POINTER;

    if (
        p.income < 0.0 ||
        p.dependents < 0 ||
        p.custom_deduction < 0.0
    )
    {
        return ERR_INVALID_INPUT;
    }

    // INSS
    double inss = calculate_inss(p.income);

    // DEPENDENT DEDUCTION
    double dependents_discount =
        p.dependents * DEPENDENT_DEDUCTION;

    // DEDUCTION SYSTEM
    double deduction = 0.0;

    // SIMPLIFIED
    if (p.deduction_mode == DEDUCTION_SIMPLIFIED)
    {
        deduction = p.income * SIMPLIFIED_RATE;

        if (deduction > SIMPLIFIED_LIMIT)
            deduction = SIMPLIFIED_LIMIT;
    }

    // PERSONALIZED
    else if (p.deduction_mode == DEDUCTION_PERSONALIZED)
    {
        deduction =
            p.custom_deduction +
            dependents_discount;
    }

    else
    {
        return ERR_INVALID_INPUT;
    }

    // TAX BASE
    double tax_base =
        p.income -
        inss -
        deduction;

    if (tax_base < 0.0)
        tax_base = 0.0;

    // TAX BRACKETS
    double rate = 0.0;
    double fixed = 0.0;

    if (tax_base <= 2112.00)
    {
        *irpf = 0.0;
        return SUCCESS;
    }

    else if (tax_base <= 2826.65)
    {
        rate = 0.075;
        fixed = 158.40;
    }

    else if (tax_base <= 3751.05)
    {
        rate = 0.15;
        fixed = 370.40;
    }

    else if (tax_base <= 4664.68)
    {
        rate = 0.225;
        fixed = 651.73;
    }

    else
    {
        rate = 0.275;
        fixed = 884.96;
    }

    *irpf = (tax_base * rate) - fixed;

    if (*irpf < 0.0)
        *irpf = 0.0;

    return SUCCESS;
}