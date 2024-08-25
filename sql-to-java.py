import os
import re
import sqlparse

def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0].lower() + ''.join(x.title() for x in components[1:])


def extract_columns(sql_query):
    parsed = sqlparse.parse(sql_query)
    statement = parsed[0]
    columns = []
    annotations =[]
    select_seen = False
    for token in statement.tokens:
        if select_seen:
            if isinstance(token, sqlparse.sql.IdentifierList):
                for identifier in token.get_identifiers():
                    stringList= str(identifier).strip().split('--')
                    if len(stringList)>1:
                        annotations.append(stringList[1].strip())
                    else:
                        annotations.append(None)
                    columns.append(stringList[0])
            elif isinstance(token, sqlparse.sql.Identifier):
                columns.append(str(token).strip())
            elif token.ttype is sqlparse.tokens.Keyword:
                break
        if token.ttype is sqlparse.tokens.DML and token.value.upper() =='SELECT':
            select_seen = True
    return [columns,annotations]

def generate_java_class(class_name, columns,annotations):
    class_template = f"public class {class_name} {{\n"
    for col,anno in zip(columns,annotations):
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
        if filename.endswith(".sql") or filename.endswith(".SQL") or filename.endswith(".txt") or filename.endswith(".TXT"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r') as file:
                sql_query = file.read()
                [columns ,annotations]= extract_columns(sql_query)
                print(columns,annotations)
                class_name = os.path.splitext(filename)[0].capitalize()
                java_class_content = generate_java_class(class_name, columns,annotations)
                output_java_file_path = os.path.join(output_folder, f"{class_name}.java")
                with open(output_java_file_path, 'w') as java_file:
                    java_file.write(java_class_content)
                print(f"Generated {output_java_file_path}")

def main():
    input_folder = 'before'  # Folder containing your SQL and text files
    output_folder = 'after'  # Folder where the Java files will be saved
    process_files_in_folder(input_folder,output_folder)

if __name__ == "__main__":
    main()