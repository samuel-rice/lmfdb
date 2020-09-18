from lmfdb.utils import display_knowl

def th_wrap(kwl, title):
    return '    <th>%s</th>' % display_knowl(kwl, title=title)
def td_wrapl(val):
    return '    <td align="left">%s</td>' % val
def td_wrapc(val):
    return '    <td align="center">%s</td>' % val
def td_wrapr(val):
    return '    <td align="right">%s</td>' % val


class NumberTheoryDataTable():
    """HTML builder class for number theoretic data tables.

    Takes data and formatting information and converts it into an HTML
    rendering of the data table via the method `to_html`.

        pinned_rows:
            if not None, specifies the maximum number of rows to be displayed
            by default. If the number of rows exceeds this value, the table
            will appear truncated with a "show more"/"show less" button.

        extra_html_classes:
            if not None, specifies a list of class names to append to the
            "class" attribute of the table. All tables use the "ntdata" class.
    """


    def __init__(self, pinned_rows=None, extra_html_classes=None, style=None, title=None):
        self.column_headings = []
        self.column_alignments = []
        self.rows = []

        self.pinned_rows = pinned_rows
        self.html_classes = ['ntdata']
        if extra_html_classes is not None:
            self.html_classes.extend(extra_html_classes)
        self.style = style
        self.title = title


    def add_column(self, knowl, title, alignment="left"):
        """Add a column to the table.

            knowl:     the name of the knowl for the column heading.
            title:     the text to be displayed for the column heading.
            alignment: the horizontal alignment of values in this column.
        """
        self.column_headings.append(display_knowl(knowl, title=title))
        self.column_alignments.append(alignment)


    def add_row(self, values):
        """Add a row of values to the table.

            values: a list of strings representing the values to be added.
                    The values must be in the same order that the column
                    headings were added.
        """
        self.rows.append(values)


    def to_html(self):
        """Return the HTML representation of this table.
        """
        lines = [f'<table {self._class_attribute()}{self._style_attribute()}>',
                 '  <thead>',
                 self._title_row(),
                 '    <tr>',
                 '      ' + self._format_headings(),
                 '    </tr>',
                 '  </thead>',
                 '  <tbody>',
                 '    ' + self._format_rows(),
                 '  </tbody>',
                 '</table>']
        return '\n'.join(lines)


    # Implementation details


    def _class_attribute(self):
        return 'class="' + ' '.join(self.html_classes) + '"'


    def _style_attribute(self):
        if self.style is not None:
            return f' style="{self.style}"'
        else:
            return ''


    def _title_row(self):
        if self.title is not None:
            return f'<tr><th colspan={len(self.column_headings)} align="center">{self.title}</th></tr>'
        else:
            return ''


    def _format_headings(self):
        """Return the <th> elements of the header row as a block of HTML"""
        cells = ['<th>{heading}</th>'.format(heading=h) for h in self.column_headings]
        return '\n      '.join(cells)


    def _get_tr_tag(self, i):
        """Return the opening <tr> tag for row i.

        If i is large, we mark the row as "more" and set it not to display by
        default.
        """
        if self.pinned_rows and i < self.pinned_rows:
            return '<tr>'
        else:
            return '<tr class="more nodisplay">'


    def _format_values(self, row):
        """Return the values in the row wrapped in <td> tags as a list.
        """
        return ['  <td align="{align}">{value}</td>'.format(align=align, value=value)
                for value, align in zip(row, self.column_alignments)]


    def _get_show_more_less_rows(self):
        """Return the magic final two rows for showing more/less.

        This is not super nice, and probably could be done with jQuery in a far
        superior manner, but this method Just Works TM.
        """
        return ['<tr class="less toggle">',
               '  <td colspan="{{colspan}}">',
               '    <a onclick="show_moreless(&quot;more&quot;); return true" href="#moreep">show more</a>',
               '  </td>',
               '</tr>',
               '<tr class="more toggle nodisplay">',
               '  <td colspan="{{colspan}}">',
               '    <a onclick="show_moreless(&quot;less&quot;); return true" href="#eptable">show less</a>',
               '  </td>',
               '</tr>']


    def _format_rows(self):
        """Return the data rows of the table as a block of HTML.
        """
        html_rows = []
        for i, row in enumerate(self.rows):
            html_rows.append(self._get_tr_tag(i))
            html_rows.extend(self._format_values(row))
            html_rows.append('</tr>')
        if len(self.rows) > self.pinned_rows:
            html_rows.extend(self._get_show_more_less_rows())
        return '\n    '.join(html_rows)
