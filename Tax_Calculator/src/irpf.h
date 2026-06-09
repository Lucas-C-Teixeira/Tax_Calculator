#ifndef IRPF_H
#define IRPF_H

#ifdef _WIN32
  #define TAX_API __declspec(dllexport)
#else
  #define TAX_API
#endif

#define SUCCESS 0
#define ERR_INVALID_INPUT -1
#define ERR_NULL_POINTER -2

typedef struct {
    double income;
    int dependents;
} Person;

TAX_API int calculate_irpf(Person p, double *irpf);

#endif