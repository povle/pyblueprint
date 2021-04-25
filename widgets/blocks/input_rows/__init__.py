from .int_row import IntInputRow
from .bool_row import BoolInputRow
from .float_row import FloatInputRow
from .str_row import StrInputRow

INPUT_ROW_TYPES = {bool: BoolInputRow,
                   int: IntInputRow,
                   float: FloatInputRow,
                   str: StrInputRow}
