from app.repository import SqlaRepositoriesContainer
from .guz import Guz
from .rgsu import Rgsu
from .rgup import Rgup
from .mgotu import Mgotu
from .spbgtu import Spbgtu
from .ptsu import Ptsu


def init_container():
    module = __name__
    container = SqlaRepositoriesContainer()
    container.wire(modules=[module])