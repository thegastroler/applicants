from app.repository import SqlaRepositoriesContainer


def init_container():
    module = __name__
    container = SqlaRepositoriesContainer()
    container.wire(modules=[module])
