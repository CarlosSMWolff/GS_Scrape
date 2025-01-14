"""
reporter.py
------------

This module provides functionality for generating LaTeX reports from publication data. It formats 
peer-reviewed publications and preprints into a structured LaTeX document, including author 
statistics (e.g., h-index, citations, first/last author counts) and journal-specific summaries.

Key Features:
- Processes a pandas DataFrame of publication data.
- Differentiates between peer-reviewed publications and preprints.
- Generates a detailed LaTeX-formatted report for academic CVs or publication summaries.
- Tracks specific journals for summary statistics.

Usage:
------
Import the `generate_latex_report` function and call it with the necessary arguments:
    from reporter import generate_latex_report

    generate_latex_report(
        df_papers=my_dataframe,
        name="C. Sánchez Muñoz",
        output_file="publications_report.tex"
    )

Dependencies:
- pandas: For handling publication data in DataFrame format.
- datetime: To include the current date in the report.

Author: C. Sánchez Muñoz
Date: January 2025
"""


from datetime import datetime
import pandas as pd


def generate_latex_report(df_papers, name, output_file,   journals_to_count = ["Nature Photonics", "Nature Communications", "Nature Materials", "Science Advances",
        "Physical Review Letters", "PRX", "PRX Quantum"]):
    """
    Generates a LaTeX report with formatted papers and statistics for a scholar, 
    including peer-reviewed papers and preprints.

    Parameters:
    ----------
    df_papers : pd.DataFrame
        DataFrame containing paper information with columns:
        - 'title': Title of the paper
        - 'authors': Authors of the paper
        - 'reference': Reference with journal/source
        - 'year': Year of publication
        - 'url': URL link to the paper
        - 'journal': Journal name
        - 'isarxiv': Boolean indicating if the paper is from arXiv (preprint)
        
    name : str
        Name of the scholar to be emphasized with \textbf{} in the authors' list.
        
    output_file : str
        Path to save the resulting LaTeX file (in this case, a single file for both papers and report).

    journals_to_count : list
        List of journals to track in the summary (with the exact names as they should appear in the report). 

    """
     
    # Initialize counters
    peer_reviewed_count = 0
    first_author_count = 0
    last_author_count = 0
    journal_counts = {journal.lower(): {"count": 0, "first_author": 0, "last_author": 0} for journal in journals_to_count}
    
    # Start the LaTeX snippet for papers list
    latex_snippet = "\\begin{enumerate}\n"

    # Initialize citation and h-index calculations
    total_citations = 0
    citation_counts = []

    # Iterate through each row in the DataFrame to format the paper details (only non-arxiv)
    for _, row in df_papers[df_papers['isarxiv'] == False].iterrows():
        title = row['title']
        authors = row['authors']  # Do not bold the name yet
        reference = row['reference'].title()
        year = row['year']
        url = row['url']
        journal_title = row['journal']
        citations = row['citations']

        # Increment peer-reviewed count
        peer_reviewed_count += 1
        citation_counts.append(citations)
        total_citations += citations

        # Split authors into a list and check for first and last author
        authors_list = [author.strip() for author in authors.split(',')]  # Remove extra spaces
        is_first_author = authors_list[0] == name
        is_last_author = authors_list[-1] == name

        # Count first and last authors
        if is_first_author:
            first_author_count += 1
            if journal_title.lower() in journal_counts:
                journal_counts[journal_title.lower()]["first_author"] += 1
        if is_last_author:
            last_author_count += 1
            if journal_title.lower() in journal_counts:
                journal_counts[journal_title.lower()]["last_author"] += 1

        # Normalize the journal name to check for matches in the list (case-insensitive)
        journal_lower = journal_title.lower()
        if journal_lower in journal_counts:
            journal_counts[journal_lower]["count"] += 1

        # After counting, bolden the scholar's name in the authors list
        authors_bolded = authors.replace(name, f"\\textbf{{{name}}}")

        # Format the entry for this paper
        latex_snippet += (
            f" \\item \\emph{{{title}}}.\\\\ \n"
            f"{{{authors_bolded}}}\\\\ \n"
            f"  \\href{{{url}}}{{{{{reference} ({year})}}}}\n\n"
        )

    # End the enumerate environment for peer-reviewed papers
    latex_snippet += "\\end{enumerate}\n"

    # Calculate the h-index (simplified version)
    sorted_citations = sorted(citation_counts, reverse=True)
    h_index = 0
    for i, citation in enumerate(sorted_citations):
        if citation >= i + 1:
            h_index = i + 1
        else:
            break

    # Generate statistics report
    current_date = datetime.now().strftime("%B %d, %Y")
    statistics_text = f"""
{peer_reviewed_count} peer-reviewed publications, {first_author_count} papers as first author, {last_author_count} papers as last author.
"""

    # Generate the journal counts for the specified journals
    journal_report = []
    for journal in journals_to_count:
        journal_lower = journal.lower()
        if journal_counts[journal_lower]["count"] > 0:
            first_author_count_journal = journal_counts[journal_lower]["first_author"]
            last_author_count_journal = journal_counts[journal_lower]["last_author"]
            # Include journal information based on counts
            journal_str = f"{journal_counts[journal_lower]['count']} {journal}"
            if first_author_count_journal > 0 and last_author_count_journal > 0:
                journal_str += f" ({first_author_count_journal} first author, {last_author_count_journal} last author)"
            elif first_author_count_journal > 0:
                journal_str += f" ({first_author_count_journal} first author)"
            elif last_author_count_journal > 0:
                journal_str += f" ({last_author_count_journal} last author)"
            journal_report.append(journal_str)

    # Include the formatted journal information if available
    if journal_report:
        statistics_text += f"These include " + ", ".join(journal_report) + ".\n"

    # Add h-index and total citations to the statistics
    statistics_text += f"\\textbf{{h-index: {h_index}. Citations: {total_citations}}} (Google Scholar, as of {current_date})."

    # Append the preprints section
    latex_snippet += "\n\\begin{center}\n\\textsc{Preprints}\n\\end{center}\n"
    latex_snippet += "\\begin{enumerate}\n"

    # Iterate through preprints (arxiv)
    for _, row in df_papers[df_papers['isarxiv'] == True].iterrows():
        title = row['title']
        authors = row['authors']
        reference = row['reference']
        year = row['year']
        url = row['url']

        # Bolden the scholar's name in the authors list
        authors_bolded = authors.replace(name, f"\\textbf{{{name}}}")

        # Format the entry for the preprint
        latex_snippet += (
            f" \\item \\emph{{{title}}}.\\\\ \n"
            f"{{{authors_bolded}}}\\\\ \n"
            f"  \\href{{{url}}}{{{{{reference} ({year})}}}}\n\n"
        )

    # End the enumerate environment for preprints
    latex_snippet += "\\end{enumerate}\n"

    # Save the final LaTeX report to a file
    with open(output_file, "w") as f:
        f.write(statistics_text + "\n\n" + latex_snippet)

    print(f"Report saved to {output_file}")
