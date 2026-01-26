#!/usr/bin/env python3
"""
Script per aggiungere un indice dinamico delle box al documento LaTeX.
Usa \label dentro le box e genera un indice custom.
"""

import re
import sys

def sanitize_label(title):
    """Crea un label valido dal titolo."""
    label = title.lower()
    label = re.sub(r'[^a-z0-9]', '_', label)
    label = re.sub(r'_+', '_', label)
    label = label.strip('_')
    return f"box:{label[:40]}"

def sanitize_toc_title(title):
    """Pulisce il titolo per il TOC."""
    toc_title = title
    toc_title = re.sub(r'\$[^$]*\$', '', toc_title)  # Rimuovi math
    toc_title = toc_title.replace('\\&', 'e')
    toc_title = toc_title.replace('&', 'e')
    toc_title = re.sub(r'\\texorpdfstring\{[^}]*\}\{([^}]*)\}', r'\1', toc_title)
    toc_title = re.sub(r'\\[a-zA-Z]+', '', toc_title)  # Rimuovi comandi
    toc_title = re.sub(r'[{}]', '', toc_title)
    toc_title = toc_title.strip()
    return toc_title

def add_toc_entries(content):
    """Modifica le righe fancytitle per aggiungere entry TOC inline."""

    # PRIMA: Pulisci TUTTO ciò che segue }; sulle righe fancytitle
    # Questo rimuove qualsiasi phantomsection/addcontentsline esistente
    # Uso .+? per gestire titoli con math mode che contengono {}
    content = re.sub(
        r'(\\node\[fancytitle[^\]]*\]\s*(?:at\s*\([^)]*\))?\s*\{[^{]*\\color\{white\}.+?\};).*$',
        r'\1',
        content,
        flags=re.MULTILINE
    )

    # POI: Cerco le righe con fancytitle e aggiungo l'addcontentsline SULLA STESSA RIGA
    # Uso .+? (non-greedy) per catturare tutto fino a }; incluso math mode con {}
    pattern = r'(\\node\[fancytitle[^\]]*\]\s*(?:at\s*\([^)]*\))?\s*\{[^{]*\\color\{white\}\s*)(.+?)(\};)'

    def replacement(match):
        prefix = match.group(1)
        title = match.group(2).strip()
        suffix = match.group(3)

        toc_title = sanitize_toc_title(title)

        if toc_title and len(toc_title) > 2:
            # Aggiungi phantomsection + addcontentsline dopo il ; ma sulla stessa riga
            return f'{prefix}{title}{suffix}\\phantomsection\\addcontentsline{{toc}}{{subsection}}{{\\texorpdfstring{{{toc_title}}}{{{toc_title}}}}}'
        return match.group(0)

    result = re.sub(pattern, replacement, content)
    return result

def add_toc_preamble(content):
    """Aggiunge i package necessari e il tableofcontents."""

    # Aggiungi hyperref se non presente
    if 'hyperref' not in content:
        content = content.replace(
            '\\usepackage{fancyhdr}',
            '\\usepackage{fancyhdr}\n\\usepackage[hidelinks, bookmarks=true]{hyperref}'
        )

    # Aggiungi tableofcontents SOLO se non esiste già
    if 'Indice delle Box' not in content:
        toc_code = '''%------------ INDICE ---------------
\\begin{center}{\\Large\\textbf{Indice delle Box}}\\end{center}
\\vspace{0.5cm}
{\\footnotesize
\\setlength{\\columnsep}{0.8cm}
\\begin{multicols}{3}
\\makeatletter
\\@starttoc{toc}
\\makeatother
\\end{multicols}
}
\\newpage
%-----------------------------------

'''
        # Inserisci prima di \begin{multicols*}{3}
        content = content.replace(
            '\\begin{multicols*}{3}',
            toc_code + '\\begin{multicols*}{3}'
        )

    # Rimuovi la numerazione delle subsection nel TOC SOLO se non esiste già
    if '\\setcounter{tocdepth}' not in content:
        content = content.replace(
            '\\begin{document}',
            '\\begin{document}\n\\setcounter{tocdepth}{2}\n\\renewcommand{\\thesubsection}{}'
        )

    return content

def count_boxes(content):
    """Conta le box con fancytitle."""
    return len(re.findall(r'\\node\[fancytitle', content))

def main():
    input_file = "CSFdE.tex"
    output_file = "CSFdE_with_toc.tex"

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    print(f"Lettura file: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    boxes_count = count_boxes(content)
    print(f"Box trovate: {boxes_count}")

    # Aggiungi entry TOC per ogni box
    print("Aggiunta entry TOC...")
    content = add_toc_entries(content)

    # Aggiungi preamble e tableofcontents
    print("Aggiunta indice...")
    content = add_toc_preamble(content)

    # Verifica
    toc_entries = len(re.findall(r'\\addcontentsline\{toc\}', content))
    print(f"Entry TOC aggiunte: {toc_entries}")

    # Scrivi risultato
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\nFile salvato: {output_file}")
    print("\nPer compilare (serve doppia compilazione per TOC):")
    print(f"  pdflatex {output_file} && pdflatex {output_file}")

if __name__ == "__main__":
    main()
