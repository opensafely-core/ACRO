"""This module contains unit tests."""

import os

import pandas as pd

from acro import ACRO


def test_crosstab_threshold():
    """Crosstab threshold test."""
    # instantiate ACRO
    acro = ACRO()
    # load test data
    path = os.path.join("data", "test_data.dta")
    data = pd.read_stata(path)
    # ACRO crosstab
    _ = acro.crosstab(data.year, data.grant_type)
    # finalise
    output: dict = acro.finalise()
    correct_output: str = (
        '{"G":{"2010":"ok","2011":"ok","2012":"ok",'
        '"2013":"ok","2014":"ok","2015":"ok"},"N":{"2010":"ok","2011":"ok",'
        '"2012":"ok","2013":"ok","2014":"ok","2015":"ok"},"R":{"2010":"ok",'
        '"2011":"ok","2012":"ok","2013":"ok","2014":"ok","2015":"ok"},'
        '"R\\/G":{"2010":"threshold; ","2011":"threshold; ","2012":"threshold; ",'
        '"2013":"threshold; ","2014":"threshold; ","2015":"threshold; "}}'
    )
    correct_summary: str = "fail; threshold: 6 cells suppressed; "
    assert output["output_0"]["outcome"] == correct_output
    assert output["output_0"]["summary"] == correct_summary


def test_crosstab_multiple():
    """Crosstab multiple rule test."""
    # instantiate ACRO
    acro = ACRO()
    # load test data
    path = os.path.join("data", "test_data.dta")
    data = pd.read_stata(path)
    # ACRO crosstab
    _ = acro.crosstab(
        data.year, data.grant_type, values=data.inc_grants, aggfunc="mean"
    )
    # finalise
    output: dict = acro.finalise()
    correct_output: str = (
        '{"G":{"2010":"ok","2011":"ok","2012":"ok","2013":"ok","2014":"ok",'
        '"2015":"ok"},"N":{"2010":"ok","2011":"ok","2012":"ok","2013":"ok",'
        '"2014":"ok","2015":"ok"},"R":{"2010":"ok","2011":"ok","2012":"ok",'
        r'"2013":"ok","2014":"ok","2015":"ok"},"R\/G":{"2010":"threshold; '
        'p-ratio; nk-rule; ","2011":"threshold; ","2012":"threshold; ",'
        '"2013":"threshold; ","2014":"threshold; ","2015":"threshold; "}}'
    )
    correct_summary: str = (
        "fail; threshold: 6 cells suppressed; p-ratio: 1 cells suppressed; "
        "nk-rule: 1 cells suppressed; "
    )
    assert output["output_0"]["outcome"] == correct_output
    assert output["output_0"]["summary"] == correct_summary


def test_pivot_table_pass():
    """Pivot table pass test."""
    # instantiate ACRO
    acro = ACRO()
    # load test data
    path = os.path.join("data", "test_data.dta")
    data = pd.read_stata(path)
    _ = acro.pivot_table(
        data, index=["grant_type"], values=["inc_grants"], aggfunc=["mean", "std"]
    )
    # finalise
    output: dict = acro.finalise()
    correct_output: str = (
        '{"(\'mean\', \'inc_grants\')":{"G":"ok","N":"ok","R":"ok","R\\/G":"ok"},'
        '"(\'std\', \'inc_grants\')":{"G":"ok","N":"ok","R":"ok","R\\/G":"ok"}}'
    )
    correct_summary: str = "pass"
    assert output["output_0"]["outcome"] == correct_output
    assert output["output_0"]["summary"] == correct_summary
