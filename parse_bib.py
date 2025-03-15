import bibtexparser
import re

def format_authors(author_str):
    authors = [a.strip() for a in re.split(r'\s+and\s+', author_str)]
    formatted_authors = []
    
    for author in authors:
        if ',' in author:
            last, first = author.split(',', 1)
            full_name = f"{first.strip()} {last.strip()}"
        else:
            full_name = author
        
        if "Thomas Robiglio" in full_name:
            full_name = f"<u>Thomas Robiglio</u>"
        
        formatted_authors.append(full_name)
    
    if len(formatted_authors) > 1:
        return ', '.join(formatted_authors[:-1]) + ', and ' + formatted_authors[-1]
    return formatted_authors[0]

def parse_bibtex(bib_file):
    with open(bib_file, 'r', encoding='utf-8') as f:
        bib_database = bibtexparser.load(f)
    
    preprints = []
    journal_articles = []
    
    for entry in bib_database.entries:
        title = entry.get('title', 'Unknown Title')
        author = format_authors(entry.get('author', 'Unknown Author'))
        journal = entry.get('journal', '')
        year = entry.get('year', '0000')
        arxiv_id = entry.get('eprint', '')
        doi = entry.get('doi', '')
        entry_type = entry.get('ENTRYTYPE', '').lower()
        
        arxiv_link = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else ""
        doi_link = f"https://doi.org/{doi}" if doi else ""
        
        publication = (int(year), title, author, journal, arxiv_id, arxiv_link, doi, doi_link)
        
        if entry_type == 'misc':
            preprints.append(publication)
        elif entry_type == 'article':
            journal_articles.append(publication)
    
    preprints.sort(reverse=True, key=lambda x: x[0])
    journal_articles.sort(reverse=True, key=lambda x: x[0])
    
    return preprints, journal_articles

def update_qmd(preprints, journal_articles, qmd_file):
    with open(qmd_file, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("title: \"Publications\"\n")
        f.write("---\n\n")
        
        if preprints:
            f.write("## Pre-prints\n\n")
            for i, (year, title, author, journal, arxiv_id, arxiv_link, doi, doi_link) in enumerate(preprints, start=1):
                letter = chr(65 + i - 1)  # Convert index to letter (A, B, C, ...)
                f.write(f"{letter}) {title}<br />\n")
                f.write(f"    {author}<br />\n")
                if arxiv_link:
                    f.write(f"    [![arXiv](https://img.shields.io/badge/arXiv-{arxiv_id}-b31b1b.svg)]({arxiv_link})<br />\n")
                if doi_link:
                    f.write(f"    <a href=\"{doi_link}\"><img src=\"https://img.shields.io/badge/DOI-{doi}-blue.svg\"></a><br />\n")
                f.write("\n")
        
        if journal_articles:
            f.write("## Journal articles\n\n")
            f.write("<ol reversed>")
            for i, (year, title, author, journal, arxiv_id, arxiv_link, doi, doi_link) in enumerate(journal_articles, start=1):
                f.write(f"<li> {title}<br />\n")
                f.write(f"    {author}<br />\n")
                if journal:
                    f.write(f"    *{journal}*<br />\n")
                if arxiv_link:
                    f.write(f"    [![arXiv](https://img.shields.io/badge/arXiv-{arxiv_id}-b31b1b.svg)]({arxiv_link})<br />\n")
                if doi_link:
                    f.write(f"    <a href=\"{doi_link}\"><img src=\"https://img.shields.io/badge/DOI-{doi}-blue.svg\"></a><br />\n")
                f.write("</li> <br />\n")
            f.write("</ol>")

if __name__ == "__main__":
    bib_file = "papers.bib"  # Change to your actual file path
    qmd_file = "publications.qmd"  # Change to your actual file path
    preprints, journal_articles = parse_bibtex(bib_file)
    update_qmd(preprints, journal_articles, qmd_file)
    print(f"Updated {qmd_file} with {len(preprints) + len(journal_articles)} publications.")