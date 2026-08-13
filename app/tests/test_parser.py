from app.services.parser import extract_text


def test_extract_text():
    html = """
    <html>
        <body>
            <h1>Hello</h1>
            <p>This is a test.</p>
        </body>
    </html>
    """

    result = extract_text(html)

    assert result == "Hello This is a test."


def test_extract_text_removes_scripts_and_styles():
    html = """
    <html>
        <head>
            <style>
                body { color: red; }
            </style>
        </head>
        <body>
            <h1>Hello</h1>
            <script>
                console.log("secret");
            </script>
            <p>Visible text</p>
        </body>
    </html>
    """

    result = extract_text(html)

    assert result == "Hello Visible text"
    assert "secret" not in result
    assert "color: red" not in result


def test_extract_text_empty_html():
    result = extract_text("")

    assert result == ""