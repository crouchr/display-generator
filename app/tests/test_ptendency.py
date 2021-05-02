import pytest

import ptendency


@pytest.mark.parametrize(
    "pressure_trend, expected_tendency, expected_forecast",
    [
        (2, 'r', 'Fair'),
        (1, 'r', 'Fair'),
        (0.3, 'r', 'Fair'),
        (0.1, 'r', 'Fair'),
        (0.0, 's', 'Settled'),
        (-0.1, 'f', 'Change'),
        (-1.4, 'f', 'Change'),
        (-1.5, 'F', 'F6-7 12h'),
        (-1.6, 'F', 'F6-7 12h'),
        (-1.7, 'F', 'F6-7 12h'),
        (-3.4, 'F', 'F6-7 12h'),
        (-3.5, 'F!', 'F6-8 6h'),
        (-3.6, 'F!', 'F6-8 6h'),
        (-5.9, 'F!', 'F6-8 6h'),
        (-6.0, 'F!!', 'F7-9 3h'),
        (-6.1, 'F!!', 'F7-9 3h'),
    ]
)
def test_tendency(pressure_trend, expected_tendency, expected_forecast):
    tendency, forecast = ptendency.get_tendency(pressure_trend)

    assert tendency == expected_tendency
    assert forecast == expected_forecast



