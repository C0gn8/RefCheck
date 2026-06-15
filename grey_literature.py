def is_grey_literature(reference):

    reference = reference.lower()

    indicators = [

        "available from",

        "http://",
        "https://",
        "www.",

        "department of health",

        "wellcome trust",

        "framework",

        "guidance",

        "policy",

        "report",

        "national institute",

        "national survivor user network",

        "nsun"
    ]

    for indicator in indicators:

        if indicator in reference:

            return True

    return False
