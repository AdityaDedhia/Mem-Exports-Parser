import datetime
import requests


def read_md_contents():
    raw_line_count = 0
    body_line_count = 0
    linespaces_count = 0
    mem_count = 0
    storage_links = 0
    external_links = 0
    current_check = False
    no_title = False

    for line in open('export.md', 'r'):
        raw_line_count += 1

        if not current_check:
            current_check = True
            mem_count += 1
            no_title = False

            if "![]" in line:
                storage_links += 1
                formatted_title = 'File' + str(storage_links)
            elif "[" in line:
                external_links += 1
                formatted_title = 'Link' + str(external_links)
            else:
                if len(str(line)) > 74:
                    no_title = True
                    formatted_title = str(line).replace("# ", "").replace("/", " or ")[:75] + '...'
                else:
                    formatted_title = str(line).replace("# ", "").replace("/", " or ")[:75]

            current_mem = open(f'Mems/{formatted_title}.md', 'w')
            if no_title:
                current_mem.write(f'{line}\n')
        else:
            if str(line).startswith('---'):
                current_mem.close()
                current_check = False
                raw_line_count -= 1  # To factor out end-of-mem denotation
            else:
                body_line_count += 1
                if str(line).startswith(' '):
                    linespaces_count += 1

                current_mem.write(f'{line}\n')

                if "![]" in line:
                    storage_links += 1
                    body_line_count -= 1
                elif "[" in line:
                    external_links += 1


    percent_empty = "%.1f%%" % (linespaces_count/body_line_count * 100)
    f = open('Mem Stats.md', 'w')
    f.write('# Mem Stats\n')
    f.write(f'Total Mems: {mem_count}\n')
    f.write(f'Raw Lines (includes titles/files): {raw_line_count} | Body Lines: {body_line_count} '
            f'| Blank Lines: {linespaces_count} | {percent_empty} empty\n')
    f.write(f'Storage Files: {storage_links}\nWeb Links: {external_links} \n')
    f.close()


def read_json_contents():
    pass


if __name__ == '__main__':
    print("Welcome to Mem Exporter. Press your option:\n1)Markdown Export (simple)\n2) JSON "
          "Export (advanced)")
    valid = False

    while not valid:
        value = input("Enter a valid option:\n")
        value = int(value)
        if value == 1:
            valid = True
            read_md_contents()
        if value == 2:
            Valid = True
            read_json_contents()

    print("Mem export successfully generated!")
