import requests
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from bs4 import BeautifulSoup
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from infrastructure.sql.models import Applicants


class Mgotu:
    YES_NO = {'Нет': False, 'Да': True}
    URL = [
        "https://ies.unitech-mo.ru/list_rating_admission?page={}&t=1&addition=0",
    ]

    @inject
    async def worker(self):
        for url in self.URL:
            response = requests.get(url.format(1), stream=True)
            if response.status_code == 200:
                text = response.text
                soup = BeautifulSoup(text, 'html.parser')
                pages = soup.find("a", text="⟫", href=True)
                table = soup.find("table", {"class": "admission_rating_table"})
                await self.get_data(table)
                if pages:
                    href = pages["href"]
                    pages = int(href[href.index("?page=")+len("?page="):href.index("&t=1&addition=0")])
                else:
                    break
                # for page in range(2, 10):
                for page in range(2, pages+1):
                    response = requests.get(url.format(page), stream=True)
                    if response.status_code == 200:
                        text = response.text
                        soup = BeautifulSoup(text, 'html.parser')
                        table = soup.find("table", {"class": "admission_rating_table"})
                        await self.get_data(table)

    async def get_data(self, table, use_case: ApplicantsRepository = Depends(Provide[SqlaRepositoriesContainer.applicants_repository])):
        rows = table.find_all("tr")[3:]
        data = [[k.text for k in i.find_all("td")] for i in rows]
        data = [i for i in data if len(i) > 5]
        indexes = [2, 4, 5, 9, 11]
        data = [[i[k] for k in indexes] for i in data]
        items = [
            Applicants(
                code=i[0],
                position=int(i[2]),
                snils=i[1],
                score=int(i[4]) if i[4] else None,
                origin=True if i[3] == "Диплом" else False,
                university='МГТОУ'
            )
            for i in data
        ]
        if items:
            await use_case.upload(items)
