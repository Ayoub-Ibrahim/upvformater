def convert_to_moodle_format(input_text):
    lines = input_text.strip().split("\n")
    output = ""
    question = ""
    options = []
    for line in lines:
        line = line.strip()  
        if line.startswith("<qm>"):
            question = ""
            options = []
        elif line.startswith("<op>"):
            option_text = line.replace("<op>", "").strip()
            options.append(option_text)
        elif line.startswith("</qm>"):
            if question and options:
                output += f"{question.strip()}? {{\n"
                for option in options:
                    if "<rc>" in option:
                        output += f"~%50%{option.replace('<rc>', '').strip()}\n"  
                    else:
                        output += f"~%-50%{option.strip()}\n" 
                output += "}\n\n"
            question = ""
            options = []
        else:
            question = line.strip()
    return output.strip()

def convert_input_to_gift(input_text):
    lines = input_text.strip().split('\n')
    if len(lines) < 3:
        raise ValueError("Input format is incorrect. Ensure there are at least three lines: <qm>, the question, and <op><rc> with the answer.")
    question_text = lines[1].strip()
    answer_line = lines[2].replace('<op><rc>', '').strip()
    if not question_text or not answer_line:
        raise ValueError("Question text or answer line is missing.")
    parts = answer_line.split(',')
    if len(parts) != 2:
        raise ValueError("Answer line format is incorrect. Ensure it contains a numeric value and a tolerance separated by a comma.")
    numeric_value, tolerance = parts
    gift_format = f"{question_text} {{#\n={numeric_value}:0\n=%50%{numeric_value}:{tolerance}\n}}"
    return gift_format
