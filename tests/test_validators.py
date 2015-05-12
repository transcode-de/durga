# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import six

from durga import exceptions, validators


@pytest.mark.parametrize('value', [
    "http://foo.com/blah_blah",
    "http://foo.com/blah_blah/",
    "http://foo.com/blah_blah_(wikipedia)",
    "http://foo.com/blah_blah_(wikipedia)_(again)",
    "http://www.example.com/wpstyle/?p=364",
    "https://www.example.com/foo/?bar=baz&inga=42&quux",
    "http://✪df.ws/123",
    "http://userid:password@example.com:8080",
    "http://userid:password@example.com:8080/",
    "http://userid@example.com",
    "http://userid@example.com/",
    "http://userid@example.com:8080",
    "http://userid@example.com:8080/",
    "http://userid:password@example.com",
    "http://userid:password@example.com/",
    "http://142.42.1.1/",
    "http://142.42.1.1:8080/",
    "http://➡.ws/䨹",
    "http://⌘.ws",
    "http://⌘.ws/",
    "http://foo.com/blah_(wikipedia)#cite-1",
    "http://foo.com/blah_(wikipedia)_blah#cite-1",
    "http://foo.com/unicode_(✪)_in_parens",
    "http://foo.com/(something)?after=parens",
    "http://☺.damowmow.com/",
    "http://code.google.com/events/#&product=browser",
    "http://j.mp",
    "ftp://foo.bar/baz",
    "http://foo.bar/?q=Test%20URL-encoded%20stuff",
    "http://مثال.إختبار",
    "http://例子.测试",
    "http://उदाहरण.परीक्षा",
    "http://-.~_!$&'()*+,;=:%40:80%2f::::::@example.com",
    "http://1337.net",
    "http://a.b-c.de",
    "http://223.255.255.254",
])
def test_url_validator(value):
    assert validators.url(value) == value


@pytest.mark.parametrize('value', [
    'http://',
    'http://.',
    'http://..',
    'http://../',
    'http://?',
    'http://??',
    'http://??/',
    'http://#',
    'http://##',
    'http://##/',
    'http://foo.bar?q=Spaces should be encoded',
    '//',
    '//a',
    '///a',
    '///',
    'http:///a',
    'foo.com',
    'rdar://1234',
    'h://test',
    ':// should fail',
    'http://3628126748',
])
def test_url_validator_fails(value):
    with pytest.raises(exceptions.ValidationError) as excinfo:
        validators.url(value)
    assert value in six.text_type(excinfo.value)


@pytest.mark.parametrize('value', [
    'email@example.com',
    'firstname.lastname@example.com',
    'email@subdomain.example.com',
    'firstname+lastname@example.com',
    'email@123.123.123.123',
    '1234567890@example.com',
    'email@example-one.com',
    '_______@example.com',
    'email@example.name',
    'email@example.museum',
    'email@example.co.jp',
    'firstname-lastname@example.com',
])
def test_email_validator(value):
    assert validators.email(value) == value


@pytest.mark.parametrize('value', [
    'plainaddress',
    '#@%^%#$@#$@#.com',
    '@example.com',
    'Joe Smith <email@example.com>',
    'email.example.com',
    'email@example@example.com',
    '.email@example.com',
    'email.@example.com',
    'email..email@example.com',
    'あいうえお@example.com',
    'email@example.com (Joe Smith)',
    'email@example',
    'email@-example.com',
    'email@example..com',
    'Abc..123@example.com',
])
def test_email_validator_fails(value):
    with pytest.raises(exceptions.ValidationError) as excinfo:
        validators.email(value)
    assert value in six.text_type(excinfo.value)


def test_uuid4_validator():
    value = 'e2ac107e6f5c4982be4a56cdcaa8a717'
    assert validators.uuid4(value) == value


def test_uuid4_validator_fails():
    value = '89eb35868a8247a4c911758a62601cf7'
    with pytest.raises(exceptions.ValidationError) as excinfo:
        validators.uuid4(value)
    assert value in six.text_type(excinfo.value)
