from api.resources.utils import date_to_ksuid, ksuid_to_date


def test_date_to_ksuid():
    print(date_to_ksuid("2023-05-18"))


def test_ksuid_to_date():
    print(ksuid_to_date("2fccJ728IkoUB2lrtntfHxoV5cn"))
