#include <stdio.h>

// Tax regimes used by the company
#define REAL_PROFIT 1        // Profit = revenue - expenses
#define PRESUMED_PROFIT 2    // Profit estimated using a margin

// Threshold above which an extra 10% tax is applied
#define SURCHARGE_THRESHOLD 20000.0

// Return codes to indicate success or specific errors
#define SUCCESS 0
#define ERR_INVALID_REGIME -1
#define ERR_INVALID_MARGIN -2
#define ERR_INVALID_INPUT -3
#define ERR_NULL_POINTER -4

// Basic company data needed for the calculation
typedef struct {
    int regime;        // Tax regime (REAL_PROFIT or PRESUMED_PROFIT)
    double revenue;    // Total revenue
    double expenses;   // Used only for real profit
    double margin;     // Used only for presumed profit
} Company;

/**
 * Calculates IRPJ (Brazilian corporate income tax).
 *
 * The calculation depends on the company's tax regime:
 * - Real profit: revenue minus expenses
 * - Presumed profit: revenue multiplied by a margin
 *
 * After finding the tax base:
 * - 15% is applied
 * - An additional 10% is applied on the amount above 20,000
 */
int calculate_irpj(Company c, double *irpj)
{
    // Make sure the output pointer is valid
    if (irpj == NULL)
        return ERR_NULL_POINTER;

    // Margin must be between 0 and 1
    if (c.margin < 0.0 || c.margin > 1.0)
        return ERR_INVALID_MARGIN;

    // Revenue and expenses cannot be negative
    if (c.revenue < 0.0 || c.expenses < 0.0)
        return ERR_INVALID_INPUT;

    double tax_base = 0.0;

    // Choose how to calculate profit depending on the regime
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
        // Unknown regime
        return ERR_INVALID_REGIME;
    }

    // Tax base should never be negative
    if (tax_base < 0.0)
        tax_base = 0.0;

    // Apply the base IRPJ rate (15%)
    *irpj = tax_base * 0.15;

    // Apply additional 10% on the amount exceeding the threshold
    if (tax_base > SURCHARGE_THRESHOLD)
    {
        *irpj += (tax_base - SURCHARGE_THRESHOLD) * 0.10;
    }

    return SUCCESS;
}