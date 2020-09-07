from lmfdb.utils import display_knowl

def th_wrap(kwl, title):
    return '    <th>%s</th>' % display_knowl(kwl, title=title)
def td_wrapl(val):
    return '    <td align="left">%s</td>' % val
def td_wrapc(val):
    return '    <td align="center">%s</td>' % val
def td_wrapr(val):
    return '    <td align="right">%s</td>' % val
