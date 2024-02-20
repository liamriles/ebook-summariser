import os
import glob
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def title_from_soup(soup):
    # Attempt to find chapter title from headings, starting from h1 to h5
    for i in range(1, 6):
        title = soup.find(f'h{i}')
        if title:
            return title.get_text(strip=True)
    # If no title is found, return None
    return None

def epub_to_txt(epub_path):
    # Load the EPUB file
    book = epub.read_epub(epub_path)

    # Iterate through each item in the EPUB file
    for idx, item in enumerate(book.get_items_of_type(ebooklib.ITEM_DOCUMENT)):
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        
        # Extract text from the parsed HTML
        text = soup.get_text()

        # Define a filename for the output TXT file, formatting the chapter number with leading zeros
        epub_filename = os.path.splitext(os.path.basename(epub_path))[0]
        chapter_filename = f'{epub_filename}_chapter_{idx + 1:03}.txt'

        # Write the extracted text to a TXT file
        with open(chapter_filename, 'w', encoding='utf-8') as text_file:
            text_file.write(text)

        print(f'Chapter {idx + 1} saved as {chapter_filename}')

if __name__ == "__main__":
    # Find all .epub files in the current directory
    epub_files = glob.glob('*.epub')
    
    # Process each found EPUB file
    for epub_file in epub_files:
        print(f'Processing {epub_file}...')
        epub_to_txt(epub_file)
