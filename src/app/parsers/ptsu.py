import requests
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from bs4 import BeautifulSoup
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from infrastructure.sql.models import Applicants


class Ptsu:
    URL = [
        ["https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_НМ_Б_Н_000002824.html", "Конструкционные наноматериалы"],
    ]
    ORIGIN = {'Копия': False, 'Оригинал': True}
    @inject
    async def worker(self, use_case: ApplicantsRepository = Depends(Provide[SqlaRepositoriesContainer.applicants_repository])):
        for url in self.URL:
            response = requests.get(url[0], headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
            if response.status_code == 200:
                text = response.text
                soup = BeautifulSoup(text, 'html.parser')
                rows = soup.find_all("tr")[13:]
                items = [[k.text for k in i.find_all("td")] for i in rows]
                indexes = [0, 1, 3, 8]
                data = [[i[k] for k in indexes] for i in items]
                for i, _ in enumerate(data):
                    data[i][3] = data[i][3].encode('l1').decode()
                items = [
                    Applicants(
                        code=url[1],
                        position=int(i[0]),
                        snils=i[1],
                        score=int(i[2]) if i[2] else None,
                        origin=self.ORIGIN[i[3]],
                        university='СПБГУ'
                    )
                    for i in data
                ]
                if items:
                    await use_case.upload(items)
