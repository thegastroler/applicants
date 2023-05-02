import os

import pdfplumber
import requests
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from infrastructure.sql.models import Applicants


class Agtu:
    @inject
    async def worker(self, use_case: ApplicantsRepository = Depends(Provide[SqlaRepositoriesContainer.applicants_repository])) -> None:
        items = []
        with pdfplumber.open("pdf/paid.pdf") as f:
            pages = f.pages
            code = None
            for i in pages:
                find_code = [k["text"] for k in i.extract_text_lines() if "УГС/Направление подготовки/специальность" in k["text"]]
                if find_code:
                    code = find_code[0].replace("УГС/Направление подготовки/специальность - ", "")
                table = i.extract_table()
                if table:
                    for row in table:
                        if not row[0] or not row[0].isdigit():
                            continue
                        items.append(
                            Applicants(
                                code=code,
                                position=int(row[0]),
                                snils=row[1].replace("\n", " "),
                                score=int(row[2]) if row[2] else None,
                                origin=True if row[10] else False,
                                university='АГТУ'
                            )
                        )
        if items:
            await use_case.upload(items)
