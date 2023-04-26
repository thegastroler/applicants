import requests
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from bs4 import BeautifulSoup
from dependency_injector.wiring import Provide
from fastapi import Depends
from infrastructure.sql.models import Applicants


class Rgup:
    URL = [
        ["https://rgup.ru/img/Priemnaya_komissiya/PRIEM%202023/spiski/ranj/bak_spec/Yurisprudentsiya%20(Bakalavr%202%20vysshee%20zaochnaya%20s%20oplatoy)%20(2022%20Zima).html", "Юриспруденция"],
        ["https://rgup.ru/img/Priemnaya_komissiya/PRIEM%202023/spiski/ranj/mag/Ekonomika%20(Magistr%20ochno-zaochnaya%20s%20oplatoy)%20(2022%20Zima).html", "Экономика"],
        ["https://rgup.ru/img/Priemnaya_komissiya/PRIEM%202023/spiski/ranj/mag/Gosudarstvennoe%20i%20munitsipalnoe%20upravlenie%20(Magistr%20ochno-zaochnaya%20s%20oplatoy)%20(2022%20Zima).html", "Государственное и муниципальное управление"],
    ]

    async def worker(self, use_case: ApplicantsRepository = Depends(Provide[SqlaRepositoriesContainer.applicants_repository])):
        for url in self.URL:
            response = requests.get(url[0], stream=True)
            if response.status_code == 200:
                text = response.text
                soup = BeautifulSoup(text, 'html.parser')
                rows = soup.find_all("tr", {"class": "R7"})
                items = [[k.text for k in i.find_all("td")] for i in rows]
                indexes = [0, 1, 2]
                data = [[i[k] for k in indexes] for i in items]
                items = [
                    Applicants(
                        code=url[1],
                        position=int(i[0]),
                        snils=i[1],
                        score=int(i[2]) if i[2] else None,
                        origin=None,
                        university='РГУП'
                    )
                    for i in data
                ]
                if items:
                    await use_case.upload(items)
