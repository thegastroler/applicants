import asyncio
import sys
from app.repository import SqlaRepositoriesContainer
from app import parsers
import uvicorn

if __name__ == "__main__":
    # container = SqlaRepositoriesContainer()
    # container.wire(modules=[sys.modules[__name__]])
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    parsers.init_container()
    asyncio.run(parsers.Mggeu().worker())
    # table = tabula.read_pdf("/tmp/metadata.pdf", pages="all", multiple_tables=False, lattice=True,)[0]
    # columns = table.columns.values
    # columns[2] = 'Направление\специальность'
    # table.columns = columns
    # for i in range(len(table)):
    #     table.iloc[i] = table.iloc[i].replace('\r', ' ', regex=True)



