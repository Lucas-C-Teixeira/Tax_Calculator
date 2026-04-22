#ifndef IRPF_H
#define IRPF_H

#define SUCCESS 0
#define ERR_INVALID_INPUT -1
#define ERR_NULL_POINTER -2

typedef struct {
    double income;
    int dependents;
} Person;

int calculate_irpf(Person p, double *irpf);

#endif