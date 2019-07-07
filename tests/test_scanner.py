import pytest
from pycc.token import Token, KEYWORDS, PUNCTUATORS


class Test_Scanner:
    @pytest.fixture
    def factory(self):
        from pycc.scanner import Scanner
        from pycc.file import File
        from pycc.error import Reporter

        def factory(text):
            return Scanner(File("", text), Reporter())

        return factory

    @pytest.mark.parametrize(
        "src, expected",
        [
            ("", Token.EOF),
            ("x", Token.IDENTIFIER),
            ("_a0", Token.IDENTIFIER),
            ("z1", Token.IDENTIFIER),
            ("0", Token.INTEGER_CONSTANT),
            ("1234567890", Token.INTEGER_CONSTANT),
            ("@", Token.INVALID),
        ],
    )
    def test_token(self, factory, src, expected):
        scanner = factory(src)
        assert scanner.scan() == expected
        assert scanner.text == src

    @pytest.mark.parametrize("keyword, expected", [(x.value, x) for x in KEYWORDS])
    def test_keyword(self, factory, keyword, expected):
        scanner = factory(keyword)
        assert scanner.scan() == expected
        assert scanner.text == keyword

    @pytest.mark.parametrize(
        "punctuator, expected", [(x.value, x) for x in PUNCTUATORS]
    )
    def test_punctuator(self, factory, punctuator, expected):
        scanner = factory(punctuator)
        assert scanner.scan() == expected
        assert scanner.text == punctuator

    @pytest.mark.parametrize(
        "punctuator, expected",
        [
            ("<:", Token.LEFT_BRACKET),
            (":>", Token.RIGHT_BRACKET),
            ("<%", Token.LEFT_BRACE),
            ("%>", Token.RIGHT_BRACE),
            ("%:", Token.HASH),
            ("%:%:", Token.HASH_HASH),
        ],
    )
    def test_digraph(self, factory, punctuator, expected):
        scanner = factory(punctuator)
        assert scanner.scan() == expected
        assert scanner.text == punctuator

    @pytest.mark.parametrize(
        "src, text",
        [
            ("_\n", "_"),
            ("a b", "a"),
            ("a_", "a_"),
            ("p29^3", "p29"),
            ("aaa+1", "aaa"),
            ("__111", "__111"),
            ("あああ", "あああ"),
        ],
    )
    def test_identifier(self, factory, src, text):
        scanner = factory(src)
        assert scanner.scan() == Token.IDENTIFIER
        assert scanner.text == text

    @pytest.mark.parametrize(
        "src, tok, value",
        [
            ("1", Token.INTEGER_CONSTANT, 1),
            ("1234567890", Token.INTEGER_CONSTANT, 1234567890),
            ("0", Token.INTEGER_CONSTANT, 0),
            ("012345670", Token.INTEGER_CONSTANT, int("012345670", base=8)),
            ("0000", Token.INTEGER_CONSTANT, 0),
            ("0x0", Token.INTEGER_CONSTANT, 0),
            ("0x1234567890", Token.INTEGER_CONSTANT, 0x1234567890),
            ("123u", Token.INTEGER_CONSTANT, 123),
            ("123U", Token.INTEGER_CONSTANT, 123),
            ("123l", Token.INTEGER_CONSTANT, 123),
            ("123L", Token.INTEGER_CONSTANT, 123),
            ("123ll", Token.INTEGER_CONSTANT, 123),
            ("123ull", Token.INTEGER_CONSTANT, 123),
            ("123ULL", Token.INTEGER_CONSTANT, 123),
            ("123lL", Token.INVALID, None),
            ("123UULL", Token.INVALID, None),
            ("123UULL", Token.INVALID, None),
            ("0x123AALZ", Token.INVALID, None),
            ("123UULLZZZ000", Token.INVALID, None),
            ("0x", Token.INVALID, None),
        ],
    )
    def test_integer_constant(self, factory, src, tok, value):
        scanner = factory(src)
        assert scanner.scan() == tok
        assert scanner.text == src
        assert scanner.value == value

    @pytest.mark.parametrize(
        "src, tok, value",
        [
            ("1.0", Token.FLOATING_CONSTANT, 1.0),
            (".1", Token.FLOATING_CONSTANT, 0.1),
            ("1.", Token.FLOATING_CONSTANT, 1.0),
            ("1.0e3", Token.FLOATING_CONSTANT, 1000.0),
            ("1.0E2", Token.FLOATING_CONSTANT, 100.0),
            ("1.0e+10", Token.FLOATING_CONSTANT, 1.0 * (10 ** 10)),
            ("1.0e-2", Token.FLOATING_CONSTANT, 0.01),
            ("10e3", Token.FLOATING_CONSTANT, 10000.0),
            ("10e-2", Token.FLOATING_CONSTANT, 0.1),
            ("10e+2", Token.FLOATING_CONSTANT, 1000.0),
            ("0.0123456789", Token.FLOATING_CONSTANT, 0.0123456789),
            ("1.2", Token.FLOATING_CONSTANT, 1.2),
            ("1.0f", Token.FLOATING_CONSTANT, 1.0),
            ("1.0L", Token.FLOATING_CONSTANT, 1.0),
            ("0x1fffp10", Token.FLOATING_CONSTANT, float.fromhex("0x1fffp10")),
            ("0x1.fffp10", Token.FLOATING_CONSTANT, float.fromhex("0x1.fffp10")),
            ("0x1.fffp+10", Token.FLOATING_CONSTANT, float.fromhex("0x1.fffp+10")),
            ("0x1.fffp-10", Token.FLOATING_CONSTANT, float.fromhex("0x1.fffp-10")),
            ("1.0e", Token.INVALID, None),
            ("1.0e+", Token.INVALID, None),
            ("0x1.0e10", Token.INVALID, None),
            ("0.10p10", Token.INVALID, None),
            ("0x1.0p", Token.INVALID, None),
        ],
    )
    def test_floating_constant(self, factory, src, tok, value):
        scanner = factory(src)
        assert scanner.scan() == tok
        assert scanner.text == src
        assert scanner.value == value

    @pytest.mark.parametrize(
        "src, tok, value",
        [
            ("'a'", Token.CHARACTER_CONSTANT, "a"),
            ("'ab'", Token.CHARACTER_CONSTANT, "ab"),
            (r"'\n'", Token.CHARACTER_CONSTANT, "\n"),
            (r"'\&'", Token.CHARACTER_CONSTANT, "&"),
            (r"'\1'", Token.CHARACTER_CONSTANT, chr(0o1)),
            (r"'\12'", Token.CHARACTER_CONSTANT, chr(0o12)),
            (r"'\123'", Token.CHARACTER_CONSTANT, chr(0o123)),
            (r"'\12a'", Token.CHARACTER_CONSTANT, chr(0o12) + "a"),
        ],
    )
    def test_character_constant(self, factory, src, tok, value):
        scanner = factory(src)
        assert scanner.scan() == tok
        assert scanner.text == src
        assert scanner.value == value

    @pytest.mark.parametrize(
        "src", ["// aaa bbb", "// aaa bbb\n", "// aaabbb \r\n", "// aaa bbb\r"]
    )
    def test_single_line_comment(self, factory, src):
        scanner = factory(src)
        assert scanner.scan() == Token.SINGLE_LINE_COMMENT
        assert scanner.text == src

    @pytest.mark.parametrize(
        "src",
        [
            "/***********/",
            "/* aaa bbb */",
            "/* aaa\nbbb */",
            "/* aaabbb \r */",
            "/** \r\n ** \n **/",
        ],
    )
    def test_multi_line_comment(self, factory, src):
        scanner = factory(src)
        assert scanner.scan() == Token.MULTI_LINE_COMMENT
        assert scanner.text == src
        assert scanner.line == len(src.splitlines())
