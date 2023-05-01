import os

import pandas as pd
import requests
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from infrastructure.sql.models import Applicants
import pdfplumber

class Mggeu:
    URL = [
        "https://mggeu.ru/wp-content/uploads/2022/08/Konkursnye-spiski-B-04.08.2022-22-15.pdf",
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
                                    code=row[2].replace('\n', ' '),
                                    position=int(row[0]),
                                    snils=row[1],
                                    score=int(row[13]) if row[13] else None,
                                    origin=True if row[17] else False,
                                    university='МГГЭУ'
                                )
                            )
                if items:
                    await use_case.upload(items)
                os.unlink("/tmp/metadata.pdf")







                # table = 1
                # # table = tabula.read_pdf("/tmp/metadata.pdf", pages="all", multiple_tables=False, lattice=True,)[0]
                # table = table.where(pd.notnull(table), None)
                # columns = table.columns.values
                # columns[2] = "Направление\специальность"
                # columns[13] = "Сумма баллов"
                # table.columns = columns
                # items = []
                # for i in range(len(table)):
                #     if i == 1938 or table.iloc[i]["No"] == "No":
                #         continue
                #     table.iloc[i] = table.iloc[i].replace('\r', ' ', regex=True)
                #     row = table.iloc[i]
                #     items.append(
                #         Applicants(
                #             code=row["Направление\специальность"],
                #             position=int(row["No"]),
                #             snils=row["Уникальный код"],
                #             score=int(row["Сумма баллов"]) if row["Сумма баллов"] else None,
                #             origin=True if row["Оригинал"] else False,
                #             university='МГГЭУ'
                #         )
                #     )
                # if items:
                #     await use_case.upload(items)
                # os.unlink("/tmp/metadata.pdf")
