import requests
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from bs4 import BeautifulSoup
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from infrastructure.sql.models import Applicant


class Pstu:
    URL = [
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_ГНФ_НГТ_Б_Н_000002875.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_ГНФ_ПГ_Б_Н_000002843.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_ГНФ_ПГ_Б_Н_000002848.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_ГНФ_Технология%20геологической%20разведки_Б_Н_000002851.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_ГНФ_ФП_Б_Н_000002872.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_БФ_ХТ_Б_Н_000003116.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_БФ_ТМО_Б_Н_000003100.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_БФ_ИВТ_Б_Н_000003094.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_БФ_ЭЭ_Б_Н_000003127.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_ГНФ_ГД_Б_Н_000002860.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_ГНФ_ГД_Б_Н_000002864.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_ГНФ_ГД_Б_Н_000002868.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_ГНФ_ГД_Б_Н_000002855.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_БФ_АТПП_Б_Н_000003108.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_МТМ_Б_Н_000002812.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_НМ_Б_Н_000002824.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_МТМ_Б_Н_000002812.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_МТМ_Б_И_000002814.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_МТМ_К_Н_000002813.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_МТМ_Ц_Н_000003619.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_МТМ_Ц_Н_000002815.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_НМ_Б_Н_000002824.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_НМ_Б_И_000002825.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_НМ_К_Н_000002827.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_ЭМ_Б_Н_000002801.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_ЭМ_Б_И_000002802.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_ЭМ_К_Н_000003487.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_ЭМ_Ц_Н_000003630.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_АРД_Б_Н_000002816.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_АРД_Б_Н_000002820.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_АРД_Б_И_000002817.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_АРД_Б_И_000002821.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_АРД_К_Н_000002819.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_АРД_К_Н_000002823.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_АРД_Ц_Н_000002818.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_АРД_Ц_Н_000003615.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_АРД_Ц_Н_000002822.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_АРД_Ц_Н_000003614.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_ППАМ_Б_Н_000002804.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_ППАМ_Б_И_000002805.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_ППАМ_К_Н_000002807.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_ППАМ_Ц_Н_000002806.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_ППАМ_Ц_Н_000003624.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_ХТЭМ_Б_Н_000002808.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_ХТЭМ_К_Н_000002811.html",
        "https://pstu.ru/files/file/Abitur/2022%20ratio/О_АКФ_ХТЭМ_Ц_Н_000003622.html",
    ]
    ORIGIN = {'Копия': False, 'Оригинал': True}
    @inject
    async def worker(self, use_case: ApplicantsRepository = Depends(Provide[SqlaRepositoriesContainer.applicants_repository])) -> None:
        for url in self.URL:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
            if response.status_code == 200:
                text = response.text
                soup = BeautifulSoup(text, 'html.parser')
                rows = soup.find_all("tr")
                spec = rows[6].find("td").text.encode('l1').decode().replace("Направление подготовки/специальность - ", "")
                rows = rows[13:]
                items = [[k.text for k in i.find_all("td")] for i in rows]
                indexes = [0, 1, 3, 8]
                data = [[i[k] for k in indexes] for i in items]
                for i, _ in enumerate(data):
                    data[i][3] = data[i][3].encode('l1').decode()
                items = [
                    Applicant(
                        code=spec,
                        position=int(i[0]),
                        snils=i[1],
                        score=int(i[2]) if i[2] else None,
                        origin=self.ORIGIN[i[3]],
                        university='ПСТУ'
                    )
                    for i in data
                ]
                if items:
                    await use_case.upload(items)
