import os

import pdfplumber
import requests
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from infrastructure.sql.models import Applicant


class Mhti:
    URL = [
        "https://www.muctr.ru/upload/iblock/5ae/en1sb1c15sjs2dz6mb6bqhc2fjarztc1.pdf",
    ]
    @inject
    async def worker(self, use_case: ApplicantsRepository = Depends(Provide[SqlaRepositoriesContainer.applicants_repository])) -> None:
        for url in self.URL:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
            if response.status_code == 200:
                content = response.content
                with open("/tmp/metadata.pdf", "wb") as f:
                    f.write(content)
                items = []
                with pdfplumber.open("/tmp/metadata.pdf", ) as f:
                    for i in f.pages:
                        table = i.extract_table()
                        if table:
                            for row in table:
                                if not row[0].isdigit():
                                    continue
                                items.append(
                                    Applicant(
                                        code="Химическая технология",
                                        position=int(row[0]),
                                        snils=row[2],
                                        score=int(row[8]) if row[8] else None,
                                        origin=True if row[10] == "Оригинал" else False if row[10] == "Копия" else None,
                                        university='МХТИ'
                                    )
                                )
                if items:
                    await use_case.upload(items)
                os.unlink("/tmp/metadata.pdf")
