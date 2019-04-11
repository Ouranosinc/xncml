import os
from collections import OrderedDict

import pytest

import xncml

here = os.path.abspath(os.path.dirname(__file__))
input_file = os.path.join(here, 'exercise1.ncml')


def test_ncml_reader_constructor():
    nc = xncml.NcmlReader(input_file)
    expected = OrderedDict(
        [
            ('@name', 'T'),
            ('@shape', 'time lat lon'),
            ('@type', 'double'),
            (
                'attribute',
                [
                    OrderedDict(
                        [
                            ('@name', 'long_name'),
                            ('@type', 'String'),
                            ('@value', 'surface temperature'),
                        ]
                    ),
                    OrderedDict([('@name', 'units'), ('@type', 'String'), ('@value', 'C')]),
                ],
            ),
        ]
    )
    res = nc.ncroot['netcdf']['variable'][1]
    assert res == expected


def test_add_variable_attribute():
    nc = xncml.NcmlReader(input_file)
    nc.add_variable_attribute(variable='T', key='container', value='ndarray')
    expected = OrderedDict(
        [
            ('@name', 'T'),
            ('@shape', 'time lat lon'),
            ('@type', 'double'),
            (
                'attribute',
                [
                    OrderedDict(
                        [
                            ('@name', 'long_name'),
                            ('@type', 'String'),
                            ('@value', 'surface temperature'),
                        ]
                    ),
                    OrderedDict([('@name', 'units'), ('@type', 'String'), ('@value', 'C')]),
                    OrderedDict(
                        [('@name', 'container'), ('@type', 'String'), ('@value', 'ndarray')]
                    ),
                ],
            ),
        ]
    )

    res = nc.ncroot['netcdf']['variable'][1]
    assert res == expected


def test_remove_variable_attribute():
    nc = xncml.NcmlReader(input_file)
    nc.remove_variable_attribute(variable='T', key='units')
    expected = OrderedDict(
        [
            ('@name', 'T'),
            ('@shape', 'time lat lon'),
            ('@type', 'double'),
            (
                'attribute',
                [
                    OrderedDict(
                        [
                            ('@name', 'long_name'),
                            ('@type', 'String'),
                            ('@value', 'surface temperature'),
                        ]
                    )
                ],
            ),
        ]
    )
    res = nc.ncroot['netcdf']['variable'][1]
    assert res == expected


def test_add_dataset_attribute():
    nc = xncml.NcmlReader(input_file)
    nc.add_dataset_attribute(key='editedby', value='foo')
    expected = [
        OrderedDict([('@name', 'title'), ('@type', 'String'), ('@value', 'Example Data')]),
        OrderedDict([('@name', 'editedby'), ('@type', 'String'), ('@value', 'foo')]),
    ]

    res = nc.ncroot['netcdf']['attribute']
    assert res == expected
