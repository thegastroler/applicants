import requests
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from bs4 import BeautifulSoup
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from infrastructure.sql.models import Applicants


class Ugtu:
    URL = ["https://www.ugtu.net/vysshee-obrazovanie-zaochnaya-forma-obucheniya-dogovornaya-osnova",]
    YES_NO = {"Да": True, "Нет": False}

    @inject
    async def worker(self, use_case: ApplicantsRepository = Depends(Provide[SqlaRepositoriesContainer.applicants_repository])) -> None:
        for url in self.URL:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                text = response.text
                soup = BeautifulSoup(text, 'html.parser')
                table = soup.find("table", {"class": "tab1"})
                specs = table.find_all("span", {"class": "t2"})
                specs = [i.text for i in specs]
                rows = []
                for i in range(1, len(specs) + 1):
                    rows.append(table.find_all("tr", {"bl": f"{i}"}))
                rows = [[[k.text for k in f.find_all("td")] for f in i] for i in rows]
                indexes = [0, 1, 3, 7]
                rows = [[[f[k] for k in indexes] for f in i] for i in rows]
                items = [
                    Applicants(
                        code=specs[idx],
                        position=int(i[0].replace(".", "")),
                        snils=i[1],
                        score=int(i[2]) if i[2] else None,
                        origin=self.YES_NO[i[3]],
                        university='УГТУ'
                    )
                    for idx, k in enumerate(rows) for i in k
                ]
                if items:
                    await use_case.upload(items)
