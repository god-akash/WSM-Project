import os


def load_documents(folder_path):
    documents = {}

    for filename in os.listdir(folder_path):

        if filename.lower().endswith(".txt"):

            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            documents[filename] = content

    return documents