import requests
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from bs4 import BeautifulSoup
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from infrastructure.sql.models import Applicants


class Spbgeu:
    URL = "https://priem.unecon.ru/stat/stat_konkurs.php?y=2022&filial_kod=1&zayav_type_kod=1&obr_konkurs_kod=0&recomend_type=null&rec_status_kod=all&ob_forma_kod={}&ob_osnova_kod={}&konkurs_grp_kod={}&prior=all&status_kod=all&is_orig_doc=all&has_agreement=all&dogovor=all&show=Показать"
    VALUES = [
        ["1", "1", "4054"], 
        ["1", "1", "4060"], 
        ["1", "1", "4053"], 
        ["1", "1", "4057"], 
        ["1", "1", "4245"], 
        ["1", "1", "4047"], 
        ["1", "1", "4050"], 
        ["1", "1", "4051"], 
        ["1", "1", "4045"], 
        ["1", "1", "4046"], 
        ["1", "1", "4058"], 
        ["1", "1", "4247"], 
        ["1", "1", "4056"], 
        ["1", "1", "4055"], 
        ["1", "1", "4059"], 
        ["1", "1", "4048"], 
        ["1", "1", "4052"], 
        ["1", "1", "4049"], 
        ["1", "1", "4246"], 
        ["1", "2", "4097"], 
        ["1", "2", "4077"], 
        ["1", "2", "4099"], 
        ["1", "2", "4257"], 
        ["1", "2", "4085"], 
        ["1", "2", "4284"], 
        ["1", "2", "4062"], 
        ["1", "2", "4067"], 
        ["1", "2", "4256"], 
        ["1", "2", "4254"], 
        ["1", "2", "4255"], 
        ["1", "2", "4087"], 
        ["1", "2", "4277"], 
        ["1", "2", "4105"], 
        ["1", "2", "4103"], 
        ["1", "2", "4061"], 
        ["1", "2", "4063"], 
        ["1", "2", "4083"], 
        ["1", "2", "4081"], 
        ["3", "1", "4258"], 
        ["3", "2", "4075"], 
        ["3", "2", "4073"], 
        ["2", "1", "4259"], 
        ["2", "2", "4071"], 
        ["2", "2", "4300"], 
    ]

    @inject
    async def worker(self, use_case: ApplicantsRepository = Depends(Provide[SqlaRepositoriesContainer.applicants_repository])) -> None:
        for i in self.VALUES:
            url = self.URL.format(i[0], i[1], i[2])
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                text = response.text
                soup = BeautifulSoup(text, 'html.parser')
                code = soup.find("div", {"id": "spisok"})
                code = code.find("h2").text if code else None
                table = soup.find_all({"table": "summary"})[-1]
                body = table.find("tbody")
                rows = body.find_all("tr")
                rows = [[k.text for k in i.find_all("td")] for i in rows]
                for i in rows:
                    if len(i) < 15:
                        i.append(i[7])
                indexes = [0, 1, 4, 11]
                data = [[i[k] for k in indexes] for i in rows]
                items = [
                    Applicants(
                        code=code,
                        position=int(i[0]),
                        snils=i[1],
                        score=None if "Без вступительных" in i[2] else int(i[2]) if i[2] else None,
                        origin=True if "Подлинник" in i[3] else False if "Копия" in i[3] else None,
                        university='СПбГЭУ'
                    )
                    for i in data
                ]
                if items:
                    await use_case.upload(items)
