"""Validation helpers that reduce false-positive PII detections."""

from __future__ import annotations

import ipaddress
import re


def is_valid_email(value: str) -> bool:
    return bool(
        re.fullmatch(
            r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
            r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
            r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+",
            value,
        )
    )


def is_valid_ssn(value: str) -> bool:
    match = re.fullmatch(r"(\d{3})-(\d{2})-(\d{4})", value)
    if match is None:
        return False
    area, group, serial = match.groups()
    return (
        area not in {"000", "666"}
        and not area.startswith("9")
        and group != "00"
        and serial != "0000"
    )


def is_valid_credit_card(value: str) -> bool:
    digits = re.sub(r"\D", "", value)
    if not 13 <= len(digits) <= 19:
        return False
    checksum = 0
    for index, digit in enumerate(reversed(digits)):
        number = int(digit)
        if index % 2:
            number *= 2
            if number > 9:
                number -= 9
        checksum += number
    return checksum % 10 == 0


def is_valid_phone(value: str) -> bool:
    digits = re.sub(r"\D", "", value)
    return 7 <= len(digits) <= 15 and any(character.isdigit() for character in value)


def is_valid_ip_address(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
    except ValueError:
        return False
    return True


def is_valid_api_key(value: str) -> bool:
    return len(value) >= 20 and bool(re.search(r"[A-Za-z]", value)) and bool(
        re.search(r"\d", value)
    )


def is_valid_employee_id(value: str) -> bool:
    return bool(re.fullmatch(r"EMP-\d{4,8}", value, flags=re.IGNORECASE))
