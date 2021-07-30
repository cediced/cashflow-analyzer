from dataclasses import dataclass

from cashflow_analyzer.transactions import TRANSACTIONS_TYPES, STEP_TYPES


@dataclass
class AnalyseRequest:
    transaction_type: str = "all"
    step: str = "yearly"
    grouped: bool = False
    payers: list = None


class AgumentsErrors(Exception):
    pass


class AnalyseRequestValidator:
    def __init__(self):
        self.errors = []

    def is_arg_allowed(self, arg, allowed_args):
        if arg not in allowed_args:
            self.errors.append(f"{arg} not in {allowed_args}")

    def is_type_allowed(self, arg, wanted_type):
        if type(arg) is not wanted_type:
            self.errors.append(f"{arg} is not {wanted_type}")

    def validate(self, request: AnalyseRequest):
        self.is_arg_allowed(request.transaction_type, list(TRANSACTIONS_TYPES.keys()))
        self.is_arg_allowed(request.step, list(STEP_TYPES.keys()))
        self.is_type_allowed(request.grouped, bool)

        if request.payers:
            self.is_type_allowed(request.payers, list)
        else:
            request.payers = []

        if len(self.errors) != 0:
            raise AgumentsErrors(self)

    def __repr__(self):
        return "\n".join(self.errors)
