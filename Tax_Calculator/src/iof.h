#ifndef IOF_H
#define IOF_H

/**
 * IOF (Tax on Financial Operations) - Constants and Definitions
 * CS50 Final Project - 2026 Updated Rates
 */

// Return Status Codes
#define SUCCESS             0
#define ERR_INVALID_OP     -1
#define ERR_INVALID_INPUT  -2
#define ERR_NULL_POINTER   -4

/**
 * Operation Types
 * These must match the switch case in your iof.c
 */
typedef enum {
    IOF_CREDITO_PJ,
    IOF_CAMBIO_CASH,
    IOF_CAMBIO_CARD,
    IOF_SEGUROS
} IOFType;

/**
 * Request Structure
 * Maps the data coming from Python/Flask
 */
typedef struct {
    double amount;          // Transaction value
    int days;               // Number of days (for credit)
    IOFType operation_type; // Type of operation selected
} IOFRequest;

/**
 * Function Prototype
 * Implementation found in iof.c
 */
int calculate_iof(IOFRequest req, double *result);

#endif