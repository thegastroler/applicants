import os

import pandas as pd
import requests
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from infrastructure.sql.models import Applicants
import pdfplumber

class Lesgaft:
    URL = [
        "http://lesgaft.spb.ru/sites/default/files//u91/fk_oo_20.pdf",
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
                        for row in i.extract_table():
                            if row[0] == '№':
                                continue
                            items.append(
                                Applicants(
                                    code=row[3].replace('\n', ' '),
                                    position=int(row[0]),
                                    snils=row[1],
                                    score=int(row[14]) if row[14] else None,
                                    origin=True if row[9] == "да" else False if row[9] == "нет" else None,
                                    university='НГУ им. П. Ф. Лесгафта'
                                )
                            )
                if items:
                    await use_case.upload(items)
                os.unlink("/tmp/metadata.pdf")
