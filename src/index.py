import pmt_utils
import declarations

pmt_utils.htmlContentType()
form=pmt_utils.getFormData()
db_name=declarations.pmt_info['db_name']

print '<HTML>'
print ' <HEAD>'
print '  <TITLE>Linuxden Web Site</TITLE>'

print ' <META NAME="description" CONTENT="Program Name Here">'

print ' <META NAME="keywords" CONTENT="engineering software hardware'
print 'secure internet server linux research not-for-profit '
print '">'

print ' <META NAME="author" CONTENT="R. Scott Davis">'

print '    <SCRIPT LANUGAGE="JavaScript">'

print '      function TOfunc() {'
print '      TO = window.setTimeout( "TOfunc()", 1000 ); }'

print '      function scroll_status (seed) {'
msg="Linuxden is an organization "
msg=msg+"performing research in a variety of innovative technologies "
msg=msg+"for the future."
print '      var msg = "%s"' % msg
print '      var out = " ";'
print '      var c = 1;'
print '      if (150 < seed) {'
print '        seed--;'
print '        var cmd="scroll_status(" + seed + ")";'
print '        timerTwo = window.setTimeout(cmd, 25);'
print '      }'
print '      else if (seed <= 150 && 0 < seed) {'
print '        for (c=0 ; c < seed ; c++) {'
print '          out+=" "; }'
print '        out+=msg;'
print '        seed--;'
print '        var cmd="scroll_status(" + seed + ")";'
print '        window.status=out;'
print '        timerTwo=window.setTimeout(cmd,25);  }'
print '      else if (seed <= 0) {'
print '        if (-seed < msg.length) {'
print '          out+=msg.substring(-seed,msg.length);'
print '          seed--;'
print '          var cmd="scroll_status(" + seed + ")";'
print '          window.status=out;'
print '          timerTwo=window.setTimeout(cmd,25);  }'
print '        else {'
print '          window.status=" ";'
print '          timerTwo=window.setTimeout("scroll_status(150)",25);  }'
print '      }'
print '      }'

print '      function setTimers() {'
print "      timerONE=window.setTimeout('scroll_status(100)',50);"
print "      TO = setTimeout( 'TOfunc()', 1000 );  }"

print '      /*setTimers();*/'

print '    </SCRIPT>'
print '  </HEAD>'


if form.has_key("username"):
    formData=""
else:
    formData="?public=2"

print '  <FRAMESET COLS="130,*" border="0">'
print '    <FRAME SRC="/%s-cgi-bin/optionsBar.pyc%s"' % (db_name,formData)
print '      NAME="options"'
print '      FRAMEBORDER=0'
print '      MARGINHEIGHT=0'
print '      MARGINWIDTH=0'
print '      SCROLLING="AUTO"'
print '      NORESIZE>'

print '      <FRAMESET ROWS="65,*" border="0">'
print '        <FRAME SRC="/%s/html/header.html"' % db_name
print '          MARGINHEIGHT=0'
print '          FRAMEBORDER=0'
print '          NAME="header"'
print '          SCROLLING = "NO"'
print '          NORESIZE>'

print '          <FRAME SRC="/%s/html/siteInfo.html"' % db_name
print '            MARGINHEIGHT=0'
print '            MARGINWIDTH=5'
print '            FRAMEBORDER=0'
print '            NAME="siteInfo"'
print '            SCROLLING="AUTO"'
print '            NORESIZE>'
print '      </FRAMESET>'
print '  </FRAMESET>'
print '</HTML>'
