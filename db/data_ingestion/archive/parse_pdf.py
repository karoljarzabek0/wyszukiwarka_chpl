import requests
import re
import fitz
import logging

def pdf_to_text(url):
    response = requests.get(url)

    if response.status_code == 200:
        # Save the PDF to a local file
        with open('test.pdf', 'wb') as f:
            f.write(response.content)

        with fitz.open('test.pdf') as doc:
            text = ""
            for page in doc:
                text += page.get_text()
                text += '\n'
                
        # Usuń znaczniki stron i ich szum
        #text = re.sub(r"\n\d+\s*\n", "[[NOWA_STRONA]]\n", text)
        text = re.sub(r"\n\d+\s*\n", "\n", text)

        # Usuń puste miejsca
        #text = re.sub(r"\n\s*\n", "\n[[PUSTE_SPACJE]]\n", text)
        text = re.sub(r"\n\s*\n", r"\n", text)
        text = re.sub(r"\s*\n", r"\n", text)
        # Popraw nagłówki
        #text = re.sub(r"\d\s*\n", " ", text)
        text = re.sub(r"\.(\d)\s*\n", r".\1 ", text)
        text = re.sub(r"(\d)\.\s*\n", r"\1. ", text)
        #text = re.sub(r"\d\s*\n", "", text)

        # Usuń podwójne spacje
        #text = re.sub(r" {2}", "[[2x spacja]]", text)
        text = re.sub(r" {2}", " ", text)

        # Popraw punktory
        text = re.sub(r"^•\s*$\n?", "• ", text, flags=re.MULTILINE)
        with open("test.txt", "w") as txt:
            txt.write(text)

        

            return text
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")
    return ""

def save_temp_text(url):
    response = requests.get(url)

    if response.status_code == 200:
        # Save the PDF to a local file
        with open('test.pdf', 'wb') as f:
            f.write(response.content)
        # print(response.content)
        logging.debug("PDF downloaded successfully.")

        with pdfplumber.open('test.pdf') as pdf:
        # Iterate through all the pages
            full_text = ""
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                full_text += text
                full_text += '\n'
            print(f"SUCCESS | URL: {url}")
        with open("test.txt", "w") as file:
            file.write(full_text)
        return full_text
    else:
        logging.warning(f"Failed to download PDF | URL: {url} | Status code: {response.status_code}")
        with open('failed_downloads.txt', 'a') as f:
            f.write(f"{url}\n")
        return "ERROR"

def extract_sections(text, url):
    """
    Extracts key sections based on predefined section headers using regex.
    The regex patterns are based on common section numbering from product characteristic documents.
    Adjust these patterns as needed for your specific PDF.
    """

    sections = {
        "nazwa_sklad_postac": r"(?s)1\.\s*NAZWA PRODUKTU LECZNICZEGO.*?3\.\s*POSTAĆ FARMACEUTYCZNA.*?(?=4\.)",
        "stosowanie_przeciwwskazania": r"(?s)4\.\s*SZCZEGÓŁOWE DANE KLINICZNE.*?4\.4\s*Specjalne ostrzeżenia i środki ostrożności dotyczące stosowania.*?(?=4\.5)",
        "interakcje_dzial_niep": r"(?s)4\.5\s*Interakcje z innymi produktami leczniczymi i inne rodzaje interakcji.*?4\.9\s*Przedawkowanie.*?(?=5\.)",
        "wlasc_farmakologiczne": r"(?s)5\.\s+WŁAŚCIWOŚCI FARMAKOLOGICZNE.*"
    }
    
    extracted = {}
    for section, pattern in sections.items():
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            extracted[section] = match.group(0).strip()
        else:
            extracted[section] = "NOT_FOUND"
            logging.warning(f"Section '{section}' NOT FOUND for URL: {url}")
            with open('failed_extraction.txt', 'a') as f:
                f.write(f"{url} - {section}\n")
    return extracted

def parseToPlainText(url: str) -> dict:
    char_text = pdf_to_text(url)
    return char_text

def main():
    url = "https://rejestry.ezdrowie.gov.pl/api/rpl/medicinal-products/2/characteristic"

    text = parseToPlainText(url)
    print(text[:100])

if __name__ == "__main__":
    main()