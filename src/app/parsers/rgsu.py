import requests
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from bs4 import BeautifulSoup
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from infrastructure.sql.models import Applicant
from loguru import logger


class Rgsu:
    YES_NO = {'Нет': False, 'Да': True}
    URL = [
        ["https://rgsu.net/abitur/spiski/konkursnye-spiski-aspirantura/?form=Очная&dir=Безопасность+труда+%28аспирантура%29&kvote=на+общих+основаниях&place=", "Безопасность труда (аспирантура)"],
        ["https://rgsu.net/abitur/spiski/konkursnye-spiski-aspirantura/?form=Очная&dir=Математическое+и+программное+обеспечение+вычислительных+систем%2C+комплексов+и+компьютерных+сетей+%28аспирантура%29&kvote=на+общих+основаниях&place=", "Математическое и программное обеспечение вычислительных систем, комплексов и компьютерных сетей (аспирантура)"],
        ["https://rgsu.net/abitur/spiski/konkursnye-spiski-aspirantura/?form=Очная&dir=Методология+и+технология+профессионального+образования+%28аспирантура%29&kvote=на+общих+основаниях&place=", "Методология и технология профессионального образования (аспирантура)"],
        ["https://rgsu.net/abitur/spiski/konkursnye-spiski-aspirantura/?form=Очная&dir=Общая+психология%2C+психология+личности%2C+история+психологии+%28аспирантура%29&kvote=на+общих+основаниях&place=", "Общая психология, психология личности, история психологии (аспирантура)"],
        ["https://rgsu.net/abitur/spiski/konkursnye-spiski-aspirantura/?form=Очная&dir=Психология+труда%2C+инженерная+психология%2C+когнитивная+эргономика+%28аспирантура%29&kvote=на+общих+основаниях&place=", "Психология труда, инженерная психология, когнитивная эргономика (аспирантура)"],
        ["https://rgsu.net/abitur/spiski/konkursnye-spiski-aspirantura/?form=Очная&dir=Региональная+и+отраслевая+экономика+%28аспирантура%29&kvote=на+общих+основаниях&place=", "Региональная и отраслевая экономика (аспирантура)"],
        ["https://rgsu.net/abitur/spiski/konkursnye-spiski-aspirantura/?form=Очная&dir=Системный+анализ%2C+управление+и+обработка+информации%2C+статистика+%28аспирантура%29&kvote=на+общих+основаниях&place=", "Системный анализ, управление и обработка информации, статистика (аспирантура)"],
        ["https://rgsu.net/abitur/spiski/konkursnye-spiski-aspirantura/?form=Очная&dir=Социальная+психология%2C+политическая+и+экономическая+психология+%28аспирантура%29&kvote=на+общих+основаниях&place=", "Социальная психология, политическая и экономическая психология (аспирантура)"],
        ["https://rgsu.net/abitur/spiski/konkursnye-spiski-aspirantura/?form=Очная&dir=Социальная+структура%2C+социальные+институты+и+процессы+%28аспирантура%29&kvote=на+общих+основаниях&place=", "Социальная структура, социальные институты и процессы (аспирантура)"],
        ["https://rgsu.net/abitur/spiski/konkursnye-spiski-aspirantura/?form=Очная&dir=Социология+управления+%28аспирантура%29&kvote=на+общих+основаниях&place=", "Социология управления (аспирантура)"],
        ["https://rgsu.net/abitur/spiski/konkursnye-spiski-aspirantura/?form=Очная&dir=Теория+и+история+культуры%2C+искусства+%28аспирантура%29&kvote=на+общих+основаниях&place=", "Теория и история культуры, искусства (аспирантура)"],
        ["https://rgsu.net/abitur/spiski/konkursnye-spiski-aspirantura/?form=Очная&dir=Управление+в+организационных+системах+%28аспирантура%29&kvote=на+общих+основаниях&place=", "Управление в организационных системах (аспирантура)"],
        ["https://rgsu.net/abitur/spiski/konkursnye-spiski-aspirantura/?form=Очная&dir=Частно-правовые+%28цивилистические%29+науки+%28аспирантура%29&kvote=на+общих+основаниях&place=", "Частно-правовые (цивилистические) науки (аспирантура)"],
        ["https://rgsu.net/abitur/spiski/konkursnye-spiski-aspirantura/?form=Очная&dir=Экология+%28аспирантура%29&kvote=на+общих+основаниях&place=", "Экология (аспирантура)"],
    ]
    BUDGET = ['бюджетные', 'внебюджетные']

    @inject
    async def worker(self, use_case: ApplicantsRepository = Depends(Provide[SqlaRepositoriesContainer.applicants_repository])) -> None:
        for _url in self.URL:
            for budget in self.BUDGET:
                try:
                    url = _url[0] + budget
                    response = requests.get(url, stream=True)
                    if response.status_code == 200:
                        text = response.text
                        soup = BeautifulSoup(text, 'html.parser')
                        table = soup.find("div", {"class": "table-wrapper"})
                        body = table.find("tbody")
                        rows = body.find_all("tr")
                        items = [[k.text for k in i.find_all("td")] for i in rows]
                        for i in items:
                            if not len(i) == 7:
                                items.remove(i)
                        indexes = [0, 1, 2, 5]
                        items = [[i[k] for k in indexes] for i in items]
                        for i in items:
                            i[-1] = self.YES_NO[i[-1]]
                        items = [
                            Applicant(
                                code=_url[1],
                                position=int(i[0]),
                                snils=i[1],
                                score=int(i[2]),
                                origin=i[3],
                                university='РГСУ'
                            )
                            for i in items
                        ]
                        if items:
                            await use_case.upload(items)
                except Exception as e:
                    logger.info(e)
