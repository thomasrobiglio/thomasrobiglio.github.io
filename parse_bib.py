import bibtexparser
import re

def format_authors(author_str):
    authors = [a.strip() for a in re.split(r'\s+and\s+', author_str)]
    formatted_authors = []
    
    for author in authors:
        if ',' in author:
            last, first = author.split(',', 1)
            formatted_authors.append(f"{first.strip()} {last.strip()}")
        else:
            formatted_authors.append(author)
    
    if len(formatted_authors) > 1:
        return ', '.join(formatted_authors[:-1]) + ' and ' + formatted_authors[-1]
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
        arxiv_id = entry.get('eprint', '')
        doi = entry.get('doi', '')
        entry_type = entry.get('ENTRYTYPE', '').lower()
        
        arxiv_link = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else ""
        doi_link = f"https://doi.org/{doi}" if doi else ""
        
        publication = (title, author, journal, arxiv_id, arxiv_link, doi, doi_link)
        
        if entry_type == 'misc':
            preprints.append(publication)
        elif entry_type == 'article':
            journal_articles.append(publication)
    
    return preprints, journal_articles

def update_qmd(preprints, journal_articles, qmd_file):
    with open(qmd_file, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("title: \"Publications\"\n")
        f.write("---\n\n")
        
        if preprints:
            f.write("## Pre-prints\n\n")
            for i, (title, author, journal, arxiv_id, arxiv_link, doi, doi_link) in enumerate(reversed(preprints), start=1):
                f.write(f"{i}. {title}<br />\n")
                f.write(f"    {author}<br />\n")
                if arxiv_link:
                    f.write(f"    🔗 [arXiv: {arxiv_id}]({arxiv_link})<br />\n")
                if doi_link:
                    f.write(f"    DOI: [{doi}]({doi_link})<br />\n")
                f.write("\n")
        
        if journal_articles:
            f.write("## Journal Papers\n\n")
            for i, (title, author, journal, arxiv_id, arxiv_link, doi, doi_link) in enumerate(reversed(journal_articles), start=1):
                f.write(f"{i}. {title}<br />\n")
                f.write(f"    {author}<br />\n")
                if journal:
                    f.write(f"    *{journal}*<br />\n")
                if arxiv_link:
                    f.write(f"    🔗 [arXiv: {arxiv_id}]({arxiv_link})<br />\n")
                if doi_link:
                    f.write(f"    DOI: [{doi}]({doi_link})<br />\n")
                f.write("\n")

if __name__ == "__main__":
    bib_file = "papers.bib"  # Change to your actual file path
    qmd_file = "publications.qmd"  # Change to your actual file path
    preprints, journal_articles = parse_bibtex(bib_file)
    update_qmd(preprints, journal_articles, qmd_file)
    print(f"Updated {qmd_file} with {len(preprints) + len(journal_articles)} publications.")
