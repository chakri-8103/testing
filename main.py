
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

APIS = [
    {"url": "http://10.70.9.231:4001/admin/vgreport/practicetest", "type": "default"},
    {"url": "http://10.70.9.231:4001/admin/vgreport/grandtest", "type": "default"},
    {"url": "http://10.70.9.231:4001/admin/vgreport/deepdive", "type": "default"},
    {"url": "http://10.70.9.195:3200/schedule/sectionwisereport", "type": "default"},
    {"url": "http://10.70.9.195:3200/schedule/sectionwise_practicereport", "type": "default"},
    {"url": "http://10.70.9.231:6012/lsrw_report/vgreport", "type": "lsrw"}
]

FROM_DATE = "2023-10-01"
TO_DATE = "2026-10-23"
TIMEOUT = 15


def check_suc(suc):
    passed = False

    for api in APIS:

        if api["type"] == "lsrw":
            payload = {
                "fromdate": FROM_DATE,
                "todate": TO_DATE,
                "suc": str(suc)
            }
        else:
            payload = {
                "from_date": FROM_DATE,
                "to_date": TO_DATE,
                "suc": str(suc)
            }

        try:
            response = requests.post(
                api["url"],
                json=payload,
                timeout=TIMEOUT
            )

            if not response.ok:
                continue

            data = response.json()

            if not isinstance(data, dict):
                continue

            result = data.get("result")

            if result is not None and result != []:
                passed = True
                break

        except (requests.RequestException, ValueError):
            continue

    # Display only when ALL APIs fail
    return None if passed else str(suc)


suc_input = input("Enter SUCs: ")

suc_list = list(dict.fromkeys(
    x.strip() for x in suc_input.split(",") if x.strip()
))

failed_sucs = []

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [
        executor.submit(check_suc, suc)
        for suc in suc_list
    ]

    for future in as_completed(futures):
        result = future.result()

        if result:
            failed_sucs.append(result)
print("Failed SUCs:")
print(",".join(failed_sucs))
