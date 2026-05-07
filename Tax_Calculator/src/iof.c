#include "iof.h"
#include <stddef.h>

// Definindo constantes para facilitar a manutenção
#define IOF_FIXED_RATE 0.0038
#define IOF_DAILY_PJ   0.000041
#define IOF_DAILY_PF   0.000082
#define IOF_FX_CASH    0.011
#define IOF_FX_CARD    0.0238 // Rate for 2026

int calculate_iof(IOFRequest req, double *result) {
    if (result == NULL) return -4;
    if (req.amount < 0 || req.days < 0) return ERR_INVALID_INPUT; // Proteção extra

    double total = 0.0;

    switch (req.operation_type) {
        case IOF_CREDITO_PJ: {
            int effective_days = (req.days > 365) ? 365 : req.days;
            total = (req.amount * IOF_FIXED_RATE) + (req.amount * IOF_DAILY_PJ * effective_days);
            break;
        }

        case IOF_CAMBIO_CASH:
            total = req.amount * IOF_FX_CASH;
            break;

        case IOF_CAMBIO_CARD:
            total = req.amount * IOF_FX_CARD;
            break;

        case IOF_SEGUROS:
            total = req.amount * 0.0738;
            break;

        default:
            return ERR_INVALID_OP;
    }

    *result = total;
    return SUCCESS;
}