#!/usr/bin/env python3
"""
Script per rimuovere i wrapper \colorbox{\parbox{...}{...}} mantenendo il contenuto.
Rimuove TUTTE le colorbox con parbox, preservando esattamente il contenuto interno.
"""

import re
import sys

def find_colorbox_end(text, start_of_content):
    """
    Trova la fine del contenuto della colorbox.
    start_of_content è la posizione subito dopo l'ultima { di apertura.
    Ritorna (end_of_content, end_of_colorbox) dove:
    - end_of_content è la posizione dell'ultimo carattere del contenuto
    - end_of_colorbox è la posizione dopo le }} di chiusura
    """
    depth = 1
    i = start_of_content

    while i < len(text) and depth > 0:
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
        i += 1

    if depth != 0:
        return -1, -1

    # Ora i punta subito dopo la prima } di chiusura (quella del parbox content)
    # Deve esserci un'altra } per chiudere la colorbox

    # La struttura è: \colorbox{color}{\parbox{width}{CONTENT}}
    # Quindi dopo il CONTENT c'è }} (chiude parbox, poi chiude colorbox)

    end_of_content = i - 1  # posizione della } che chiude il parbox content

    # Verifica che ci sia un'altra } subito dopo
    if i < len(text) and text[i] == '}':
        end_of_colorbox = i + 1  # posizione dopo la } finale
        return end_of_content, end_of_colorbox
    else:
        return -1, -1

def remove_colorbox_wrappers(content):
    """Rimuove tutti i wrapper colorbox mantenendo il contenuto."""

    # Pattern per trovare \colorbox{...}{\parbox{...}{
    # Cattura tutto fino all'apertura del contenuto
    pattern = r'\\colorbox\{[^}]+\}\{\\parbox\{[^}]+\}\{'

    result = content
    removed = 0
    max_iterations = 500

    for iteration in range(max_iterations):
        match = re.search(pattern, result)
        if not match:
            break

        start_of_colorbox = match.start()
        start_of_content = match.end()

        # Trova la fine
        end_of_content, end_of_colorbox = find_colorbox_end(result, start_of_content)

        if end_of_content == -1:
            print(f"Warning: impossibile trovare la fine della colorbox alla posizione {start_of_colorbox}")
            # Rimuovi questo match dal pattern per evitare loop infinito
            result = result[:start_of_colorbox] + "%%REMOVED%%" + result[match.end():]
            continue

        # Estrai il contenuto interno (senza la } di chiusura del parbox)
        inner_content = result[start_of_content:end_of_content]

        # Sostituisci
        result = result[:start_of_colorbox] + inner_content + result[end_of_colorbox:]
        removed += 1

    # Ripristina eventuali marker
    result = result.replace("%%REMOVED%%", "\\colorbox")

    return result, removed

def count_colorbox(text):
    """Conta le colorbox con parbox."""
    return len(re.findall(r'\\colorbox\{[^}]+\}\{\\parbox', text))

def main():
    input_file = "CSFdE.tex"
    output_file = "CSFdE_no_colorbox.tex"

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    print(f"Lettura file: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    count_before = count_colorbox(content)
    print(f"Colorbox trovate: {count_before}")

    # Rimuovi wrapper
    result, removed = remove_colorbox_wrappers(content)

    count_after = count_colorbox(result)

    print(f"Colorbox rimosse: {removed}")
    print(f"Colorbox rimaste: {count_after}")

    # Verifica
    if count_after > 0:
        print(f"\nATTENZIONE: {count_after} colorbox non rimosse (potrebbero essere pattern non standard)")

    # Scrivi risultato
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"\nFile salvato: {output_file}")
    print("\nPer verificare e applicare:")
    print(f"  diff {input_file} {output_file} | head -50")
    print(f"  pdflatex -interaction=nonstopmode {output_file}")
    print(f"  mv {output_file} {input_file}")

if __name__ == "__main__":
    main()
