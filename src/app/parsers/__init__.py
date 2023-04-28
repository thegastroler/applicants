import sys
from app.repository import SqlaRepositoriesContainer
from .guz import Guz
from .rgsu import Rgsu
from .rgup import Rgup
from .mgotu import Mgotu
from .spbgtu import Spbgtu
from .ptsu import Ptsu
from .ugtu import Ugtu
from .omgups import Omgups


def init_container():
    container = SqlaRepositoriesContainer()
    container.wire(modules=[sys.modules[__name__]])