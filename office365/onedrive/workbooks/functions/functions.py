from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult
from office365.permissions import require_permission
from office365.runtime.queries.service_operation import ServiceOperationQuery

if TYPE_CHECKING:
    from office365.runtime.types.json import Json


class WorkbookFunctions(Entity):
    """Used as a container for Microsoft Excel worksheet function"""

    @require_permission(delegated=["Files.ReadWrite"], application=["Files.ReadWrite.All"])
    def abs(self, number):
        """Returns the absolute value of a number. The absolute value of a number is the number without its sign

        Args:
            number (float): The real number of which you want the absolute value.
        """
        return_type = WorkbookFunctionResult(self.context)
        payload = {
            "number": number,
        }
        qry = ServiceOperationQuery(self, "abs", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(delegated=["Files.ReadWrite"], application=["Files.ReadWrite.All"])
    def accr_int(self, issue, first_interest, settlement, rate, par, frequency):
        """Returns the accrued interest for a security that pays periodic interest.

        Args:
            issue (any): The real number of which you want the absolute value.
            first_interest (any): The security's first interest date.
            settlement (any): The security's settlement date. The security settlement date is the date after the
              issue date when the security is traded to the buyer.
            rate (any): The security's annual coupon rate.
            par (any): The security's par value. If you omit par, ACCRINT uses $1,000.
            frequency (any): The number of coupon payments per year. For annual payments, frequency = 1;
              for semiannual, frequency = 2; for quarterly, frequency = 4.
        """
        return_type = WorkbookFunctionResult(self.context)
        payload = {
            "issue": issue,
            "firstInterest": first_interest,
            "settlement": settlement,
            "rate": rate,
            "par": par,
            "frequency": frequency,
        }
        qry = ServiceOperationQuery(self, "accrInt", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(delegated=["Files.ReadWrite"], application=["Files.ReadWrite.All"])
    def accr_int_m(self, issue, settlement, rate, par, basis):
        """Returns the accrued interest for a security that pays periodic interest.

        Args:
            issue (any): The real number of which you want the absolute value.
            settlement (any): The security's settlement date. The security settlement date is the date after the
              issue date when the security is traded to the buyer.
            rate (any): The security's annual coupon rate.
            par (any): The security's par value. If you omit par, ACCRINT uses $1,000.
            basis (any):
        """
        return_type = WorkbookFunctionResult(self.context)
        payload = {
            "issue": issue,
            "settlement": settlement,
            "rate": rate,
            "par": par,
            "basis": basis,
        }
        qry = ServiceOperationQuery(self, "accrIntM", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(delegated=["Files.ReadWrite"], application=["Files.ReadWrite.All"])
    def days(self, start_date: datetime, end_date: datetime) -> WorkbookFunctionResult:
        """Returns the number of days between two dates.

        Args:
            start_date (datetime.datetime): Two dates between which you want to know the number of days.
            end_date (datetime.datetime): Two dates between which you want to know the number of days.
        """
        return_type = WorkbookFunctionResult(self.context)
        payload = {
            "startDate": start_date.isoformat() + "Z",
            "endDate": end_date.isoformat() + "Z",
        }
        qry = ServiceOperationQuery(self, "days", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(delegated=["Files.ReadWrite"], application=["Files.ReadWrite.All"])
    def power(self, number, power):
        """Returns the result of a number raised to a power.

        Args:
            number (int): The base number.
            power (int): The exponent to which the base number is raised.
        """
        return_type = WorkbookFunctionResult(self.context)
        payload = {
            "number": number,
            "power": power,
        }
        qry = ServiceOperationQuery(self, "power", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookFunctions"

    def delta(self, number1: Json, number2: Json) -> WorkbookFunctionResult:
        """delta operation.

        Args:
            number1 (Json):
                number1 parameter
            number2 (Json):
                number2 parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "delta", None, {"number1": number1, "number2": number2}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def acos(self, number: Json) -> WorkbookFunctionResult:
        """acos operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "acos", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def acosh(self, number: Json) -> WorkbookFunctionResult:
        """acosh operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "acosh", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def acot(self, number: Json) -> WorkbookFunctionResult:
        """acot operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "acot", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def acoth(self, number: Json) -> WorkbookFunctionResult:
        """acoth operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "acoth", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def amor_degrc(
        self, cost: Json, date_purchased: Json, first_period: Json, salvage: Json, period: Json, rate: Json, basis: Json
    ) -> WorkbookFunctionResult:
        """amorDegrc operation.

        Args:
            cost (Json):
                cost parameter
            date_purchased (Json):
                datePurchased parameter
            first_period (Json):
                firstPeriod parameter
            salvage (Json):
                salvage parameter
            period (Json):
                period parameter
            rate (Json):
                rate parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "amorDegrc",
            None,
            {
                "cost": cost,
                "datePurchased": date_purchased,
                "firstPeriod": first_period,
                "salvage": salvage,
                "period": period,
                "rate": rate,
                "basis": basis,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def amor_linc(
        self, cost: Json, date_purchased: Json, first_period: Json, salvage: Json, period: Json, rate: Json, basis: Json
    ) -> WorkbookFunctionResult:
        """amorLinc operation.

        Args:
            cost (Json):
                cost parameter
            date_purchased (Json):
                datePurchased parameter
            first_period (Json):
                firstPeriod parameter
            salvage (Json):
                salvage parameter
            period (Json):
                period parameter
            rate (Json):
                rate parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "amorLinc",
            None,
            {
                "cost": cost,
                "datePurchased": date_purchased,
                "firstPeriod": first_period,
                "salvage": salvage,
                "period": period,
                "rate": rate,
                "basis": basis,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def and_(self, values: Json) -> WorkbookFunctionResult:
        """and operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "and", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def arabic(self, text: Json) -> WorkbookFunctionResult:
        """arabic operation.

        Args:
            text (Json):
                text parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "arabic", None, {"text": text}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def areas(self, reference: Json) -> WorkbookFunctionResult:
        """areas operation.

        Args:
            reference (Json):
                reference parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "areas", None, {"reference": reference}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def asc(self, text: Json) -> WorkbookFunctionResult:
        """asc operation.

        Args:
            text (Json):
                text parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "asc", None, {"text": text}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def asin(self, number: Json) -> WorkbookFunctionResult:
        """asin operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "asin", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def asinh(self, number: Json) -> WorkbookFunctionResult:
        """asinh operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "asinh", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def atan(self, number: Json) -> WorkbookFunctionResult:
        """atan operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "atan", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def atan2(self, xnum: Json, ynum: Json) -> WorkbookFunctionResult:
        """atan2 operation.

        Args:
            xnum (Json):
                xNum parameter
            ynum (Json):
                yNum parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "atan2", None, {"xNum": xnum, "yNum": ynum}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def atanh(self, number: Json) -> WorkbookFunctionResult:
        """atanh operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "atanh", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def ave_dev(self, values: Json) -> WorkbookFunctionResult:
        """aveDev operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "aveDev", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def average(self, values: Json) -> WorkbookFunctionResult:
        """average operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "average", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def average_a(self, values: Json) -> WorkbookFunctionResult:
        """averageA operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "averageA", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def average_if(self, range_: Json, criteria: Json, average_range: Json) -> WorkbookFunctionResult:
        """averageIf operation.

        Args:
            range_ (Json):
                range parameter
            criteria (Json):
                criteria parameter
            average_range (Json):
                averageRange parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "averageIf",
            None,
            {"range": range_, "criteria": criteria, "averageRange": average_range},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def average_ifs(self, average_range: Json, values: Json) -> WorkbookFunctionResult:
        """averageIfs operation.

        Args:
            average_range (Json):
                averageRange parameter
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "averageIfs", None, {"averageRange": average_range, "values": values}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def baht_text(self, number: Json) -> WorkbookFunctionResult:
        """bahtText operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "bahtText", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def base(self, number: Json, radix: Json, min_length: Json) -> WorkbookFunctionResult:
        """base operation.

        Args:
            number (Json):
                number parameter
            radix (Json):
                radix parameter
            min_length (Json):
                minLength parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "base", None, {"number": number, "radix": radix, "minLength": min_length}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def bessel_i(self, x: Json, n: Json) -> WorkbookFunctionResult:
        """besselI operation.

        Args:
            x (Json):
                x parameter
            n (Json):
                n parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "besselI", None, {"x": x, "n": n}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def bessel_j(self, x: Json, n: Json) -> WorkbookFunctionResult:
        """besselJ operation.

        Args:
            x (Json):
                x parameter
            n (Json):
                n parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "besselJ", None, {"x": x, "n": n}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def bessel_k(self, x: Json, n: Json) -> WorkbookFunctionResult:
        """besselK operation.

        Args:
            x (Json):
                x parameter
            n (Json):
                n parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "besselK", None, {"x": x, "n": n}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def bessel_y(self, x: Json, n: Json) -> WorkbookFunctionResult:
        """besselY operation.

        Args:
            x (Json):
                x parameter
            n (Json):
                n parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "besselY", None, {"x": x, "n": n}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def beta_dist(self, x: Json, alpha: Json, beta: Json, cumulative: Json, a: Json, b: Json) -> WorkbookFunctionResult:
        """beta_Dist operation.

        Args:
            x (Json):
                x parameter
            alpha (Json):
                alpha parameter
            beta (Json):
                beta parameter
            cumulative (Json):
                cumulative parameter
            a (Json):
                A parameter
            b (Json):
                B parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "beta_Dist",
            None,
            {"x": x, "alpha": alpha, "beta": beta, "cumulative": cumulative, "A": a, "B": b},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def beta_inv(self, probability: Json, alpha: Json, beta: Json, a: Json, b: Json) -> WorkbookFunctionResult:
        """beta_Inv operation.

        Args:
            probability (Json):
                probability parameter
            alpha (Json):
                alpha parameter
            beta (Json):
                beta parameter
            a (Json):
                A parameter
            b (Json):
                B parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "beta_Inv",
            None,
            {"probability": probability, "alpha": alpha, "beta": beta, "A": a, "B": b},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def bin2_dec(self, number: Json) -> WorkbookFunctionResult:
        """bin2Dec operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "bin2Dec", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def bin2_hex(self, number: Json, places: Json) -> WorkbookFunctionResult:
        """bin2Hex operation.

        Args:
            number (Json):
                number parameter
            places (Json):
                places parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "bin2Hex", None, {"number": number, "places": places}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def bin2_oct(self, number: Json, places: Json) -> WorkbookFunctionResult:
        """bin2Oct operation.

        Args:
            number (Json):
                number parameter
            places (Json):
                places parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "bin2Oct", None, {"number": number, "places": places}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def binom_dist(self, number_s: Json, trials: Json, probability_s: Json, cumulative: Json) -> WorkbookFunctionResult:
        """binom_Dist operation.

        Args:
            number_s (Json):
                numberS parameter
            trials (Json):
                trials parameter
            probability_s (Json):
                probabilityS parameter
            cumulative (Json):
                cumulative parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "binom_Dist",
            None,
            {"numberS": number_s, "trials": trials, "probabilityS": probability_s, "cumulative": cumulative},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def binom_dist_range(
        self, trials: Json, probability_s: Json, number_s: Json, number_s2: Json
    ) -> WorkbookFunctionResult:
        """binom_Dist_Range operation.

        Args:
            trials (Json):
                trials parameter
            probability_s (Json):
                probabilityS parameter
            number_s (Json):
                numberS parameter
            number_s2 (Json):
                numberS2 parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "binom_Dist_Range",
            None,
            {"trials": trials, "probabilityS": probability_s, "numberS": number_s, "numberS2": number_s2},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def binom_inv(self, trials: Json, probability_s: Json, alpha: Json) -> WorkbookFunctionResult:
        """binom_Inv operation.

        Args:
            trials (Json):
                trials parameter
            probability_s (Json):
                probabilityS parameter
            alpha (Json):
                alpha parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "binom_Inv", None, {"trials": trials, "probabilityS": probability_s, "alpha": alpha}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def bitand(self, number1: Json, number2: Json) -> WorkbookFunctionResult:
        """bitand operation.

        Args:
            number1 (Json):
                number1 parameter
            number2 (Json):
                number2 parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "bitand", None, {"number1": number1, "number2": number2}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def bitlshift(self, number: Json, shift_amount: Json) -> WorkbookFunctionResult:
        """bitlshift operation.

        Args:
            number (Json):
                number parameter
            shift_amount (Json):
                shiftAmount parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "bitlshift", None, {"number": number, "shiftAmount": shift_amount}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def bitor(self, number1: Json, number2: Json) -> WorkbookFunctionResult:
        """bitor operation.

        Args:
            number1 (Json):
                number1 parameter
            number2 (Json):
                number2 parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "bitor", None, {"number1": number1, "number2": number2}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def bitrshift(self, number: Json, shift_amount: Json) -> WorkbookFunctionResult:
        """bitrshift operation.

        Args:
            number (Json):
                number parameter
            shift_amount (Json):
                shiftAmount parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "bitrshift", None, {"number": number, "shiftAmount": shift_amount}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def bitxor(self, number1: Json, number2: Json) -> WorkbookFunctionResult:
        """bitxor operation.

        Args:
            number1 (Json):
                number1 parameter
            number2 (Json):
                number2 parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "bitxor", None, {"number1": number1, "number2": number2}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def ceiling_math(self, number: Json, significance: Json, mode: Json) -> WorkbookFunctionResult:
        """ceiling_Math operation.

        Args:
            number (Json):
                number parameter
            significance (Json):
                significance parameter
            mode (Json):
                mode parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "ceiling_Math", None, {"number": number, "significance": significance, "mode": mode}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def ceiling_precise(self, number: Json, significance: Json) -> WorkbookFunctionResult:
        """ceiling_Precise operation.

        Args:
            number (Json):
                number parameter
            significance (Json):
                significance parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "ceiling_Precise", None, {"number": number, "significance": significance}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def char(self, number: Json) -> WorkbookFunctionResult:
        """char operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "char", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def chi_sq_dist(self, x: Json, deg_freedom: Json, cumulative: Json) -> WorkbookFunctionResult:
        """chiSq_Dist operation.

        Args:
            x (Json):
                x parameter
            deg_freedom (Json):
                degFreedom parameter
            cumulative (Json):
                cumulative parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "chiSq_Dist", None, {"x": x, "degFreedom": deg_freedom, "cumulative": cumulative}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def chi_sq_dist_rt(self, x: Json, deg_freedom: Json) -> WorkbookFunctionResult:
        """chiSq_Dist_RT operation.

        Args:
            x (Json):
                x parameter
            deg_freedom (Json):
                degFreedom parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "chiSq_Dist_RT", None, {"x": x, "degFreedom": deg_freedom}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def chi_sq_inv(self, probability: Json, deg_freedom: Json) -> WorkbookFunctionResult:
        """chiSq_Inv operation.

        Args:
            probability (Json):
                probability parameter
            deg_freedom (Json):
                degFreedom parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "chiSq_Inv", None, {"probability": probability, "degFreedom": deg_freedom}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def chi_sq_inv_rt(self, probability: Json, deg_freedom: Json) -> WorkbookFunctionResult:
        """chiSq_Inv_RT operation.

        Args:
            probability (Json):
                probability parameter
            deg_freedom (Json):
                degFreedom parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "chiSq_Inv_RT", None, {"probability": probability, "degFreedom": deg_freedom}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def choose(self, index_num: Json, values: Json) -> WorkbookFunctionResult:
        """choose operation.

        Args:
            index_num (Json):
                indexNum parameter
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "choose", None, {"indexNum": index_num, "values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def clean(self, text: Json) -> WorkbookFunctionResult:
        """clean operation.

        Args:
            text (Json):
                text parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "clean", None, {"text": text}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def code(self, text: Json) -> WorkbookFunctionResult:
        """code operation.

        Args:
            text (Json):
                text parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "code", None, {"text": text}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def columns(self, array: Json) -> WorkbookFunctionResult:
        """columns operation.

        Args:
            array (Json):
                array parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "columns", None, {"array": array}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def combin(self, number: Json, number_chosen: Json) -> WorkbookFunctionResult:
        """combin operation.

        Args:
            number (Json):
                number parameter
            number_chosen (Json):
                numberChosen parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "combin", None, {"number": number, "numberChosen": number_chosen}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def combina(self, number: Json, number_chosen: Json) -> WorkbookFunctionResult:
        """combina operation.

        Args:
            number (Json):
                number parameter
            number_chosen (Json):
                numberChosen parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "combina", None, {"number": number, "numberChosen": number_chosen}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def complex(self, real_num: Json, inum: Json, suffix: Json) -> WorkbookFunctionResult:
        """complex operation.

        Args:
            real_num (Json):
                realNum parameter
            inum (Json):
                iNum parameter
            suffix (Json):
                suffix parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "complex", None, {"realNum": real_num, "iNum": inum, "suffix": suffix}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def concatenate(self, values: Json) -> WorkbookFunctionResult:
        """concatenate operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "concatenate", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def confidence_norm(self, alpha: Json, standard_dev: Json, size: Json) -> WorkbookFunctionResult:
        """confidence_Norm operation.

        Args:
            alpha (Json):
                alpha parameter
            standard_dev (Json):
                standardDev parameter
            size (Json):
                size parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "confidence_Norm", None, {"alpha": alpha, "standardDev": standard_dev, "size": size}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def confidence_t(self, alpha: Json, standard_dev: Json, size: Json) -> WorkbookFunctionResult:
        """confidence_T operation.

        Args:
            alpha (Json):
                alpha parameter
            standard_dev (Json):
                standardDev parameter
            size (Json):
                size parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "confidence_T", None, {"alpha": alpha, "standardDev": standard_dev, "size": size}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def convert(self, number: Json, from_unit: Json, to_unit: Json) -> WorkbookFunctionResult:
        """convert operation.

        Args:
            number (Json):
                number parameter
            from_unit (Json):
                fromUnit parameter
            to_unit (Json):
                toUnit parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "convert", None, {"number": number, "fromUnit": from_unit, "toUnit": to_unit}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def cos(self, number: Json) -> WorkbookFunctionResult:
        """cos operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "cos", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def cosh(self, number: Json) -> WorkbookFunctionResult:
        """cosh operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "cosh", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def cot(self, number: Json) -> WorkbookFunctionResult:
        """cot operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "cot", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def coth(self, number: Json) -> WorkbookFunctionResult:
        """coth operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "coth", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def count(self, values: Json) -> WorkbookFunctionResult:
        """count operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "count", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def count_a(self, values: Json) -> WorkbookFunctionResult:
        """countA operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "countA", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def count_blank(self, range_: Json) -> WorkbookFunctionResult:
        """countBlank operation.

        Args:
            range_ (Json):
                range parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "countBlank", None, {"range": range_}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def count_if(self, range_: Json, criteria: Json) -> WorkbookFunctionResult:
        """countIf operation.

        Args:
            range_ (Json):
                range parameter
            criteria (Json):
                criteria parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "countIf", None, {"range": range_, "criteria": criteria}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def count_ifs(self, values: Json) -> WorkbookFunctionResult:
        """countIfs operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "countIfs", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def coup_day_bs(self, settlement: Json, maturity: Json, frequency: Json, basis: Json) -> WorkbookFunctionResult:
        """coupDayBs operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            frequency (Json):
                frequency parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "coupDayBs",
            None,
            {"settlement": settlement, "maturity": maturity, "frequency": frequency, "basis": basis},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def coup_days(self, settlement: Json, maturity: Json, frequency: Json, basis: Json) -> WorkbookFunctionResult:
        """coupDays operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            frequency (Json):
                frequency parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "coupDays",
            None,
            {"settlement": settlement, "maturity": maturity, "frequency": frequency, "basis": basis},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def coup_days_nc(self, settlement: Json, maturity: Json, frequency: Json, basis: Json) -> WorkbookFunctionResult:
        """coupDaysNc operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            frequency (Json):
                frequency parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "coupDaysNc",
            None,
            {"settlement": settlement, "maturity": maturity, "frequency": frequency, "basis": basis},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def coup_ncd(self, settlement: Json, maturity: Json, frequency: Json, basis: Json) -> WorkbookFunctionResult:
        """coupNcd operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            frequency (Json):
                frequency parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "coupNcd",
            None,
            {"settlement": settlement, "maturity": maturity, "frequency": frequency, "basis": basis},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def coup_num(self, settlement: Json, maturity: Json, frequency: Json, basis: Json) -> WorkbookFunctionResult:
        """coupNum operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            frequency (Json):
                frequency parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "coupNum",
            None,
            {"settlement": settlement, "maturity": maturity, "frequency": frequency, "basis": basis},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def coup_pcd(self, settlement: Json, maturity: Json, frequency: Json, basis: Json) -> WorkbookFunctionResult:
        """coupPcd operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            frequency (Json):
                frequency parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "coupPcd",
            None,
            {"settlement": settlement, "maturity": maturity, "frequency": frequency, "basis": basis},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def csc(self, number: Json) -> WorkbookFunctionResult:
        """csc operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "csc", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def csch(self, number: Json) -> WorkbookFunctionResult:
        """csch operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "csch", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def cum_i_pmt(
        self, rate: Json, nper: Json, pv: Json, start_period: Json, end_period: Json, type_: Json
    ) -> WorkbookFunctionResult:
        """cumIPmt operation.

        Args:
            rate (Json):
                rate parameter
            nper (Json):
                nper parameter
            pv (Json):
                pv parameter
            start_period (Json):
                startPeriod parameter
            end_period (Json):
                endPeriod parameter
            type_ (Json):
                type parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "cumIPmt",
            None,
            {"rate": rate, "nper": nper, "pv": pv, "startPeriod": start_period, "endPeriod": end_period, "type": type_},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def cum_princ(
        self, rate: Json, nper: Json, pv: Json, start_period: Json, end_period: Json, type_: Json
    ) -> WorkbookFunctionResult:
        """cumPrinc operation.

        Args:
            rate (Json):
                rate parameter
            nper (Json):
                nper parameter
            pv (Json):
                pv parameter
            start_period (Json):
                startPeriod parameter
            end_period (Json):
                endPeriod parameter
            type_ (Json):
                type parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "cumPrinc",
            None,
            {"rate": rate, "nper": nper, "pv": pv, "startPeriod": start_period, "endPeriod": end_period, "type": type_},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def date(self, year: Json, month: Json, day: Json) -> WorkbookFunctionResult:
        """date operation.

        Args:
            year (Json):
                year parameter
            month (Json):
                month parameter
            day (Json):
                day parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "date", None, {"year": year, "month": month, "day": day}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def datevalue(self, date_text: Json) -> WorkbookFunctionResult:
        """datevalue operation.

        Args:
            date_text (Json):
                dateText parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "datevalue", None, {"dateText": date_text}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def daverage(self, database: Json, field: Json, criteria: Json) -> WorkbookFunctionResult:
        """daverage operation.

        Args:
            database (Json):
                database parameter
            field (Json):
                field parameter
            criteria (Json):
                criteria parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "daverage", None, {"database": database, "field": field, "criteria": criteria}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def day(self, serial_number: Json) -> WorkbookFunctionResult:
        """day operation.

        Args:
            serial_number (Json):
                serialNumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "day", None, {"serialNumber": serial_number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def days360(self, start_date: Json, end_date: Json, method: Json) -> WorkbookFunctionResult:
        """days360 operation.

        Args:
            start_date (Json):
                startDate parameter
            end_date (Json):
                endDate parameter
            method (Json):
                method parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "days360", None, {"startDate": start_date, "endDate": end_date, "method": method}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def db(self, cost: Json, salvage: Json, life: Json, period: Json, month: Json) -> WorkbookFunctionResult:
        """db operation.

        Args:
            cost (Json):
                cost parameter
            salvage (Json):
                salvage parameter
            life (Json):
                life parameter
            period (Json):
                period parameter
            month (Json):
                month parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "db",
            None,
            {"cost": cost, "salvage": salvage, "life": life, "period": period, "month": month},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def dbcs(self, text: Json) -> WorkbookFunctionResult:
        """dbcs operation.

        Args:
            text (Json):
                text parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "dbcs", None, {"text": text}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def dcount(self, database: Json, field: Json, criteria: Json) -> WorkbookFunctionResult:
        """dcount operation.

        Args:
            database (Json):
                database parameter
            field (Json):
                field parameter
            criteria (Json):
                criteria parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "dcount", None, {"database": database, "field": field, "criteria": criteria}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def dcount_a(self, database: Json, field: Json, criteria: Json) -> WorkbookFunctionResult:
        """dcountA operation.

        Args:
            database (Json):
                database parameter
            field (Json):
                field parameter
            criteria (Json):
                criteria parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "dcountA", None, {"database": database, "field": field, "criteria": criteria}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def ddb(self, cost: Json, salvage: Json, life: Json, period: Json, factor: Json) -> WorkbookFunctionResult:
        """ddb operation.

        Args:
            cost (Json):
                cost parameter
            salvage (Json):
                salvage parameter
            life (Json):
                life parameter
            period (Json):
                period parameter
            factor (Json):
                factor parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "ddb",
            None,
            {"cost": cost, "salvage": salvage, "life": life, "period": period, "factor": factor},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def dec2_bin(self, number: Json, places: Json) -> WorkbookFunctionResult:
        """dec2Bin operation.

        Args:
            number (Json):
                number parameter
            places (Json):
                places parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "dec2Bin", None, {"number": number, "places": places}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def dec2_hex(self, number: Json, places: Json) -> WorkbookFunctionResult:
        """dec2Hex operation.

        Args:
            number (Json):
                number parameter
            places (Json):
                places parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "dec2Hex", None, {"number": number, "places": places}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def dec2_oct(self, number: Json, places: Json) -> WorkbookFunctionResult:
        """dec2Oct operation.

        Args:
            number (Json):
                number parameter
            places (Json):
                places parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "dec2Oct", None, {"number": number, "places": places}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def decimal(self, number: Json, radix: Json) -> WorkbookFunctionResult:
        """decimal operation.

        Args:
            number (Json):
                number parameter
            radix (Json):
                radix parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "decimal", None, {"number": number, "radix": radix}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def degrees(self, angle: Json) -> WorkbookFunctionResult:
        """degrees operation.

        Args:
            angle (Json):
                angle parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "degrees", None, {"angle": angle}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def dev_sq(self, values: Json) -> WorkbookFunctionResult:
        """devSq operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "devSq", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def dget(self, database: Json, field: Json, criteria: Json) -> WorkbookFunctionResult:
        """dget operation.

        Args:
            database (Json):
                database parameter
            field (Json):
                field parameter
            criteria (Json):
                criteria parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "dget", None, {"database": database, "field": field, "criteria": criteria}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def disc(self, settlement: Json, maturity: Json, pr: Json, redemption: Json, basis: Json) -> WorkbookFunctionResult:
        """disc operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            pr (Json):
                pr parameter
            redemption (Json):
                redemption parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "disc",
            None,
            {"settlement": settlement, "maturity": maturity, "pr": pr, "redemption": redemption, "basis": basis},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def dmax(self, database: Json, field: Json, criteria: Json) -> WorkbookFunctionResult:
        """dmax operation.

        Args:
            database (Json):
                database parameter
            field (Json):
                field parameter
            criteria (Json):
                criteria parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "dmax", None, {"database": database, "field": field, "criteria": criteria}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def dmin(self, database: Json, field: Json, criteria: Json) -> WorkbookFunctionResult:
        """dmin operation.

        Args:
            database (Json):
                database parameter
            field (Json):
                field parameter
            criteria (Json):
                criteria parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "dmin", None, {"database": database, "field": field, "criteria": criteria}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def dollar(self, number: Json, decimals: Json) -> WorkbookFunctionResult:
        """dollar operation.

        Args:
            number (Json):
                number parameter
            decimals (Json):
                decimals parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "dollar", None, {"number": number, "decimals": decimals}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def dollar_de(self, fractional_dollar: Json, fraction: Json) -> WorkbookFunctionResult:
        """dollarDe operation.

        Args:
            fractional_dollar (Json):
                fractionalDollar parameter
            fraction (Json):
                fraction parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "dollarDe", None, {"fractionalDollar": fractional_dollar, "fraction": fraction}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def dollar_fr(self, decimal_dollar: Json, fraction: Json) -> WorkbookFunctionResult:
        """dollarFr operation.

        Args:
            decimal_dollar (Json):
                decimalDollar parameter
            fraction (Json):
                fraction parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "dollarFr", None, {"decimalDollar": decimal_dollar, "fraction": fraction}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def dproduct(self, database: Json, field: Json, criteria: Json) -> WorkbookFunctionResult:
        """dproduct operation.

        Args:
            database (Json):
                database parameter
            field (Json):
                field parameter
            criteria (Json):
                criteria parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "dproduct", None, {"database": database, "field": field, "criteria": criteria}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def dst_dev(self, database: Json, field: Json, criteria: Json) -> WorkbookFunctionResult:
        """dstDev operation.

        Args:
            database (Json):
                database parameter
            field (Json):
                field parameter
            criteria (Json):
                criteria parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "dstDev", None, {"database": database, "field": field, "criteria": criteria}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def dst_dev_p(self, database: Json, field: Json, criteria: Json) -> WorkbookFunctionResult:
        """dstDevP operation.

        Args:
            database (Json):
                database parameter
            field (Json):
                field parameter
            criteria (Json):
                criteria parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "dstDevP", None, {"database": database, "field": field, "criteria": criteria}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def dsum(self, database: Json, field: Json, criteria: Json) -> WorkbookFunctionResult:
        """dsum operation.

        Args:
            database (Json):
                database parameter
            field (Json):
                field parameter
            criteria (Json):
                criteria parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "dsum", None, {"database": database, "field": field, "criteria": criteria}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def duration(
        self, settlement: Json, maturity: Json, coupon: Json, yld: Json, frequency: Json, basis: Json
    ) -> WorkbookFunctionResult:
        """duration operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            coupon (Json):
                coupon parameter
            yld (Json):
                yld parameter
            frequency (Json):
                frequency parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "duration",
            None,
            {
                "settlement": settlement,
                "maturity": maturity,
                "coupon": coupon,
                "yld": yld,
                "frequency": frequency,
                "basis": basis,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def dvar(self, database: Json, field: Json, criteria: Json) -> WorkbookFunctionResult:
        """dvar operation.

        Args:
            database (Json):
                database parameter
            field (Json):
                field parameter
            criteria (Json):
                criteria parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "dvar", None, {"database": database, "field": field, "criteria": criteria}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def dvar_p(self, database: Json, field: Json, criteria: Json) -> WorkbookFunctionResult:
        """dvarP operation.

        Args:
            database (Json):
                database parameter
            field (Json):
                field parameter
            criteria (Json):
                criteria parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "dvarP", None, {"database": database, "field": field, "criteria": criteria}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def ecma_ceiling(self, number: Json, significance: Json) -> WorkbookFunctionResult:
        """ecma_Ceiling operation.

        Args:
            number (Json):
                number parameter
            significance (Json):
                significance parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "ecma_Ceiling", None, {"number": number, "significance": significance}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def edate(self, start_date: Json, months: Json) -> WorkbookFunctionResult:
        """edate operation.

        Args:
            start_date (Json):
                startDate parameter
            months (Json):
                months parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "edate", None, {"startDate": start_date, "months": months}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def effect(self, nominal_rate: Json, npery: Json) -> WorkbookFunctionResult:
        """effect operation.

        Args:
            nominal_rate (Json):
                nominalRate parameter
            npery (Json):
                npery parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "effect", None, {"nominalRate": nominal_rate, "npery": npery}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def eo_month(self, start_date: Json, months: Json) -> WorkbookFunctionResult:
        """eoMonth operation.

        Args:
            start_date (Json):
                startDate parameter
            months (Json):
                months parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "eoMonth", None, {"startDate": start_date, "months": months}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def erf(self, lower_limit: Json, upper_limit: Json) -> WorkbookFunctionResult:
        """erf operation.

        Args:
            lower_limit (Json):
                lowerLimit parameter
            upper_limit (Json):
                upperLimit parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "erf", None, {"lowerLimit": lower_limit, "upperLimit": upper_limit}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def erf_c(self, x: Json) -> WorkbookFunctionResult:
        """erfC operation.

        Args:
            x (Json):
                x parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "erfC", None, {"x": x}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def erf_c_precise(self, x: Json) -> WorkbookFunctionResult:
        """erfC_Precise operation.

        Args:
            x (Json):
                X parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "erfC_Precise", None, {"X": x}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def erf_precise(self, x: Json) -> WorkbookFunctionResult:
        """erf_Precise operation.

        Args:
            x (Json):
                X parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "erf_Precise", None, {"X": x}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def error_type(self, error_val: Json) -> WorkbookFunctionResult:
        """error_Type operation.

        Args:
            error_val (Json):
                errorVal parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "error_Type", None, {"errorVal": error_val}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def even(self, number: Json) -> WorkbookFunctionResult:
        """even operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "even", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def exact(self, text1: Json, text2: Json) -> WorkbookFunctionResult:
        """exact operation.

        Args:
            text1 (Json):
                text1 parameter
            text2 (Json):
                text2 parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "exact", None, {"text1": text1, "text2": text2}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def exp(self, number: Json) -> WorkbookFunctionResult:
        """exp operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "exp", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def expon_dist(self, x: Json, lambda_: Json, cumulative: Json) -> WorkbookFunctionResult:
        """expon_Dist operation.

        Args:
            x (Json):
                x parameter
            lambda_ (Json):
                lambda parameter
            cumulative (Json):
                cumulative parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "expon_Dist", None, {"x": x, "lambda": lambda_, "cumulative": cumulative}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def fact(self, number: Json) -> WorkbookFunctionResult:
        """fact operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "fact", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def fact_double(self, number: Json) -> WorkbookFunctionResult:
        """factDouble operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "factDouble", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def false(self) -> WorkbookFunctionResult:
        """false operation."""
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "false", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def find(self, find_text: Json, within_text: Json, start_num: Json) -> WorkbookFunctionResult:
        """find operation.

        Args:
            find_text (Json):
                findText parameter
            within_text (Json):
                withinText parameter
            start_num (Json):
                startNum parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "find",
            None,
            {"findText": find_text, "withinText": within_text, "startNum": start_num},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def find_b(self, find_text: Json, within_text: Json, start_num: Json) -> WorkbookFunctionResult:
        """findB operation.

        Args:
            find_text (Json):
                findText parameter
            within_text (Json):
                withinText parameter
            start_num (Json):
                startNum parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "findB",
            None,
            {"findText": find_text, "withinText": within_text, "startNum": start_num},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def fisher(self, x: Json) -> WorkbookFunctionResult:
        """fisher operation.

        Args:
            x (Json):
                x parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "fisher", None, {"x": x}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def fisher_inv(self, y: Json) -> WorkbookFunctionResult:
        """fisherInv operation.

        Args:
            y (Json):
                y parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "fisherInv", None, {"y": y}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def fixed(self, number: Json, decimals: Json, no_commas: Json) -> WorkbookFunctionResult:
        """fixed operation.

        Args:
            number (Json):
                number parameter
            decimals (Json):
                decimals parameter
            no_commas (Json):
                noCommas parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "fixed", None, {"number": number, "decimals": decimals, "noCommas": no_commas}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def floor_math(self, number: Json, significance: Json, mode: Json) -> WorkbookFunctionResult:
        """floor_Math operation.

        Args:
            number (Json):
                number parameter
            significance (Json):
                significance parameter
            mode (Json):
                mode parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "floor_Math", None, {"number": number, "significance": significance, "mode": mode}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def floor_precise(self, number: Json, significance: Json) -> WorkbookFunctionResult:
        """floor_Precise operation.

        Args:
            number (Json):
                number parameter
            significance (Json):
                significance parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "floor_Precise", None, {"number": number, "significance": significance}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def fv(self, rate: Json, nper: Json, pmt: Json, pv: Json, type_: Json) -> WorkbookFunctionResult:
        """fv operation.

        Args:
            rate (Json):
                rate parameter
            nper (Json):
                nper parameter
            pmt (Json):
                pmt parameter
            pv (Json):
                pv parameter
            type_ (Json):
                type parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "fv", None, {"rate": rate, "nper": nper, "pmt": pmt, "pv": pv, "type": type_}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def fvschedule(self, principal: Json, schedule: Json) -> WorkbookFunctionResult:
        """fvschedule operation.

        Args:
            principal (Json):
                principal parameter
            schedule (Json):
                schedule parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "fvschedule", None, {"principal": principal, "schedule": schedule}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def fdist(self, x: Json, deg_freedom1: Json, deg_freedom2: Json, cumulative: Json) -> WorkbookFunctionResult:
        """f_Dist operation.

        Args:
            x (Json):
                x parameter
            deg_freedom1 (Json):
                degFreedom1 parameter
            deg_freedom2 (Json):
                degFreedom2 parameter
            cumulative (Json):
                cumulative parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "f_Dist",
            None,
            {"x": x, "degFreedom1": deg_freedom1, "degFreedom2": deg_freedom2, "cumulative": cumulative},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def fdist_rt(self, x: Json, deg_freedom1: Json, deg_freedom2: Json) -> WorkbookFunctionResult:
        """f_Dist_RT operation.

        Args:
            x (Json):
                x parameter
            deg_freedom1 (Json):
                degFreedom1 parameter
            deg_freedom2 (Json):
                degFreedom2 parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "f_Dist_RT",
            None,
            {"x": x, "degFreedom1": deg_freedom1, "degFreedom2": deg_freedom2},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def finv(self, probability: Json, deg_freedom1: Json, deg_freedom2: Json) -> WorkbookFunctionResult:
        """f_Inv operation.

        Args:
            probability (Json):
                probability parameter
            deg_freedom1 (Json):
                degFreedom1 parameter
            deg_freedom2 (Json):
                degFreedom2 parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "f_Inv",
            None,
            {"probability": probability, "degFreedom1": deg_freedom1, "degFreedom2": deg_freedom2},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def finv_rt(self, probability: Json, deg_freedom1: Json, deg_freedom2: Json) -> WorkbookFunctionResult:
        """f_Inv_RT operation.

        Args:
            probability (Json):
                probability parameter
            deg_freedom1 (Json):
                degFreedom1 parameter
            deg_freedom2 (Json):
                degFreedom2 parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "f_Inv_RT",
            None,
            {"probability": probability, "degFreedom1": deg_freedom1, "degFreedom2": deg_freedom2},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def gamma(self, x: Json) -> WorkbookFunctionResult:
        """gamma operation.

        Args:
            x (Json):
                x parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "gamma", None, {"x": x}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def gamma_ln(self, x: Json) -> WorkbookFunctionResult:
        """gammaLn operation.

        Args:
            x (Json):
                x parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "gammaLn", None, {"x": x}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def gamma_ln_precise(self, x: Json) -> WorkbookFunctionResult:
        """gammaLn_Precise operation.

        Args:
            x (Json):
                x parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "gammaLn_Precise", None, {"x": x}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def gamma_dist(self, x: Json, alpha: Json, beta: Json, cumulative: Json) -> WorkbookFunctionResult:
        """gamma_Dist operation.

        Args:
            x (Json):
                x parameter
            alpha (Json):
                alpha parameter
            beta (Json):
                beta parameter
            cumulative (Json):
                cumulative parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "gamma_Dist", None, {"x": x, "alpha": alpha, "beta": beta, "cumulative": cumulative}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def gamma_inv(self, probability: Json, alpha: Json, beta: Json) -> WorkbookFunctionResult:
        """gamma_Inv operation.

        Args:
            probability (Json):
                probability parameter
            alpha (Json):
                alpha parameter
            beta (Json):
                beta parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "gamma_Inv", None, {"probability": probability, "alpha": alpha, "beta": beta}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def gauss(self, x: Json) -> WorkbookFunctionResult:
        """gauss operation.

        Args:
            x (Json):
                x parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "gauss", None, {"x": x}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def gcd(self, values: Json) -> WorkbookFunctionResult:
        """gcd operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "gcd", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def geo_mean(self, values: Json) -> WorkbookFunctionResult:
        """geoMean operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "geoMean", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def ge_step(self, number: Json, step: Json) -> WorkbookFunctionResult:
        """geStep operation.

        Args:
            number (Json):
                number parameter
            step (Json):
                step parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "geStep", None, {"number": number, "step": step}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def har_mean(self, values: Json) -> WorkbookFunctionResult:
        """harMean operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "harMean", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def hex2_bin(self, number: Json, places: Json) -> WorkbookFunctionResult:
        """hex2Bin operation.

        Args:
            number (Json):
                number parameter
            places (Json):
                places parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "hex2Bin", None, {"number": number, "places": places}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def hex2_dec(self, number: Json) -> WorkbookFunctionResult:
        """hex2Dec operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "hex2Dec", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def hex2_oct(self, number: Json, places: Json) -> WorkbookFunctionResult:
        """hex2Oct operation.

        Args:
            number (Json):
                number parameter
            places (Json):
                places parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "hex2Oct", None, {"number": number, "places": places}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def hlookup(
        self, lookup_value: Json, table_array: Json, row_index_num: Json, range_lookup: Json
    ) -> WorkbookFunctionResult:
        """hlookup operation.

        Args:
            lookup_value (Json):
                lookupValue parameter
            table_array (Json):
                tableArray parameter
            row_index_num (Json):
                rowIndexNum parameter
            range_lookup (Json):
                rangeLookup parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "hlookup",
            None,
            {
                "lookupValue": lookup_value,
                "tableArray": table_array,
                "rowIndexNum": row_index_num,
                "rangeLookup": range_lookup,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def hour(self, serial_number: Json) -> WorkbookFunctionResult:
        """hour operation.

        Args:
            serial_number (Json):
                serialNumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "hour", None, {"serialNumber": serial_number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def hyperlink(self, link_location: Json, friendly_name: Json) -> WorkbookFunctionResult:
        """hyperlink operation.

        Args:
            link_location (Json):
                linkLocation parameter
            friendly_name (Json):
                friendlyName parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "hyperlink", None, {"linkLocation": link_location, "friendlyName": friendly_name}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def hyp_geom_dist(
        self, sample_s: Json, number_sample: Json, population_s: Json, number_pop: Json, cumulative: Json
    ) -> WorkbookFunctionResult:
        """hypGeom_Dist operation.

        Args:
            sample_s (Json):
                sampleS parameter
            number_sample (Json):
                numberSample parameter
            population_s (Json):
                populationS parameter
            number_pop (Json):
                numberPop parameter
            cumulative (Json):
                cumulative parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "hypGeom_Dist",
            None,
            {
                "sampleS": sample_s,
                "numberSample": number_sample,
                "populationS": population_s,
                "numberPop": number_pop,
                "cumulative": cumulative,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def if_(self, logical_test: Json, value_if_true: Json, value_if_false: Json) -> WorkbookFunctionResult:
        """if operation.

        Args:
            logical_test (Json):
                logicalTest parameter
            value_if_true (Json):
                valueIfTrue parameter
            value_if_false (Json):
                valueIfFalse parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "if",
            None,
            {"logicalTest": logical_test, "valueIfTrue": value_if_true, "valueIfFalse": value_if_false},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def im_abs(self, inumber: Json) -> WorkbookFunctionResult:
        """imAbs operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imAbs", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def imaginary(self, inumber: Json) -> WorkbookFunctionResult:
        """imaginary operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imaginary", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_argument(self, inumber: Json) -> WorkbookFunctionResult:
        """imArgument operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imArgument", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_conjugate(self, inumber: Json) -> WorkbookFunctionResult:
        """imConjugate operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imConjugate", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_cos(self, inumber: Json) -> WorkbookFunctionResult:
        """imCos operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imCos", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_cosh(self, inumber: Json) -> WorkbookFunctionResult:
        """imCosh operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imCosh", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_cot(self, inumber: Json) -> WorkbookFunctionResult:
        """imCot operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imCot", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_csc(self, inumber: Json) -> WorkbookFunctionResult:
        """imCsc operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imCsc", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_csch(self, inumber: Json) -> WorkbookFunctionResult:
        """imCsch operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imCsch", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_div(self, inumber1: Json, inumber2: Json) -> WorkbookFunctionResult:
        """imDiv operation.

        Args:
            inumber1 (Json):
                inumber1 parameter
            inumber2 (Json):
                inumber2 parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imDiv", None, {"inumber1": inumber1, "inumber2": inumber2}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_exp(self, inumber: Json) -> WorkbookFunctionResult:
        """imExp operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imExp", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_ln(self, inumber: Json) -> WorkbookFunctionResult:
        """imLn operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imLn", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_log10(self, inumber: Json) -> WorkbookFunctionResult:
        """imLog10 operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imLog10", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_log2(self, inumber: Json) -> WorkbookFunctionResult:
        """imLog2 operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imLog2", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_power(self, inumber: Json, number: Json) -> WorkbookFunctionResult:
        """imPower operation.

        Args:
            inumber (Json):
                inumber parameter
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imPower", None, {"inumber": inumber, "number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_product(self, values: Json) -> WorkbookFunctionResult:
        """imProduct operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imProduct", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_real(self, inumber: Json) -> WorkbookFunctionResult:
        """imReal operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imReal", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_sec(self, inumber: Json) -> WorkbookFunctionResult:
        """imSec operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imSec", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_sech(self, inumber: Json) -> WorkbookFunctionResult:
        """imSech operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imSech", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_sin(self, inumber: Json) -> WorkbookFunctionResult:
        """imSin operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imSin", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_sinh(self, inumber: Json) -> WorkbookFunctionResult:
        """imSinh operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imSinh", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_sqrt(self, inumber: Json) -> WorkbookFunctionResult:
        """imSqrt operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imSqrt", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_sub(self, inumber1: Json, inumber2: Json) -> WorkbookFunctionResult:
        """imSub operation.

        Args:
            inumber1 (Json):
                inumber1 parameter
            inumber2 (Json):
                inumber2 parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imSub", None, {"inumber1": inumber1, "inumber2": inumber2}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_sum(self, values: Json) -> WorkbookFunctionResult:
        """imSum operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imSum", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def im_tan(self, inumber: Json) -> WorkbookFunctionResult:
        """imTan operation.

        Args:
            inumber (Json):
                inumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "imTan", None, {"inumber": inumber}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def int(self, number: Json) -> WorkbookFunctionResult:
        """int operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "int", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def int_rate(
        self, settlement: Json, maturity: Json, investment: Json, redemption: Json, basis: Json
    ) -> WorkbookFunctionResult:
        """intRate operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            investment (Json):
                investment parameter
            redemption (Json):
                redemption parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "intRate",
            None,
            {
                "settlement": settlement,
                "maturity": maturity,
                "investment": investment,
                "redemption": redemption,
                "basis": basis,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def ipmt(self, rate: Json, per: Json, nper: Json, pv: Json, fv: Json, type_: Json) -> WorkbookFunctionResult:
        """ipmt operation.

        Args:
            rate (Json):
                rate parameter
            per (Json):
                per parameter
            nper (Json):
                nper parameter
            pv (Json):
                pv parameter
            fv (Json):
                fv parameter
            type_ (Json):
                type parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "ipmt",
            None,
            {"rate": rate, "per": per, "nper": nper, "pv": pv, "fv": fv, "type": type_},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def irr(self, values: Json, guess: Json) -> WorkbookFunctionResult:
        """irr operation.

        Args:
            values (Json):
                values parameter
            guess (Json):
                guess parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "irr", None, {"values": values, "guess": guess}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def is_err(self, value: Json) -> WorkbookFunctionResult:
        """isErr operation.

        Args:
            value (Json):
                value parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "isErr", None, {"value": value}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def is_error(self, value: Json) -> WorkbookFunctionResult:
        """isError operation.

        Args:
            value (Json):
                value parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "isError", None, {"value": value}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def is_even(self, number: Json) -> WorkbookFunctionResult:
        """isEven operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "isEven", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def is_formula(self, reference: Json) -> WorkbookFunctionResult:
        """isFormula operation.

        Args:
            reference (Json):
                reference parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "isFormula", None, {"reference": reference}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def is_logical(self, value: Json) -> WorkbookFunctionResult:
        """isLogical operation.

        Args:
            value (Json):
                value parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "isLogical", None, {"value": value}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def is_na(self, value: Json) -> WorkbookFunctionResult:
        """isNA operation.

        Args:
            value (Json):
                value parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "isNA", None, {"value": value}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def is_non_text(self, value: Json) -> WorkbookFunctionResult:
        """isNonText operation.

        Args:
            value (Json):
                value parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "isNonText", None, {"value": value}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def is_number(self, value: Json) -> WorkbookFunctionResult:
        """isNumber operation.

        Args:
            value (Json):
                value parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "isNumber", None, {"value": value}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def is_odd(self, number: Json) -> WorkbookFunctionResult:
        """isOdd operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "isOdd", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def iso_week_num(self, date: Json) -> WorkbookFunctionResult:
        """isoWeekNum operation.

        Args:
            date (Json):
                date parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "isoWeekNum", None, {"date": date}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def iso_ceiling(self, number: Json, significance: Json) -> WorkbookFunctionResult:
        """iso_Ceiling operation.

        Args:
            number (Json):
                number parameter
            significance (Json):
                significance parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "iso_Ceiling", None, {"number": number, "significance": significance}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def ispmt(self, rate: Json, per: Json, nper: Json, pv: Json) -> WorkbookFunctionResult:
        """ispmt operation.

        Args:
            rate (Json):
                rate parameter
            per (Json):
                per parameter
            nper (Json):
                nper parameter
            pv (Json):
                pv parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "ispmt", None, {"rate": rate, "per": per, "nper": nper, "pv": pv}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def isref(self, value: Json) -> WorkbookFunctionResult:
        """isref operation.

        Args:
            value (Json):
                value parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "isref", None, {"value": value}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def is_text(self, value: Json) -> WorkbookFunctionResult:
        """isText operation.

        Args:
            value (Json):
                value parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "isText", None, {"value": value}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def kurt(self, values: Json) -> WorkbookFunctionResult:
        """kurt operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "kurt", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def large(self, array: Json, k: Json) -> WorkbookFunctionResult:
        """large operation.

        Args:
            array (Json):
                array parameter
            k (Json):
                k parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "large", None, {"array": array, "k": k}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def lcm(self, values: Json) -> WorkbookFunctionResult:
        """lcm operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "lcm", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def left(self, text: Json, num_chars: Json) -> WorkbookFunctionResult:
        """left operation.

        Args:
            text (Json):
                text parameter
            num_chars (Json):
                numChars parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "left", None, {"text": text, "numChars": num_chars}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def leftb(self, text: Json, num_bytes: Json) -> WorkbookFunctionResult:
        """leftb operation.

        Args:
            text (Json):
                text parameter
            num_bytes (Json):
                numBytes parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "leftb", None, {"text": text, "numBytes": num_bytes}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def len(self, text: Json) -> WorkbookFunctionResult:
        """len operation.

        Args:
            text (Json):
                text parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "len", None, {"text": text}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def lenb(self, text: Json) -> WorkbookFunctionResult:
        """lenb operation.

        Args:
            text (Json):
                text parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "lenb", None, {"text": text}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def ln(self, number: Json) -> WorkbookFunctionResult:
        """ln operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "ln", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def log(self, number: Json, base: Json) -> WorkbookFunctionResult:
        """log operation.

        Args:
            number (Json):
                number parameter
            base (Json):
                base parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "log", None, {"number": number, "base": base}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def log10(self, number: Json) -> WorkbookFunctionResult:
        """log10 operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "log10", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def log_norm_dist(self, x: Json, mean: Json, standard_dev: Json, cumulative: Json) -> WorkbookFunctionResult:
        """logNorm_Dist operation.

        Args:
            x (Json):
                x parameter
            mean (Json):
                mean parameter
            standard_dev (Json):
                standardDev parameter
            cumulative (Json):
                cumulative parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "logNorm_Dist",
            None,
            {"x": x, "mean": mean, "standardDev": standard_dev, "cumulative": cumulative},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def log_norm_inv(self, probability: Json, mean: Json, standard_dev: Json) -> WorkbookFunctionResult:
        """logNorm_Inv operation.

        Args:
            probability (Json):
                probability parameter
            mean (Json):
                mean parameter
            standard_dev (Json):
                standardDev parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "logNorm_Inv",
            None,
            {"probability": probability, "mean": mean, "standardDev": standard_dev},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def lookup(self, lookup_value: Json, lookup_vector: Json, result_vector: Json) -> WorkbookFunctionResult:
        """lookup operation.

        Args:
            lookup_value (Json):
                lookupValue parameter
            lookup_vector (Json):
                lookupVector parameter
            result_vector (Json):
                resultVector parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "lookup",
            None,
            {"lookupValue": lookup_value, "lookupVector": lookup_vector, "resultVector": result_vector},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def lower(self, text: Json) -> WorkbookFunctionResult:
        """lower operation.

        Args:
            text (Json):
                text parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "lower", None, {"text": text}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def match(self, lookup_value: Json, lookup_array: Json, match_type: Json) -> WorkbookFunctionResult:
        """match operation.

        Args:
            lookup_value (Json):
                lookupValue parameter
            lookup_array (Json):
                lookupArray parameter
            match_type (Json):
                matchType parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "match",
            None,
            {"lookupValue": lookup_value, "lookupArray": lookup_array, "matchType": match_type},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def max(self, values: Json) -> WorkbookFunctionResult:
        """max operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "max", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def max_a(self, values: Json) -> WorkbookFunctionResult:
        """maxA operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "maxA", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def mduration(
        self, settlement: Json, maturity: Json, coupon: Json, yld: Json, frequency: Json, basis: Json
    ) -> WorkbookFunctionResult:
        """mduration operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            coupon (Json):
                coupon parameter
            yld (Json):
                yld parameter
            frequency (Json):
                frequency parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "mduration",
            None,
            {
                "settlement": settlement,
                "maturity": maturity,
                "coupon": coupon,
                "yld": yld,
                "frequency": frequency,
                "basis": basis,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def median(self, values: Json) -> WorkbookFunctionResult:
        """median operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "median", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def mid(self, text: Json, start_num: Json, num_chars: Json) -> WorkbookFunctionResult:
        """mid operation.

        Args:
            text (Json):
                text parameter
            start_num (Json):
                startNum parameter
            num_chars (Json):
                numChars parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "mid", None, {"text": text, "startNum": start_num, "numChars": num_chars}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def midb(self, text: Json, start_num: Json, num_bytes: Json) -> WorkbookFunctionResult:
        """midb operation.

        Args:
            text (Json):
                text parameter
            start_num (Json):
                startNum parameter
            num_bytes (Json):
                numBytes parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "midb", None, {"text": text, "startNum": start_num, "numBytes": num_bytes}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def min(self, values: Json) -> WorkbookFunctionResult:
        """min operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "min", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def min_a(self, values: Json) -> WorkbookFunctionResult:
        """minA operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "minA", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def minute(self, serial_number: Json) -> WorkbookFunctionResult:
        """minute operation.

        Args:
            serial_number (Json):
                serialNumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "minute", None, {"serialNumber": serial_number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def mirr(self, values: Json, finance_rate: Json, reinvest_rate: Json) -> WorkbookFunctionResult:
        """mirr operation.

        Args:
            values (Json):
                values parameter
            finance_rate (Json):
                financeRate parameter
            reinvest_rate (Json):
                reinvestRate parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "mirr",
            None,
            {"values": values, "financeRate": finance_rate, "reinvestRate": reinvest_rate},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def mod(self, number: Json, divisor: Json) -> WorkbookFunctionResult:
        """mod operation.

        Args:
            number (Json):
                number parameter
            divisor (Json):
                divisor parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "mod", None, {"number": number, "divisor": divisor}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def month(self, serial_number: Json) -> WorkbookFunctionResult:
        """month operation.

        Args:
            serial_number (Json):
                serialNumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "month", None, {"serialNumber": serial_number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def mround(self, number: Json, multiple: Json) -> WorkbookFunctionResult:
        """mround operation.

        Args:
            number (Json):
                number parameter
            multiple (Json):
                multiple parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "mround", None, {"number": number, "multiple": multiple}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def multi_nomial(self, values: Json) -> WorkbookFunctionResult:
        """multiNomial operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "multiNomial", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def n(self, value: Json) -> WorkbookFunctionResult:
        """n operation.

        Args:
            value (Json):
                value parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "n", None, {"value": value}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def na(self) -> WorkbookFunctionResult:
        """na operation."""
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "na", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def neg_binom_dist(
        self, number_f: Json, number_s: Json, probability_s: Json, cumulative: Json
    ) -> WorkbookFunctionResult:
        """negBinom_Dist operation.

        Args:
            number_f (Json):
                numberF parameter
            number_s (Json):
                numberS parameter
            probability_s (Json):
                probabilityS parameter
            cumulative (Json):
                cumulative parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "negBinom_Dist",
            None,
            {"numberF": number_f, "numberS": number_s, "probabilityS": probability_s, "cumulative": cumulative},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def network_days(self, start_date: Json, end_date: Json, holidays: Json) -> WorkbookFunctionResult:
        """networkDays operation.

        Args:
            start_date (Json):
                startDate parameter
            end_date (Json):
                endDate parameter
            holidays (Json):
                holidays parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "networkDays",
            None,
            {"startDate": start_date, "endDate": end_date, "holidays": holidays},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def network_days_intl(
        self, start_date: Json, end_date: Json, weekend: Json, holidays: Json
    ) -> WorkbookFunctionResult:
        """networkDays_Intl operation.

        Args:
            start_date (Json):
                startDate parameter
            end_date (Json):
                endDate parameter
            weekend (Json):
                weekend parameter
            holidays (Json):
                holidays parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "networkDays_Intl",
            None,
            {"startDate": start_date, "endDate": end_date, "weekend": weekend, "holidays": holidays},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def nominal(self, effect_rate: Json, npery: Json) -> WorkbookFunctionResult:
        """nominal operation.

        Args:
            effect_rate (Json):
                effectRate parameter
            npery (Json):
                npery parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "nominal", None, {"effectRate": effect_rate, "npery": npery}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def norm_dist(self, x: Json, mean: Json, standard_dev: Json, cumulative: Json) -> WorkbookFunctionResult:
        """norm_Dist operation.

        Args:
            x (Json):
                x parameter
            mean (Json):
                mean parameter
            standard_dev (Json):
                standardDev parameter
            cumulative (Json):
                cumulative parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "norm_Dist",
            None,
            {"x": x, "mean": mean, "standardDev": standard_dev, "cumulative": cumulative},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def norm_inv(self, probability: Json, mean: Json, standard_dev: Json) -> WorkbookFunctionResult:
        """norm_Inv operation.

        Args:
            probability (Json):
                probability parameter
            mean (Json):
                mean parameter
            standard_dev (Json):
                standardDev parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "norm_Inv",
            None,
            {"probability": probability, "mean": mean, "standardDev": standard_dev},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def norm_s_dist(self, z: Json, cumulative: Json) -> WorkbookFunctionResult:
        """norm_S_Dist operation.

        Args:
            z (Json):
                z parameter
            cumulative (Json):
                cumulative parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "norm_S_Dist", None, {"z": z, "cumulative": cumulative}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def norm_s_inv(self, probability: Json) -> WorkbookFunctionResult:
        """norm_S_Inv operation.

        Args:
            probability (Json):
                probability parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "norm_S_Inv", None, {"probability": probability}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def not_(self, logical: Json) -> WorkbookFunctionResult:
        """not operation.

        Args:
            logical (Json):
                logical parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "not", None, {"logical": logical}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def now(self) -> WorkbookFunctionResult:
        """now operation."""
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "now", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def nper(self, rate: Json, pmt: Json, pv: Json, fv: Json, type_: Json) -> WorkbookFunctionResult:
        """nper operation.

        Args:
            rate (Json):
                rate parameter
            pmt (Json):
                pmt parameter
            pv (Json):
                pv parameter
            fv (Json):
                fv parameter
            type_ (Json):
                type parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "nper", None, {"rate": rate, "pmt": pmt, "pv": pv, "fv": fv, "type": type_}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def npv(self, rate: Json, values: Json) -> WorkbookFunctionResult:
        """npv operation.

        Args:
            rate (Json):
                rate parameter
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "npv", None, {"rate": rate, "values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def number_value(self, text: Json, decimal_separator: Json, group_separator: Json) -> WorkbookFunctionResult:
        """numberValue operation.

        Args:
            text (Json):
                text parameter
            decimal_separator (Json):
                decimalSeparator parameter
            group_separator (Json):
                groupSeparator parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "numberValue",
            None,
            {"text": text, "decimalSeparator": decimal_separator, "groupSeparator": group_separator},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def oct2_bin(self, number: Json, places: Json) -> WorkbookFunctionResult:
        """oct2Bin operation.

        Args:
            number (Json):
                number parameter
            places (Json):
                places parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "oct2Bin", None, {"number": number, "places": places}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def oct2_dec(self, number: Json) -> WorkbookFunctionResult:
        """oct2Dec operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "oct2Dec", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def oct2_hex(self, number: Json, places: Json) -> WorkbookFunctionResult:
        """oct2Hex operation.

        Args:
            number (Json):
                number parameter
            places (Json):
                places parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "oct2Hex", None, {"number": number, "places": places}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def odd(self, number: Json) -> WorkbookFunctionResult:
        """odd operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "odd", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def odd_f_price(
        self,
        settlement: Json,
        maturity: Json,
        issue: Json,
        first_coupon: Json,
        rate: Json,
        yld: Json,
        redemption: Json,
        frequency: Json,
        basis: Json,
    ) -> WorkbookFunctionResult:
        """oddFPrice operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            issue (Json):
                issue parameter
            first_coupon (Json):
                firstCoupon parameter
            rate (Json):
                rate parameter
            yld (Json):
                yld parameter
            redemption (Json):
                redemption parameter
            frequency (Json):
                frequency parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "oddFPrice",
            None,
            {
                "settlement": settlement,
                "maturity": maturity,
                "issue": issue,
                "firstCoupon": first_coupon,
                "rate": rate,
                "yld": yld,
                "redemption": redemption,
                "frequency": frequency,
                "basis": basis,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def odd_f_yield(
        self,
        settlement: Json,
        maturity: Json,
        issue: Json,
        first_coupon: Json,
        rate: Json,
        pr: Json,
        redemption: Json,
        frequency: Json,
        basis: Json,
    ) -> WorkbookFunctionResult:
        """oddFYield operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            issue (Json):
                issue parameter
            first_coupon (Json):
                firstCoupon parameter
            rate (Json):
                rate parameter
            pr (Json):
                pr parameter
            redemption (Json):
                redemption parameter
            frequency (Json):
                frequency parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "oddFYield",
            None,
            {
                "settlement": settlement,
                "maturity": maturity,
                "issue": issue,
                "firstCoupon": first_coupon,
                "rate": rate,
                "pr": pr,
                "redemption": redemption,
                "frequency": frequency,
                "basis": basis,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def odd_l_price(
        self,
        settlement: Json,
        maturity: Json,
        last_interest: Json,
        rate: Json,
        yld: Json,
        redemption: Json,
        frequency: Json,
        basis: Json,
    ) -> WorkbookFunctionResult:
        """oddLPrice operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            last_interest (Json):
                lastInterest parameter
            rate (Json):
                rate parameter
            yld (Json):
                yld parameter
            redemption (Json):
                redemption parameter
            frequency (Json):
                frequency parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "oddLPrice",
            None,
            {
                "settlement": settlement,
                "maturity": maturity,
                "lastInterest": last_interest,
                "rate": rate,
                "yld": yld,
                "redemption": redemption,
                "frequency": frequency,
                "basis": basis,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def odd_l_yield(
        self,
        settlement: Json,
        maturity: Json,
        last_interest: Json,
        rate: Json,
        pr: Json,
        redemption: Json,
        frequency: Json,
        basis: Json,
    ) -> WorkbookFunctionResult:
        """oddLYield operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            last_interest (Json):
                lastInterest parameter
            rate (Json):
                rate parameter
            pr (Json):
                pr parameter
            redemption (Json):
                redemption parameter
            frequency (Json):
                frequency parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "oddLYield",
            None,
            {
                "settlement": settlement,
                "maturity": maturity,
                "lastInterest": last_interest,
                "rate": rate,
                "pr": pr,
                "redemption": redemption,
                "frequency": frequency,
                "basis": basis,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def or_(self, values: Json) -> WorkbookFunctionResult:
        """or operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "or", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def pduration(self, rate: Json, pv: Json, fv: Json) -> WorkbookFunctionResult:
        """pduration operation.

        Args:
            rate (Json):
                rate parameter
            pv (Json):
                pv parameter
            fv (Json):
                fv parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "pduration", None, {"rate": rate, "pv": pv, "fv": fv}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def percentile_exc(self, array: Json, k: Json) -> WorkbookFunctionResult:
        """percentile_Exc operation.

        Args:
            array (Json):
                array parameter
            k (Json):
                k parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "percentile_Exc", None, {"array": array, "k": k}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def percentile_inc(self, array: Json, k: Json) -> WorkbookFunctionResult:
        """percentile_Inc operation.

        Args:
            array (Json):
                array parameter
            k (Json):
                k parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "percentile_Inc", None, {"array": array, "k": k}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def percent_rank_exc(self, array: Json, x: Json, significance: Json) -> WorkbookFunctionResult:
        """percentRank_Exc operation.

        Args:
            array (Json):
                array parameter
            x (Json):
                x parameter
            significance (Json):
                significance parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "percentRank_Exc", None, {"array": array, "x": x, "significance": significance}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def percent_rank_inc(self, array: Json, x: Json, significance: Json) -> WorkbookFunctionResult:
        """percentRank_Inc operation.

        Args:
            array (Json):
                array parameter
            x (Json):
                x parameter
            significance (Json):
                significance parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "percentRank_Inc", None, {"array": array, "x": x, "significance": significance}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def permut(self, number: Json, number_chosen: Json) -> WorkbookFunctionResult:
        """permut operation.

        Args:
            number (Json):
                number parameter
            number_chosen (Json):
                numberChosen parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "permut", None, {"number": number, "numberChosen": number_chosen}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def permutationa(self, number: Json, number_chosen: Json) -> WorkbookFunctionResult:
        """permutationa operation.

        Args:
            number (Json):
                number parameter
            number_chosen (Json):
                numberChosen parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "permutationa", None, {"number": number, "numberChosen": number_chosen}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def phi(self, x: Json) -> WorkbookFunctionResult:
        """phi operation.

        Args:
            x (Json):
                x parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "phi", None, {"x": x}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def pi(self) -> WorkbookFunctionResult:
        """pi operation."""
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "pi", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def pmt(self, rate: Json, nper: Json, pv: Json, fv: Json, type_: Json) -> WorkbookFunctionResult:
        """pmt operation.

        Args:
            rate (Json):
                rate parameter
            nper (Json):
                nper parameter
            pv (Json):
                pv parameter
            fv (Json):
                fv parameter
            type_ (Json):
                type parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "pmt", None, {"rate": rate, "nper": nper, "pv": pv, "fv": fv, "type": type_}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def poisson_dist(self, x: Json, mean: Json, cumulative: Json) -> WorkbookFunctionResult:
        """poisson_Dist operation.

        Args:
            x (Json):
                x parameter
            mean (Json):
                mean parameter
            cumulative (Json):
                cumulative parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "poisson_Dist", None, {"x": x, "mean": mean, "cumulative": cumulative}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def ppmt(self, rate: Json, per: Json, nper: Json, pv: Json, fv: Json, type_: Json) -> WorkbookFunctionResult:
        """ppmt operation.

        Args:
            rate (Json):
                rate parameter
            per (Json):
                per parameter
            nper (Json):
                nper parameter
            pv (Json):
                pv parameter
            fv (Json):
                fv parameter
            type_ (Json):
                type parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "ppmt",
            None,
            {"rate": rate, "per": per, "nper": nper, "pv": pv, "fv": fv, "type": type_},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def price(
        self, settlement: Json, maturity: Json, rate: Json, yld: Json, redemption: Json, frequency: Json, basis: Json
    ) -> WorkbookFunctionResult:
        """price operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            rate (Json):
                rate parameter
            yld (Json):
                yld parameter
            redemption (Json):
                redemption parameter
            frequency (Json):
                frequency parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "price",
            None,
            {
                "settlement": settlement,
                "maturity": maturity,
                "rate": rate,
                "yld": yld,
                "redemption": redemption,
                "frequency": frequency,
                "basis": basis,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def price_disc(
        self, settlement: Json, maturity: Json, discount: Json, redemption: Json, basis: Json
    ) -> WorkbookFunctionResult:
        """priceDisc operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            discount (Json):
                discount parameter
            redemption (Json):
                redemption parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "priceDisc",
            None,
            {
                "settlement": settlement,
                "maturity": maturity,
                "discount": discount,
                "redemption": redemption,
                "basis": basis,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def price_mat(
        self, settlement: Json, maturity: Json, issue: Json, rate: Json, yld: Json, basis: Json
    ) -> WorkbookFunctionResult:
        """priceMat operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            issue (Json):
                issue parameter
            rate (Json):
                rate parameter
            yld (Json):
                yld parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "priceMat",
            None,
            {"settlement": settlement, "maturity": maturity, "issue": issue, "rate": rate, "yld": yld, "basis": basis},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def product(self, values: Json) -> WorkbookFunctionResult:
        """product operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "product", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def proper(self, text: Json) -> WorkbookFunctionResult:
        """proper operation.

        Args:
            text (Json):
                text parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "proper", None, {"text": text}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def pv(self, rate: Json, nper: Json, pmt: Json, fv: Json, type_: Json) -> WorkbookFunctionResult:
        """pv operation.

        Args:
            rate (Json):
                rate parameter
            nper (Json):
                nper parameter
            pmt (Json):
                pmt parameter
            fv (Json):
                fv parameter
            type_ (Json):
                type parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "pv", None, {"rate": rate, "nper": nper, "pmt": pmt, "fv": fv, "type": type_}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def quartile_exc(self, array: Json, quart: Json) -> WorkbookFunctionResult:
        """quartile_Exc operation.

        Args:
            array (Json):
                array parameter
            quart (Json):
                quart parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "quartile_Exc", None, {"array": array, "quart": quart}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def quartile_inc(self, array: Json, quart: Json) -> WorkbookFunctionResult:
        """quartile_Inc operation.

        Args:
            array (Json):
                array parameter
            quart (Json):
                quart parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "quartile_Inc", None, {"array": array, "quart": quart}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def quotient(self, numerator: Json, denominator: Json) -> WorkbookFunctionResult:
        """quotient operation.

        Args:
            numerator (Json):
                numerator parameter
            denominator (Json):
                denominator parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "quotient", None, {"numerator": numerator, "denominator": denominator}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def radians(self, angle: Json) -> WorkbookFunctionResult:
        """radians operation.

        Args:
            angle (Json):
                angle parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "radians", None, {"angle": angle}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def rand(self) -> WorkbookFunctionResult:
        """rand operation."""
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "rand", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def rand_between(self, bottom: Json, top: Json) -> WorkbookFunctionResult:
        """randBetween operation.

        Args:
            bottom (Json):
                bottom parameter
            top (Json):
                top parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "randBetween", None, {"bottom": bottom, "top": top}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def rank_avg(self, number: Json, ref: Json, order: Json) -> WorkbookFunctionResult:
        """rank_Avg operation.

        Args:
            number (Json):
                number parameter
            ref (Json):
                ref parameter
            order (Json):
                order parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "rank_Avg", None, {"number": number, "ref": ref, "order": order}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def rank_eq(self, number: Json, ref: Json, order: Json) -> WorkbookFunctionResult:
        """rank_Eq operation.

        Args:
            number (Json):
                number parameter
            ref (Json):
                ref parameter
            order (Json):
                order parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "rank_Eq", None, {"number": number, "ref": ref, "order": order}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def rate(self, nper: Json, pmt: Json, pv: Json, fv: Json, type_: Json, guess: Json) -> WorkbookFunctionResult:
        """rate operation.

        Args:
            nper (Json):
                nper parameter
            pmt (Json):
                pmt parameter
            pv (Json):
                pv parameter
            fv (Json):
                fv parameter
            type_ (Json):
                type parameter
            guess (Json):
                guess parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "rate",
            None,
            {"nper": nper, "pmt": pmt, "pv": pv, "fv": fv, "type": type_, "guess": guess},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def received(
        self, settlement: Json, maturity: Json, investment: Json, discount: Json, basis: Json
    ) -> WorkbookFunctionResult:
        """received operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            investment (Json):
                investment parameter
            discount (Json):
                discount parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "received",
            None,
            {
                "settlement": settlement,
                "maturity": maturity,
                "investment": investment,
                "discount": discount,
                "basis": basis,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def replace(self, old_text: Json, start_num: Json, num_chars: Json, new_text: Json) -> WorkbookFunctionResult:
        """replace operation.

        Args:
            old_text (Json):
                oldText parameter
            start_num (Json):
                startNum parameter
            num_chars (Json):
                numChars parameter
            new_text (Json):
                newText parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "replace",
            None,
            {"oldText": old_text, "startNum": start_num, "numChars": num_chars, "newText": new_text},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def replace_b(self, old_text: Json, start_num: Json, num_bytes: Json, new_text: Json) -> WorkbookFunctionResult:
        """replaceB operation.

        Args:
            old_text (Json):
                oldText parameter
            start_num (Json):
                startNum parameter
            num_bytes (Json):
                numBytes parameter
            new_text (Json):
                newText parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "replaceB",
            None,
            {"oldText": old_text, "startNum": start_num, "numBytes": num_bytes, "newText": new_text},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def rept(self, text: Json, number_times: Json) -> WorkbookFunctionResult:
        """rept operation.

        Args:
            text (Json):
                text parameter
            number_times (Json):
                numberTimes parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "rept", None, {"text": text, "numberTimes": number_times}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def right(self, text: Json, num_chars: Json) -> WorkbookFunctionResult:
        """right operation.

        Args:
            text (Json):
                text parameter
            num_chars (Json):
                numChars parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "right", None, {"text": text, "numChars": num_chars}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def rightb(self, text: Json, num_bytes: Json) -> WorkbookFunctionResult:
        """rightb operation.

        Args:
            text (Json):
                text parameter
            num_bytes (Json):
                numBytes parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "rightb", None, {"text": text, "numBytes": num_bytes}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def roman(self, number: Json, form: Json) -> WorkbookFunctionResult:
        """roman operation.

        Args:
            number (Json):
                number parameter
            form (Json):
                form parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "roman", None, {"number": number, "form": form}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def round(self, number: Json, num_digits: Json) -> WorkbookFunctionResult:
        """round operation.

        Args:
            number (Json):
                number parameter
            num_digits (Json):
                numDigits parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "round", None, {"number": number, "numDigits": num_digits}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def round_down(self, number: Json, num_digits: Json) -> WorkbookFunctionResult:
        """roundDown operation.

        Args:
            number (Json):
                number parameter
            num_digits (Json):
                numDigits parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "roundDown", None, {"number": number, "numDigits": num_digits}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def round_up(self, number: Json, num_digits: Json) -> WorkbookFunctionResult:
        """roundUp operation.

        Args:
            number (Json):
                number parameter
            num_digits (Json):
                numDigits parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "roundUp", None, {"number": number, "numDigits": num_digits}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def rows(self, array: Json) -> WorkbookFunctionResult:
        """rows operation.

        Args:
            array (Json):
                array parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "rows", None, {"array": array}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def rri(self, nper: Json, pv: Json, fv: Json) -> WorkbookFunctionResult:
        """rri operation.

        Args:
            nper (Json):
                nper parameter
            pv (Json):
                pv parameter
            fv (Json):
                fv parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "rri", None, {"nper": nper, "pv": pv, "fv": fv}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def sec(self, number: Json) -> WorkbookFunctionResult:
        """sec operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "sec", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def sech(self, number: Json) -> WorkbookFunctionResult:
        """sech operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "sech", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def second(self, serial_number: Json) -> WorkbookFunctionResult:
        """second operation.

        Args:
            serial_number (Json):
                serialNumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "second", None, {"serialNumber": serial_number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def series_sum(self, x: Json, n: Json, m: Json, coefficients: Json) -> WorkbookFunctionResult:
        """seriesSum operation.

        Args:
            x (Json):
                x parameter
            n (Json):
                n parameter
            m (Json):
                m parameter
            coefficients (Json):
                coefficients parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "seriesSum", None, {"x": x, "n": n, "m": m, "coefficients": coefficients}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def sheet(self, value: Json) -> WorkbookFunctionResult:
        """sheet operation.

        Args:
            value (Json):
                value parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "sheet", None, {"value": value}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def sheets(self, reference: Json) -> WorkbookFunctionResult:
        """sheets operation.

        Args:
            reference (Json):
                reference parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "sheets", None, {"reference": reference}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def sign(self, number: Json) -> WorkbookFunctionResult:
        """sign operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "sign", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def sin(self, number: Json) -> WorkbookFunctionResult:
        """sin operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "sin", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def sinh(self, number: Json) -> WorkbookFunctionResult:
        """sinh operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "sinh", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def skew(self, values: Json) -> WorkbookFunctionResult:
        """skew operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "skew", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def skew_p(self, values: Json) -> WorkbookFunctionResult:
        """skew_p operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "skew_p", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def sln(self, cost: Json, salvage: Json, life: Json) -> WorkbookFunctionResult:
        """sln operation.

        Args:
            cost (Json):
                cost parameter
            salvage (Json):
                salvage parameter
            life (Json):
                life parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "sln", None, {"cost": cost, "salvage": salvage, "life": life}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def small(self, array: Json, k: Json) -> WorkbookFunctionResult:
        """small operation.

        Args:
            array (Json):
                array parameter
            k (Json):
                k parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "small", None, {"array": array, "k": k}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def sqrt(self, number: Json) -> WorkbookFunctionResult:
        """sqrt operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "sqrt", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def sqrt_pi(self, number: Json) -> WorkbookFunctionResult:
        """sqrtPi operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "sqrtPi", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def standardize(self, x: Json, mean: Json, standard_dev: Json) -> WorkbookFunctionResult:
        """standardize operation.

        Args:
            x (Json):
                x parameter
            mean (Json):
                mean parameter
            standard_dev (Json):
                standardDev parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "standardize", None, {"x": x, "mean": mean, "standardDev": standard_dev}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def st_dev_a(self, values: Json) -> WorkbookFunctionResult:
        """stDevA operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "stDevA", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def st_dev_pa(self, values: Json) -> WorkbookFunctionResult:
        """stDevPA operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "stDevPA", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def st_dev_p(self, values: Json) -> WorkbookFunctionResult:
        """stDev_P operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "stDev_P", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def st_dev_s(self, values: Json) -> WorkbookFunctionResult:
        """stDev_S operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "stDev_S", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def substitute(self, text: Json, old_text: Json, new_text: Json, instance_num: Json) -> WorkbookFunctionResult:
        """substitute operation.

        Args:
            text (Json):
                text parameter
            old_text (Json):
                oldText parameter
            new_text (Json):
                newText parameter
            instance_num (Json):
                instanceNum parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "substitute",
            None,
            {"text": text, "oldText": old_text, "newText": new_text, "instanceNum": instance_num},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def subtotal(self, function_num: Json, values: Json) -> WorkbookFunctionResult:
        """subtotal operation.

        Args:
            function_num (Json):
                functionNum parameter
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "subtotal", None, {"functionNum": function_num, "values": values}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def sum(self, values: Json) -> WorkbookFunctionResult:
        """sum operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "sum", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def sum_if(self, range_: Json, criteria: Json, sum_range: Json) -> WorkbookFunctionResult:
        """sumIf operation.

        Args:
            range_ (Json):
                range parameter
            criteria (Json):
                criteria parameter
            sum_range (Json):
                sumRange parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "sumIf", None, {"range": range_, "criteria": criteria, "sumRange": sum_range}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def sum_ifs(self, sum_range: Json, values: Json) -> WorkbookFunctionResult:
        """sumIfs operation.

        Args:
            sum_range (Json):
                sumRange parameter
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "sumIfs", None, {"sumRange": sum_range, "values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def sum_sq(self, values: Json) -> WorkbookFunctionResult:
        """sumSq operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "sumSq", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def syd(self, cost: Json, salvage: Json, life: Json, per: Json) -> WorkbookFunctionResult:
        """syd operation.

        Args:
            cost (Json):
                cost parameter
            salvage (Json):
                salvage parameter
            life (Json):
                life parameter
            per (Json):
                per parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "syd", None, {"cost": cost, "salvage": salvage, "life": life, "per": per}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def t(self, value: Json) -> WorkbookFunctionResult:
        """t operation.

        Args:
            value (Json):
                value parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "t", None, {"value": value}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def tan(self, number: Json) -> WorkbookFunctionResult:
        """tan operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "tan", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def tanh(self, number: Json) -> WorkbookFunctionResult:
        """tanh operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "tanh", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def tbill_eq(self, settlement: Json, maturity: Json, discount: Json) -> WorkbookFunctionResult:
        """tbillEq operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            discount (Json):
                discount parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "tbillEq",
            None,
            {"settlement": settlement, "maturity": maturity, "discount": discount},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def tbill_price(self, settlement: Json, maturity: Json, discount: Json) -> WorkbookFunctionResult:
        """tbillPrice operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            discount (Json):
                discount parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "tbillPrice",
            None,
            {"settlement": settlement, "maturity": maturity, "discount": discount},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def tbill_yield(self, settlement: Json, maturity: Json, pr: Json) -> WorkbookFunctionResult:
        """tbillYield operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            pr (Json):
                pr parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "tbillYield", None, {"settlement": settlement, "maturity": maturity, "pr": pr}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def text(self, value: Json, format_text: Json) -> WorkbookFunctionResult:
        """text operation.

        Args:
            value (Json):
                value parameter
            format_text (Json):
                formatText parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "text", None, {"value": value, "formatText": format_text}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def time(self, hour: Json, minute: Json, second: Json) -> WorkbookFunctionResult:
        """time operation.

        Args:
            hour (Json):
                hour parameter
            minute (Json):
                minute parameter
            second (Json):
                second parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "time", None, {"hour": hour, "minute": minute, "second": second}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def timevalue(self, time_text: Json) -> WorkbookFunctionResult:
        """timevalue operation.

        Args:
            time_text (Json):
                timeText parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "timevalue", None, {"timeText": time_text}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def today(self) -> WorkbookFunctionResult:
        """today operation."""
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "today", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def trim(self, text: Json) -> WorkbookFunctionResult:
        """trim operation.

        Args:
            text (Json):
                text parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "trim", None, {"text": text}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def trim_mean(self, array: Json, percent: Json) -> WorkbookFunctionResult:
        """trimMean operation.

        Args:
            array (Json):
                array parameter
            percent (Json):
                percent parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "trimMean", None, {"array": array, "percent": percent}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def true(self) -> WorkbookFunctionResult:
        """true operation."""
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "true", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def trunc(self, number: Json, num_digits: Json) -> WorkbookFunctionResult:
        """trunc operation.

        Args:
            number (Json):
                number parameter
            num_digits (Json):
                numDigits parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "trunc", None, {"number": number, "numDigits": num_digits}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def type(self, value: Json) -> WorkbookFunctionResult:
        """type operation.

        Args:
            value (Json):
                value parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "type", None, {"value": value}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def tdist(self, x: Json, deg_freedom: Json, cumulative: Json) -> WorkbookFunctionResult:
        """t_Dist operation.

        Args:
            x (Json):
                x parameter
            deg_freedom (Json):
                degFreedom parameter
            cumulative (Json):
                cumulative parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "t_Dist", None, {"x": x, "degFreedom": deg_freedom, "cumulative": cumulative}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def tdist_2_t(self, x: Json, deg_freedom: Json) -> WorkbookFunctionResult:
        """t_Dist_2T operation.

        Args:
            x (Json):
                x parameter
            deg_freedom (Json):
                degFreedom parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "t_Dist_2T", None, {"x": x, "degFreedom": deg_freedom}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def tdist_rt(self, x: Json, deg_freedom: Json) -> WorkbookFunctionResult:
        """t_Dist_RT operation.

        Args:
            x (Json):
                x parameter
            deg_freedom (Json):
                degFreedom parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "t_Dist_RT", None, {"x": x, "degFreedom": deg_freedom}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def tinv(self, probability: Json, deg_freedom: Json) -> WorkbookFunctionResult:
        """t_Inv operation.

        Args:
            probability (Json):
                probability parameter
            deg_freedom (Json):
                degFreedom parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "t_Inv", None, {"probability": probability, "degFreedom": deg_freedom}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def tinv_2_t(self, probability: Json, deg_freedom: Json) -> WorkbookFunctionResult:
        """t_Inv_2T operation.

        Args:
            probability (Json):
                probability parameter
            deg_freedom (Json):
                degFreedom parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "t_Inv_2T", None, {"probability": probability, "degFreedom": deg_freedom}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def unichar(self, number: Json) -> WorkbookFunctionResult:
        """unichar operation.

        Args:
            number (Json):
                number parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "unichar", None, {"number": number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def unicode(self, text: Json) -> WorkbookFunctionResult:
        """unicode operation.

        Args:
            text (Json):
                text parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "unicode", None, {"text": text}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def upper(self, text: Json) -> WorkbookFunctionResult:
        """upper operation.

        Args:
            text (Json):
                text parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "upper", None, {"text": text}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def usdollar(self, number: Json, decimals: Json) -> WorkbookFunctionResult:
        """usdollar operation.

        Args:
            number (Json):
                number parameter
            decimals (Json):
                decimals parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "usdollar", None, {"number": number, "decimals": decimals}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def value(self, text: Json) -> WorkbookFunctionResult:
        """value operation.

        Args:
            text (Json):
                text parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "value", None, {"text": text}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def var_a(self, values: Json) -> WorkbookFunctionResult:
        """varA operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "varA", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def var_pa(self, values: Json) -> WorkbookFunctionResult:
        """varPA operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "varPA", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def var_p(self, values: Json) -> WorkbookFunctionResult:
        """var_P operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "var_P", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def var_s(self, values: Json) -> WorkbookFunctionResult:
        """var_S operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "var_S", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def vdb(
        self, cost: Json, salvage: Json, life: Json, start_period: Json, end_period: Json, factor: Json, no_switch: Json
    ) -> WorkbookFunctionResult:
        """vdb operation.

        Args:
            cost (Json):
                cost parameter
            salvage (Json):
                salvage parameter
            life (Json):
                life parameter
            start_period (Json):
                startPeriod parameter
            end_period (Json):
                endPeriod parameter
            factor (Json):
                factor parameter
            no_switch (Json):
                noSwitch parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "vdb",
            None,
            {
                "cost": cost,
                "salvage": salvage,
                "life": life,
                "startPeriod": start_period,
                "endPeriod": end_period,
                "factor": factor,
                "noSwitch": no_switch,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def vlookup(
        self, lookup_value: Json, table_array: Json, col_index_num: Json, range_lookup: Json
    ) -> WorkbookFunctionResult:
        """vlookup operation.

        Args:
            lookup_value (Json):
                lookupValue parameter
            table_array (Json):
                tableArray parameter
            col_index_num (Json):
                colIndexNum parameter
            range_lookup (Json):
                rangeLookup parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "vlookup",
            None,
            {
                "lookupValue": lookup_value,
                "tableArray": table_array,
                "colIndexNum": col_index_num,
                "rangeLookup": range_lookup,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def weekday(self, serial_number: Json, return_type: Json) -> WorkbookFunctionResult:
        """weekday operation.

        Args:
            serial_number (Json):
                serialNumber parameter
            return_type (Json):
                returnType parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type_ = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "weekday", None, {"serialNumber": serial_number, "returnType": return_type}, None, return_type_
        )
        self.context.add_query(qry)
        return return_type_

    def week_num(self, serial_number: Json, return_type: Json) -> WorkbookFunctionResult:
        """weekNum operation.

        Args:
            serial_number (Json):
                serialNumber parameter
            return_type (Json):
                returnType parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type_ = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "weekNum", None, {"serialNumber": serial_number, "returnType": return_type}, None, return_type_
        )
        self.context.add_query(qry)
        return return_type_

    def weibull_dist(self, x: Json, alpha: Json, beta: Json, cumulative: Json) -> WorkbookFunctionResult:
        """weibull_Dist operation.

        Args:
            x (Json):
                x parameter
            alpha (Json):
                alpha parameter
            beta (Json):
                beta parameter
            cumulative (Json):
                cumulative parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "weibull_Dist",
            None,
            {"x": x, "alpha": alpha, "beta": beta, "cumulative": cumulative},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def work_day(self, start_date: Json, days: Json, holidays: Json) -> WorkbookFunctionResult:
        """workDay operation.

        Args:
            start_date (Json):
                startDate parameter
            days (Json):
                days parameter
            holidays (Json):
                holidays parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "workDay", None, {"startDate": start_date, "days": days, "holidays": holidays}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def work_day_intl(self, start_date: Json, days: Json, weekend: Json, holidays: Json) -> WorkbookFunctionResult:
        """workDay_Intl operation.

        Args:
            start_date (Json):
                startDate parameter
            days (Json):
                days parameter
            weekend (Json):
                weekend parameter
            holidays (Json):
                holidays parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "workDay_Intl",
            None,
            {"startDate": start_date, "days": days, "weekend": weekend, "holidays": holidays},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def xirr(self, values: Json, dates: Json, guess: Json) -> WorkbookFunctionResult:
        """xirr operation.

        Args:
            values (Json):
                values parameter
            dates (Json):
                dates parameter
            guess (Json):
                guess parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "xirr", None, {"values": values, "dates": dates, "guess": guess}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def xnpv(self, rate: Json, values: Json, dates: Json) -> WorkbookFunctionResult:
        """xnpv operation.

        Args:
            rate (Json):
                rate parameter
            values (Json):
                values parameter
            dates (Json):
                dates parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "xnpv", None, {"rate": rate, "values": values, "dates": dates}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def xor(self, values: Json) -> WorkbookFunctionResult:
        """xor operation.

        Args:
            values (Json):
                values parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "xor", None, {"values": values}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def year(self, serial_number: Json) -> WorkbookFunctionResult:
        """year operation.

        Args:
            serial_number (Json):
                serialNumber parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "year", None, {"serialNumber": serial_number}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def year_frac(self, start_date: Json, end_date: Json, basis: Json) -> WorkbookFunctionResult:
        """yearFrac operation.

        Args:
            start_date (Json):
                startDate parameter
            end_date (Json):
                endDate parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self, "yearFrac", None, {"startDate": start_date, "endDate": end_date, "basis": basis}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def yield_(
        self, settlement: Json, maturity: Json, rate: Json, pr: Json, redemption: Json, frequency: Json, basis: Json
    ) -> WorkbookFunctionResult:
        """yield operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            rate (Json):
                rate parameter
            pr (Json):
                pr parameter
            redemption (Json):
                redemption parameter
            frequency (Json):
                frequency parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "yield",
            None,
            {
                "settlement": settlement,
                "maturity": maturity,
                "rate": rate,
                "pr": pr,
                "redemption": redemption,
                "frequency": frequency,
                "basis": basis,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def yield_disc(
        self, settlement: Json, maturity: Json, pr: Json, redemption: Json, basis: Json
    ) -> WorkbookFunctionResult:
        """yieldDisc operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            pr (Json):
                pr parameter
            redemption (Json):
                redemption parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "yieldDisc",
            None,
            {"settlement": settlement, "maturity": maturity, "pr": pr, "redemption": redemption, "basis": basis},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def yield_mat(
        self, settlement: Json, maturity: Json, issue: Json, rate: Json, pr: Json, basis: Json
    ) -> WorkbookFunctionResult:
        """yieldMat operation.

        Args:
            settlement (Json):
                settlement parameter
            maturity (Json):
                maturity parameter
            issue (Json):
                issue parameter
            rate (Json):
                rate parameter
            pr (Json):
                pr parameter
            basis (Json):
                basis parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(
            self,
            "yieldMat",
            None,
            {"settlement": settlement, "maturity": maturity, "issue": issue, "rate": rate, "pr": pr, "basis": basis},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def ztest(self, array: Json, x: Json, sigma: Json) -> WorkbookFunctionResult:
        """z_Test operation.

        Args:
            array (Json):
                array parameter
            x (Json):
                x parameter
            sigma (Json):
                sigma parameter
        """
        from office365.onedrive.workbooks.functions.result import WorkbookFunctionResult

        return_type = WorkbookFunctionResult(self.context)
        qry = ServiceOperationQuery(self, "z_Test", None, {"array": array, "x": x, "sigma": sigma}, None, return_type)
        self.context.add_query(qry)
        return return_type
