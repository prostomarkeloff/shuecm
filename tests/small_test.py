from api import __author__ as aauthor
from api import __version__ as aversion
from db import __author__ as dauthor
from db import __version__ as dversion
from shuecm import __author__ as sauthor
from shuecm import __version__ as sversion


def test_version():
    assert sversion == "0.1.0"
    assert dversion == "0.1.0"
    assert aversion == "0.1.0"


def test_author():
    assert sauthor == "Shue Developers"
    assert dauthor == "Shue Developers"
    assert aauthor == "Shue Developers"
