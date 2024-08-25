# sql-to-java

sql select 구문에서 colum 명을 java class의 DTO로 변경하는 실행 파일
before폴더에 .txt , .TXT, .sql, .SQL파일을 넣어두면
java 폴더안에 파일명의 java 클래스 파일 생성

_폴더명 바꾸려면_

```python
def main():
    input_folder = 'before'  # 바꾸고 싶은 파일 폴더
    output_folder = 'java'  # 바뀌고 난 파일 폴더
```

## sqlparse 설치 필요

```bash
pip3 install sqlparse
```

## 디렉토리 구조

```bash
/your_project_folder
    /before
        example.sql
        another_query.txt
    /java
        generate_java_class.exe
```
