import requests
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from bs4 import BeautifulSoup
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from infrastructure.sql.models import Applicants


class Spbgu:
    URL = [
        ["https://technolog.edu.ru/content/clists/04.03.01_Химия_Очная_Бюджет", "Химия"],
    ]

    @inject
    async def worker(self, use_case: ApplicantsRepository = Depends(Provide[SqlaRepositoriesContainer.applicants_repository])) -> None:
        for url in self.URL:
            response = requests.get(url[0], stream=True)
            if response.status_code == 200:
                text = response.text
                soup = BeautifulSoup(text, 'html.parser')
                table = soup.find("table", {"class": "sticky-headers"})
                rows = table.find_all("tr")[1:]
                items = [[k.text for k in i.find_all("td")] for i in rows]
                indexes = [0, 2]
                data = [[i[k] for k in indexes] for i in items]
                for idx, _ in enumerate(data):
                    data[idx] = [idx + 1] + data[idx]
                items = [
                    Applicants(
                        code=url[1],
                        position=int(i[0]),
                        snils=i[1],
                        score=int(i[2]) if i[2] else None,
                        origin=None,
                        university='СПБГУ'
                    )
                    for i in data
                ]
                if items:
                    await use_case.upload(items)
