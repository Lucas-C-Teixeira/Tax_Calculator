#include "irpf.h"
#include <stdio.h>

//  CONSTANTS 
// Deduction per dependent (monthly)
#define DEPENDENT_DEDUCTION 189.59

// Simplified deduction: 20% of income, capped
#define SIMPLIFIED_RATE 0.20
#define SIMPLIFIED_LIMIT 528.00


//  INSS CALCULATION 
/**
 * Calculates the INSS (Brazilian social security contribution)
 * using a progressive tax system with multiple brackets.
 *
 * @param salary Gross monthly salary
 * @return INSS contribution amount
 */
static double calculate_inss(double salary)
{
    double inss = 0.0;

    // First bracket: up to 1412.00 (7.5%)
    if (salary <= 1412.00)
        return salary * 0.075;

    inss += 1412.00 * 0.075;

    // Second bracket: 1412.01 to 2666.68 (9%)
    if (salary <= 2666.68)
        return inss + (salary - 1412.00) * 0.09;

    inss += (2666.68 - 1412.00) * 0.09;

    // Third bracket: 2666.69 to 4000.03 (12%)
    if (salary <= 4000.03)
        return inss + (salary - 2666.68) * 0.12;

    inss += (4000.03 - 2666.68) * 0.12;

    // Fourth bracket: 4000.04 to 7786.02 (14%)
    if (salary <= 7786.02)
        return inss + (salary - 4000.03) * 0.14;

    // Above ceiling: contribution is capped
    inss += (7786.02 - 4000.03) * 0.14;

    return inss;
}


//  IRPF CALCULATION 
/**
 * Calculates IRPF (Brazilian income tax) using:
 * - INSS deduction
 * - Dependent deduction OR simplified deduction (whichever is greater)
 * - Progressive tax table
 *
 * @param p Struct containing income and number of dependents
 * @param irpf Pointer to store the calculated tax
 * @return SUCCESS (0) or error code (< 0)
 */
int calculate_irpf(Person p, double *irpf)
{
    // Validate pointer
    if (irpf == NULL)
        return ERR_NULL_POINTER;

    // Validate input data
    if (p.income < 0.0 || p.dependents < 0)
        return ERR_INVALID_INPUT;

    // Calculate INSS contribution
    double inss = calculate_inss(p.income);

    //  DEDUCTIONS

    // Deduction based on number of dependents
    double dependent_discount = p.dependents * DEPENDENT_DEDUCTION;

    // Simplified deduction (20% capped)
    double simplified_discount = p.income * SIMPLIFIED_RATE;
    if (simplified_discount > SIMPLIFIED_LIMIT)
        simplified_discount = SIMPLIFIED_LIMIT;

    // Choose the most advantageous deduction
    double deduction = (dependent_discount > simplified_discount)
                        ? dependent_discount
                        : simplified_discount;

    //  TAX BASE 

    // Taxable income after deductions
    double tax_base = p.income - inss - deduction;

    // Ensure tax base is not negative
    if (tax_base < 0.0)
        tax_base = 0.0;

    //  PROGRESSIVE TAX TABLE 

    double rate = 0.0;
    double fixed = 0.0;

    // Exempt bracket
    if (tax_base <= 2112.00)
    {
        *irpf = 0.0;
        return SUCCESS;
    }
    // 7.5% bracket
    else if (tax_base <= 2826.65)
    {
        rate = 0.075;
        fixed = 158.40;
    }
    // 15% bracket
    else if (tax_base <= 3751.05)
    {
        rate = 0.15;
        fixed = 370.40;
    }
    // 22.5% bracket
    else if (tax_base <= 4664.68)
    {
        rate = 0.225;
        fixed = 651.73;
    }
    // 27.5% bracket
    else
    {
        rate = 0.275;
        fixed = 884.96;
    }

    // Final IRPF calculation
    *irpf = (tax_base * rate) - fixed;

    // Ensure tax is not negative
    if (*irpf < 0.0)
        *irpf = 0.0;

    return SUCCESS;
}