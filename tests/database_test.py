#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import ipaddress
import sys
import unittest

sys.path.append("..")

import geoip2.database
import maxminddb

try:
    import maxminddb.extension
except ImportError:
    maxminddb.extension = None  # type: ignore


class BaseTestReader(unittest.TestCase):
    def test_language_list(self) -> None:
        reader = geoip2.database.Reader(
            "tests/data/test-data/GeoIP2-Country-Test.mmdb",
            ["xx", "ru", "pt-BR", "es", "en"],
        )
        record = reader.country("81.2.69.160")

        self.assertEqual(record.country.name, "Великобритания")
        reader.close()

    def test_unknown_address(self) -> None:
        reader = geoip2.database.Reader("tests/data/test-data/GeoIP2-City-Test.mmdb")
        with self.assertRaisesRegex(
            geoip2.errors.AddressNotFoundError,
            "The address 10.10.10.10 is not in the " "database.",
        ):
            reader.city("10.10.10.10")
        reader.close()

    def test_wrong_database(self) -> None:
        reader = geoip2.database.Reader("tests/data/test-data/GeoIP2-City-Test.mmdb")
        with self.assertRaisesRegex(
            TypeError,
            "The country method cannot be used with " "the GeoIP2-City database",
        ):
            reader.country("1.1.1.1")
        reader.close()

    def test_invalid_address(self) -> None:
        reader = geoip2.database.Reader("tests/data/test-data/GeoIP2-City-Test.mmdb")
        with self.assertRaisesRegex(
            ValueError, "u?'invalid' does not appear to be an " "IPv4 or IPv6 address"
        ):
            reader.city("invalid")
        reader.close()

    def test_anonymous_ip(self) -> None:
        reader = geoip2.database.Reader(
            "tests/data/test-data/GeoIP2-Anonymous-IP-Test.mmdb"
        )
        ip_address = "1.2.0.1"

        record = reader.anonymous_ip(ip_address)
        self.assertEqual(record.is_anonymous, True)
        self.assertEqual(record.is_anonymous_vpn, True)
        self.assertEqual(record.is_hosting_provider, False)
        self.assertEqual(record.is_public_proxy, False)
        self.assertEqual(record.is_tor_exit_node, False)
        self.assertEqual(record.ip_address, ip_address)
        self.assertEqual(record.network, ipaddress.ip_network("1.2.0.0/16"))
        reader.close()

    def test_asn(self) -> None:
        reader = geoip2.database.Reader("tests/data/test-data/GeoLite2-ASN-Test.mmdb")

        ip_address = "1.128.0.0"
        record = reader.asn(ip_address)

        self.assertEqual(record, eval(repr(record)), "ASN repr can be eval'd")

        self.assertEqual(record.autonomous_system_number, 1221)
        self.assertEqual(record.autonomous_system_organization, "Telstra Pty Ltd")
        self.assertEqual(record.ip_address, ip_address)
        self.assertEqual(record.network, ipaddress.ip_network("1.128.0.0/11"))

        self.assertRegex(
            str(record),
            r"geoip2.models.ASN\(.*1\.128\.0\.0.*\)",
            "str representation is correct",
        )

        reader.close()

    def test_city(self) -> None:
        reader = geoip2.database.Reader("tests/data/test-data/GeoIP2-City-Test.mmdb")
        record = reader.city("81.2.69.160")

        self.assertEqual(
            record.country.name, "United Kingdom", "The default locale is en"
        )
        self.assertEqual(record.country.is_in_european_union, True)
        self.assertEqual(
            record.location.accuracy_radius, 100, "The accuracy_radius is populated"
        )
        self.assertEqual(record.registered_country.is_in_european_union, False)

        reader.close()

    def test_connection_type(self) -> None:
        reader = geoip2.database.Reader(
            "tests/data/test-data/GeoIP2-Connection-Type-Test.mmdb"
        )
        ip_address = "1.0.1.0"

        record = reader.connection_type(ip_address)

        self.assertEqual(
            record, eval(repr(record)), "ConnectionType repr can be eval'd"
        )

        self.assertEqual(record.connection_type, "Cable/DSL")
        self.assertEqual(record.ip_address, ip_address)
        self.assertEqual(record.network, ipaddress.ip_network("1.0.1.0/24"))

        self.assertRegex(
            str(record),
            r"ConnectionType\(\{.*Cable/DSL.*\}\)",
            "ConnectionType str representation is reasonable",
        )

        reader.close()

    def test_country(self) -> None:
        reader = geoip2.database.Reader("tests/data/test-data/GeoIP2-Country-Test.mmdb")
        record = reader.country("81.2.69.160")
        self.assertEqual(
            record.traits.ip_address, "81.2.69.160", "IP address is added to model"
        )
        self.assertEqual(record.traits.network, ipaddress.ip_network("81.2.69.160/27"))
        self.assertEqual(record.country.is_in_european_union, True)
        self.assertEqual(record.registered_country.is_in_european_union, False)
        reader.close()

    def test_domain(self) -> None:
        reader = geoip2.database.Reader("tests/data/test-data/GeoIP2-Domain-Test.mmdb")

        ip_address = "1.2.0.0"
        record = reader.domain(ip_address)

        self.assertEqual(record, eval(repr(record)), "Domain repr can be eval'd")

        self.assertEqual(record.domain, "maxmind.com")
        self.assertEqual(record.ip_address, ip_address)
        self.assertEqual(record.network, ipaddress.ip_network("1.2.0.0/16"))

        self.assertRegex(
            str(record),
            r"Domain\(\{.*maxmind.com.*\}\)",
            "Domain str representation is reasonable",
        )

        reader.close()

    def test_enterprise(self) -> None:
        with geoip2.database.Reader(
            "tests/data/test-data/GeoIP2-Enterprise-Test.mmdb"
        ) as reader:
            ip_address = "74.209.24.0"
            record = reader.enterprise(ip_address)
            self.assertEqual(record.city.confidence, 11)
            self.assertEqual(record.country.confidence, 99)
            self.assertEqual(record.country.geoname_id, 6252001)
            self.assertEqual(record.country.is_in_european_union, False)
            self.assertEqual(record.location.accuracy_radius, 27)
            self.assertEqual(record.registered_country.is_in_european_union, False)
            self.assertEqual(record.traits.connection_type, "Cable/DSL")
            self.assertTrue(record.traits.is_legitimate_proxy)
            self.assertEqual(record.traits.ip_address, ip_address)
            self.assertEqual(
                record.traits.network, ipaddress.ip_network("74.209.16.0/20")
            )

    def test_isp(self) -> None:
        reader = geoip2.database.Reader("tests/data/test-data/GeoIP2-ISP-Test.mmdb")

        ip_address = "1.128.0.0"
        record = reader.isp(ip_address)
        self.assertEqual(record, eval(repr(record)), "ISP repr can be eval'd")

        self.assertEqual(record.autonomous_system_number, 1221)
        self.assertEqual(record.autonomous_system_organization, "Telstra Pty Ltd")
        self.assertEqual(record.isp, "Telstra Internet")
        self.assertEqual(record.organization, "Telstra Internet")
        self.assertEqual(record.ip_address, ip_address)
        self.assertEqual(record.network, ipaddress.ip_network("1.128.0.0/11"))

        self.assertRegex(
            str(record),
            r"ISP\(\{.*Telstra.*\}\)",
            "ISP str representation is reasonable",
        )

        reader.close()

    def test_context_manager(self) -> None:
        with geoip2.database.Reader(
            "tests/data/test-data/GeoIP2-Country-Test.mmdb"
        ) as reader:
            record = reader.country("81.2.69.160")
            self.assertEqual(record.traits.ip_address, "81.2.69.160")


@unittest.skipUnless(maxminddb.extension, "No C extension module found. Skipping tests")
class TestExtensionReader(BaseTestReader):
    mode = geoip2.database.MODE_MMAP_EXT


class TestMMAPReader(BaseTestReader):
    mode = geoip2.database.MODE_MMAP


class TestFileReader(BaseTestReader):
    mode = geoip2.database.MODE_FILE


class TestMemoryReader(BaseTestReader):
    mode = geoip2.database.MODE_MEMORY


class TestFDReader(unittest.TestCase):
    mode = geoip2.database.MODE_FD


class TestAutoReader(BaseTestReader):
    mode = geoip2.database.MODE_AUTO
