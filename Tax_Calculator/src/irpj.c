#include "irpj.h"
#include <stddef.h>

// Keep only constants that are EXCLUSIVE to the calculation logic
#define SURCHARGE_THRESHOLD 20000.0

int calculate_irpj(Company c, double *irpj)
{
    if (irpj == NULL)
        return ERR_NULL_POINTER;

    // Validation
    if (c.margin < 0.0 || c.margin > 1.0)
        return ERR_INVALID_MARGIN;

    if (c.revenue < 0.0 || c.expenses < 0.0)
        return ERR_INVALID_INPUT;

    double tax_base = 0.0;

    // Calculation logic using the enum from irpj.h
    if (c.regime == REAL_PROFIT)
    {
        tax_base = c.revenue - c.expenses;
    }
    else if (c.regime == PRESUMED_PROFIT)
    {
        tax_base = c.revenue * c.margin;
    }
    else
    {
        return ERR_INVALID_REGIME;
    }

    if (tax_base < 0.0)
        tax_base = 0.0;

    // Base tax (15%)
    *irpj = tax_base * 0.15;

    // Surcharge tax (10%)
    if (tax_base > SURCHARGE_THRESHOLD)
    {
        *irpj += (tax_base - SURCHARGE_THRESHOLD) * 0.10;
    }

    return SUCCESS;
}