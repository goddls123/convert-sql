import os
import sqlparse
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0].lower() + ''.join(x.title() for x in components[1:])

def parse_identifier(identifier):
    parts = identifier.split('--')
    col_name = parts[0].strip()

    if ' AS ' in col_name.upper():
        col_name = col_name.upper().split(' AS ', 1)[1].strip()
    elif '.' in col_name:
        col_name = col_name.split('.')[-1].strip()

    annotation = parts[1].strip() if len(parts) > 1 else None
    return col_name, annotation

def extract_columns_and_annotations(sql_query):
    parsed = sqlparse.parse(sql_query)
    statement = parsed[0]
    columns = []
    annotations =[]
    select_seen = False
    for token in statement.tokens:
        if select_seen:
            if isinstance(token, sqlparse.sql.IdentifierList):
                for identifier in token.get_identifiers():
                    col_name, annotation = parse_identifier(str(identifier).strip())
                    columns.append(col_name)
                    annotations.append(annotation)
            elif isinstance(token, sqlparse.sql.Identifier):
                col_name, annotation = parse_identifier(str(token).strip())
                columns.append(col_name)
                annotations.append(annotation)
            elif token.ttype is sqlparse.tokens.Keyword:
                break
        if token.ttype is sqlparse.tokens.DML and token.value.upper() =='SELECT':
            select_seen = True
    return columns, annotations

def generate_java_class(class_name, columns, annotations):
    class_template = f"public class {class_name} {{\n"
    for col,anno in zip(columns, annotations):
        camel = to_camel_case(col) 
        if anno:
            class_template += f"    private String {camel};  //{anno}\n"
        else:
            class_template += f"    private String {camel};\n"

    # 아래 코드는 getter setter 생성하려면 
    # class_template += "\n    // Getters and Setters\n"
    # for col in columns:
    #     class_template += f"    public String get{col.capitalize()}() {{\n"
    #     class_template += f"        return {col};\n"
    #     class_template += "    }\n\n"
    #     class_template += f"    public void set{col.capitalize()}(String {col}) {{\n"
    #     class_template += f"        this.{col} = {col};\n"
    #     class_template += "    }\n\n"
    class_template += "}\n"
    return class_template

def process_files_in_folder(input_folder,output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.sql', '.txt')):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                sql_query = file.read()
                columns ,annotations= extract_columns_and_annotations(sql_query)
                class_name = os.path.splitext(filename)[0].capitalize()
                java_class_content = generate_java_class(class_name, columns,annotations)
                output_java_file_path = os.path.join(output_folder, f"{class_name}.java")
                with open(output_java_file_path, 'w') as java_file:
                    java_file.write(java_class_content)
                # print(f"Generated {output_java_file_path}")

def main():
    input_folder = 'before'  # 바꾸고 싶은 파일 폴더
    output_folder = 'java'  # 바뀌고 난 파일 폴더

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