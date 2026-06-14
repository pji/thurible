"""
test_man
~~~~~~~~

Unit tests for the clireader.man module.
"""
from collections import namedtuple

import pytest as pt

from thurible import man


# Fixtures.
@pt.fixture
def doc_indent():
    return (
        '.RS 4\n'
        '.P\n'
        'This paragraph is indented.\n'
        '.P\n'
        'This one proves the indentation persists.\n'
    )


@pt.fixture
def indent_base():
    return (
        '        This paragraph\n'
        '        is indented.\n'
        '\n'
        '        This one proves\n'
        '        the indentation\n'
        '        persists.\n'
        '\n'
    )


@pt.fixture
def indent_outdent():
    return (
        '    The indentation is\n'
        '    removed.\n'
        '\n'
        '    The indentation is\n'
        '    still removed.\n'
        '\n'
    )


@pt.fixture
def vals():
    TestStrings = namedtuple('TestStrings', [
        'head',
        'indent',
        'line_0',
        'line_1',
        'line_2',
        'tag_0',
        'tag_1',
        'opt_name_0', 'opt_arg_0',
        'opt_name_1', 'opt_arg_1',
        'opt_name_2', 'opt_arg_2',
    ])
    return TestStrings(
        'spam',
        '1',
        'eggs bacon',
        'ham baked beans',
        'tomato',
        'muffin',
        'toast',
        'coffee', '-c',
        'orange', '-o',
        'tea', '-t',
    )


@pt.fixture
def w():
    return 24


# Common terminal command strings.
BOLD = '\x1b[1m'
LINK = '\x1b]8'
NML = '\x1b(B\x1b[m'
ST = '\x1b\\'
UDLN = '\x1b[4m'


# Test cases.
class TestDocument:
    def test_ip_indent_persists_until_p(self, indent_base, indent_outdent, w):
        """An indent set by the .IP macro should last until a .P macro."""
        doc = (
            '.IP  8\n'
            'This paragraph is indented.\n'
            '.IP\n'
            'This one proves the indentation persists.\n'
            '.P \n'
            'The indentation is removed.\n'
            '.IP\n'
            'The indentation is still removed.\n'
        )
        assert man.main(doc, w) == (
            f'{indent_base}'
            f'{indent_outdent}'
        )

    def test_rs_margin_persists(self, doc_indent, indent_base, w):
        """Indentation from the .RS macro should persist to the
        next paragraph.
        """
        assert man.main(doc_indent, w) == indent_base

    def test_re_changes_margin(
        self, doc_indent,
        indent_base,
        indent_outdent,
        w
    ):
        """.RE should reduce indentation from the next paragraph."""
        doc = (
            f'{doc_indent}'
            '.RE 4\n'
            '.P \n'
            'The indentation is removed.\n'
            '.P\n'
            'The indentation is still removed.\n'
        )
        assert man.main(doc, w) == (
            f'{indent_base}'
            f'{indent_outdent}'
        )

    def test_sh_removes_margin(
        self, doc_indent,
        indent_base,
        indent_outdent,
        w
    ):
        """.SH should reset the margin location."""
        doc = (
            f'{doc_indent}'
            '.SH SPAM\n'
            'The indentation is removed.\n'
            '.P\n'
            'The indentation is still removed.\n'
        )
        assert man.main(doc, w) == (
            f'{indent_base}'
            f'{BOLD}SPAM{NML}\n'
            f'{indent_outdent}'
        )

    def test_ss_removes_margin(
        self, doc_indent,
        indent_base,
        indent_outdent,
        w
    ):
        """.SS should reset the margin location."""
        doc = (
            f'{doc_indent}'
            '.SS SPAM\n'
            'The indentation is removed.\n'
            '.P\n'
            'The indentation is still removed.\n'
        )
        assert man.main(doc, w) == (
            f'{indent_base}'
            f'  {BOLD}SPAM{NML}\n'
            f'{indent_outdent}'
        )

    def test_tp_indent_persists_until_p(self, indent_outdent, w):
        """An indent set by the .TP macro should last until a .P macro."""
        doc = (
            '.TP 8\n'
            'Spam\n'
            'This paragraph is indented.\n'
            '.TP\n'
            'Eggs\n'
            'This one proves the indentation persists.\n'
            '.P \n'
            'The indentation is removed.\n'
            '.TP\n'
            '\n'
            'The indentation is still removed.\n'
        )
        assert man.main(doc, w) == (
            'Spam    This paragraph\n'
            '        is indented.\n'
            '\n'
            'Eggs    This one proves\n'
            '        the indentation\n'
            '        persists.\n'
            '\n'
            f'{indent_outdent}'
        )


class TestLex:
    # Document structure macros.
    def test_example(self):
        """When encountering an example begin macro (.EX), the Lexer
        should begin collecting the following lines into a token until
        an example end macro (.EE) is encountered. Then return the
        correct token.
        """
        s0 = 'spam'
        s1 = 'eggs bacon'
        text = (
            '.EX\n'
            f'{s0}\n'
            f'{s1}\n'
            '.EE\n'
        )
        assert man.lex(text) == (man.Example([
            man.Text(s0),
            man.Text(s1),
        ]),)

    def test_relative_indent_end(self):
        """When encountering a relative indent start header macro (.RE)
        and up to one parameter, the Lexer should return the correct
        token.
        """
        s = '2'
        text = f'.RE {s}'
        assert man.lex(text) == (man.RelativeIndentEnd(s),)

    def test_relative_indent_end_without_param(self):
        """When encountering a relative indent start header macro (.RE)
        without a parameter, the Lexer should return the correct token.
        """
        s = '1'
        text = f'.RE'
        assert man.lex(text) == (man.RelativeIndentEnd(s),)

    def test_relative_indent_end_without_param(self):
        """When encountering a relative indent start header macro (.RE)
        without a parameter, the Lexer should return the correct token.
        """
        text = f'.RE'
        assert man.lex(text) == (man.RelativeIndentEnd('1'),)

    def test_relative_indent_start(self):
        """When encountering a relative indent start header macro (.RS)
        without a parameter, the Lexer should return the correct token.
        """
        s = '2'
        text = f'.RS {s}'
        assert man.lex(text) == (man.RelativeIndentStart(s),)

    def test_relative_indent_start_without_param(self):
        """When encountering a relative indent start header macro (.RS)
        and up to one parameter, the Lexer should return the correct
        token.
        """
        text = f'.RS'
        assert man.lex(text) == (man.RelativeIndentStart('1'),)

    def test_section(self):
        """When encountering a section header macro (.SH) and one
        parameter, the Lexer should return the correct token.
        """
        s = 'spam'
        text = f'.SH {s}'
        exp = (man.Section(s),)

    def test_section_with_params_in_next_line(self, vals):
        """When encountering a section header macro (.SH) with a
        parameter on the next line, the Lexer should return the correct
        token.
        """
        text = (
            f'.SH {vals.head}\n'
            f'{vals.line_0}\n'
            f'{vals.line_1}\n'
        )
        assert man.lex(text) == (man.Section(vals.head, [
            man.Text(vals.line_0),
            man.Text(vals.line_1),
        ]),)

    def test_section_with_following_text(self, vals):
        """When encountering a section header macro (.SH) with a
        parameter on the next line and following text lines, the
        lexer should return the correct token.
        """
        text = (
            '.SH\n'
            f'{vals.head}\n'
            f'{vals.line_0}\n'
            f'{vals.line_1}\n'
        )
        assert man.lex(text) == (man.Section(vals.head, [
            man.Text(vals.line_0),
            man.Text(vals.line_1),
        ]),)

    def test_subheading(self, vals):
        """When encountering a subheading macro (.SS) and up to
        five parameters, the Lexer should return the correct token.
        """
        text = (
            f'.SS {vals.head}\n'
            f'{vals.line_0}\n'
            f'{vals.line_1}\n'
        )
        assert man.lex(text) == (man.Subheading(vals.head, [
            man.Text(vals.line_0),
            man.Text(vals.line_1),
        ]),)

    def test_subheading_with_following_text(self, vals):
        """When encountering a subheading macro (.SS) with a
        parameter on the next line and following text lines, the
        lexer should return the correct token.
        """
        text = (
            '.SS\n'
            f'{vals.head}\n'
            f'{vals.line_0}\n'
            f'{vals.line_1}\n'
        )
        assert man.lex(text) == (man.Subheading(vals.head, [
            man.Text(vals.line_0),
            man.Text(vals.line_1),
        ]),)

    def test_title(self):
        """When encountering a title header macro (.TH) and up to
        five parameters, the Lexer should return the correct token.
        """
        title = 'spam'
        section = '1'
        foot_middle = 'eggs'
        foot_inside = 'bacon'
        head_middle = 'hame'
        text = (
            f'.TH {title}'
            f' {section}'
            f' {foot_middle}'
            f' {foot_inside}'
            f' {head_middle}'
        )
        assert man.lex(text) == (man.Title(
            title,
            section,
            foot_middle,
            foot_inside,
            head_middle
        ),)

    # Paragraph macros.
    def test_indented_paragraph(self, vals):
        """When encountering an indented paragraph macro (.IP), the
        Lexer should begin collecting the following lines into a token
        then return a Paragraph token containing the collected text.
        """
        indent = '1'
        text = (
            f'.IP {vals.head} {indent}\n'
            f'{vals.line_0}\n'
            f'{vals.line_1}\n'
            f'.B {vals.line_2}\n'
        )
        assert man.lex(text) == (man.IndentedParagraph(vals.head, indent, [
            man.Text(vals.line_0),
            man.Text(vals.line_1),
            man.Bold(vals.line_2),
        ]), )

    def test_paragraph(self, vals):
        """When encountering a paragraph macro (.P), the Lexer
        should begin collecting the following lines into a token then
        return a Paragraph token containing the collected text.
        """
        text = (
            '.P\n'
            f'{vals.line_0}\n'
            f'{vals.line_1}\n'
        )
        exp = (man.Paragraph([
            man.Text(vals.line_0),
            man.Text(vals.line_1),
        ]),)

    def test_paragraph_lp(self, vals):
        """When encountering a paragraph macro (.LP), the Lexer
        should begin collecting the following lines into a token then
        return a Paragraph token containing the collected text.
        """
        text = (
            '.LP\n'
            f'{vals.line_0}\n'
            f'{vals.line_1}\n'
        )
        exp = (man.Paragraph([
            man.Text(vals.line_0),
            man.Text(vals.line_1),
        ]),)

    def test_paragraph_pp(self, vals):
        """When encountering a paragraph macro (.PP), the Lexer
        should begin collecting the following lines into a token then
        return a Paragraph token containing the collected text.
        """
        text = (
            '.PP\n'
            f'{vals.line_0}\n'
            f'{vals.line_1}\n'
        )
        exp = (man.Paragraph([
            man.Text(vals.line_0),
            man.Text(vals.line_1),
        ]),)

    def test_paragraph_with_empty_token(self, vals):
        """When encountering a paragraph macro (.P), the Lexer
        should begin collecting the following lines into a token then
        return a Paragraph token containing the collected text.
        """
        text = (
            '.P\n'
            f'{vals.line_0}\n'
            f'{vals.line_1}\n'
            f'{vals.line_2}\n'
        )
        exp = (man.Paragraph([
            man.Empty(vals.line_0),
            man.Text(vals.line_1),
            man.Text(vals.line_2),
        ]),)

    def test_tagged_paragraph(self, vals):
        """When encountering a tagged paragraph macro (.TP), the Lexer
        should collect an optional parameter on the same line as the
        indentation level, a parameter on the next line as a tag, and
        the following lines as the paragraph. It should then return a
        TaggedParagraph token.
        """
        indent = '1'
        text = (
            f'.TP {vals.indent}\n'
            f'{vals.head}\n'
            f'{vals.line_0}\n'
            f'{vals.line_1}\n'
            f'.B {vals.line_2}\n'
        )
        assert man.lex(text) == (man.TaggedParagraph(
            vals.indent,
            [vals.head,],
            [
                man.Text(vals.line_0),
                man.Text(vals.line_1),
                man.Bold(vals.line_2),
            ]
        ),)

    def test_tagged_paragraph_with_TQ(self, vals):
        """When encountering a tagged paragraph macro (.TQ), the Lexer
        should collect an optional parameter on the same line as the
        indentation level, a parameter on the next line as a tag, and
        the following lines as the paragraph. It should then return a
        TaggedParagraph token.
        """
        text = (
            f'.TP {vals.indent}\n'
            f'{vals.head}\n'
            '.TQ\n'
            f'{vals.tag_0}\n'
            '.TQ\n'
            f'{vals.tag_1}\n'
            f'{vals.line_0}\n'
            f'{vals.line_1}\n'
        )
        assert man.lex(text) == (man.TaggedParagraph(
            vals.indent,
            [vals.head, vals.tag_0, vals.tag_1],
            [man.Text(vals.line_0), man.Text(vals.line_1),]
        ),)

    # Command synopsis macros.
    def test_synopsis(self, vals):
        """When encountering a synopsis begin macro (.SY), the lexer
        should begin collecting lines and tokens until it reaches a
        synopsis end macro (.YS) macro. The lexer should then return
        a Synopsis token containing the collected tokens.
        """
        text = (
            f'.SY {vals.head}\n'
            '.YS'
        )
        assert man.lex(text) == (man.Synopsis(vals.head),)

    def test_synopsis_with_option(self, vals):
        """When encountering an option macro (.OP) after a synopsis
        begin macro (.SY) but before a synopsis end macro (.YS), the
        lexer should. The lexer should then return a Synopsis token
        containing the collected tokens.
        """
        text = (
            f'.SY {vals.head}\n'
            f'.OP {vals.opt_name_0} '
            f'{vals.opt_arg_0}\n'
            '.YS'
        )
        assert man.lex(text) == (man.Synopsis(vals.head, [man.Option(
            vals.opt_name_0,
            vals.opt_arg_0
        ),]),)

    def test_synopsis_with_option_and_multiple_synopses(self, vals):
        """When encountering a synopsis begin macro (.SY) after a
        synopsis begin macro (.SY) but before a synopsis end macro
        (.YS), the lexer should then return a Synopsis token
        containing the collected tokens.
        """
        text = (
            f'.SY {vals.head}\n'
            f'.OP {vals.opt_name_0} '
            f'{vals.opt_arg_0}\n'
            f'.OP {vals.opt_name_1} '
            f'{vals.opt_arg_1}\n'
            f'.SY {vals.tag_0}\n'
            f'.OP {vals.opt_name_2} '
            f'{vals.opt_arg_2}\n'
            '.YS'
        )
        assert man.lex(text) == (man.Synopsis(vals.head, [
            man.Option(vals.opt_name_0, vals.opt_arg_0),
            man.Option(vals.opt_name_1, vals.opt_arg_1),
            man.Synopsis(vals.tag_0, []),
            man.Option(vals.opt_name_2, vals.opt_arg_2),
        ]),)

    # Hyperlink and email macros.
    def test_email_address(self):
        """When encountering an email address begin macro (.MT), the
        lexer should collect the email address from the parameter and
        the following lines as hypertext until it reaches an email
        address end macro (.ME). It should then return an EmailAddress
        token with the collected data.
        """
        address = 'fred.foonly@fubar.net'
        name = 'Fred Foonly'
        punct = '!'
        text = (
            f'.MT {address}\n'
            f'{name}\n'
            f'.ME {punct}\n'
        )
        assert man.lex(text) == (man.EmailAddress(
            address,
            [man.Text(name),],
            punct
        ),)

    def test_url(self):
        """When encountering a URL begin macro (.UR), the lexer should
        collect the URL from the parameter and the following lines as
        hypertext until it reaches an URL end macro (.UE). It should
        then return a Url token with the collected data.
        """
        url = 'https://www.gnu.org/software/groff'
        tag = 'groff'
        punct = '!'
        text = (
            f'.UR {url}\n'
            f'{tag}\n'
            f'.UE {punct}\n'
        )
        assert man.lex(text) == (man.Url(url, [man.Text(tag),], punct),)

    # Font style macros.
    def test_bold(self, vals):
        """When encountering a bold macro (.B) while collecting lines
        for a multiline macro, the lexer should create a Bold token
        with the given text and add the token to the token for the
        multiline macro.
        """
        text = (
            '.P\n'
            f'{vals.line_0}\n'
            f'.B {vals.line_1}\n'
            f'{vals.line_2}\n'
        )
        assert man.lex(text) == (man.Paragraph([
            man.Text(vals.line_0),
            man.Bold(vals.line_1),
            man.Text(vals.line_2),
        ]),)

    def test_bold_with_param_in_next_line(self, vals):
        """When encountering a bold macro (.B) while collecting lines
        for a multiline macro, the lexer should create a Bold token
        with the given text and add the token to the token for the
        multiline macro.
        """
        text = (
            '.P\n'
            f'{vals.line_0}\n'
            '.B\n'
            f'{vals.line_1}\n'
            f'{vals.line_2}\n'
        )
        assert man.lex(text) == (man.Paragraph([
            man.Text(vals.line_0),
            man.Bold(vals.line_1),
            man.Text(vals.line_2),
        ]),)

    def test_bold_italics(self, vals):
        """When encountering a bold italics macro (.BI) while collecting
        lines for a multiline macro, the lexer should create a
        BoldItalic token with the given text and add the token to the
        token for the multiline macro.
        """
        text = (
            '.P\n'
            f'{vals.line_0}\n'
            f'.BI {vals.line_1}\n'
            f'{vals.line_2}\n'
        )
        assert man.lex(text) == (man.Paragraph([
            man.Text(vals.line_0),
            man.BoldItalic(vals.line_1),
            man.Text(vals.line_2),
        ]),)

    def test_bold_roman(self, vals):
        """When encountering a bold roman macro (.BR) while collecting
        lines for a multiline macro, the lexer should create a
        BoldRoman token with the given text and add the token to the
        token for the multiline macro.
        """
        text = (
            '.P\n'
            f'{vals.line_0}\n'
            f'.BR {vals.line_1}\n'
            f'{vals.line_2}\n'
        )
        assert man.lex(text) == (man.Paragraph([
            man.Text(vals.line_0),
            man.BoldRoman(vals.line_1),
            man.Text(vals.line_2),
        ]),)

    def test_italics(self, vals):
        """When encountering an italics macro (.I) while collecting
        lines for a multiline macro, the lexer should create a Italics
        token with the given text and add the token to the token for
        the multiline macro.
        """
        text = (
            '.P\n'
            f'{vals.line_0}\n'
            f'.I {vals.line_1}\n'
            f'{vals.line_2}\n'
        )
        assert man.lex(text) == (man.Paragraph([
            man.Text(vals.line_0),
            man.Italic(vals.line_1),
            man.Text(vals.line_2),
        ]),)

    def test_italics_with_param_in_next_line(self, vals):
        """When encountering an italics macro (.I) while collecting
        lines for a multiline macro, the lexer should create an Italics
        token with the given text and add the token to the token for
        the multiline macro.
        """
        text = (
            '.P\n'
            f'{vals.line_0}\n'
            '.I\n'
            f'{vals.line_1}\n'
            f'{vals.line_2}\n'
        )
        assert man.lex(text) == (man.Paragraph([
            man.Text(vals.line_0),
            man.Italic(vals.line_1),
            man.Text(vals.line_2),
        ]),)

    def test_italic_bold(self, vals):
        """When encountering a italics bold macro (.IB) while collecting
        lines for a multiline macro, the lexer should create a
        ItalicBold token with the given text and add the token to the
        token for the multiline macro.
        """
        text = (
            '.P\n'
            f'{vals.line_0}\n'
            f'.IB {vals.line_1}\n'
            f'{vals.line_2}\n'
        )
        assert man.lex(text) == (man.Paragraph([
            man.Text(vals.line_0),
            man.ItalicBold(vals.line_1),
            man.Text(vals.line_2),
        ]),)

    def test_italic_roman(self, vals):
        """When encountering a italics roman macro (.IR) while collecting
        lines for a multiline macro, the lexer should create a
        ItalicRoman token with the given text and add the token to the
        token for the multiline macro.
        """
        text = (
            '.P\n'
            f'{vals.line_0}\n'
            f'.IR {vals.line_1}\n'
            f'{vals.line_2}\n'
        )
        assert man.lex(text) == (man.Paragraph([
            man.Text(vals.line_0),
            man.ItalicRoman(vals.line_1),
            man.Text(vals.line_2),
        ]),)

    def test_roman_bold(self, vals):
        """When encountering a roman bold macro (.RB) while collecting
        lines for a multiline macro, the lexer should create a
        RomanBold token with the given text and add the token to the
        token for the multiline macro.
        """
        text = (
            '.P\n'
            f'{vals.line_0}\n'
            f'.RB {vals.line_1}\n'
            f'{vals.line_2}\n'
        )
        assert man.lex(text) == (man.Paragraph([
            man.Text(vals.line_0),
            man.RomanBold(vals.line_1),
            man.Text(vals.line_2),
        ]),)

    def test_roman_italic(self, vals):
        """When encountering a roman italic macro (.RI) while collecting
        lines for a multiline macro, the lexer should create a
        RomanItalic token with the given text and add the token to the
        token for the multiline macro.
        """
        text = (
            '.P\n'
            f'{vals.line_0}\n'
            f'.RI {vals.line_1}\n'
            f'{vals.line_2}\n'
        )
        assert man.lex(text) == (man.Paragraph([
            man.Text(vals.line_0),
            man.RomanItalic(vals.line_1),
            man.Text(vals.line_2),
        ]),)

    def test_small(self, vals):
        """When encountering an small macro (.SM) while collecting
        lines for a multiline macro, the lexer should create a Small
        token with the given text and add the token to the token for
        the multiline macro.
        """
        text = (
            '.P\n'
            f'{vals.line_0}\n'
            f'.SM {vals.line_1}\n'
            f'{vals.line_2}\n'
        )
        assert man.lex(text) == (man.Paragraph([
            man.Text(vals.line_0),
            man.Small(vals.line_1),
            man.Text(vals.line_2),
        ]),)

    def test_small_with_param_in_next_line(self, vals):
        """When encountering a small macro (.SM) while collecting
        lines for a multiline macro, the lexer should create a Small
        token with the given text and add the token to the token for
        the multiline macro.
        """
        text = (
            '.P\n'
            f'{vals.line_0}\n'
            '.SM\n'
            f'{vals.line_1}\n'
            f'{vals.line_2}\n'
        )
        assert man.lex(text) == (man.Paragraph([
            man.Text(vals.line_0),
            man.Small(vals.line_1),
            man.Text(vals.line_2),
        ]),)

    def test_small_bold(self, vals):
        """When encountering an small bold macro (.SB) while collecting
        lines for a multiline macro, the lexer should create a SmallBold
        token with the given text and add the token to the token for
        the multiline macro.
        """
        text = (
            '.P\n'
            f'{vals.line_0}\n'
            f'.SB {vals.line_1}\n'
            f'{vals.line_2}\n'
        )
        assert man.lex(text) == (man.Paragraph([
            man.Text(vals.line_0),
            man.SmallBold(vals.line_1),
            man.Text(vals.line_2),
        ]),)

    def test_small_bold_with_param_in_next_line(self, vals):
        """When encountering a small bold macro (.SB) while collecting
        lines for a multiline macro, the lexer should create a SmallBold
        token with the given text and add the token to the token for
        the multiline macro.
        """
        text = (
            '.P\n'
            f'{vals.line_0}\n'
            '.SB\n'
            f'{vals.line_1}\n'
            f'{vals.line_2}\n'
        )
        assert man.lex(text) == (man.Paragraph([
            man.Text(vals.line_0),
            man.SmallBold(vals.line_1),
            man.Text(vals.line_2),
        ]),)

    def test_text(self, vals):
        """When encountering a line that doesn't start with a macro,
        the lexer should create a Text token with the given text.
        """
        text = (
            f'{vals.line_0}\n'
            f'{vals.line_1}\n'
        )
        assert man.lex(text) == (
            man.Text(vals.line_0),
            man.Text(vals.line_1),
        )

    # Other macros.
    def test_empty(self):
        """When encountering a line that starts with a period but
        doesn't contain a recognized macro, the lexer should
        collect the line and return it in a Empty token.
        """
        text = '.spam\n'
        assert man.lex(text) == (man.Empty('spam'),)


class TestParse:
    def test_simplest_doc(self, w):
        """Given the simplest document, the parse should return a
        string containing its contents.
        """
        tokens = (man.Text('spam'),)
        assert man.parse(tokens, w) == 'spam'

    def test_doc_with_simple_title(self, w):
        """Given the simplest document, the parser should return a
        string containing its contents.
        """
        tokens = (
            man.Title('spam'),
            man.Text('eggs'),
        )
        assert man.parse(tokens, w) == (
            'SPAM                SPAM\n'
            '\n'
            '\n'
            '\n'
            'eggs\n'
            '\n'
            '\n'
            '                    SPAM\n'
        )

    def test_doc_with_complex_title(self, w):
        """Given a document with a complex title, the parser should
        return a string containing its contents.
        """
        tokens = (
            man.Title('spam', '1', '1/1/70', 'ham', 'bacon'),
            man.Text('eggs'),
        )
        assert man.parse(tokens, w) == (
            'SPAM(1)  bacon   SPAM(1)\n'
            '\n'
            '\n'
            '\n'
            'eggs\n'
            '\n'
            '\n'
            'ham    1/1/70    SPAM(1)\n'
        )

    def test_simple_man_page_doc(self, w):
        """Given the tokens for a very simple man page, the parser
        should return a string containing the page.
        """
        b = BOLD
        n = NML
        u = UDLN
        L = LINK
        s = ST
        tokens = (
            man.Title('spam', '1', '1/1/70', 'ham', 'bacon'),
            man.Section('NAME', [
                man.Text('spam - example man page.'),
            ]),
            man.Section('SYNOPSIS', [
                man.Synopsis('spam', [
                    man.Option('-acdkKZ'),
                    man.Option('-r', 'eggs'),
                ])
            ]),
            man.Paragraph([
                man.Text('This is'),
                man.Bold('just'),
                man.Text('an example.'),
            ]),
            man.Section('DESCRIPTION', [
                man.Text('Some text explaining what spam is.'),
            ]),
            man.Paragraph([
                man.Text('Even more text, which is probably too much.'),
            ]),
            man.Section('OPTIONS', [
                man.Text('This will have info about the options.'),
            ]),
            man.Subheading('Options', [
                man.Text('These are the options:'),
            ]),
            man.RelativeIndentStart('4'),
            man.TaggedParagraph('4', ['-a',], [man.Text('Option 1.'),]),
            man.TaggedParagraph('4', ['-b',], [
                man.Text('This option is very important.'),
            ]),
            man.TaggedParagraph('4', ['-c',], [man.Text('Option 3.'),]),
            man.IndentedParagraph('-d', '4', [man.Text('Option 4.'),]),
            man.Paragraph([
                man.Text('There is more to say on this.'),
            ]),
            man.RelativeIndentEnd('4'),
            man.Paragraph([
                man.Text('That\'s it.'),
            ]),
            man.Section('AUTHOR', [
                man.Text('This was written by'),
                man.EmailAddress(
                    'spam@spam',
                    [man.Text('John Cleese'),],
                    '.'
                ),
            ]),
        )
        assert man.parse(tokens, w) == (
            'SPAM(1)  bacon   SPAM(1)\n'
            '\n'
            '\n'
            '\n'
            f'{b}NAME{n}\n'
            '    spam - example man\n'
            '    page.\n'
            '\n'
            f'{b}SYNOPSIS{n}\n'
            f'    {b}spam{n} [{b}-acdkKZ{n}] [{b}-r{n}\n'
            f'         {u}eggs{n}]\n'
            '\n'
            f'    This is {b}just{n} an\n'
            '    example.\n'
            '\n'
            f'{b}DESCRIPTION{n}\n'
            '    Some text explaining\n'
            '    what spam is.\n'
            '\n'
            '    Even more text,\n'
            '    which is probably\n'
            '    too much.\n'
            '\n'
            f'{b}OPTIONS{n}\n'
            '    This will have info\n'
            '    about the options.\n'
            '\n'
            f'  {b}Options{n}\n'
            '    These are the\n'
            '    options:\n'
            '\n'
            '    -a  Option 1.\n'
            '\n'
            '    -b  This option is\n'
            '        very important.\n'
            '\n'
            '    -c  Option 3.\n'
            '\n'
            '    -d  Option 4.\n'
            '\n'
            '        There is more to\n'
            '        say on this.\n'
            '\n'
            '    That\'s it.\n'
            '\n'
            f'{b}AUTHOR{n}\n'
            '    This was written by\n'
            f'    {L};;mailto:spam@spam{s}John Cleese{L};;{s}.\n'
            '\n'
            '\n'
            '\n'
            '\n'
            'ham    1/1/70    SPAM(1)\n'
        )


class TestEscapedText:
    def test_escaped_period(self, w):
        """A backslash followed by a period should be rendered as a
        period.
        """
        token = man.Text(r'\.TH')
        assert token.parse(w) == ('.TH', 0, 4)

    def test_escaped_backslash(self, w):
        """A backslash followed by a backslash should be rendered as a
        single backslash.
        """
        token = man.Text(r'\\TH')
        assert token.parse(w) == (r'\TH', 0, 4)


class TestParseToken:
    bold = BOLD
    indent = 4
    link = LINK
    margin = 0
    nml = NML
    st = ST
    udln = UDLN

    # Document structure tokens.
    def test_example(self, w):
        """Given a terminal width, a margin, and an indent,
        Section.parse() should return a string representing
        the object, a margin, and an indent. Since filling is disabled,
        the contents are not reflowed for the given width but are
        instead truncated.
        """
        margin = 1
        indent = 3
        token = man.Example([
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            '    spam eggs bacon ham \n'
            '    spam\n'
            '    spam eggs\n'
            '    spam eggs bacon ham \n'
        ), margin, indent,)

    def test_section(self, w):
        """Given a terminal width, a margin, and an indent,
        Section.parse() should return a string representing
        the object, a margin, and an indent.
        """
        margin = self.margin
        indent = self.indent
        token = man.Section('spam', [
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            f'{self.bold}spam{self.nml}\n'
            '    spam eggs bacon ham\n'
            '    baked beans spam\n'
            '    spam eggs spam eggs\n'
            '    bacon ham baked\n'
            '    beans tomato\n'
            '\n'
        ), margin, indent)

    def test_section_resets_indent(self, w):
        """If the Section.parse() is given an indent that is different
        than the default indent, the Section indents to the default
        amount and returns the default amount.
        """
        margin = 0
        indent = 8
        token = man.Section('spam', [
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            f'{self.bold}spam{self.nml}\n'
            '    spam eggs bacon ham\n'
            '    baked beans spam\n'
            '    spam eggs spam eggs\n'
            '    bacon ham baked\n'
            '    beans tomato\n'
            '\n'
        ), margin, 4)

    def test_section_resets_margin(self, w):
        """If the Section.parse() is given an margin that is different
        than the default margin, the Section indents to the default
        amount and returns the default amount.
        """
        margin = 4
        indent = 4
        token = man.Section('spam', [
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            f'{self.bold}spam{self.nml}\n'
            '    spam eggs bacon ham\n'
            '    baked beans spam\n'
            '    spam eggs spam eggs\n'
            '    bacon ham baked\n'
            '    beans tomato\n'
            '\n'
        ), 0, indent)

    def test_subheading(self, w):
        """Given a terminal width, a margin, and an indent,
        Subheading.parse() should return a string representing
        the object, a margin, and an indent.
        """
        margin = self.margin
        indent = self.indent
        token = man.Subheading('spam', [
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            f'  {self.bold}spam{self.nml}\n'
            '    spam eggs bacon ham\n'
            '    baked beans spam\n'
            '    spam eggs spam eggs\n'
            '    bacon ham baked\n'
            '    beans tomato\n'
            '\n'
        ), margin, indent)

    def test_section_resets_indent(self, w):
        """If the Subheading.parse() is given an indent that is different
        than the default indent, the Subheading indents to the default
        amount and returns the default amount.
        """
        margin = self.margin
        indent = 8
        token = man.Subheading('spam', [
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            f'  {self.bold}spam{self.nml}\n'
            '    spam eggs bacon ham\n'
            '    baked beans spam\n'
            '    spam eggs spam eggs\n'
            '    bacon ham baked\n'
            '    beans tomato\n'
            '\n'
        ), margin, self.indent)

    def test_section_resets_margin(self, w):
        """If the Subheading.parse() is given an margin that is different
        than the default margin, the Subheading indents to the default
        amount and returns the default amount.
        """
        margin = 4
        indent = self.indent
        token = man.Subheading('spam', [
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            f'  {self.bold}spam{self.nml}\n'
            '    spam eggs bacon ham\n'
            '    baked beans spam\n'
            '    spam eggs spam eggs\n'
            '    bacon ham baked\n'
            '    beans tomato\n'
            '\n'
        ), self.margin, indent)

    def test_title(self, w):
        """Given a terminal width, a margin, and an indent,
        Title.parse() should return a string representing
        the object, a margin, and an indent.
        """
        margin = self.margin
        indent = self.indent
        token = man.Title('spam', '1', '1/1/70', 'ham', 'bacon')
        assert token.parse(w, margin, indent) == ((
            'SPAM(1)  bacon   SPAM(1)\n'
            '\n'
            '\n'
            '\n'
        ), margin, indent)
        token = man.Title('spam', '1', '1/1/70', 'ham', 'bacon')

    # Test paragraph tokens.
    def test_indented_paragraph(self, w):
        """Given a terminal width, a margin, and an indent,
        IndentedParagraph.parse() should return a string
        representing the object, a margin, and an indent.
        """
        margin = self.margin
        indent = self.indent
        token = man.IndentedParagraph(contents=[
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            '    spam eggs bacon ham\n'
            '    baked beans spam\n'
            '    spam eggs spam eggs\n'
            '    bacon ham baked\n'
            '    beans tomato\n'
            '\n'
        ), margin, indent)

    def test_indented_paragraph_sets_indent(self, w):
        """If the IndentedParagraph is given an indent that is
        different than the indent set on the token, the
        IndentedParagraph indents the paragraph to the amount set
        on the token and returns that amount.
        """
        margin = self.margin
        indent = 2
        token = man.IndentedParagraph(indent=str(self.indent), contents=[
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            '    spam eggs bacon ham\n'
            '    baked beans spam\n'
            '    spam eggs spam eggs\n'
            '    bacon ham baked\n'
            '    beans tomato\n'
            '\n'
        ), margin, self.indent)

    def test_indented_paragraph_tags_handle_escapes(self, w):
        """If the IndentedParagraph's tag contains escaped text, that
        escape is parsed properly.
        """
        margin = self.margin
        indent = self.indent
        token = man.IndentedParagraph(r'\.', str(indent), [
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            '.   spam eggs bacon ham\n'
            '    baked beans spam\n'
            '    spam eggs spam eggs\n'
            '    bacon ham baked\n'
            '    beans tomato\n'
            '\n'
        ), margin, indent)

    def test_indented_paragraph_with_tag(self, w):
        """If the IndentedParagraph has a tag and the tag is longer
        than the indent, the tag should be printed at the margin
        on the line above the paragraph.
        """
        margin = self.margin
        indent = self.indent
        token = man.IndentedParagraph('spam', str(indent), [
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            'spam\n'
            '    spam eggs bacon ham\n'
            '    baked beans spam\n'
            '    spam eggs spam eggs\n'
            '    bacon ham baked\n'
            '    beans tomato\n'
            '\n'
        ), margin, indent)

    def test_indented_paragraph_with_short_tag(self, w):
        """If the IndentedParagraph has a tag and the tag is shorter
        than the indent, the tag should be printed at the margin
        with the first line of the paragraph.
        """
        margin = self.margin
        indent = self.indent
        token = man.IndentedParagraph('*', str(indent), [
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            '*   spam eggs bacon ham\n'
            '    baked beans spam\n'
            '    spam eggs spam eggs\n'
            '    bacon ham baked\n'
            '    beans tomato\n'
            '\n'
        ), margin, indent)

    def test_paragraph(self, w):
        """Given a terminal width, a margin, and an indent,
        Paragraph.parse() should return a string representing
        the object, a margin, and an indent.
        """
        margin = self.margin
        indent = self.indent
        token = man.Paragraph([
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            '    spam eggs bacon ham\n'
            '    baked beans spam\n'
            '    spam eggs spam eggs\n'
            '    bacon ham baked\n'
            '    beans tomato\n'
            '\n'
        ), margin, indent)

    def test_paragraph_resets_indent(self, w):
        """If the Paragraph.parse() is given an indent that is different
        than the default indent, the Paragraph indents the paragraph to
        the default amount and returns the default amount.
        """
        margin = self.margin
        indent = 8
        token = man.Paragraph([
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            '    spam eggs bacon ham\n'
            '    baked beans spam\n'
            '    spam eggs spam eggs\n'
            '    bacon ham baked\n'
            '    beans tomato\n'
            '\n'
        ), margin, self.indent)

    def test_paragraph_uses_margin(self, w):
        """If the Paragraph.parse() is given an margin that is different
        than the default margin, the Paragraph indents the paragraph to
        the margin amount and returns the margin amount.
        """
        margin = 4
        indent = self.indent
        token = man.Paragraph([
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            '        spam eggs bacon\n'
            '        ham baked beans\n'
            '        spam spam eggs\n'
            '        spam eggs bacon\n'
            '        ham baked beans\n'
            '        tomato\n'
            '\n'
        ), margin, indent)

    def test_tagged_paragraph(self, w):
        """Given a terminal width, a margin, and an indent,
        TaggedParagraph.parse() should return a string
        representing the object, a margin, and an indent.
        """
        margin = self.margin
        indent = self.indent
        token = man.TaggedParagraph(str(indent), ['spam',], [
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            'spam\n'
            '    spam eggs bacon ham\n'
            '    baked beans spam\n'
            '    spam eggs spam eggs\n'
            '    bacon ham baked\n'
            '    beans tomato\n'
            '\n'
        ), margin, indent)

    def test_tagged_paragraph_sets_indent(self, w):
        """If the TaggedParagraph is given an indent that is
        different than the indent set on the token, the
        TaggedParagraph indents the paragraph to the amount set
        on the token and returns that amount.
        """
        margin = self.margin
        indent = 2
        token = man.TaggedParagraph(str(self.indent), ['spam',], [
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            'spam\n'
            '    spam eggs bacon ham\n'
            '    baked beans spam\n'
            '    spam eggs spam eggs\n'
            '    bacon ham baked\n'
            '    beans tomato\n'
            '\n'
        ), margin, self.indent)

    def test_tagged_paragraph_tags_handle_escapes(self, w):
        """If the TaggedParagraph's tag contains escaped text, that
        escape is parsed properly.
        """
        margin = self.margin
        indent = self.indent
        token = man.TaggedParagraph(str(indent), [r'\.',], [
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            '.   spam eggs bacon ham\n'
            '    baked beans spam\n'
            '    spam eggs spam eggs\n'
            '    bacon ham baked\n'
            '    beans tomato\n'
            '\n'
        ), margin, indent)

    def test_tagged_paragraph_with_short_tag(self, w):
        """If the TaggedParagraph's tag is shorter than the indent,
        the tag should be printed at the margin with the first line
        of the paragraph.
        """
        margin = self.margin
        indent = self.indent
        token = man.TaggedParagraph(str(indent), ['*',], [
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            '*   spam eggs bacon ham\n'
            '    baked beans spam\n'
            '    spam eggs spam eggs\n'
            '    bacon ham baked\n'
            '    beans tomato\n'
            '\n'
        ), margin, indent)

    def test_tagged_paragraph_with_multiple_tags(self, w):
        """If the TaggedParagraph has multiple tags, they are printed
        on separate lines at the margin.
        """
        margin = self.margin
        indent = self.indent
        token = man.TaggedParagraph(str(indent), ['+', '$', '*'], [
            man.Text('spam eggs bacon ham baked beans'),
            man.Text('spam'),
            man.Text('spam eggs'),
            man.Text('spam eggs bacon ham baked beans tomato'),
        ])
        assert token.parse(w, margin, indent) == ((
            '+\n'
            '$\n'
            '*   spam eggs bacon ham\n'
            '    baked beans spam\n'
            '    spam eggs spam eggs\n'
            '    bacon ham baked\n'
            '    beans tomato\n'
            '\n'
        ), margin, indent)

    # Command synopsis tokens.
    def test_option(self, w):
        """Given a terminal width, a margin, and an indent,
        Option.parse() should return a string
        representing the object, a margin, and an indent.
        """
        margin = self.margin
        indent = self.indent
        token = man.Option('-s', 'spam')
        assert token.parse(w, margin, indent) == (
            f'[{self.bold}-s{self.nml} {self.udln}spam{self.nml}]',
            margin,
            indent,
        )

    def test_synopsis(self, w):
        """Given a terminal width, a margin, and an indent,
        Synopsis.parse() should return a string
        representing the object, a margin, and an indent.
        """
        margin = self.margin
        indent = 0
        token = man.Synopsis('spam', [
            man.Option('-s', 'spam'),
            man.Option('-e', 'eggs'),
            man.Option('-b', 'bacon')
        ])
        assert token.parse(w, margin, indent) == ((
            f'{self.bold}spam{self.nml} '
            f'[{self.bold}-s{self.nml} {self.udln}spam{self.nml}] '
            f'[{self.bold}-e{self.nml} {self.udln}eggs{self.nml}]\n'
            f'     [{self.bold}-b{self.nml} {self.udln}bacon{self.nml}]\n'
            '\n'
        ), margin, indent)

    def test_synopsis_with_multiple_synopses(self, w):
        """If there are multiple commands within the Synopsis, the
        string should not contain a blank line between the end of the
        last option of the last command and the next command.
        """
        margin = self.margin
        indent = 0
        token = man.Synopsis('spam', [
            man.Option('-s', 'spam'),
            man.Option('-e', 'eggs'),
            man.Option('-b', 'bacon'),
            man.Synopsis('ham', []),
            man.Option('-f', 'flapjack')
        ])
        assert token.parse(w, margin, indent) == ((
            f'{self.bold}spam{self.nml} '
            f'[{self.bold}-s{self.nml} {self.udln}spam{self.nml}] '
            f'[{self.bold}-e{self.nml} {self.udln}eggs{self.nml}]\n'
            f'     [{self.bold}-b{self.nml} {self.udln}bacon{self.nml}]\n'
            f'{self.bold}ham{self.nml} '
            f'[{self.bold}-f{self.nml} {self.udln}flapjack{self.nml}]\n'
            '\n'
        ), margin, indent)

    # Hyperlink and email tokens.
    def test_email_address(self, w):
        """Given a terminal width, a margin, and an indent,
        EmailAddress.parse() should return a string
        representing the object, a margin, and an indent.
        """
        margin = self.margin
        indent = self.indent
        token = man.EmailAddress('spam', [man.Text('bacon'),], '.')
        assert token.parse(w, margin, indent) == (
            f'{self.link};;mailto:spam{self.st}bacon{self.link};;{self.st}.',
            margin,
            indent,
        )

    def test_url(self, w):
        """Given a terminal width, a margin, and an indent,
        Url.parse() should return a string
        representing the object, a margin, and an indent.
        """
        margin = self.margin
        indent = self.indent
        token = man.Url('http://spam', [man.Text('bacon'),], '.')
        assert token.parse(w, margin, indent) == (
            f'{self.link};;http://spam{self.st}bacon{self.link};;{self.st}.',
            margin,
            indent,
        )

    # Font style macros.
    def test_bold(self, w):
        """Given a terminal width, a margin, and an indent,
        Bold.parse() should return a string
        representing the object, a margin, and an indent.
        """
        margin = self.margin
        indent = self.indent
        token = man.Paragraph([man.Bold('spam'),])
        assert token.parse(w, margin, indent) == (
            f'    {self.bold}spam{self.nml}\n\n',
            margin,
            indent,
        )

    def test_italic(self, w):
        """Given a terminal width, a margin, and an indent,
        Italic.parse() should return a string
        representing the object, a margin, and an indent.
        """
        margin = self.margin
        indent = self.indent
        token = man.Paragraph([man.Italic('spam'),])
        assert token.parse(w, margin, indent) == (
            f'    {self.udln}spam{self.nml}\n\n',
            margin,
            indent,
        )

    def test_small(self, w):
        """Given a terminal width, a margin, and an indent,
        Small.parse() should return a string
        representing the object, a margin, and an indent.
        """
        margin = self.margin
        indent = self.indent
        token = man.Paragraph([man.Small('spam'),])
        assert token.parse(w, margin, indent) == (
            f'    spam\n\n',
            margin,
            indent,
        )

    def test_smallbold(self, w):
        """Given a terminal width, a margin, and an indent,
        SmallBold.parse() should return a string
        representing the object, a margin, and an indent.
        """
        margin = self.margin
        indent = self.indent
        token = man.Paragraph([man.SmallBold('spam'),])
        assert token.parse(w, margin, indent) == (
            f'    {self.bold}spam{self.nml}\n\n',
            margin,
            indent,
        )

    # Alternating font style macros.
    def test_bold_italic(self, w):
        """Given a terminal width, a margin, and an indent,
        BoldItalic.parse() should return a string
        representing the object, a margin, and an indent.
        """
        margin = self.margin
        indent = self.indent
        token = man.Paragraph([man.BoldItalic('spam eggs bacon'),])
        assert token.parse(w, margin, indent) == ((
            f'    {self.bold}spam{self.nml} '
            f'{self.udln}eggs{self.nml} '
            f'{self.bold}bacon{self.nml}\n\n'
        ), margin, indent)

    def test_bold_roman(self, w):
        """Given a terminal width, a margin, and an indent,
        BoldRoman.parse() should return a string
        representing the object, a margin, and an indent.
        """
        margin = self.margin
        indent = self.indent
        token = man.Paragraph([man.BoldRoman('spam eggs bacon'),])
        assert token.parse(w, margin, indent) == ((
            f'    {self.bold}spam{self.nml} '
            f'eggs{self.nml} '
            f'{self.bold}bacon{self.nml}\n\n'
        ), margin, indent)

    def test_italic_bold(self, w):
        """Given a terminal width, a margin, and an indent,
        ItalicBold.parse() should return a string
        representing the object, a margin, and an indent.
        """
        margin = self.margin
        indent = self.indent
        token = man.Paragraph([man.ItalicBold('spam eggs bacon'),])
        assert token.parse(w, margin, indent) == ((
            f'    {self.udln}spam{self.nml} '
            f'{self.bold}eggs{self.nml} '
            f'{self.udln}bacon{self.nml}\n\n'
        ), margin, indent)

    def test_italic_roman(self, w):
        """Given a terminal width, a margin, and an indent,
        ItalicRoman.parse() should return a string
        representing the object, a margin, and an indent.
        """
        margin = self.margin
        indent = self.indent
        token = man.Paragraph([man.ItalicRoman('spam eggs bacon'),])
        assert token.parse(w, margin, indent) == ((
            f'    {self.udln}spam{self.nml} '
            f'eggs{self.nml} '
            f'{self.udln}bacon{self.nml}\n\n'
        ), margin, indent)

    def test_roman_bold(self, w):
        """Given a terminal width, a margin, and an indent,
        RomanBold.parse() should return a string
        representing the object, a margin, and an indent.
        """
        margin = self.margin
        indent = self.indent
        token = man.Paragraph([man.RomanBold('spam eggs bacon'),])
        assert token.parse(w, margin, indent) == ((
            f'    spam{self.nml} '
            f'{self.bold}eggs{self.nml} '
            f'bacon{self.nml}\n\n'
        ), margin, indent)

    def test_roman_italic(self, w):
        """Given a terminal width, a margin, and an indent,
        RomanItalic.parse() should return a string
        representing the object, a margin, and an indent.
        """
        margin = self.margin
        indent = self.indent
        token = man.Paragraph([man.RomanItalic('spam eggs bacon'),])
        assert token.parse(w, margin, indent) == ((
            f'    spam{self.nml} '
            f'{self.udln}eggs{self.nml} '
            f'bacon{self.nml}\n\n'
        ), margin, indent)
