from vimbot.bot.process_response import add_target_blank, process_markdown


def test_add_target_blank():
    # Test case 1: Check if target="_blank" is added to links
    html = '<a href="https://example.com">Example</a>'
    expected_output = '<a href="https://example.com" target="_blank">Example</a>'
    assert add_target_blank(html) == expected_output

    # Test case 2: Check if multiple links are handled correctly
    html = '<a href="https://example1.com">Example1</a><a href="https://example2.com">Example2</a>'
    expected_output = '<a href="https://example1.com" target="_blank">Example1</a><a href="https://example2.com" target="_blank">Example2</a>'
    assert add_target_blank(html) == expected_output

    # Test case 3: Check if non-link tags are left unchanged
    html = '<p>This is a paragraph.</p><a href="https://example.com">Example</a>'
    expected_output = '<p>This is a paragraph.</p><a href="https://example.com" target="_blank">Example</a>'
    assert add_target_blank(html) == expected_output


def test_process_markdown():
    # Test case 1: Check if markdown is converted to HTML correctly
    markdown = "# Heading\n\nThis is a paragraph."
    expected_output = "<h1>Heading</h1>\n<p>This is a paragraph.</p>\n"
    assert process_markdown(markdown) == expected_output

    # Test case 2: Check if links in markdown are converted to HTML links
    markdown = "Visit [Example](https://example.com) for more information."
    expected_output = (
        '<p>Visit <a href="https://example.com">Example</a> for more information.</p>\n'
    )
    assert process_markdown(markdown) == expected_output


def test_integration():
    # Test case: Check if the entire process works as expected
    markdown = "# Anemia\n\nFor more information, visit:\n\n- [American Society of Hematology](https://www.hematology.org/Patients/Anemia.aspx)\n- [National Institute of Diabetes and Digestive and Kidney Diseases](https://www.niddk.nih.gov/health-information/anemia)"
    expected_output = '<h1>Anemia</h1>\n<p>For more information, visit:</p>\n<ul>\n<li><a href="https://www.hematology.org/Patients/Anemia.aspx" target="_blank">American Society of Hematology</a></li>\n<li><a href="https://www.niddk.nih.gov/health-information/anemia" target="_blank">National Institute of Diabetes and Digestive and Kidney Diseases</a></li>\n</ul>\n'
    assert add_target_blank(process_markdown(markdown)) == expected_output
