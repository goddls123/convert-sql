import re
import sys
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

def remove_comments(sql):
    # Remove single line comments starting with --
    sql = re.sub(r'--.*', '', sql)
    # Remove multi-line comments starting with /* and ending with */
    sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
    return sql.strip()

def convert_to_mybatis_mapper(sql):
    """Convert SQL to MyBatis Mapper format with indentation."""
    # Create the root <mapper> element with a namespace attribute
    mapper = ET.Element('mapper', attrib={'namespace': 'YourNamespace'})
    
    # Create the <select> element with id and resultType attributes
    select = ET.SubElement(mapper, 'select', attrib={'id': 'yourSelectId', 'parameterType':'yourParamType', 'resultType': 'YourResultType'})
    
    # Maintain the indentation and formatting of the SQL content
    select.text = "\n\t    " + sql.strip().replace("\n", "\n\t    ") + "\n\t"

    # Generate a pretty-printed XML string
    xml_str = ET.tostring(mapper, encoding='utf-8')
    pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="    ")

    return pretty_xml_str

def process_files_in_folder(input_folder,output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.sql', '.txt')):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                sql_query = file.read()
                sql_content = remove_comments(sql_query)
                mapper = convert_to_mybatis_mapper(sql_content)

                output_filename = os.path.splitext(filename)[0].capitalize()
                output_mapper_file_path = os.path.join(output_folder, f"{output_filename}.xml")

                with open(output_mapper_file_path, 'w') as mapper_file:
                    mapper_file.write(mapper)

def main():
    input_folder = 'before'  # 바꾸고 싶은 파일 폴더
    output_folder = 'sql'  # 바뀌고 난 파일 폴더

    # Check if the input folder exists
    if not os.path.exists(input_folder):
        print(f"The input folder '{input_folder}' does not exist. Exiting.")
        return
    
    # Check if the input folder contains any files
    if not os.listdir(input_folder):
        print(f"The input folder '{input_folder}' is empty. Exiting.")
        return

    process_files_in_folder(input_folder,output_folder)

if __name__ == "__main__":
    main()