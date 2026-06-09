#ifndef IRPF_H
#define IRPF_H

#ifdef _WIN32
  #define TAX_API __declspec(dllexport)
#else
  #define TAX_API
#endif

// SUCCESS / ERROR CODES
#define SUCCESS 0
#define ERR_NULL_POINTER -1
#define ERR_INVALID_INPUT -2

// DEDUCTION MODES
#define DEDUCTION_SIMPLIFIED 0
#define DEDUCTION_PERSONALIZED 1

typedef struct
{
    double income;
    int dependents;
    double custom_deduction;
    int deduction_mode;

} Person;

// MAIN FUNCTION
TAX_API int calculate_irpf(Person p, double *irpf);

#endif