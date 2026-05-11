import ctypes
import os

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
class Company(ctypes.Structure):
    _fields_ = [
        ("regime", ctypes.c_int),
        ("revenue", ctypes.c_double),
        ("expenses", ctypes.c_double),
        ("margin", ctypes.c_double)
    ]

class Person(ctypes.Structure):
    _fields_ = [
        ("income", ctypes.c_double),
        ("dependents", ctypes.c_int)
    ]

class IOFRequest(ctypes.Structure):
    _fields_ = [
        ("amount", ctypes.c_double),
        ("days", ctypes.c_int),
        ("operation_type", ctypes.c_int) 
    ]

# --- THE FLASK BRIDGE CLASS ---
class TaxEngineBridge:
    def __init__(self):
        # 1. Reliable absolute pathing to prevent Flask routing errors
        base_dir = os.path.dirname(os.path.abspath(__file__))
        lib_path = os.path.join(base_dir, 'bin', 'libtaxes.dll')

        try:
            self.tax_lib = ctypes.CDLL(lib_path)
        except OSError as e:
            raise RuntimeError(f"ERROR: Could not load libtaxes.dll at {lib_path}\nDetails: {e}")

        self._setup_signatures()

    def _setup_signatures(self):
        """Defines the C function signatures to ensure memory safety."""
        # IRPJ
        self.tax_lib.calculate_irpj.argtypes = [Company, ctypes.POINTER(ctypes.c_double)]
        self.tax_lib.calculate_irpj.restype = ctypes.c_int
        # IRPF
        self.tax_lib.calculate_irpf.argtypes = [Person, ctypes.POINTER(ctypes.c_double)]
        self.tax_lib.calculate_irpf.restype = ctypes.c_int
        # IOF
        self.tax_lib.calculate_iof.argtypes = [IOFRequest, ctypes.POINTER(ctypes.c_double)]
        self.tax_lib.calculate_iof.restype = ctypes.c_int

    def map_db_regime_to_c(self, db_regime_code):
        """Translates the SQLite string codes into C Enum integers."""
        mapping = {
            'REAL': TaxRegime.REAL_PROFIT,
            'PRESUMED': TaxRegime.PRESUMED_PROFIT
            # Note: Add 'SIMPLES' here if you update the C code in the future
        }
        # Returns PRESUMED_PROFIT as a safe default fallback
        return mapping.get(str(db_regime_code).upper(), TaxRegime.PRESUMED_PROFIT)

    # --- FLASK WRAPPER METHODS ---
    # These methods handle the conversion from HTML form Strings to C numeric types

    def run_irpj(self, db_regime_code, revenue, expenses, margin):
        regime_int = self.map_db_regime_to_c(db_regime_code)
        
        # Cast inputs to float/int to prevent crashes when receiving web data
        comp = Company(
            regime=regime_int,
            revenue=float(revenue),
            expenses=float(expenses),
            margin=float(margin)
        )
        
        result = ctypes.c_double(0.0)
        status = self.tax_lib.calculate_irpj(comp, ctypes.byref(result))
        
        if status == 0:
            return result.value
        raise ValueError("C Engine failed to calculate IRPJ.")

    def run_irpf(self, income, dependents):
        person = Person(
            income=float(income), 
            dependents=int(dependents)
        )
        
        result = ctypes.c_double(0.0)
        status = self.tax_lib.calculate_irpf(person, ctypes.byref(result))
        
        if status == 0:
            return result.value
        raise ValueError("C Engine failed to calculate IRPF.")

    def run_iof(self, amount, days, operation_type):
        req = IOFRequest(
            amount=float(amount),
            days=int(days),
            operation_type=int(operation_type)
        )
        
        result = ctypes.c_double(0.0)
        status = self.tax_lib.calculate_iof(req, ctypes.byref(result))
        
        if status == 0:
            return result.value
        raise ValueError("C Engine failed to calculate IOF.")

    @staticmethod
    def format_brl(value):
        """Formats a float to a Brazilian Real currency string."""
        return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- TEST EXECUTION ---
if __name__ == "__main__":
    print("\n--- Tax Engine Bridge Test Suite ---")
    bridge = TaxEngineBridge()
    
    # Testing with simulated dynamic inputs (like they would come from Flask/DB)
    test_db_code = "PRESUMED"
    test_revenue = "100000.0" # Simulated string from an HTML form
    test_expenses = "50000.0"
    test_margin = "0.32"

    try:
        res = bridge.run_irpj(test_db_code, test_revenue, test_expenses, test_margin)
        print(f"IRPJ Dynamic Test: {bridge.format_brl(res)}")
    except Exception as e:
        print(f"Test Failed: {e}")