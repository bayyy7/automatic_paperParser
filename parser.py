import xml.etree.ElementTree as ET
import json
import os

input_directory = "Dataset"
output_directory = "JSON_parsed"

os.makedirs(output_directory, exist_ok=True)

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

def extract_text_elements(root, start_tag, end_tag):
    """Extracts text content from XML elements between start_tag and end_tag."""
    text_content = []
    collecting = False
    for elem in root.iter():
        if elem.tag.endswith(start_tag):
            collecting = True
        elif elem.tag.endswith(end_tag):
            break
        if collecting and elem.tag.endswith('p'):
            text_content.append(' '.join(elem.itertext()))
    return ' '.join(text_content)

def process_xml_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        xml_data = file.read()

    tree = ET.ElementTree(ET.fromstring(xml_data))
    root = tree.getroot()

    titles = root.find('.//tei:titleStmt//tei:title', ns).text

    authors = []
    for author in root.findall('.//tei:author', ns):
        forename = author.find('.//tei:forename', ns)
        surname = author.find('.//tei:surname', ns)
        email = author.find('.//tei:email', ns)
        author_info = {
            'name': f"{forename.text if forename is not None else ''} {surname.text if surname is not None else ''}".strip(),
            'email': email.text if email is not None else ''
        }
        authors.append(author_info)

    abstract_elem = root.find('.//tei:abstract//tei:p', ns)
    abstract_text = ''.join(abstract_elem.itertext()) if abstract_elem is not None else ''

    full_text = []
    in_section = False
    current_section = {}
    for elem in root.iter():
        tag_name = elem.tag.split('}')[-1]  # Remove namespace
        if tag_name == 'head' and in_section:
            full_text.append(current_section)
            current_section = {}
            in_section = False
        if tag_name == 'head':
            in_section = True
            current_section['title'] = elem.text
            current_section['content'] = []
        if in_section and tag_name == 'p':
            current_section['content'].append(''.join(elem.itertext()))

    if in_section:
        full_text.append(current_section)

    # Extract references
    references = []
    for bibl in root.findall('.//tei:listBibl//tei:biblStruct', ns):
        ref_authors = []
        for author in bibl.findall('.//tei:author', ns):
            ref_forename = author.find('.//tei:forename', ns)
            ref_surname = author.find('.//tei:surname', ns)
            ref_authors.append(f"{ref_forename.text if ref_forename is not None else ''} {ref_surname.text if ref_surname is not None else ''}".strip())

        title = bibl.find('.//tei:title', ns)
        pub_date = bibl.find('.//tei:date', ns)

        references.append({
            'authors': ref_authors,
            'title': title.text if title is not None else '',
            'publication_date': pub_date.text if pub_date is not None else ''
        })

    structured_data = {
        "teiHeader": {
            "fileDesc": {
                "titleStmt": {
                    "title": titles
                },
                "publicationStmt": {
                    "date": root.find('.//tei:publicationStmt//tei:date', ns).text if root.find('.//tei:publicationStmt//tei:date', ns) is not None else ''
                },
                "sourceDesc": {
                    "biblStruct": {
                        "authors": authors
                    }
                }
            }
        },
        "profileDesc": {
            "abstract": abstract_text
        },
        "text": {
            "body": full_text
        },
        "back": {
            "references": references
        }
    }
    json_filename = os.path.join(output_directory, f"{titles}.json")
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(structured_data, json_file, indent=4)

# Process all XML files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.xml'):
        file_path = os.path.join(input_directory, filename)
        process_xml_file(file_path)

print("All files have been processed and saved as JSON in the 'JSON_parsed' directory.")