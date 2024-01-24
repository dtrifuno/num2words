# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

from __future__ import unicode_literals
from decimal import Decimal

from .base import Num2Word_Base
from .currency import parse_currency_parts, prefix_currency
from .utils import get_digits, splitbyx

GENDER_TO_IDX = {"m": 0, "f": 1, "n": 2}
PLURAL_IDX = 3

ZERO = "нула"

ONES = {
    1: ("еден", "една", "едно"),
    2: ("два", "две", "две"),
    3: ("три", "три", "три"),
    4: ("четири", "четири", "четири"),
    5: ("пет", "пет", "пет"),
    6: ("шест", "шест", "шест"),
    7: ("седум", "седум", "седум"),
    8: ("осум", "осум", "осум"),
    9: ("девет", "девет", "девет"),
}

ORDINAL_ONES = {
    1: ("прв", "прва", "прво", "први"),
    2: ("втор", "втора", "второ", "втори"),
    3: ("трет", "трета", "трето", "трети"),
    4: ("четврт", "четврта", "четврто", "четврти"),
    5: ("петти", "петта", "петто", "петти"),
    6: ("шестти", "шестта", "шестто", "шестти"),
    7: ("седми", "седма", "седмо", "седми"),
    8: ("осми", "осма", "осмо", "осми"),
    9: ("деветти", "деветта", "деветто", "деветти"),
}

TENS = {
    0: "десет",
    1: "единаесет",
    2: "дванаесет",
    3: "тринаесет",
    4: "четиринаесет",
    5: "петнаесет",
    6: "шеснаесет",
    7: "седумнаесет",
    8: "осумнаесет",
    9: "деветнаесет",
}

ORDINAL_TENS = {
    0: ("десетти", "десетта", "десетто", "десетти"),
    1: ("единаесетти", "единаесетта", "единаесетто", "единаесетти"),
    2: ("дванаесетти", "дванаесетта", "дванаесетто", "дванаесетти"),
    3: ("тринаесетти", "тринаесетта", "тринаесетто", "тринаесетти"),
    4: ("четиринаесетти", "четиринаесетта", "четиринаесетто", "четиринаесетти"),
    5: ("петнаесетти", "петнаесетта", "петнаесетто", "петнаесетти"),
    6: ("шеснаесетти", "шеснаесетта", "шеснаесетто", "шеснаесетти"),
    7: ("седумнаесетти", "седумнаесетта", "седумнаесетто", "седумнаесетти"),
    8: ("осумнаесетти", "осумнаесетта", "осумнаесетто", "осумнаесетти"),
    9: ("деветнаесетти", "деветнаесетта", "деветнаесетто", "деветнаесетти"),
}

TWENTIES = {
    2: "дваесет",
    3: "триесет",
    4: "четириесет",
    5: "педесет",
    6: "шеесет",
    7: "седумдесет",
    8: "осумдесет",
    9: "деведесет",
}

ORDINAL_TWENTIES = {
    2: ("дваесетти", "дваесетта", "дваесетто", "дваесетти"),
    3: ("триесетти", "триесетта", "триесетто", "триесетти"),
    4: ("четириесетти", "четириесетта", "четириесетто", "четириесетти"),
    5: ("педесетти", "педесетта", "педесетто", "педесетти"),
    6: ("шеесетти", "шеесетта", "шеесетто", "шеесетти"),
    7: ("седумдесетти", "седумдесетта", "седумсетто", "седумдесетти"),
    8: ("осумдесетти", "осумдесетта", "осумдесетто", "осумдесетти"),
    9: ("деведесетти", "деведесетта", "деведесетто", "деведесетти"),
}

HUNDREDS = {
    1: "сто",
    2: "двесте",
    3: "триста",
    4: "четиристотини",
    5: "петстотини",
    6: "шестотини",
    7: "седумстотини",
    8: "осумстотини",
    9: "деветстотини",
}

ORDINAL_HUNDREDS = {
    1: ("стоти", "стота", "стото", "стоти"),
    2: ("двестоти", "двестота", "двестото", "двестоти"),
    3: ("тристоти", "тристота", "тристото", "тристоти"),
    4: ("четиристоти", "четиристота", "четиристото", "четиристоти"),
    5: ("петстоти", "петстота", "петстото", "петстоти"),
    6: ("шестоти", "шестота", "шестото", "шестоти"),
    7: ("седумстоти", "седумстота", "седумстото", "седумстоти"),
    8: ("осумстоти", "осумстота", "осумстото", "осумстоти"),
    9: ("деветстоти", "деветстота", "деветстото", "деветстоти"),
}

SCALE = {
    0: ("", "", ""),
    1: ("илјада", "илјади", "f"),  # 10^3
    2: ("милион", "милиони", "m"),  # 10^6
    3: ("милијарда", "милијарди", "f"),  # 10^9
    4: ("билион", "билиони", "m"),  # 10^12
    5: ("билијарда", "билијарди", "f"),  # 10^15
    6: ("трилион", "трилиони", "m"),  # 10^18
    7: ("трилијарда", "трилијарди", "f"),  # 10^21
    8: ("квадрилион", "квадрилиони", "m"),  # 10^24
    9: ("квадрилијарда", "квадрилијарди", "f"),  # 10^27
    10: ("квинтилион", "квинтилиони", "m"),  # 10^30
}

ORDINAL_SCALE = {
    0: ("", "", "", ""),
    1: ("илјадит", "илјадита", "илјадито", "илјадити"),
    2: ("милионит", "милионита", "милионито", "милионити"),
}


class Num2Word_MK(Num2Word_Base):
    CURRENCY_FORMS = {
        "MKD": (("денар", "денари", "m"), ("ден", "дени", "m")),
        "EUR": (("евро", "евра", "n"), ("цент", "центи", "m")),
        "USD": (("долар", "долари", "m"), ("цент", "центи", "m")),
    }

    def setup(self):
        self.negword = "минус"
        self.pointword = "запирка"
        self.MAXVAL = 10 ** (3 * len(SCALE))
        self.ORDMAXVAL = 10 ** (3 * len(ORDINAL_SCALE))

    def str_to_number(self, value):
        return Decimal(value.replace(",", "."))

    def pluralize(self, number, forms):
        number = number % 100
        form = 1
        if number == 1 or (number > 20 and number % 10 == 1):
            form = 0
        return forms[form]

    def to_cardinal(self, value, form="m"):
        try:
            assert int(value) == value
        except (ValueError, TypeError, AssertionError):
            return self.to_cardinal_float(value, form)

        out = ""
        if value < 0:
            value = abs(value)
            out = "%s " % self.negword.strip()
        elif value == 0:
            return ZERO

        if value >= self.MAXVAL:
            raise OverflowError(self.errmsg_toobig % (value, self.MAXVAL))

        return out + self._int2word(int(value), form)

    def to_cardinal_float(self, value, form):
        n = str(value)
        if "." in n:
            left, right = n.split(".")
            leading_zero_count = len(right) - len(right.lstrip("0"))
            decimal_part = (ZERO + " ") * leading_zero_count + self._int2word(
                int(right), form
            )
            return "%s %s %s" % (
                self._int2word(int(left), form),
                self.pointword,
                decimal_part,
            )
        else:
            return

    def to_ordinal(self, value, form="m"):
        self.verify_ordinal(value)  # FIXME

        chunks = list(splitbyx(str(value), 3))
        last_chunk_idx = 0
        for i, chunk in enumerate(chunks):
            if chunk != 0:
                last_chunk_idx = i

        last_chunk = chunks[last_chunk_idx]

        chunks[last_chunk_idx] = 0
        ordinal_part = int("".join(f"{chunk:03d}" for chunk in chunks))
        prefix = "" if ordinal_part == 0 else self._int2word(ordinal_part, "m")

        suffix = self._chunk2ordinal(
            last_chunk,
            len(chunks) - 1 - last_chunk_idx,
            last_chunk_idx == 0,
            form,
        )
        if prefix:
            return "%s %s" % (prefix, suffix)
        else:
            return suffix

    def to_ordinal_num(self, value, form="m"):
        suffix = self.to_ordinal(value, form)[-2:]
        return "%s-%s" % (value, suffix)

    def to_year(self, number):
        return self.to_ordinal(number, form="f")

    def _cents_verbose(self, number, currency):
        if number == 0:
            return ZERO
        return self._int2word(number, self.CURRENCY_FORMS[currency][1][-1])

    def _cents_terse(self, number, currency):
        return "%d" % number

    def _int2word(self, number, form):
        words = []
        chunks = list(splitbyx(str(number), 3))
        chunk_len = len(chunks)
        for chunk in chunks:
            chunk_len -= 1
            ones_digit, tens_digit, hundreds_digit = get_digits(chunk)

            if hundreds_digit > 0:
                words.append(HUNDREDS[hundreds_digit])

            if hundreds_digit != 0 or (chunk_len == 0 and number > 99):
                if tens_digit == 1 or (tens_digit > 1 and ones_digit == 0):
                    words.append("и")

            if tens_digit > 1:
                words.append(TWENTIES[tens_digit])

            if tens_digit == 1:
                words.append(TENS[ones_digit])
            elif ones_digit == 0 or (chunk == 1 and chunk_len > 0):
                pass
            else:
                if chunk > 9 or (chunk_len == 0 and number > 9):
                    words.append("и")

                chunk_gender = SCALE[chunk_len][-1] or form
                chunk_gender_idx = GENDER_TO_IDX[chunk_gender]
                words.append(ONES[ones_digit][chunk_gender_idx])

            if chunk_len > 0 and chunk != 0:
                words.append(self.pluralize(chunk, SCALE[chunk_len]))

        return " ".join(words)

    def _chunk2ordinal(self, chunk, chunk_idx, first_chunk, form):
        words = []
        ones_digit, tens_digit, hundreds_digit = get_digits(chunk)
        gender_idx = PLURAL_IDX if form == "p" else GENDER_TO_IDX[form]

        if hundreds_digit > 0:
            if chunk % 100 == 0 and chunk_idx == 0:
                words.append(ORDINAL_HUNDREDS[hundreds_digit][gender_idx])
            else:
                words.append(HUNDREDS[hundreds_digit])

        if hundreds_digit != 0 or (chunk_idx == 0 and not first_chunk):
            if tens_digit == 1 or (tens_digit > 1 and ones_digit == 0):
                words.append("и")

        if tens_digit > 1:
            if chunk % 10 == 0 and chunk_idx == 0:
                words.append(ORDINAL_TWENTIES[tens_digit][gender_idx])
            else:
                words.append(TWENTIES[tens_digit])

        if tens_digit == 1:
            if chunk_idx == 0:
                words.append(ORDINAL_TENS[ones_digit][gender_idx])
            else:
                words.append(TENS[ones_digit])
        elif ones_digit == 0 or (chunk == 1 and chunk_idx > 0):
            pass
        else:
            if chunk > 9 or (chunk_idx == 0 and not first_chunk):
                words.append("и")

            if chunk_idx == 0:
                words.append(ORDINAL_ONES[ones_digit][gender_idx])
            else:
                words.append(ONES[ones_digit][gender_idx])

        if chunk_idx > 0:
            words.append(ORDINAL_SCALE[chunk_idx][gender_idx])

        return " ".join(words)

    def to_currency(
        self, val, currency="EUR", cents=True, separator=",", adjective=False
    ):
        """
        Args:
            val: Numeric value
            currency (str): Currency code
            cents (bool): Verbose cents
            separator (str): Cent separator
            adjective (bool): Prefix currency name with adjective
        Returns:
            str: Formatted string

        """
        left, right, is_negative = parse_currency_parts(val)

        try:
            cr1, cr2 = self.CURRENCY_FORMS[currency]

        except KeyError:
            raise NotImplementedError(
                'Currency code "%s" not implemented for "%s"'
                % (currency, self.__class__.__name__)
            )

        if adjective and currency in self.CURRENCY_ADJECTIVES:
            cr1 = prefix_currency(self.CURRENCY_ADJECTIVES[currency], cr1)

        minus_str = "%s " % self.negword if is_negative else ""
        cents_str = (
            self._cents_verbose(right, currency)
            if cents
            else self._cents_terse(right, currency)
        )

        return "%s%s %s%s %s %s" % (
            minus_str,
            self.to_cardinal(left, form=cr1[-1]),
            self.pluralize(left, cr1),
            separator,
            cents_str,
            self.pluralize(right, cr2),
        )
