"""Import the target file."""

input_file = open("code_highlights.txt", "r")
content = input_file.read()
input_file.close()

# print(content)


def get_quotes(content):
    quotes_list = []
    sentence = ""
    switch = False
    for i in range(len(content)):
        if not switch:
            if content[i] == '"' and content[i + 1] != '"':
                switch = True
                continue
        if switch:
            if content[i] != '"':
                sentence += content[i]
            else:
                switch = False
                if sentence not in quotes_list:
                    quotes_list.append(f'"{sentence}"')

                sentence = ""
    return quotes_list


# quotes
quotes_list = get_quotes(content)
for item in quotes_list:
    content = content.replace(item, f"<code_quotes>{item}</code_quotes>")


def replace_strings_having_periods(content, string, target_color):
    string_copy = string.replace(".", " . ")
    string_copy = string_copy.split(" ")
    result = ""
    for word in string_copy:
        if word != ".":
            word = f"<{target_color}>{word}</{target_color}>"
        result += word

    return content.replace(string, result)


# yellowish
yellowish_custom = [
    "generate_ulid",
    "signup_token_email",
    "account_activation",
    "activation_resend",
    "token_expire_date",
    "get_current_site",
    "send_mail",
    "signup_page",
    "validate_password",
    "encrypt_email",
    "hexdigest",
    "utcnow",
    "timestamp",
    "randbits",
    "strftime",
    "decrypt_email",
]
for word in yellowish_custom:
    content = content.replace(word, f"<code_yellowish>{word}</code_yellowish>")
content = content.replace("redirect(", "<code_yellowish>redirect</code_yellowish>(")
content = content.replace("render(", "<code_yellowish>render</code_yellowish>(")
content = content.replace("print(", "<code_yellowish>print</code_yellowish>(")
content = content.replace("len(", "<code_yellowish>len</code_yellowish>(")
content = content.replace(".is_valid(", ".<code_yellowish>is_valid</code_yellowish>(")
content = content.replace(
    ".cleaned_data(", ".<code_yellowish>cleaned_data</code_yellowish>("
)
content = content.replace(".md5", ".<code_yellowish>md5</code_yellowish>")
content = content.replace(".create", ".<code_yellowish>create</code_yellowish>")
content = content.replace(".save", ".<code_yellowish>save</code_yellowish>")
content = content.replace(".delete", ".<code_yellowish>delete</code_yellowish>")
content = content.replace(".get", ".<code_yellowish>get</code_yellowish>")
content = content.replace(".error", ".<code_yellowish>error</code_yellowish>")

# blue
content = content.replace("request", "<code_blue>request</code_blue>")

# strong blue
strongblue_custom = [
    "UserRegistrationForm",
    "User",
    "TokenRegistration",
    "ActivationResend",
    "Meta",
    "Exception",
    "utils",
    "hashlib",
    "secrets",
    "datetime",
    "timedelta",
]
for word in strongblue_custom:
    content = content.replace(word, f"<code_strongblue>{word}</code_strongblue>")
content = content.replace(".forms", "<code_strongblue>.forms</code_strongblue>")
content = content.replace(".models", "<code_strongblue>.models</code_strongblue>")
# content = content.replace("utils.", "<code_strongblue>utils</code_strongblue>.")
content = content.replace("messages.", "<code_strongblue>messages</code_strongblue>.")
content = replace_strings_having_periods(content, "models.CharField", "code_strongblue")
content = replace_strings_having_periods(content, "models.Model", "code_strongblue")
content = replace_strings_having_periods(content, "forms.ModelForm", "code_strongblue")
content = replace_strings_having_periods(content, "forms.TextInput", "code_strongblue")
content = replace_strings_having_periods(content, "forms.EmailField", "code_strongblue")
content = replace_strings_having_periods(content, "django.core.mail", "code_strongblue")
content = replace_strings_having_periods(
    content, "django.contrib.sites.shortcuts", "code_strongblue"
)


# dark blue
content = content.replace("def ", "<code_darkblue>def</code_darkblue> ")
content = content.replace("= True", "= <code_darkblue>True</code_darkblue>")
content = content.replace("=True", "=<code_darkblue>True</code_darkblue>")
content = content.replace("= False", "= <code_darkblue>False</code_darkblue>")
content = content.replace("=False", "=<code_darkblue>False</code_darkblue>")
content = content.replace("class ", "<code_darkblue>class</code_darkblue> ")
content = content.replace(
    "f<code_quotes>", "<code_darkblue>f</code_darkblue><code_quotes>"
)


# purplish
content = content.replace("import ", "<code_purplish>import</code_purplish> ")
content = content.replace("from ", "<code_purplish>from</code_purplish> ")
content = content.replace("return ", "<code_purplish>return</code_purplish> ")
content = content.replace("for ", "<code_purplish>for</code_purplish> ")
content = content.replace("if ", "<code_purplish>if</code_purplish> ")
content = content.replace("else:", "<code_purplish>else</code_purplish>:")
content = content.replace("try:", "<code_purplish>try</code_purplish>:")
content = content.replace("except ", "<code_purplish>except</code_purplish> ")
content = content.replace("except:", "<code_purplish>except</code_purplish>:")
content = content.replace("{", "<code_purplish>{</code_purplish>")
content = content.replace("}", "<code_purplish>}</code_purplish>")

# to finish, change parenthesis' color in dark blue
content = content.replace("(", "<code_darkblue>(</code_darkblue>")
content = content.replace(")", "<code_darkblue>)</code_darkblue>")

content = f'<pre><div class="code">{content}</div></pre>'

input_file = open("code_highlights_rendered.txt", "w")
input_file.write(content)
input_file.close()
