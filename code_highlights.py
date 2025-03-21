import re
import code_highlights_colors

input_file = open("code_highlights.txt", "r")
content = input_file.read()
input_file.close()


def syntax_highlighter(content):
    content_lines = content.splitlines()

    print("Number of lines in the code:", len(content_lines))

    words_purplish = code_highlights_colors.words_purplish
    words_strongblue = code_highlights_colors.words_strongblue
    words_yellowish = code_highlights_colors.words_yellowish
    words_darkblue = code_highlights_colors.words_darkblue
    words_blue = code_highlights_colors.words_blue

    new_content = ""
    sentence = ""
    quotes_lines = []

    parenthesis = False
    parenthesis_counter = 0
    startwith_from = False
    is_quote = False
    split_quote = False
    format_quote = False

    def_titles = words_yellowish
    strong_blue_titles = []
    brackets_list = ["(", ")", "{", "}"]
    skip = ["", " ", ".", "(", ")", ",", "+", "="]

    for word in words_strongblue:
        strong_blue_titles.append(word)
    print(f"\tstrong_blue_titles: {strong_blue_titles}")

    def startswith_from(line):
        new_line = ""

        for word in re.split("(\W)", line):
            if word in words_purplish:
                word = f"<code_purplish>{word}</code_purplish>"
            elif word in words_yellowish:
                word = f"<code_yellowish>{word}</code_yellowish>"
            elif word in skip:
                pass
            else:
                if word not in strong_blue_titles:
                    strong_blue_titles.append(word)
                word = f"<code_strongblue>{word}</code_strongblue>"

            new_line += f"{word}"

        return f"{new_line}"

    def startswith_def(line):
        # print(f"LINE DEF* {line}")
        new_line = ""
        new_line += f"<code_darkblue>{line[:3]}</code_darkblue>"
        line = line[3:]
        def_titles.append(line.strip().split("(")[0])

        in_parenthesis = ""
        for g in range(len(line)):
            if line[g] == "(":
                g += 1
                while line[g] != ")":
                    in_parenthesis += line[g]
                    g += 1
                break

        formatted_words = ""
        if "," in in_parenthesis:
            in_parenthesis = re.split(("(,)"), in_parenthesis)
            print(f"in_parenthesis: {in_parenthesis}")
            for word in in_parenthesis:
                if word != ",":
                    word = f"<code_blue>{word}</code_blue>"
                formatted_words += word
        else:
            formatted_words = f"<code_blue>{in_parenthesis}</code_blue>"
        print(f"formatted_words: {formatted_words}")

        for h in range(len(line)):
            if line[h] == "(":
                new_line += f"{line[:h+1]}{formatted_words}):"
                break

        print(f"LIIIINE: {new_line}")

        # new_line += line

        return f"{new_line}"

    def startswith_class(line):
        new_line = ""
        new_line += f"<code_darkblue>{line[:5]}</code_darkblue>"
        line = line[5:]
        line_words = re.split("(\W)", line)
        print(f"\n\tclass line: {line_words}")
        for h in range(len(line_words)):
            if line_words[h].isalpha():
                if line_words[h] not in strong_blue_titles:
                    strong_blue_titles.append(line_words[h])
        for word in strong_blue_titles:
            if word in line:
                line = line.replace(word, f"<code_strongblue>{word}</code_strongblue>")
        print(f"new class line: {line}")
        new_line += line

        return f"{new_line}"

    def other_type(line):
        is_blue = False
        blue_words = ""
        new_line = ""
        if '"' not in line:
            for word in re.split("(\W)", line):
                if word in words_purplish:
                    word = f"<code_purplish>{word}</code_purplish>"
                elif word in skip:
                    pass
                elif word in strong_blue_titles:
                    word = f"<code_strongblue>{word}</code_strongblue>"
                else:
                    if not word.isdigit():
                        word = f"<code_blue>{word}</code_blue>"

                new_line += f"{word}"
            # print(f"DONE LINE: {line}")
            return f"{new_line}"

    def quote_curly_brackets(format_quote, line):
        if not format_quote:
            return line
        else:
            in_brackets = ""
            new_line = ""
            for g in range(len(line)):
                if line[g] == "{":
                    new_line += f"{line[: g + 1]}"
                    g += 1
                    while line[g] != "}":
                        in_brackets += line[g]
                        g += 1
                    new_line += f"{other_type(in_brackets)}{line[g:]}"
                    break
            new_line = new_line.replace("{", "<code_brackets>{</code_brackets>")
            new_line = new_line.replace("}", "<code_brackets>}</code_brackets>")

            return new_line

    print(
        quote_curly_brackets(
            True,
            'glubutl = f"this is a test with a variable {variable_here} and other things"',
        )
    )

    # Colors lists:
    # words_purplish <code_purplish>
    # words_strongblue <code_strongblue>
    # words_yellowish <code_yellowish>
    # words_darkblue <code_darkblue>
    # words_blue <code_blue>

    def quote_check_line(line):
        pass

    def check_line(line):
        tab = ""
        skip_characters = "#@"

        if line.strip() == "":
            return "\n"

        for i in range(len(line)):
            if line[i].isalpha() or line[i] in skip_characters:
                break
            else:
                tab += " "

        new_line = ""
        comment_part = ""

        if "#" in line:
            if line.strip().startswith("#"):
                new_line += f"{tab}<code_comment>{line.strip()}</code_comment>\n"
            else:
                for i in range(len(line)):
                    if line[i] == "#":
                        comment_part = f" <code_comment>{line[i:]}</code_comment>"
                        line = line[:i]
                        break

        if line.strip().startswith("from") and not line.strip().endswith("("):
            new_line += f"{tab}{startswith_from(line.strip())}\n"
        elif line.strip().startswith("import"):
            new_line += f"{tab}{startswith_from(line.strip())}{comment_part}\n"
        elif line.strip().startswith("def"):
            new_line += f"{tab}{startswith_def(line.strip())}{comment_part}\n"
        elif line.strip().startswith("class"):
            new_line += f"{tab}{startswith_class(line.strip())}{comment_part}\n"
        elif line.strip().startswith("@"):
            new_line += f"{tab}<code_yellowish>{(line.strip())}</code_yellowish>{comment_part}\n"
        elif parenthesis and not startwith_from:
            new_line += f"{other_type(line)}"
        elif parenthesis and startwith_from:
            new_line += f"{startswith_from(line)}"
        else:
            if '"' not in line and "#" not in line:
                if not is_quote:
                    new_line += f"{other_type(line)}\n"
                else:
                    new_line += f"{other_type(line)}"

        return new_line

    def triple_quote(format_quote, line, line_num, split_quote):
        new_line = ""
        n = 0

        while n != len(line):
            if line[n : n + 3] == '"""':

                # ----- IF THE QUOTE IS SPLIT -----
                if '"""' not in line[(n + 3) :] and not split_quote:
                    split_quote = True
                    if line[:n]:
                        # print(f"LINE1: {line[:n]}")
                        new_line += f"{check_line(line[:n])}<code_quotes>{line[n:]}"
                    else:
                        new_line += f"<code_quotes>{line[n:]}"
                    new_line += "\n"
                    quotes_lines.append(line_num + 1)
                    line_num += 1
                    break

                if split_quote:
                    new_line += f"{line[:n+3]}</code_quotes>"
                    line = line[n + 3 :]
                    if line:
                        # print(f"not yet: {line}")
                        if '"""' in line:
                            n = 0
                            split_quote = False
                            # print("continue")
                            continue
                        else:
                            new_line += f"{check_line(line)}"
                            split_quote = False

                    else:
                        pass
                        # print("end of line")
                    # print(line)
                    split_quote = False
                    new_line += "\n"
                    quotes_lines.append(line_num + 1)
                    print("before line_num += 1")
                    line_num += 1
                    break

                # ----- IF THE QUOTE IS ON ONE LINE -----
                else:
                    print("QUOTE ON ONE LINE")
                    if line[:n]:
                        print(f"line[:n]: {line[:n]}, {line}")
                        # new_line += f"{check_line(line[n])}"
                        new_line += f"{check_line(line[:n])}<code_quotes>{line[n]}"
                        print(f"triple quote new_line 1: {new_line}")
                    else:
                        new_line += f"<code_quotes>{line[n]}"
                        print(f"triple quote new_line 2: {new_line}")
                    n += 1
                    while line[n : n + 3] != '"""':
                        new_line += line[n]
                        n += 1
                    new_line += f"{line[n:n+3]}</code_quotes>"
                    line = line[n + 3 :]
                    if line:
                        print(f"not yet2: {line}")
                        new_line += f"{check_line(line)}"
                    new_line += "\n"
                    quotes_lines.append(line_num + 1)

                    break
            else:
                n += 1
                continue

        print(f"\tnew_line: {new_line}")
        if format_quote:
            new_line = new_line.replace(
                '<code_blue>f</code_blue><code_quotes>"',
                '<code_darkblue>f</code_darkblue><code_quotes>"',
            )
        new_line = quote_curly_brackets(format_quote, new_line)

        return new_line, line_num, split_quote

    for line_num in range(len(content_lines)):
        line = content_lines[line_num]
        new_line = ""
        line_done = False

        if '"""' in line and not line.strip().startswith("def"):
            if '"""' in line:
                quote_mark = '"""'
            elif "'" in line:
                quote_mark = "'"
            else:
                quote_mark = '"'

            is_quote = True
            if 'f"""' in line:
                format_quote = True

            new_line, line_num, split_quote = triple_quote(
                format_quote, line, line_num, split_quote
            )
            format_quote = False

        elif '"""' not in line and split_quote:
            is_quote = True
            new_line += f"{line}\n"
            quotes_lines.append(line_num + 1)

        else:
            if is_quote:
                new_line += f"{check_line(line)}\n"
                is_quote = False
            line_num += 1
        if is_quote:
            new_content += f"{new_line}"

        print(quotes_lines, line_num)

        if line.strip().endswith("("):
            parenthesis = True
        if parenthesis:
            if line.strip().startswith("from"):
                startwith_from = True
            if "(" in line:
                parenthesis_counter += 1
            if ")" in line:
                parenthesis_counter -= 1
            if not line.strip().endswith(")"):
                new_content += f"{check_line(line)}\n"
                line_num += 1
                continue
            else:
                new_content += f"{check_line(line)}\n"
                if parenthesis_counter == 0:
                    parenthesis = False
                    if startwith_from:
                        startwith_from = False

        else:
            if not is_quote:
                new_content += f"{check_line(line)}"

    # for func_title in def_titles:
    #     print(f"func_title: {func_title}")
    #     new_content = new_content.replace(
    #         func_title, f"<code_yellowish>{func_title}</code_yellowish>"
    #     )
    # for bracket in brackets_list:
    #     new_content = new_content.replace(
    #         bracket, f"<code_brackets>{bracket}</code_brackets>"
    #     )

    new_content_lines = new_content.split("\n")
    for line_number in range(len(new_content_lines)):
        if line_number + 1 not in quotes_lines:
            new_content_lines[line_number] = new_content_lines[line_number].replace(
                "len(", "<code_yellowish>len</code_yellowish>("
            )
            for func_title in def_titles:
                new_content_lines[line_number] = new_content_lines[line_number].replace(
                    func_title, f"<code_yellowish>{func_title}</code_yellowish>"
                )
            for bracket in brackets_list:
                new_content_lines[line_number] = new_content_lines[line_number].replace(
                    bracket, f"<code_brackets>{bracket}</code_brackets>"
                )

    total_lines = len(new_content_lines)

    final_content = ""
    print("Number of lines in the code:", total_lines)
    for line_number in range(total_lines):
        final_content += f"<line_number>{line_number + 1}</line_number>    {new_content_lines[line_number]}\n"

    # print(f'\n***** new_content:\n<pre><div class="code">{final_content}</div></pre>')
    content = f'<pre><div class="code">{final_content}</div></pre>'
    # print(f"\nFUNCTIONS TITLES: {def_titles}")
    # print(f"\nSTRONG_BLUE TITLES: {strong_blue_titles}")

    print(f"quotes_lines: {quotes_lines}")

    input_file = open("code_highlights_rendered.txt", "w")
    input_file.write(content)
    input_file.close()

    return content


syntax_highlighter(content)

# TESTING DIFFERENT THINGS:

# input_file = open("message_file.txt", "r")
# message_content = input_file.read()
# input_file.close()


# def make_dictionary(message_content):
#     message_dictionary = {}

#     message_content = message_content.split("\n")

#     for i in message_content:
#         if i.strip():
#             i = i.split(" ")
#             message_dictionary[int(i[0])] = i[1]

#     message_dictionary = dict(sorted(message_dictionary.items()))

#     return message_dictionary


# def get_numbers(message_dictionary):
#     return [i for i in message_dictionary]


# def make_pyramid(numbers):
#     i = 0
#     numbers_to_keep = []
#     numbers_string = ""
#     pyramid = []
#     while numbers:
#         for u in range(i + 1):
#             numbers_string += f"{numbers[u]} "
#         i += 1
#         numbers = numbers[i:]
#         pyramid.append(numbers_string[:-1])
#         numbers_to_keep.append(numbers_string.strip().split(" ")[-1])
#         numbers_string = ""
#     return pyramid, numbers_to_keep


# def decode(message_file):
#     message_dictionary = make_dictionary(message_file)

#     numbers = get_numbers(message_dictionary)

#     print(f"numbers: {numbers}")

#     pyramid, numbers_to_keep = make_pyramid(numbers)
#     for line in pyramid:
#         print(line)

#     final_string = ""
#     for number in numbers_to_keep:
#         final_string += f"{message_dictionary[int(number)]} "
#     return final_string[:-1]


# print(decode(message_content))


# def get_decimals(number, desired_decimal):
#     try:
#         number = float(number)
#     except ValueError:
#         return "\nBad input, please enter a number."

#     number = str(number).split(".")
#     result = float(f"{number[0]}.{number[1][:desired_decimal]}")
#     return result


# print(get_decimals(45.778, 2))
# print(get_decimals("45.778", 2))
# print(get_decimals(-45.778, 2))
# print(get_decimals("-45.778", 2))
# print(get_decimals("45.77a8", 2))

# print(f"{1.29999:.3f}")


# import decimal

# my_decimal = decimal.Decimal("-1.29999")
# rounded_decimal_1 = my_decimal.quantize(
#     decimal.Decimal(".000"), rounding=decimal.ROUND_HALF_UP
# )
# rounded_decimal_2 = my_decimal.quantize(
#     decimal.Decimal(".000"), rounding=decimal.ROUND_FLOOR
# )

# # All in one line:
# rounded_decimal_3 = decimal.Decimal("-1.29999").quantize(
#     decimal.Decimal(".000"), rounding=decimal.ROUND_FLOOR
# )
# print(rounded_decimal_1, rounded_decimal_2, rounded_decimal_3)


# def draw_crown(height, width, symbol):
#     if width < 5:
#         return print(
#             "Please enter a number greater than 5 (it starts getting nice from 9)"
#         )

#     x = int((width - 3) / 2)
#     endings = 1

#     if width % 2 == 0:
#         middle = 2
#     else:
#         middle = 1

#     for i in range(height):
#         spaces = " " * x
#         if x <= 0:
#             print(symbol * width)
#         else:
#             print(f"{symbol*endings}{spaces}{symbol*middle}{spaces}{symbol*endings}")
#             endings += 1
#             middle += 2
#             x -= 2


# draw_crown(7, 13, "*")
# draw_crown(20, 41, "@")

#############################
# def draw_star(size, symbol):
#     if size % 2 == 0 or size < 5:
#         return print("Please enter an ODD number >= 5.")
#     spaces = int((size - 3) / 2)
#     a = 0
#     while a != spaces + 1:
#         space = " " * (spaces - a)
#         print(f"{' '*a}{symbol}{space}{symbol}{space}{symbol}")
#         a += 1

#     print(symbol * size)

#     while a != 0:
#         a -= 1
#         space = " " * (spaces - a)
#         print(f"{' '*a}{symbol}{space}{symbol}{space}{symbol}")


# draw_star(7, "o")

#############################
# sentence = "I love my little furball panda. Maybe I overfed him a bit too much..."
# print(sentence[::-1])

# print("".join(reversed(sentence)))


# reversed_sentence = ""
# for i in range(len(sentence) - 1, -1, -1):
#     reversed_sentence += sentence[i]
# print(reversed_sentence)

# u = [sentence[i] for i in range(len(sentence) - 1, -1, -1)]
# for x in u:
#     print(x, end="")


#############################
# html_text = """
# <body>
#     <header class="header">
#     <h1 class="header-title">text text</h1>
#     <h2 id="h2_id">H2 title</h2>
#     <nav class="main-nav">
#         <ul class="nav-list">
#             <li class="nav-item"><a href class="a-item">item</a></li>
#             <li class="nav-item"><a href class="a-item">item</a></li>
#             <li class="nav-item"><a href class="a-item">item</a></li>
#             <li class="nav-item"><a href class="a-item">item</a></li>
#         </ul>
#     <p id="p_id01">Text text</p>
# </body>
# """


# def convert_html_classes_to_css(text):
#     classes = []
#     ids = []
#     is_class = False
#     is_id = False
#     for line in text.split("\n"):
#         class_item = ""
#         if line:
#             u = 0
#             while u != len(line):
#                 if line[u] == '"':
#                     if line[:u].endswith("id="):
#                         is_id = True
#                     else:
#                         is_class = True
#                     u += 1
#                     while line[u] != '"':
#                         class_item += line[u]
#                         u += 1
#                     if class_item not in classes:
#                         if is_id:
#                             ids.append(class_item)
#                             is_id = False
#                         elif is_class:
#                             classes.append(class_item)
#                             is_class = False
#                     class_item = ""
#                 u += 1

#     for item in classes:
#         print(f".{item}", "{\n")
#         print("}\n")
#     for item in ids:
#         print(f"#{item}", "{\n")
#         print("}\n")


# convert_html_classes_to_css(html_text)


#############################

# sign = "+"
# print("  10")
# print(f"{sign} 15")
# print("----")
# print("____")
