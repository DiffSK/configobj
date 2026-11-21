from configobj import ConfigObj


def test_merge_writes_comments_for_new_entries():
    destination = ConfigObj([
        "[Section1]",
        "# Keep the destination comment",
        "existing = old # keep inline",
    ])
    source = ConfigObj([
        "[Section1]",
        "# Source comment for an existing entry",
        "existing = new # source inline",
        "# A new scalar",
        "added = foo # scalar inline",
        "# A new subsection",
        "[[Section2]] # section inline",
        "option2 = bar",
    ])

    destination.merge(source)

    assert destination.write() == [
        "[Section1]",
        "# Keep the destination comment",
        "existing = new # keep inline",
        "# A new scalar",
        "added = foo # scalar inline",
        "# A new subsection",
        "[[Section2]] # section inline",
        "option2 = bar",
    ]
