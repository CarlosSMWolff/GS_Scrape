""""
scraper.py
----------

This script provides tools to scrape publication data from Google Scholar for a specific user. It uses Selenium 
to interact with the Google Scholar interface, navigate through pages, and extract detailed publication 
information, including title, authors, journal, citations, and year of publication.

Key Features:
-------------
- Extracts a comprehensive list of publications for a Google Scholar user.
- Handles pseudonym unification and author name formatting.
- Differentiates between peer-reviewed papers and preprints (e.g., arXiv).
- Outputs the data as a pandas DataFrame for further analysis.
- Includes a command-line interface (CLI) for scraping directly from the terminal.


Functions:
----------
1. unify_pseudonyms(input_string, pseudonyms, name):
   Replaces pseudonyms in an input string with a standardized name.

2. format_names(name_string):
   Formats a list of author names by capitalizing and punctuating initials.

3. getGSdata(scholarUserId, name, pseudonyms):
   Scrapes Google Scholar for a specified user and returns a pandas DataFrame with the extracted data.

CLI Functionality:
------------------
The script can be executed directly from the terminal to scrape Google Scholar data. 
Usage:
    python scraper.py --scholar_id="SCHOLAR_ID" --name "Author Name" --pseudonyms "Pseudonym1" "Pseudonym2" --output papers.csv

Example:
    python scraper.py --scholar_id="-VPPZ8YAAAAJ" --name "C. Sánchez Muñoz" --pseudonyms "C S Munoz" "C S Muñoz" --output papers.csv

Arguments:
    --scholar_id : The Google Scholar user ID (e.g., '-VPPZ8YAAAAJ').
    --name       : The canonical author name (e.g., 'C. Sánchez Muñoz') to highlight in the authors' list.
    --pseudonyms : A list of alternate author names (pseudonyms) to unify under the canonical name.
    --output     : The name of the output CSV file (default: papers.csv).

Dependencies:
-------------
- pandas: For handling publication data in tabular format.
- selenium: For automating browser interactions.
- time: To handle delays during browser operations.

Usage Example:
--------------

1. **Import and Use as a Library**:
   You can import the `getGSdata` function into your Python scripts or notebooks and call it directly:

   ```python
   from gsscrape.scraper import getGSdata

   # Scrape data programmatically
   df_papers = getGSdata(
       scholarUserId="SCHOLAR_ID", 
       name="C. Sánchez Muñoz", 
       pseudonyms=["C S Munoz", "C S Muñoz"]
   )

   # Save the results to a CSV file
   df_papers.to_csv("papers.csv", index=False)


2. **Run Directly from Terminal**:
   The script also supports a command-line interface (CLI) for convenience. You can scrape data and save it to 
   a CSV file without writing additional Python code.

   Example Command:
   ----------------
   python scraper.py --scholar_id "-VPPZ8YAAAAJ" --name "C. Sánchez Muñoz" --pseudonyms "C S Munoz" "C S Muñoz" --output papers.csv

   Command-Line Arguments:
   ------------------------
   --scholar_id : str
       The Google Scholar user ID (e.g., '-VPPZ8YAAAAJ').
   --name : str
       The canonical author name to highlight in the authors' list (e.g., 'C. Sánchez Muñoz').
   --pseudonyms : list of str
       A list of pseudonyms to unify (e.g., 'C S Munoz', 'C S Muñoz').
   --output : str (optional)
       The name of the output CSV file (default: 'papers.csv').

   This method is ideal for quick data extraction without writing additional Python scripts.
   

Author:
-------
C. Sánchez Muñoz, January 2025
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import argparse



def unify_pseudonyms(input_string,pseudonyms,name):
    """
    Replaces all occurrences of pseudonyms in the input string with a standardized name.

    Args:
        input_string (str): The input text where replacements will be made.
        pseudonyms (list): A list of strings representing alternate names to replace.
        name (str): The standardized name to replace the pseudonyms with.

    Returns:
        str: The modified string with pseudonyms replaced by the standardized name.
    """
    for pseudonym in pseudonyms:
        input_string = input_string.replace(pseudonym, name)
    return input_string


def format_names(name_string):
    """
    Formats a string of names by adding periods to initials and capitalizing them.

    Args:
        name_string (str): A string containing names separated by commas.

    Returns:
        str: A formatted string with initials properly punctuated and capitalized.
    """
    # Split the string into individual names
    names = name_string.split(", ")

    # Process each name
    formatted_names = []
    for name in names:
        # Extract the surname and initials
        surname = " ".join(name.split(" ")[1:])
        initials = name.split(" ")[0]
        
        # Check if the first part is a full name (criterion: three or more letters)
        isname = len(initials)>= 3
        if isname == True:
            # If it's a full name, take the first letter as the initial
            initials = initials[0]

        # Add periods to the initials and capitalize them
        initials = initials.upper()
        initials= '.'.join(initials) + '.'
        formatted_name = ' '.join([initials,surname])
        formatted_names.append(formatted_name)

    # Join all formatted names back into a single string

    return ", ".join(formatted_names)


def getGSdata(scholarUserId, name, pseudonyms):
    """
    Scrape Google Scholar data for a given user and return it as a DataFrame.

    This function interacts with Google Scholar using Selenium to scrape publication data for the specified user.
    It handles multiple pages of results, extracts publication details, and formats the data for further analysis.

    Parameters:
    ----------
    scholarUserId : str
        The Google Scholar user ID for the target scholar.
    name : str
        The canonical name of the target scholar to unify pseudonyms in the authorship list.
    pseudonyms : list of str
        A list of pseudonyms to be replaced with the canonical name of the target scholar.

    Returns:
    -------
    pd.DataFrame
        A DataFrame containing information about the user's publications, including:
        - Title of the paper
        - Authors (formatted)
        - Reference
        - Journal or source
        - Year of publication
        - Number of citations
        - URL to the publication
        - Citations per year (from the year the paper was published).
        - Whether the publication is a preprint on arXiv.
    """

    # Set up the Firefox driver with headless mode
    options = Options()
    options.headless = True
    urlpage = f'https://scholar.google.es/citations?hl=es&user={scholarUserId}&view_op=list_works&sortby=pubdate'
    driver = webdriver.Firefox(options=options)

    # Open the Google Scholar page
    driver.get(urlpage)
    time.sleep(3)   

    # Initialize variables for pagination handling
    npapersOld=0
    updateFlag = 0

    # Load all publications by clicking "Show more" until no new papers are loaded
    while(updateFlag==0):
        papers=driver.find_elements(By.CLASS_NAME, "gsc_a_tr")
        npapersOld = len(papers)
        print("Refreshing page")
        try:
            driver.find_element(By.XPATH, "//span[text()='Mostrar más']").click()
        except Exception:
            break  # Exit loop if "Show more" button is not found
        papers=driver.find_elements(By.CLASS_NAME, "gsc_a_tr")
        npapers = len(papers)
        if npapers==npapersOld:
            updateFlag=1   

    time.sleep(3)   

    print("Maximum number of papers displayed on screen")

    # Extract information from each paper
    papers=driver.find_elements(By.CLASS_NAME, "gsc_a_tr")
    infoList = []

    print(f'{len(papers)} papers found')
    print('Extracting information...')

    for paper in papers:
        # Extract title and link
        title=paper.find_element(By.CLASS_NAME, "gsc_a_at").text
        gslink=paper.find_element(By.CLASS_NAME, "gsc_a_at").get_attribute("href")

        # Extract reference and year
        reference=(paper.find_elements(By.CLASS_NAME, "gs_gray")[1].text)
        year = int(paper.find_element(By.CLASS_NAME, "gsc_a_y").text)
        
        # Extract citation count (default to 0 if not available)
        try:
            citations = int(paper.find_element(By.CLASS_NAME, "gsc_a_ac").text)
        except:
            citations = 0

        # Save the handle of the original window
        original_window = driver.current_window_handle

        # Open a new window and switch to it
        driver.execute_script("window.open('');")
        time.sleep(1)  # Wait for the new window to open
        new_window = [window for window in driver.window_handles if window != original_window][0]
        driver.switch_to.window(new_window)

        # Open the detailed paper page and extract additional information
        driver.get(gslink)
        paperlink = driver.find_element(By.CLASS_NAME,'gsc_oci_title_link').get_attribute('href')
        citegraphs = driver.find_elements(By.CLASS_NAME,'gsc_oci_g_al')
        citeyears=[element.get_attribute("innerHTML") for element in citegraphs]
        journalTitle = driver.find_elements(By.CLASS_NAME,'gsc_oci_value')[2].text.title()
        authors = driver.find_elements(By.CLASS_NAME,'gsc_oci_value')[0].text.title()

        # Format and unify author names
        unify_pseudonyms(authors, pseudonyms, name)
        authors_formatted = format_names(authors)

        # Close the new window and return to the original
        driver.close()
        driver.switch_to.window(original_window)

        # Adjust journal and reference if the publication is on arXiv
        isarxiv = 'arxiv' in journalTitle.lower()
        if isarxiv:
            reference = 'arXiv: '+(reference.split('arXiv:')[1])
            journalTitle = 'arXiv'

        # Compile paper information into a list
        paperInfo = [title,  authors_formatted,reference, journalTitle, year, citations, paperlink, citeyears, isarxiv ]
        infoList.append(paperInfo)

    driver.quit()
    # Create a DataFrame from the collected information
    df_papers = pd.DataFrame(infoList, columns=['title', 'authors',  'reference','journal', 'year','citations', 'url', 'citationsyears', 'isarxiv'])

    return df_papers



if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Scrape Google Scholar publication data.")
    parser.add_argument("--scholar_id", required=True, help="Google Scholar user ID")
    parser.add_argument("--name", required=True, help="Author name to unify (e.g., 'C. Sánchez Muñoz')")
    parser.add_argument("--pseudonyms", nargs="+", required=True, help="List of pseudonyms to replace with the author's name")
    parser.add_argument("--output", default="papers.csv", help="Output CSV file (default: papers.csv)")
    
    args = parser.parse_args()
    
    # Run the scraper
    df_papers = getGSdata(scholarUserId=args.scholar_id, name=args.name, pseudonyms=args.pseudonyms)
    
    # Save results to a CSV file
    df_papers.to_csv(args.output, index=False)
    print(f"Scraping complete. Data saved to {args.output}")