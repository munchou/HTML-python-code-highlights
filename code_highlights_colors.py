# purplish
words_purplish = [
    "from",
    "import",
    "return",
]

# strong blue
words_strongblue = [
    "forms",
    "ModelForm",
    "utils",
    "Meta",
    "Exception",
    "hashlib",
    "secrets",
    "datetime",
    "timedelta",
]

# yellowish
words_yellowish = [
    "send_mail",
    "encrypt_email",
    "hexdigest",
    "utcnow",
    "timestamp",
    "randbits",
    "strftime",
    "randbits",
    "format",
    "render",
    "redirect",
    "login",
    "authenticate",
    "get_user_model",
    "login_required",
    "validate_password",
    "render_to_string",
    "get_current_site",
    "force_bytes",
    "urlsafe_base64_encode",
    "urlsafe_base64_decode",
]

words_darkblue = []  # "def", parenthesis
words_blue = []  # for ex "request"


"""
<code_comment>
<code_quotes>
<code_yellowish>
<code_blue>
<code_strongblue>
<code_darkblue> (def, (, ), ... )
<code_purplish> (from, import, return, ...)

# to finish, change parenthesis' color in dark blue
content = content.replace("(", "<code_darkblue>(</code_darkblue>")
content = content.replace(")", "<code_darkblue>)</code_darkblue>")
"""
