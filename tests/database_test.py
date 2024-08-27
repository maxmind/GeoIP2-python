#!/usr/bin/env python


import ipaddress
import re
import unittest
from unittest.mock import patch, MagicMock

import pytest

import geoip2.database
import geoip2.errors
import maxminddb

try:
    import maxminddb.extension
except ImportError:
    maxminddb.extension = None  # type: ignore


class TestReader(unittest.TestCase):
    def test_language_list(self) -> None:
        reader = geoip2.database.Reader(
            "tests/data/test-data/GeoIP2-Country-Test.mmdb",
            ["xx", "ru", "pt-BR", "es", "en"],
        )
        record = reader.country("81.2.69.160")

        assert record.country.name == "Великобритания"
        reader.close()

    def test_unknown_address(self) -> None:
        reader = geoip2.database.Reader("tests/data/test-data/GeoIP2-City-Test.mmdb")
        with pytest.raises(
            geoip2.errors.AddressNotFoundError,
            match="The address 10.10.10.10 is not in the database.",
        ):
            reader.city("10.10.10.10")
        reader.close()

    def test_unknown_address_network(self) -> None:
        reader = geoip2.database.Reader("tests/data/test-data/GeoIP2-City-Test.mmdb")
        with pytest.raises(geoip2.errors.AddressNotFoundError) as ei:
            reader.city("10.10.10.10")
        assert ei.value.network == ipaddress.ip_network("10.0.0.0/8")
        reader.close()

    def test_wrong_database(self) -> None:
        reader = geoip2.database.Reader("tests/data/test-data/GeoIP2-City-Test.mmdb")
        with pytest.raises(
            TypeError,
            match="The country method cannot be used with the GeoIP2-City database",
        ):
            reader.country("1.1.1.1")
        reader.close()

    def test_invalid_address(self) -> None:
        reader = geoip2.database.Reader("tests/data/test-data/GeoIP2-City-Test.mmdb")
        with pytest.raises(
            ValueError,
            match="u?'invalid' does not appear to be an " "IPv4 or IPv6 address",
        ):
            reader.city("invalid")
        reader.close()

    def test_anonymous_ip(self) -> None:
        reader = geoip2.database.Reader(
            "tests/data/test-data/GeoIP2-Anonymous-IP-Test.mmdb"
        )
        ip_address = "1.2.0.1"

        record = reader.anonymous_ip(ip_address)
        assert record.is_anonymous is True
        assert record.is_anonymous_vpn is True
        assert record.is_hosting_provider is False
        assert record.is_public_proxy is False
        assert record.is_residential_proxy is False
        assert record.is_tor_exit_node is False
        assert record.ip_address == ip_address
        assert record.network == ipaddress.ip_network("1.2.0.0/16")
        reader.close()

    def test_anonymous_ip_all_set(self) -> None:
        reader = geoip2.database.Reader(
            "tests/data/test-data/GeoIP2-Anonymous-IP-Test.mmdb"
        )
        ip_address = "81.2.69.1"

        record = reader.anonymous_ip(ip_address)
        assert record.is_anonymous is True
        assert record.is_anonymous_vpn is True
        assert record.is_hosting_provider is True
        assert record.is_public_proxy is True
        assert record.is_residential_proxy is True
        assert record.is_tor_exit_node is True
        assert record.ip_address == ip_address
        assert record.network == ipaddress.ip_network("81.2.69.0/24")
        reader.close()

    def test_asn(self) -> None:
        reader = geoip2.database.Reader("tests/data/test-data/GeoLite2-ASN-Test.mmdb")

        ip_address = "1.128.0.0"
        record = reader.asn(ip_address)

        assert record == eval(repr(record)), "ASN repr can be eval'd"

        assert record.autonomous_system_number == 1221
        assert record.autonomous_system_organization == "Telstra Pty Ltd"
        assert record.ip_address == ip_address
        assert record.network == ipaddress.ip_network("1.128.0.0/11")

        assert re.search(
            r"geoip2.models.ASN\(.*1\.128\.0\.0.*\)", str(record)
        ), "str representation is correct"

        reader.close()

    def test_city(self) -> None:
        reader = geoip2.database.Reader("tests/data/test-data/GeoIP2-City-Test.mmdb")
        record = reader.city("81.2.69.160")

        assert record.country.name == "United Kingdom", "The default locale is en"
        assert record.country.is_in_european_union is False
        assert (
            record.location.accuracy_radius == 100
        ), "The accuracy_radius is populated"
        assert record.registered_country.is_in_european_union is False
        assert not record.traits.is_anycast

        record = reader.city("214.1.1.0")
        assert record.traits.is_anycast

        reader.close()

    def test_connection_type(self) -> None:
        reader = geoip2.database.Reader(
            "tests/data/test-data/GeoIP2-Connection-Type-Test.mmdb"
        )
        ip_address = "1.0.1.0"

        record = reader.connection_type(ip_address)

        assert record == eval(repr(record)), "ConnectionType repr can be eval'd"

        assert record.connection_type == "Cellular"
        assert record.ip_address == ip_address
        assert record.network == ipaddress.ip_network("1.0.1.0/24")
        assert re.search(
            r"ConnectionType\(\{.*Cellular.*\}\)", str(record)
        ), "ConnectionType str representation is reasonable"
        reader.close()

    def test_country(self) -> None:
        reader = geoip2.database.Reader("tests/data/test-data/GeoIP2-Country-Test.mmdb")
        record = reader.country("81.2.69.160")
        assert record.traits.ip_address == "81.2.69.160", "IP address is added to model"
        assert record.traits.network == ipaddress.ip_network("81.2.69.160/27")
        assert record.country.is_in_european_union is False
        assert record.registered_country.is_in_european_union is False
        assert not record.traits.is_anycast

        record = reader.country("214.1.1.0")
        assert record.traits.is_anycast

        reader.close()

    def test_domain(self) -> None:
        reader = geoip2.database.Reader("tests/data/test-data/GeoIP2-Domain-Test.mmdb")

        ip_address = "1.2.0.0"
        record = reader.domain(ip_address)

        assert record == eval(repr(record)), "Domain repr can be eval'd"

        assert record.domain == "maxmind.com"
        assert record.ip_address == ip_address
        assert record.network == ipaddress.ip_network("1.2.0.0/16")
        assert re.search(
            r"Domain\(\{.*maxmind.com.*\}\)", str(record)
        ), "Domain str representation is reasonable"

        reader.close()

    def test_enterprise(self) -> None:
        with geoip2.database.Reader(
            "tests/data/test-data/GeoIP2-Enterprise-Test.mmdb"
        ) as reader:
            ip_address = "74.209.24.0"
            record = reader.enterprise(ip_address)
            assert record.city.confidence == 11
            assert record.country.confidence == 99
            assert record.country.geoname_id == 6252001
            assert record.country.is_in_european_union is False
            assert record.location.accuracy_radius == 27
            assert record.registered_country.is_in_european_union is False
            assert record.traits.connection_type == "Cable/DSL"
            assert record.traits.is_legitimate_proxy
            assert record.traits.ip_address == ip_address
            assert record.traits.network == ipaddress.ip_network("74.209.16.0/20")
            assert not record.traits.is_anycast

            record = reader.enterprise("149.101.100.0")
            assert record.traits.mobile_country_code == "310"
            assert record.traits.mobile_network_code == "004"

            record = reader.enterprise("214.1.1.0")
            assert record.traits.is_anycast

    def test_isp(self) -> None:
        with geoip2.database.Reader(
            "tests/data/test-data/GeoIP2-ISP-Test.mmdb"
        ) as reader:
            ip_address = "1.128.0.0"
            record = reader.isp(ip_address)
            assert record == eval(repr(record)), "ISP repr can be eval'd"

            assert record.autonomous_system_number == 1221
            assert record.autonomous_system_organization == "Telstra Pty Ltd"
            assert record.isp == "Telstra Internet"
            assert record.organization == "Telstra Internet"
            assert record.ip_address == ip_address
            assert record.network == ipaddress.ip_network("1.128.0.0/11")
            assert re.search(
                r"ISP\(\{.*Telstra.*\}\)", str(record)
            ), "ISP str representation is reasonable"
            record = reader.isp("149.101.100.0")

            assert record.mobile_country_code == "310"
            assert record.mobile_network_code == "004"

    def test_context_manager(self) -> None:
        with geoip2.database.Reader(
            "tests/data/test-data/GeoIP2-Country-Test.mmdb"
        ) as reader:
            record = reader.country("81.2.69.160")
            assert record.traits.ip_address == "81.2.69.160"

    @patch("maxminddb.open_database")
    def test_modes(self, mock_open) -> None:
        mock_open.return_value = MagicMock()

        path = "tests/data/test-data/GeoIP2-Country-Test.mmdb"
        with geoip2.database.Reader(
            path,
            mode=geoip2.database.MODE_MMAP_EXT,
        ) as reader:
            mock_open.assert_called_once_with(path, geoip2.database.MODE_MMAP_EXT)
