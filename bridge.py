import ctypes
import os


# Enums

class TaxRegime:
    REAL_PROFIT = 1
    PRESUMED_PROFIT = 2


class TaxPeriod:
    MONTHLY = 1
    QUARTERLY = 2
    ANNUAL = 3


class DeductionMode:
    SIMPLIFIED = 0
    PERSONALIZED = 1


# C structures

class Company(ctypes.Structure):

    _fields_ = [
        ("regime", ctypes.c_int),
        ("revenue", ctypes.c_double),
        ("expenses", ctypes.c_double),
        ("margin", ctypes.c_double),
        ("period", ctypes.c_int)
    ]


class Person(ctypes.Structure):

    _fields_ = [
        ("income", ctypes.c_double),
        ("dependents", ctypes.c_int),
        ("custom_deduction", ctypes.c_double),
        ("deduction_mode", ctypes.c_int)
    ]


# Main bridge class

class TaxEngineBridge:

    def __init__(self):

        base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        lib_path = os.path.join(
            base_dir,
            "bin",
            "libtaxes.dll"
        )

        try:
            self.tax_lib = ctypes.CDLL(lib_path)

        except OSError as e:

            raise RuntimeError(
                f"ERROR: Could not load libtaxes.dll at {lib_path}\nDetails: {e}"
            )

        self._setup_signatures()

    # Configure C function signatures

    def _setup_signatures(self):

        self.tax_lib.calculate_irpj.argtypes = [
            Company,
            ctypes.POINTER(ctypes.c_double)
        ]

        self.tax_lib.calculate_irpj.restype = ctypes.c_int

        self.tax_lib.calculate_irpf.argtypes = [
            Person,
            ctypes.POINTER(ctypes.c_double)
        ]

        self.tax_lib.calculate_irpf.restype = ctypes.c_int

    # Convert database regime codes to C enums

    def map_db_regime_to_c(self, db_regime_code):

        mapping = {
            "REAL": TaxRegime.REAL_PROFIT,
            "PRESUMED": TaxRegime.PRESUMED_PROFIT
        }

        # Default to presumed profit if the regime is unknown
        return mapping.get(
            str(db_regime_code).upper(),
            TaxRegime.PRESUMED_PROFIT
        )

    # Convert period strings to C enums

    def map_period_to_c(self, period):

        mapping = {
            "monthly": TaxPeriod.MONTHLY,
            "quarterly": TaxPeriod.QUARTERLY,
            "annual": TaxPeriod.ANNUAL
        }

        # Default to quarterly calculations if the period is unknown
        return mapping.get(
            str(period).lower(),
            TaxPeriod.QUARTERLY
        )

    # Calculate IRPJ

    def run_irpj(
        self,
        db_regime_code,
        revenue,
        expenses,
        margin,
        period="quarterly"
    ):

        regime_int = self.map_db_regime_to_c(
            db_regime_code
        )

        period_int = self.map_period_to_c(
            period
        )

        comp = Company(
            regime=regime_int,
            revenue=float(revenue),
            expenses=float(expenses),
            margin=float(margin),
            period=period_int
        )

        result = ctypes.c_double(0.0)

        status = self.tax_lib.calculate_irpj(
            comp,
            ctypes.byref(result)
        )

        if status == 0:
            return result.value

        raise ValueError(
            f"C Engine failed to calculate IRPJ. Status code: {status}"
        )

    # Calculate IRPF

    def run_irpf(
        self,
        income,
        dependents,
        custom_deduction,
        deduction_mode
    ):

        person = Person(
            income=float(income),
            dependents=int(dependents),
            custom_deduction=float(custom_deduction),
            deduction_mode=int(deduction_mode)
        )

        result = ctypes.c_double(0.0)

        status = self.tax_lib.calculate_irpf(
            person,
            ctypes.byref(result)
        )

        if status == 0:
            return result.value

        raise ValueError(
            "C Engine failed to calculate IRPF."
        )

    # Format values as Brazilian currency

    @staticmethod
    def format_brl(value):

        return (
            f"R$ {float(value):,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )


# Local test

if __name__ == "__main__":

    print("\n--- Tax Engine Bridge Test Suite ---")

    bridge = TaxEngineBridge()

    try:

        result = bridge.run_irpj(
            db_regime_code="PRESUMED",
            revenue=100000,
            expenses=0,
            margin=0.32,
            period="quarterly"
        )

        print(
            "IRPJ:",
            bridge.format_brl(result)
        )

    except Exception as e:

        print("Error:", e)