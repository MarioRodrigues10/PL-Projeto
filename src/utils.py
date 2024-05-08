def extract_text(lines):
    extracted_text = ""
    list = []
    bool = False
    for line in lines:
        if (line.startswith(":") or bool == True) and not ";" in line:
            extracted_text += line + " "
            bool = True
        elif ";" in line and bool == True:
            extracted_text += line
            bool = False
            new_text = extracted_text
            list.append(new_text)
            extracted_text = ""

        else:
            list.append(line)

    return list


def remove_enters(lines):
    new_lines = []
    for line in lines:
        new_line = line.replace("\n", "")
        new_lines.append(new_line)

    new_lines = [line for line in new_lines if line]
    return new_lines


def treat_inputs(lines):
    lines = extract_text(lines)
    lines = remove_enters(lines)
    return lines
