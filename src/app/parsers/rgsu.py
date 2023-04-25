import requests
from bs4 import BeautifulSoup
import asyncio
from fastapi import Depends
from dependency_injector.wiring import Provide
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository

class Rgsu:
    URL = "https://rgsu.net/abitur/spiski/konkursnye-spiski-aspirantura/"
    async def parse_aspirantura(self, use_case: ApplicantsRepository = Depends(Provide[SqlaRepositoriesContainer.applicants_repository])):
        await use_case.execute(12)
        response = requests.get(self.URL, stream=True)
        if response.status_code == 200:
            text = response.text
        else:
            return
        soup = BeautifulSoup(text, 'html.parser')
        form = soup.find("select", {"id": "form"})
        forms = [i.text for i in form.find_all("option") if i.text != "--выбрать--"]
        _dir = soup.find("select", {"id": "dir"})
        dirs = [i.text for i in _dir.find_all("option") if i.text != "--выбрать--"]
        table = soup.find("div", {"class": "table-wrapper"})
        tbody = table.find("tbody")
        applicants = tbody.find_all("tr")
        applicants = [k.split("\n") for k in [i.text for i in applicants]]
        applicants = [print(i[1:-2]) for i in applicants]
        return response
