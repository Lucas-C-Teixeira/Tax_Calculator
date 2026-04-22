#include <stdio.h>
#include "../src/irpj.h"

int main(void)
{
    // Test Case 1: Successful calculation
    Company my_company = {1, 50000.0, 10000.0, 0.32};
    double result = 0.0;
    
    int status = calculate_irpj(my_company, &result);
    
    if (status == SUCCESS)
    {
        printf("Test 1 (Success) passed! Calculated IRPJ: R$ %.2f\n", result);
    }
    else
    {
        printf("Test 1 failed with status code: %d\n", status);
    }

    // Test Case 2: Invalid regime test
    Company invalid_company = {99, 1000.0, 0.0, 0.0};
    status = calculate_irpj(invalid_company, &result);
    
    if (status == ERR_INVALID_REGIME)
    {
        printf("Test 2 (Invalid Regime) passed! System correctly caught the error.\n");
    }

    return 0;
}