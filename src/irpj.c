#include "irpj.h"
#include <stddef.h>

int calculate_irpj(
    Company c,
    double *irpj
)
{
    if (irpj == NULL)
        return ERR_NULL_POINTER;

    /* =========================
       VALIDAÇÕES
       ========================= */

    if (c.margin < 0.0 || c.margin > 1.0)
        return ERR_INVALID_MARGIN;

    if (c.revenue < 0.0 || c.expenses < 0.0)
        return ERR_INVALID_INPUT;

    double tax_base = 0.0;

    /* =========================
       BASE DE CÁLCULO
       ========================= */

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
    {
        tax_base = 0.0;
    }

    /* =========================
       LIMITE DO ADICIONAL
       ========================= */

    double surcharge_threshold;

    switch (c.period)
    {
        case MONTHLY:
            surcharge_threshold = 20000.0;
            break;

        case QUARTERLY:
            surcharge_threshold = 60000.0;
            break;

        case ANNUAL:
            surcharge_threshold = 240000.0;
            break;

        default:
            surcharge_threshold = 60000.0;
            break;
    }

    /* =========================
       IRPJ BASE (15%)
       ========================= */

    *irpj = tax_base * 0.15;

    /* =========================
       ADICIONAL DE IRPJ (10%)
       ========================= */

    if (tax_base > surcharge_threshold)
    {
        *irpj +=
            (tax_base - surcharge_threshold)
            * 0.10;
    }

    return SUCCESS;
}