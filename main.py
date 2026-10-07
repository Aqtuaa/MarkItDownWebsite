from markitdown import MarkItDown

def convert_file(input_path, output_path):
    md = MarkItDown()
    result = md.convert(input_path)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result.text_content)

    print("Conversion success:", output_path)


if __name__ == "__main__":
    input_file = "test.pdf"     
    output_file = "output.md"

    convert_file(input_file, output_file)