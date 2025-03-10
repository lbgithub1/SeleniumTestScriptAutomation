import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import load_dotenv
import os
from bs4 import Comment
import tiktoken
from IMPORTANTSeleniumTesting5AnmeldungWiWa import anmeldungWiWa
from Prepocessor_2 import deleteEmptyTables, compactHtml, deleteEmptyTables2


# Alternativ:
# with open("TestingPageEcoForest.html", "r", encoding="utf-8") as file:
#     html_content = file.read()


def htmlPreprocesser(url, outputFile):
    # Basic connections
    # anmeldungWiWa()
    print("AnmeldungWiWa finnished")
    time.sleep(1)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(4)
    html = driver.page_source
    # print(html)
    driver.quit()

    # <meta>-Tag finden für description und Title -> Kontext für LLM
    soup = BeautifulSoup(html, 'html.parser')
    description_content = "Keine Beschreibung gefunden."
    meta_description = soup.find("meta", {"name": "description"})
    if meta_description and "content" in meta_description.attrs:
        description_content = meta_description["content"]
    print(f"Beschreibung: {description_content}")

    # Titel-Meta-Tag finden
    title_content = "Kein Titel gefunden."
    meta_title = soup.find("meta", {"name": re.compile(r"title$", re.IGNORECASE)})
    if meta_title and "content" in meta_title.attrs:
        title_content = meta_title["content"]
    print(f"Titel: {title_content}")

    tags_to_remove = {
        "head", "script", "link",
        "style", "footer", "rect",
        "stop", "lineargradient", "radialgradient",
        "rect", "circle", "path", "clippath",
        "svg", "defs", "use", "meta",
        "circle", "strong", "br", "pre",
        "dd", "dt", "dl", "dfn", "var"
    }
    # style, i, span

    for element in soup.find_all(True):  # find_all(True) findet alle Tags
        if element.name in tags_to_remove:
            element.decompose()

    # Kommentare entfernen
    comments = soup.find_all(string=Comment)
    for comment in comments:
        comment.extract()

    # Titel und Beschreibung am Anfang des HTML-Dokuments hinzufügen -> Für Kontext LLM
    soup.insert(0, BeautifulSoup(f"<p>{title_content}</p>", "html.parser"))
    soup.insert(1, BeautifulSoup(f"<p>{description_content}</p>", "html.parser"))

    soup = deleteEmptyTables(soup, outputFile)

    # HTML in Datei speichern
    with open(outputFile, "w", encoding="utf-8") as file:
        file.write(str(soup))
    # print(soup.prettify().strip())
    # print(soup)
    return str(soup)


def htmlPreprocesser2(xy, outputFile):
    html = xy

    # <meta>-Tag finden für description und Title -> Kontext für LLM
    soup = BeautifulSoup(html, 'html.parser')
    description_content = "Keine Beschreibung gefunden."
    meta_description = soup.find("meta", {"name": "description"})
    if meta_description and "content" in meta_description.attrs:
        description_content = meta_description["content"]
    print(f"Beschreibung: {description_content}")

    # Titel-Meta-Tag finden
    title_content = "Kein Titel gefunden."
    meta_title = soup.find("meta", {"name": re.compile(r"title$", re.IGNORECASE)})
    if meta_title and "content" in meta_title.attrs:
        title_content = meta_title["content"]
    print(f"Titel: {title_content}")

    extractedHtmlFromScripts = []
    for script in soup.find_all("script"):
        scriptContent = script.string
        if scriptContent:
            html_matches = re.findall(r"(['\"])(<.*?>)\1", scriptContent, re.DOTALL)
            for match in html_matches:
                extractedHtmlFromScripts.append(match[1])  # HTML-Code speichern

    for script in soup.find_all("script"):
        script.decompose()

    if extractedHtmlFromScripts:
        extracted_html_string = "\n".join(extractedHtmlFromScripts)
        soup.append(BeautifulSoup(f"<div id='extracted-script-html'>{extracted_html_string}</div>", "html.parser"))

    tags_to_remove = {
        "head", "script", "link",
        "style", "footer", "rect",
        "stop", "lineargradient", "radialgradient",
        "rect", "circle", "path", "clippath",
        "svg", "defs", "use", "meta",
        "circle", "strong", "br", "pre",
        "dd", "dt", "dl", "dfn", "var"
    }
    # style, i, span

    for element in soup.find_all(True):  # find_all(True) findet alle Tags
        if element.name in tags_to_remove:
            element.decompose()

    # Kommentare entfernen
    comments = soup.find_all(string=Comment)
    for comment in comments:
        comment.extract()

    # Titel und Beschreibung am Anfang des HTML-Dokuments hinzufügen -> Für Kontext LLM
    soup.insert(0, BeautifulSoup(f"<p>{title_content}</p>", "html.parser"))
    soup.insert(1, BeautifulSoup(f"<p>{description_content}</p>", "html.parser"))

    # for script in retained_scripts:
    #     new_script = soup.new_tag("script")
    #     new_script.string = script["content"]  # Füge den ursprünglichen Inhalt hinzu
    #     soup.body.append(new_script)

    soup = deleteEmptyTables(soup, outputFile)

    with open(outputFile, "w", encoding="utf-8") as file:
        file.write(str(soup))

    print(soup)
    # print(soup)
    # print(retained_scripts)
    return str(soup)


def htmlPreprocesser2Multiplepages(page1, page2, outputFile):
    helperStr = ""
    listOfPages = [page1, page2]
    for x in range(len(listOfPages)):
        # <meta>-Tag finden für description und Title -> Kontext für LLM
        soup = BeautifulSoup(listOfPages[x], 'html.parser')
        print(soup.prettify())
        description_content = "Keine Beschreibung gefunden."
        meta_description = soup.find("meta", {"name": "description"})
        if meta_description and "content" in meta_description.attrs:
            description_content = meta_description["content"]
        print(f"Beschreibung: {description_content}")

        # Titel-Meta-Tag finden
        title_content = "Kein Titel gefunden."
        meta_title = soup.find("meta", {"name": re.compile(r"title$", re.IGNORECASE)})
        if meta_title and "content" in meta_title.attrs:
            title_content = meta_title["content"]
        print(f"Titel: {title_content}")

        extractedHtmlFromScripts = []
        for script in soup.find_all("script"):
            scriptContent = script.string
            if scriptContent:
                html_matches = re.findall(r"(['\"])(<.*?>)\1", scriptContent, re.DOTALL)
                for match in html_matches:
                    extractedHtmlFromScripts.append(match[1])  # HTML-Code speichern

        for script in soup.find_all("script"):
            script.decompose()

        if extractedHtmlFromScripts:
            extracted_html_string = "\n".join(extractedHtmlFromScripts)
            soup.append(BeautifulSoup(f"<div id='extracted-script-html'>{extracted_html_string}</div>", "html.parser"))

        tags_to_remove = {
            "head", "script", "link",
            "style", "footer", "rect",
            "stop", "lineargradient", "radialgradient",
            "rect", "circle", "path", "clippath",
            "svg", "defs", "use", "meta",
            "circle", "strong", "br", "pre",
            "dd", "dt", "dl", "dfn", "var"
        }

        for element in soup.find_all(True):  # find_all(True) findet alle Tags
            if element.name in tags_to_remove:
                element.decompose()

        # Kommentare entfernen
        comments = soup.find_all(string=Comment)
        for comment in comments:
            comment.extract()

        # Titel und Beschreibung am Anfang des HTML-Dokuments hinzufügen -> Für Kontext LLM
        soup.insert(0, BeautifulSoup(f"<p>{title_content}</p>", "html.parser"))
        soup.insert(1, BeautifulSoup(f"<p>{description_content}</p>", "html.parser"))

        # for script in retained_scripts:
        #     new_script = soup.new_tag("script")
        #     new_script.string = script["content"]  # Füge den ursprünglichen Inhalt hinzu
        #     soup.body.append(new_script)

        soup = deleteEmptyTables(soup, outputFile)

        if x == 0:
            helperStr += "<h1>FIRST WEBPAGE:</h1>"
            helperStr += str(soup)
        else:
            helperStr += "<h1>SECOND WEBPAGE:</h1>"
            helperStr += str(soup)

    with open(outputFile, "w", encoding="utf-8") as file:
        file.write(helperStr)
    print(helperStr)
    return str(helperStr)


def htmlPreprocesser2Keywords(xy, outputFile, keywordList: list):
    # Basic connections
    # anmeldungWiWa()
    # print("AnmeldungWiWa finnished")
    # time.sleep(1)
    # options = webdriver.ChromeOptions()
    # driver = webdriver.Chrome(options=options)
    # driver.get(url)
    # time.sleep(4)
    # html = driver.page_source
    html = xy
    # print(html)
    # driver.quit()

    # <meta>-Tag finden für description und Title -> Kontext für LLM
    soup1 = BeautifulSoup(html, 'html.parser')
    soup2 = BeautifulSoup(html, 'html.parser')
    description_content = "Keine Beschreibung gefunden."
    meta_description = soup1.find("meta", {"name": "description"})
    if meta_description and "content" in meta_description.attrs:
        description_content = meta_description["content"]
    print(f"Beschreibung: {description_content}")

    # Titel-Meta-Tag finden
    title_content = "Kein Titel gefunden."
    meta_title = soup1.find("meta", {"name": re.compile(r"title$", re.IGNORECASE)})
    if meta_title and "content" in meta_title.attrs:
        title_content = meta_title["content"]
    print(f"Titel: {title_content}")

    tags_to_remove = {
        "head", "script", "link",
        "style", "footer", "rect",
        "stop", "lineargradient", "radialgradient",
        "rect", "circle", "path", "clippath",
        "svg", "defs", "use", "meta",
        "circle", "strong", "br", "pre",
        "dd", "dt", "dl", "dfn", "var"
    }
    # style, i, span

    for element in soup1.find_all(True):  # find_all(True) findet alle Tags
        if element.name in tags_to_remove:
            element.decompose()

    # Kommentare entfernen
    comments = soup1.find_all(string=Comment)
    for comment in comments:
        comment.extract()

    # Titel und Beschreibung am Anfang des HTML-Dokuments hinzufügen -> Für Kontext LLM
    soup1.insert(0, BeautifulSoup(f"<p>{title_content}</p>", "html.parser"))
    soup1.insert(1, BeautifulSoup(f"<p>{description_content}</p>", "html.parser"))

    # Hier den Code erweitern um eine For-Schleife
    tags_to_remove2 = {
        "head", "script"
    }

    # Entfernung der Tags aus tags_to_remove2
    for element in soup2.find_all(True):  # find_all(True) findet alle Tags
        if element.name in tags_to_remove2:
            print(f"Entferne das folgende Tag hier: {element}")
            element.decompose()

    # keywords look-Up -> in soup2, und gleichzeitig schauen, dass die Elemente unique sind
    for keyword in keywordList:
        # Suche nach Tags, die das Schlüsselwort enthalten
        matching_tags = soup2.find_all(string=lambda text: text and keyword in text)

        for tag in matching_tags:
            # Hole den übergeordneten Tag (Eltern-Tag), um das vollständige Element zu erhalten
            parent_tag = tag.find_parent()

            if parent_tag and parent_tag not in soup1:
                print(f"Füge hinzu: {parent_tag}")
                soup1.append(parent_tag)  # Füge das Tag zu soup1 hinzu

    # HTML in Datei speichern
    with open(outputFile, "w", encoding="utf-8") as file:
        file.write(str(soup1))

    print(soup1.prettify().strip())
    return str(soup1)


# Übersicht über alle vorhandenen Tags einer Webseite generieren
def extract_tags_from_html(file_name):
    try:
        # Öffnen und Lesen der HTML-Datei
        with open(file_name, "r", encoding="utf-8") as file:
            html_content = file.read()

        # HTML-Inhalt analysieren
        soup = BeautifulSoup(html_content, "html.parser")

        # Alle einzigartigen Tags finden
        tags = set([tag.name for tag in soup.find_all(True)])  # Alle Tags extrahieren und in ein Set speichern

        # Ausgabe der verschiedenen Tags
        print("Gefundene Tags in der HTML-Datei:")
        for tag in tags:
            print(tag)

    except FileNotFoundError:
        print(f"Die Datei '{file_name}' wurde nicht gefunden.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


def tokenCounter(input):
    encoding = tiktoken.encoding_for_model("gpt-4o")
    # Überprüfung Datei oder String
    try:
        if os.path.isfile(input):
            with open(input, "r", encoding="utf-8") as file:
                inputText = file.read()
        else:
            inputText = input
        # tokens = encoding.encode(inputText) -> Encoding und Decoding
        # decodedText = encoding.decode(tokens)
        numTokens = len(encoding.encode(inputText))
        print(numTokens)
        return numTokens
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return 0


# 1. Methode und danach dann GPT zur Verfügung stellen
def contextChunking(text, max_tokens=6140):
    encoder = tiktoken.encoding_for_model("gpt-4o")
    # ALT: o200k_base
    tokens = encoder.encode(text)

    chunks = []
    token_counts = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = encoder.decode(chunk_tokens)
        chunks.append(chunk_text)
        token_counts.append(len(chunk_tokens))
    print(f"Gesamtzahl der Tokens: {sum(token_counts)}")
    print("Total Chunks:", len(chunks))
    # for idx, (chunk, count) in enumerate(zip(chunks, token_counts)):
    #     print(f"Chunk {idx + 1}: {count} Tokens")

    return chunks


def contextChunkingDS(text, max_tokens=36840):
    encoder = tiktoken.encoding_for_model("gpt-4o")
    tokens = encoder.encode(text)
    # print(tokens)
    chunks = [encoder.decode(tokens[i:i + max_tokens]) for i in range(0, len(tokens), max_tokens)]
    print(chunks)
    print(len(chunks))
    # result = [
    #     text[i: i + max_tokens] for i in range(0, len(text), max_tokens)
    # ]
    # print(result)
    # print(len(result))
    # Obligatorisch
    return chunks

# max_tokens=36840n  18420
def contextChunkingDS02(text, max_tokens=36840, overlap=15):
    encoder = tiktoken.encoding_for_model("gpt-4o")
    # ALT: o200k_base
    tokens = encoder.encode(text)

    chunks = []
    token_counts = []

    i = 0
    while i < len(tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = encoder.decode(chunk_tokens)
        chunks.append(chunk_text)
        token_counts.append(len(chunk_tokens))

        i += max_tokens - overlap
    print(f"Gesamtzahl der Tokens: {sum(token_counts)}")
    print("Total Chunks:", len(chunks))
    # for idx, (chunk, count) in enumerate(zip(chunks, token_counts)):
    #     print(f"Chunk {idx + 1}: {count} Tokens")

    return chunks


if __name__ == "__main__":
    website = "https://eccoforst.de/"
    datei = "CleanedPageEccoForest.html"
    datei5 = "htmlPreprocesser2Pages.html"
    urli51 = "https://wiwa.uni-trier.de"
    urli52 = "https://wiwa.uni-trier.de/index.php/home/loop"
    urli3 = "https://wiwa.uni-trier.de/produkte/produkte"
    keywordList = ["Filter anwenden"]
    # strWebsite = htmlPreprocesser(website, datei)
    # tokenCounter(strWebsite)
    # contextChunking(strWebsite)
    # extract_tags_from_html("TestingPageInteliJ.html")
    # extract_tags_from_html("CleanedWaWi.html")
    # tokenCounter("CleanedPageEccoForest.html")
    # htmlPreprocesser2Keywords(anmeldungWiWa(urli5), datei5, keywordList)
    # htmlPreprocesser2Multiplepages(anmeldungWiWa(urli51), anmeldungWiWa(urli52), datei5)
    hierIstDasHTML = htmlPreprocesser2(anmeldungWiWa(urli3), datei5)
    # htmlPreprocesser2(anmeldungWiWa(urli51), datei5)
    # contextChunkingDS(hierIstDasHTML)
    contextChunkingDS02(hierIstDasHTML)
