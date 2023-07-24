import firebase_admin
from firebase_admin import credentials, firestore
import requests
from bs4 import BeautifulSoup
import google.api_core.exceptions
import time
import random

# Use a service account.
cred = credentials.Certificate('creds.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

def delete_document_and_subcollections(doc_ref):
    # Delete subcollections recursively
    collections = doc_ref.collections()
    for collection in collections:
        delete_collection(collection)

    # Delete the document itself
    doc_ref.delete()

def delete_collection(collection_ref, batch_size=100):
    query = collection_ref.limit(batch_size)

    while True:
        try:
            docs = query.stream()

            deleted = 0
            for doc in docs:
                delete_document_and_subcollections(doc.reference)
                deleted += 1

            if deleted < batch_size:
                break

        except google.api_core.exceptions.DeadlineExceeded:
            print("Timeout occurred. Retrying after a delay...")
            time.sleep(random.uniform(1, 5))  # Random delay between 1 to 5 seconds
            continue

        except Exception as e:
            print(f"An error occurred: {e}")
            break

def delete_data():
    main_collection_ref = db.collection('title26')
    delete_collection(main_collection_ref)

if __name__ == "__main__":
    cred = credentials.Certificate('creds.json')
    
    # Check if the app is already initialized
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    main_collection_ref = db.collection('title26')

    delete_data()

    url = 'https://www.law.cornell.edu/uscode/text/26'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    ol = soup.find("ol",class_="list-unstyled")
    lists = ol.find_all("li",class_="tocitem")

    #collection_ref = db.collection("title26")
    for li in lists:
        doc_ref = main_collection_ref.document(li.text)
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
            chapters = list.text.split("—")[0]
            chapter = chapters.split(' ')
            chapterText = chapter[0].lower().replace('[','').replace(']','')
            chapterAlpha = chapter[1]
            print(chapterText)
            print(chapterAlpha)

            if not chapterText.startswith("§"):

                sub_chapter_url = f"https://www.law.cornell.edu/uscode/text/26/{subtitleText}-{subtitleAlpha}/{chapterText}-{chapterAlpha}"
                print(sub_chapter_url)
                response = requests.get(sub_chapter_url)
                soup = BeautifulSoup(response.text, "html.parser")
                orderedList = soup.find("ol",class_="list-unstyled")

                if orderedList:

                    lists1 = orderedList.find_all("li",class_="tocitem")
                    collection_ref2= doc_ref1.collection(list.text)

                    for chapList in lists1:
                        print(chapList.text)
                        doc_ref2=collection_ref2.document(chapList.text)
                        doc_ref2.create({})
                        subChapters = chapList.text.split("—")[0]
                        subChapter = subChapters.split(' ')
                        subChapterText = subChapter[0].lower().replace('[','').replace(']','')
                        subChapterAlpha = subChapter[1]

                        if not subChapterText.startswith("§"):
                            subChapter_url = f"https://www.law.cornell.edu/uscode/text/26/{subtitleText}-{subtitleAlpha}/{chapterText}-{chapterAlpha}/{subChapterText}-{subChapterAlpha}"
                            print(subChapter_url)
                            response = requests.get(subChapter_url)
                            soup = BeautifulSoup(response.text, "html.parser")
                            orderedList1 = soup.find("ol",class_="list-unstyled")
                            lists2 = orderedList1.find_all("li",class_="tocitem")
                            collection_ref3= doc_ref2.collection(chapList.text)

                            for subChapList in lists2:
                                print(subChapList.text)
                                doc_ref3=collection_ref3.document(subChapList.text)
                                doc_ref3.create({})

                                parts = subChapList.text.split("—")[0]
                                part = parts.split(' ')
                                partText = part[0].lower().replace('[','').replace(']','')
                                partNum = part[1]

                                if not partText.startswith("§"):
                                    part_url = f"https://www.law.cornell.edu/uscode/text/26/{subtitleText}-{subtitleAlpha}/{chapterText}-{chapterAlpha}/{subChapterText}-{subChapterAlpha}/{partText}-{partNum}"
                                    print(part_url)
                                    response = requests.get(part_url)
                                    soup = BeautifulSoup(response.text, "html.parser")
                                    orderedList2 = soup.find("ol",class_="list-unstyled")
                                    lists3 = orderedList2.find_all("li",class_="tocitem")
                                    collection_ref4= doc_ref3.collection(subChapList.text)

                                    for partList in lists3:
                                        print(partList.text)
                                        doc_ref4=collection_ref4.document(partList.text)
                                        doc_ref4.create({})

                                        subParts = partList.text.split("—")[0]
                                        subPart = subParts.split(' ')
                                        subPartText = subPart[0].lower().replace('[','').replace(']','')
                                        subPartNum = subPart[1]

                                        if not subPartText.startswith("§"):
                                            subPartUrl = f"https://www.law.cornell.edu/uscode/text/26/{subtitleText}-{subtitleAlpha}/{chapterText}-{chapterAlpha}/{subChapterText}-{subChapterAlpha}/{partText}-{partNum}/{subPartText}-{subPartNum}"
                                            print(subPartUrl)
                                            response = requests.get(subPartUrl)
                                            soup = BeautifulSoup(response.text, "html.parser")
                                            orderedList3 = soup.find("ol",class_="list-unstyled")
                                            lists4 = orderedList3.find_all("li",class_="tocitem")
                                            collection_ref5= doc_ref4.collection(partList.text)

                                            for subPartList in lists4:
                                                print(subPartList.text)
                                                doc_ref5=collection_ref5.document(subPartList.text)
                                                doc_ref5.create({})
                                        else:
                                            topic4 = subPartText.split(".")[0].split(" ")[1]
                                            topic_url = f"https://www.law.cornell.edu/uscode/text/26/{topic4}"
                                            response = requests.get(topic_url)
                                            soup = BeautifulSoup(response.text, "html.parser")
                                            topic = soup.find("text")
                                            if not topic:
                                                print(topic)
                                                continue
                                            doc_ref4.set({"Data": topic.text})





                                else:
                                    topic3 = partText.split(".")[0].split(" ")[1]
                                    topic_url = f"https://www.law.cornell.edu/uscode/text/26/{topic3}"
                                    response = requests.get(topic_url)
                                    soup = BeautifulSoup(response.text, "html.parser")
                                    topic = soup.find("text")
                                    if not topic:
                                        print(topic)
                                        continue
                                    doc_ref3.set({"Data": topic.text})



                        else:
                            topic2 = subChapterText.split(".")[0].split(" ")[1]
                            topic_url = f"https://www.law.cornell.edu/uscode/text/26/{topic2}"
                            response = requests.get(topic_url)
                            soup = BeautifulSoup(response.text, "html.parser")
                            topic = soup.find("text")
                            if not topic:
                                print(topic)
                                continue
                            doc_ref2.set({"Data": topic.text})
                else:
                    topic = soup.find("text").text
                    print(topic)
                    collection_ref2= doc_ref1.collection(list.text)
                    doc_ref2=collection_ref2.document(list.text)
                    topic = soup.find("div",class_="text").text
                    doc_ref2.set({"Data":topic })

            else:
                topic1 = chapterText.split(".")[0].split(" ")[1]
                topic_url = f"https://www.law.cornell.edu/uscode/text/26/{topic1}"
                response = requests.get(topic_url)
                soup = BeautifulSoup(response.text, "html.parser")
                topic = soup.find("text")
                if not topic:
                    print(topic)
                    continue
                doc_ref1.set({"Data": topic.text})