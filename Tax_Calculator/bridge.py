import ctypes
import os

# 1. Load the dynamic library
lib_path = os.path.join(os.getcwd(), 'bin', 'libtaxes.dll')

try:
    tax_lib = ctypes.CDLL(lib_path)
except OSError as e:
    print(f"ERROR: Could not load libtaxes.dll at {lib_path}")
    print(f"Details: {e}")
    exit(1)

# --- C ENUMS MIRRORING ---
class TaxRegime:
    REAL_PROFIT = 1
    PRESUMED_PROFIT = 2

class IOFType:
    IOF_CREDITO_PJ = 0
    IOF_CAMBIO_CASH = 1
    IOF_CAMBIO_CARD = 2
    IOF_SEGUROS = 3

# --- C STRUCTS MIRRORING ---

# From irpj.h
class Company(ctypes.Structure):
    _fields_ = [
        ("regime", ctypes.c_int),
        ("revenue", ctypes.c_double),
        ("expenses", ctypes.c_double),
        ("margin", ctypes.c_double)
    ]

# From irpf.h
class Person(ctypes.Structure):
    _fields_ = [
        ("income", ctypes.c_double),
        ("dependents", ctypes.c_int)
    ]

# From iof.h - Updated to match your latest C struct
class IOFRequest(ctypes.Structure):
    _fields_ = [
        ("amount", ctypes.c_double),
        ("days", ctypes.c_int),
        ("operation_type", ctypes.c_int) # Matches IOFType in C
    ]

# --- FUNCTION SIGNATURES ---

# IRPJ: int calculate_irpj(Company c, double *irpj)
tax_lib.calculate_irpj.argtypes = [Company, ctypes.POINTER(ctypes.c_double)]
tax_lib.calculate_irpj.restype = ctypes.c_int

# IRPF: int calculate_irpf(Person p, double *irpf)
tax_lib.calculate_irpf.argtypes = [Person, ctypes.POINTER(ctypes.c_double)]
tax_lib.calculate_irpf.restype = ctypes.c_int

# IOF: int calculate_iof(IOFRequest req, double *result)
# Fixed: Now only 2 arguments to match your iof.h
tax_lib.calculate_iof.argtypes = [IOFRequest, ctypes.POINTER(ctypes.c_double)]
tax_lib.calculate_iof.restype = ctypes.c_int

# --- UTILS FOR BRAZILIAN FORMATTING ---
def format_brl(value):
    """Formats a float to Brazilian Real currency string."""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- TEST EXECUTION ---
if __name__ == "__main__":
    print("\n--- Tax Engine Bridge Test Suite ---")
    
    # 1. Test IRPJ
    test_comp = Company(regime=TaxRegime.PRESUMED_PROFIT, revenue=100000.0, expenses=50000.0, margin=0.32)
    irpj_res = ctypes.c_double(0.0)
    if tax_lib.calculate_irpj(test_comp, ctypes.byref(irpj_res)) == 0:
        print(f"IRPJ Test: {format_brl(irpj_res.value)}")

    # 2. Test IRPF
    test_person = Person(income=5000.0, dependents=2)
    irpf_res = ctypes.c_double(0.0)
    if tax_lib.calculate_irpf(test_person, ctypes.byref(irpf_res)) == 0:
        print(f"IRPF Test: {format_brl(irpf_res.value)}")

    # 3. Test IOF
    # Type 0 = CREDITO_PJ. We pass operation_type INSIDE the struct now.
    test_iof_req = IOFRequest(amount=10000.0, days=30, operation_type=IOFType.IOF_CREDITO_PJ)
    iof_res = ctypes.c_double(0.0)
    
    if tax_lib.calculate_iof(test_iof_req, ctypes.byref(iof_res)) == 0:
        print(f"IOF Test:  {format_brl(iof_res.value)}")
    else:
        print("IOF Test:  Failed (Check C logic or recompilation)")