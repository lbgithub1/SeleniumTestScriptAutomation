from bs4 import BeautifulSoup


def removeEmptyLists(soup):
    typesToBeRemoved = ["th", "td", "tr", "tbody"]

    for typ in typesToBeRemoved:
        elements = soup.find_all(typ)

        print(typ)
        for element in elements:

            if (element is not None):

                if (element.get("class")):
                    print(element.get("class"))
                if not element.get('class') and not element.get_text(strip=True):
                    # Fehler bei get Class
                    # AttributeError: 'NoneType' object has no attribute 'get'
                    # Checkt aber ob NoneType?
                    # Fehler ist beim tbody an 3 stelle (index 2)
                    # Auf den kann man aber ganz normal zugreifen
                    element.decompose()


with open('CleanedWaWiCopy.html', 'r', encoding='utf-8') as file:
    html_content2 = file.read()


def compactHtml(html_content):
    import re

    compacted_html = re.sub(r">\s+<", "><", html_content)
    compacted_html = compacted_html.strip()

    return compacted_html


def deleteEmptyTables(soup, output_file):
    # soup = BeautifulSoup(soup, 'html.parser')

    preElements = soup.find_all("pre")
    for preElement in preElements:
        if not bool(preElement.attrs) and not bool(preElement.text.strip()) and not bool(preElement.find_all()):
            preElement.decompose()

    tdElements = soup.find_all("td")
    for tdElement in tdElements:
        if not bool(tdElement.attrs) and not bool(tdElement.text.strip()) and not bool(tdElement.find_all()):
            tdElement.decompose()

    thElments = soup.find_all("th")
    for thElement in thElments:
        if not bool(thElement.attrs) and not bool(thElement.text) and not bool(thElement.find_all()):
            thElement.decompose()

    trElements = soup.find_all("tr")
    for trElement in trElements:
        if not bool(trElement.attrs) and not bool(trElement.text.strip()) and not bool(trElement.find_all()):
            trElement.decompose()

    tbodyElements = soup.find_all("tbody")
    for tbodyElement in tbodyElements:
        if not bool(tbodyElement.attrs) and not bool(tbodyElement.text.strip()) and not bool(tbodyElement.find_all()):
            tbodyElement.decompose()

    theadElements = soup.find_all("thead")
    for theadElement in theadElements:
        if not bool(theadElement.attrs) and not bool(theadElement.text.strip()) and not bool(theadElement.find_all()):
            theadElement.decompose()

    tableElements = soup.find_all("table")
    for tableElement in tableElements:
        if not bool(tableElement.attrs) and not bool(tableElement.text) and not bool(tableElement.find_all()):
            tableElement.decompose()

    compactHTML = compactHtml(str(soup))

    with open("cleanedStringHTML1.html", "w", encoding="utf-8") as file:
        file.write(compactHTML)

    return compactHTML


def deleteEmptyTables2(soup, output_file):
    types = ["pre", "td", "th", "tr", "tbody", "thead", "table"]
    for typ in types:
        elements = soup.find_all(typ)
        for element in elements:
            if not bool(element.attrs) and not bool(element.text.strip()) and not bool(element.find_all()):
                element.decompose()
    compactHTML = compactHtml(str(soup))

    with open("cleanedStringHTML1.html", "w", encoding="utf-8") as file:
        file.write(compactHTML)

    return compactHTML

# cleaned_html = deleteEmptyTables(html_content2, "cleaned_table.html")
# print(cleaned_html)