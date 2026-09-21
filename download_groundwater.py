import os
import requests


DATA_DIR = "data"

DATASETS = {
    "chennai_groundwater_2024.csv":
        "https://newdata.opencity.in/dataset/8ed6e15c-ea1f-4f41-850a-9c52090f3647/resource/3a41ca9e-dbe1-495a-9ee3-c14aeaa988c6/download/a6f24910-b2cc-40e6-b08e-9dd7c37a1f4f.csv",

    "chennai_groundwater_2023.csv":
        "https://newdata.opencity.in/dataset/8ed6e15c-ea1f-4f41-850a-9c52090f3647/resource/2ccf989b-a340-4c49-8264-80a0b60717aa/download/fb45ece0-04ef-451c-bceb-95138b098c8c.csv",

    "chennai_groundwater_2022.csv":
        "https://newdata.opencity.in/dataset/8ed6e15c-ea1f-4f41-850a-9c52090f3647/resource/0e44c0a9-4965-4385-8988-ff4ed6f7534c/download/853e6067-9b2b-4944-b4cc-ec70777f949b.csv",

    "chennai_groundwater_2021.csv":
        "https://newdata.opencity.in/dataset/8ed6e15c-ea1f-4f41-850a-9c52090f3647/resource/61ef9b4e-feae-4e73-b503-aa2cba9eda50/download/933767dd-306d-41f3-894d-d7f4b5ee27e6.csv"
}


def download_file(filename, url):

    os.makedirs(DATA_DIR, exist_ok=True)

    path = os.path.join(DATA_DIR, filename)

    print("Downloading:", filename)

    response = requests.get(url, timeout=30)

    response.raise_for_status()

    with open(path, "wb") as file:
        file.write(response.content)

    print("Saved:", path)


if __name__ == "__main__":

    for filename, url in DATASETS.items():

        try:
            download_file(filename, url)

        except Exception as error:

            print("Failed:", filename)
            print(error)