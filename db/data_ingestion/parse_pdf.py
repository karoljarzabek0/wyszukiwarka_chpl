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
                # print(f"Page {i + 1}")
                # if text:
                #     print(f"Page {i + 1}:\n{text}\n{'='*40}")
                # else:
                #     print(f"Page {i + 1}: No text found.\n{'='*40}")
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
    char_sections = extract_sections(char_text, url)
    return char_sections, char_text


def main():
    url = "https://rejestry.ezdrowie.gov.pl/api/rpl/medicinal-products/2/characteristic"

    sections, text = parseToPlainText(url)
    print(f"Type of extions variable {type(sections)}")
    for key, value in sections.items():
        print(key)
        print("--------")
        print(value)
        print("--------")



    # sections = {
    #     "nazwa_produktu_leczniczego": r"1\. NAZWA PRODUKTU LECZNICZEGO\s*(.*?)\s*(?=\d\.|$)",
    #     "sklad": r"2\. SKŁAD JAKOŚCIOWY I ILOŚCIOWY\s*(.*?)\s*(?=\d\.|$)",
    #     "postac_farmaceutyczna": r"3\. POSTAĆ FARMACEUTYCZNA\s*(.*?)\s*(?=\d\.|$)",
    #     "wskazania_do_stosowania": r"4\. SZCZEGÓŁOWE DANE KLINICZNE\s*4\.1\s*Wskazania do stosowania\s*(.*?)\s*(?=4\.2|$)",
    #     "dawkowanie_sposob_podania": r"4\.2 Dawkowanie i sposób podawania\s*(.*?)\s*(?=4\.3|$)",
    #     "przeciwwskazania": r"4\.3 Przeciwwskazania\s*(.*?)\s*(?=4\.4|$)",
    #     "ostrzezenia": r"4\.4 Specjalne ostrzeżenia i środki ostrożności dotyczące stosowania\s*(.*?)\s*(?=4\.5|$)",
    #     "interakcje": r"4\.5 Interakcje z innymi produktami leczniczymi i inne rodzaje interakcji\s*(.*?)\s*(?=4\.6|$)",
    #     "dzialania_niepozadane": r"4\.8 Działania niepożądane\s*(.*?)\s*(?=4\.9|$)",
    #     "przedawkowanie": r"4\.9 Przedawkowanie\s*(.*?)\s*(?=5\.|$)",
    #     "wlasciwosci_farmakologiczne": r"5\. WŁAŚCIWOŚCI FARMAKOLOGICZNE\s*(.*?)\s*(?=6\.|$)",
    #     "dane_farmaceutyczne": r"6\. DANE FARMACEUTYCZNE\s*(.*?)\s*(?=7\.|$)",
    # }