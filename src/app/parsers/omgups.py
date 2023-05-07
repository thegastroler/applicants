import requests
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from bs4 import BeautifulSoup
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from infrastructure.sql.models import Applicant


class Omgups:
    URL = [["https://www.omgups.ru/abitur/ks/БС//Заочная_09.03.02%20Информационные%20системы%20и%20технологии%20(Программирвание%20и%20информационные%20технологии)_Бюджетная%20основа.html", "Информационные системы и технологии (Программирвание и информационные технологии)"], ]
    YES_NO = {"Да": True, "Нет": False}

    @inject
    async def worker(self, use_case: ApplicantsRepository = Depends(Provide[SqlaRepositoriesContainer.applicants_repository])) -> None:
        for url in self.URL:
            response = requests.get(url[0], stream=True)
            if response.status_code == 200:
                text = response.text
                soup = BeautifulSoup(text, 'html.parser')
                rows = soup.find_all("tr", {"class": "R0"})[3:]
                rows = [[k.text for k in i.find_all("td")] for i in rows]
                indexes = [0, 1, 3, 12]
                rows = [[i[k] for k in indexes] for i in rows]
                items = [
                    Applicant(
                        code=url[1],
                        position=int(i[0]),
                        snils=i[1],
                        score=int(i[2]) if i[2] else None,
                        origin=True if i[3] else None,
                        university='ОМГУПС'
                    )
                    for i in rows
                ]
                if items:
                    await use_case.upload(items)
