import sys
from app.repository import SqlaRepositoriesContainer
from .guz import Guz
from .rgsu import Rgsu
from .rgup import Rgup
from .mgotu import Mgotu
from .spbgtu import Spbgtu
from .pstu import Pstu
from .ugtu import Ugtu
from .omgups import Omgups
from .spbgeu import Spbgeu
from .mggeu import Mggeu
from .lesgaft import Lesgaft
from .ieup import Ieup
from .mhti import Mhti


def init_container():
    container = SqlaRepositoriesContainer()
    container.wire(modules=[sys.modules[__name__]])