from bs4 import BeautifulSoup
import urllib3
import re

# This script contains functions to clean and set up input files for
# the LingPy library's input format. It runs a web scraper on Wiktionary
# articles that contain Swadesh lists and creates a csv file with the
# necessary columns for analysis in LingPy
#
# Author: Kate Collins

http = urllib3.PoolManager()
urllib3.disable_warnings()


# Converts list representation of Wiktionary Swadesh list article into
# a dictionary
# Params: list of headings in each table in article, list of tables in article
# Returns: dictionary representation of article
def swadesh_lists_to_dict(headings, tables):
    ipa_links_found = []
    new_swadesh_list_rows = []
    for table in tables:  # data split up into tables in Wiktionary article
        for row in table.find_all("tr")[1:]:  # each row is a different word. ignore header row
            table_links_found = []
            table_row = []
            links_in_cell = []
            for cell in row.find_all("td")[1:]:
                if cell and cell.get_text():
                    table_row.append(cell.get_text().split()[0])
                else:
                    table_row.append(str(None))
                links_in_cell += cell.find_all('a')
                if links_in_cell:
                    table_links_found.append(links_in_cell[0].get('href'))
                else:
                    table_links_found.append(str(None))
            new_swadesh_list_rows.append(table_row)
            ipa_links_found.append(table_links_found)

    dict_swadesh_list = []
    for i, row in enumerate(new_swadesh_list_rows):
        row_link_all = list(zip(headings, row, ipa_links_found[i]))
        dict_swadesh_list.append(row_link_all)

    return dict_swadesh_list


# creates intermediate file of all IPA strings found in article
# Params: dictionary Swadesh list, url base where IPA articles can be found
# Returns: None. Writes a file of IPA strings
def create_ipa_file(dict_of_rows, request_path):
    with open("input/ipa_tokens.txt", "w+") as f:
        for row in dict_of_rows:
            for cell_list in row:
                ipa_text = None
                if cell_list[2] is not None:
                    ipa_request = http.request('GET', request_path + cell_list[2])
                    ipa_request = ipa_request.data.decode('UTF-8')
                    ipa_query_soup = BeautifulSoup(ipa_request, "html.parser")
                    ipa_text = ipa_query_soup.find('span', {'class': 'IPA'})
                    if ipa_text:
                        ipa_text = ipa_text.get_text()
                f.write(str(ipa_text)+"\n")


# reads file of IPA strings and creates list of lists with LingPy input data,
# to write to csv file
# Params: file name, dictionary Swadesh list, headings used in table Swadesh list
# Returns: list of list of rows of output file
def read_ipa_file(file_name, dict_swadesh_list, headings):
    output_list_of_rows = []
    print(len(dict_swadesh_list[0]), len(headings))
    with open(file_name, "r") as f:
        accumulator = 0
        for i, row in enumerate(dict_swadesh_list):
            concept = row[0][1]
            for j, heading in enumerate(headings):
                print(row[j], len(row), len(row[j]))
                token = f.readline().strip().strip('[]/')
                token = ''.join(re.split(r'\W+', token))
                csv_row = [str(accumulator), concept, row[j][1].strip(','), token,  heading]
                print(csv_row)
                output_list_of_rows.append(csv_row)
            accumulator += 1
    return output_list_of_rows


# creates a csv output file in LingPy's format
# params: list of content for rows in output
# Returns: None. Writes output file
def create_lingpy_file(rows_to_output):
    with open("slavic.tsv", "w") as outfile:
        outfile.write("#\n")
        outfile.write("\t".join(['COGNACY', 'CONCEPT', 'COUNTERPART', 'IPA', 'DOCULECT']) + "\n")
        for row in rows_to_output:
            print(row)
            outfile.write("\t".join(row) + "\n")


def main():
    base = 'http://en.wiktionary.org'
    r = http.request('GET', base+'/wiki/Appendix:Slavic_Swadesh_lists')
    r = r.data.decode('UTF-8')

    soup = BeautifulSoup(r, "html.parser")
    all_tables = soup.findAll('table', {'class': 'wikitable'})

    all_headings = [th.get_text().strip() for th in all_tables[0].find("tr").find_all(["th", "td"])][1:]

    swadesh_dict = swadesh_lists_to_dict(all_headings, all_tables)
    create_ipa_file(swadesh_dict, base)
    rows_to_write = read_ipa_file("input/ipa_tokens.txt", swadesh_dict, all_headings)

    create_lingpy_file(rows_to_write)

if __name__ == "__main__":
    main()
