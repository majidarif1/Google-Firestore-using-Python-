import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests
from bs4 import BeautifulSoup


# Use a service account.
cred = credentials.Certificate('creds.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

url = 'https://www.law.cornell.edu/uscode/text/26'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
ol = soup.find("ol",class_="list-unstyled")
lists = ol.find_all("li",class_="tocitem")

collection_ref = db.collection("title26")
for li in lists:
    doc_ref = collection_ref.document(li.text)
    doc_ref.create({})
    print(li.text)
    subtitles = li.text.split("—")[0]
    subtitle = subtitles.split(' ')
    subtitleText = subtitle[0].lower().replace('[','').replace(']','')
    subtitleAlpha = subtitle[1]

    chapter_url = f"https://www.law.cornell.edu/uscode/text/26/{subtitleText}-{subtitleAlpha}"
    print(chapter_url)
    response = requests.get(chapter_url)
    soup = BeautifulSoup(response.text, "html.parser")
    orderedList = soup.find("ol",class_="list-unstyled")
    lists1 = orderedList.find_all("li",class_="tocitem")
    collection_ref1= doc_ref.collection(li.text)
    for list in lists1:
        doc_ref1=collection_ref1.document(list.text)
        doc_ref1.create({})
        print(list.text)
        subChapters = list.text.split("—")[0]
        subChapter = subChapters.split(' ')
        subChapterText = subChapter[0].lower().replace('[','').replace(']','')
        subChapterAlpha = subChapter[1]
        sub_chapter_url = f"https://www.law.cornell.edu/uscode/text/26/{subtitleText}-{subtitleAlpha}/{subChapterText}-{subChapterAlpha}"
        print(sub_chapter_url)
        response = requests.get(sub_chapter_url)
        soup = BeautifulSoup(response.text, "html.parser")
        orderedList = soup.find("ol",class_="list-unstyled")
        lists1 = orderedList.find_all("li",class_="tocitem")
        collection_ref2= doc_ref1.collection(list.text)
        for subChapList in lists1:
            print(subChapList.text)
            doc_ref2=collection_ref2.document(subChapList.text)
            doc_ref2.create({})