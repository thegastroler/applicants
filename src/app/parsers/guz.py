import requests
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from bs4 import BeautifulSoup
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from infrastructure.sql.models import Applicant


class Guz:
    URL = "https://www.guz.ru/applicants/priemnaya-kampaniya-2022-2023/enrollees/view_ratings.php?levelTraining="

    @inject
    async def worker(self, use_case: ApplicantsRepository = Depends(Provide[SqlaRepositoriesContainer.applicants_repository])) -> None:
        response = requests.get(self.URL, stream=True, timeout=10)
        if response.status_code == 200:
            text = response.content
            soup = BeautifulSoup(text, 'html.parser')
            table = soup.find("div", {"class": "data_table"})
            specs = table.find_all("h2", {"class": "spec"})
            items = table.find_all("tbody")
            specs = [i.text for i in specs]
            items = [i.find_all("tr") for i in items]
            items = [[[f.text for f in k.find_all("td")] for k in i] for i in items]
            indexes = [0, 1, 3, 4]
            items = [[[k[f] for f in indexes] for k in i] for i in items]
            for i in items:
                for k in i:
                    k[2] = False if k[2] == "-" else True
            items = [
                Applicant(
                    code=specs[idx],
                    position=int(i[0]),
                    snils=i[1],
                    score=int(float(i[3])) if i[3] else None,
                    origin=i[2],
                    university='ГУЗ'
                )
                for idx, val in enumerate(items) for i in val
            ]
            if items:
                for i in range(0, len(items), 500):
                    await use_case.upload(items[i:i+500])
