import pytest
from pycc.token import Token
from pycc.file import File


class Test_Scanner:
    @pytest.fixture
    def target(self):
        from pycc.scanner import Scanner

        return Scanner

    @pytest.mark.parametrize(
        "src, expected",
        [
            ("", Token.EOF),
            ("x", Token.IDENTIFIER),
            ("_a0", Token.IDENTIFIER),
            ("z1", Token.IDENTIFIER),
            ("break", Token.BREAK),
            ("case", Token.CASE),
            ("char", Token.CHAR),
            ("continue", Token.CONTINUE),
            ("default", Token.DEFAULT),
            ("do", Token.DO),
            ("else", Token.ELSE),
            ("enum", Token.ENUM),
            ("if", Token.IF),
            ("int", Token.INT),
            ("long", Token.LONG),
            ("restrict", Token.RESTRICT),
            ("return", Token.RETURN),
            ("short", Token.SHORT),
            ("sizeof", Token.SIZEOF),
            ("switch", Token.SWITCH),
            ("typedef", Token.TYPEDEF),
            ("unsigned", Token.UNSIGNED),
            ("void", Token.VOID),
            ("while", Token.WHILE),
            ("0", Token.INTEGER_CONSTANT),
            ("1234567890", Token.INTEGER_CONSTANT),
            ("{", Token.LEFT_BRACE),
            ("}", Token.RIGHT_BRACE),
            ("(", Token.LEFT_PAREN),
            (")", Token.RIGHT_PAREN),
            ("[", Token.LEFT_BRACKET),
            ("]", Token.RIGHT_BRACKET),
            (".", Token.DOT),
            (",", Token.COMMA),
            (";", Token.SEMICOLON),
            ("<", Token.LESS_THAN),
            ("<=", Token.LESS_THAN_EQUALS),
            ("<<", Token.LESS_THAN_LESS_THAN),
            ("<<=", Token.LESS_THAN_LESS_THAN_EQUALS),
            (">", Token.GREATER_THAN),
            (">=", Token.GREATER_THAN_EQUALS),
            (">>", Token.GREATER_THAN_GREATER_THAN),
            (">>=", Token.GREATER_THAN_GREATER_THAN_EQUALS),
            ("=", Token.EQUALS),
            ("==", Token.EQUALS_EQUALS),
            ("!", Token.EXCLAMATION),
            ("!=", Token.EXCLAMATION_EQUALS),
            ("+", Token.PLUS),
            ("++", Token.PLUS_PLUS),
            ("+=", Token.PLUS_EQUALS),
            ("-", Token.MINUS),
            ("--", Token.MINUS_MINUS),
            ("-=", Token.MINUS_EQUALS),
            ("->", Token.ARROW),
            ("*", Token.STAR),
            ("*=", Token.STAR_EQUALS),
            ("/", Token.SLASH),
            ("/=", Token.SLASH_EQUALS),
            ("//", Token.SINGLE_LINE_COMMENT),
            ("/**/", Token.MULTI_LINE_COMMENT),
            ("%", Token.PERCENT),
            ("%=", Token.PERCENT_EQUALS),
            ("&", Token.AMPERSAND),
            ("&&", Token.AMPERSAND_AMPERSAND),
            ("&=", Token.AMPERSAND_EQUALS),
            ("|", Token.PIPE),
            ("||", Token.PIPE_PIPE),
            ("|=", Token.PIPE_EQUALS),
            ("^", Token.CARET),
            ("^=", Token.CARET_EQUALS),
            ("~", Token.TILDE),
            ("?", Token.QUESTION),
            (":", Token.COLON),
            ("@", Token.INVALID),
        ],
    )
    def test_token(self, target, src, expected):
        scanner = target(File("", src))
        assert scanner.scan() == expected
        assert scanner.text == src

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
    def test_identifier(self, target, src, text):
        scanner = target(File("", src))
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
    def test_integer_constant(self, target, src, tok, value):
        scanner = target(File("", src))
        assert scanner.scan() == tok, scanner.errors
        assert scanner.text == src
        if value is None:
            assert scanner.value is None
        else:
            assert scanner.value.value == value
            assert scanner.value.text == src

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
    def test_floating_constant(self, target, src, tok, value):
        scanner = target(File("", src))
        assert scanner.scan() == tok, scanner.errors
        assert scanner.text == src
        if value is None:
            assert scanner.value is None
        else:
            assert scanner.value.value == value
            assert scanner.value.text == src

    @pytest.mark.parametrize(
        "src", ["// aaa bbb", "// aaa bbb\n", "// aaabbb \r\n", "// aaa bbb\r"]
    )
    def test_single_line_comment(self, target, src):
        scanner = target(File("", src))
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
    def test_multi_line_comment(self, target, src):
        scanner = target(File("", src))
        assert scanner.scan() == Token.MULTI_LINE_COMMENT
        assert scanner.text == src
        assert scanner.line == len(src.splitlines())
