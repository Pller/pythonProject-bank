import os
import re

def remove_trailing_whitespace(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Удалить пробелы в конце строк
    content = re.sub(r'[ \t]+\n', '\n', content)
    # Удалить пустые строки с пробелами
    content = re.sub(r'\n[ \t]+\n', '\n\n', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                print(f'Cleaning {filepath}')
                remove_trailing_whitespace(filepath)

if __name__ == '__main__':
    process_directory('src')
    process_directory('tests')
    print('Cleaning completed!')
