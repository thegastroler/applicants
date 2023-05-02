import os

import pdfplumber
import requests
from app.repository import SqlaRepositoriesContainer
from app.repository.applicants_repository import ApplicantsRepository
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from infrastructure.sql.models import Applicants


class Spbutuie:
    URL = [
        "https://spbame.ru/abit/SPbUTUiE/Zachislennye/enr__37.03.01_o-GSN-P.pdf",
        "https://spbame.ru/abit/SPbUTUiE/Zachislennye/enr__42.03.01_o-GSN-R.pdf",
        "https://spbame.ru/abit/SPbUTUiE/Zachislennye/enr__42.03.05_o-GSN-MK.pdf",
        "https://spbame.ru/abit/SPbUTUiE/Zachislennye/enr__43.03.01_o-GSN-S.pdf",
        "https://spbame.ru/abit/SPbUTUiE/Zachislennye/enr__43.03.02_o-GSN-T.pdf",
        "https://spbame.ru/abit/SPbUTUiE/Zachislennye/enr__43.03.03_o-GSN-GD.pdf",
        "https://spbame.ru/abit/SPbUTUiE/Zachislennye/enr__44.03.01_o-GSN-PO.pdf",
        "https://spbame.ru/abit/SPbUTUiE/Zachislennye/enr__45.03.02_o-GSN-L.pdf",
        "https://spbame.ru/abit/SPbUTUiE/Zachislennye/enr__09.03.03_o-EMI-PI.pdf",
        "https://spbame.ru/abit/SPbUTUiE/Zachislennye/enr__38.03.02_o-EMI-M.pdf",
        "https://spbame.ru/abit/SPbUTUiE/Zachislennye/enr__38.03.04_o-EMI-G.pdf",
        "https://spbame.ru/abit/SPbUTUiE/Zachislennye/enr__40.03.01_o-YUI-YU.pdf",
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
                    pages = f.pages
                    code = pages[0].extract_text_lines()[1]["text"].split()[1].replace('"', "")
                    for i in pages:
                        table = i.extract_table()
                        if table:
                            for row in table:
                                if not row[0] or not row[0].isdigit():
                                    continue
                                items.append(
                                    Applicants(
                                        code=code,
                                        position=int(row[0]),
                                        snils=row[1],
                                        score=int(row[12]) if row[12] else None,
                                        origin=True,
                                        university='СПбУТУиЭ'
                                    )
                                )
                if items:
                    await use_case.upload(items)
                os.unlink("/tmp/metadata.pdf")
