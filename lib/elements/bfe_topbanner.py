# -*- coding: utf-8 -*-
##
## $Id$
##
## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007 CERN.
##
## CDS Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## CDS Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.  
##
## You should have received a copy of the GNU General Public License
## along with CDS Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
"""BibFormat element - Prints HTML topbanner with categorz, rep. number, etc.
"""
__revision__ = "$Id$"

import cgi

def format(bfo):
    """
    HTML top page banner containing category, rep. number, etc
    """
    collection_indicator = bfo.kb("dbcollid2coll", bfo.field("980__a"))
    collection_indicator = cgi.escape(collection_indicator)
    subject = bfo.field("65017a")
    subject = cgi.escape(subject)
    subject_2 = bfo.field("65027a")
    subject_2 = cgi.escape(subject_2)
    additional_report_numbers = bfo.fields("088__a")
    
    source_of_aquisition = bfo.field("037__a")
    source_of_aquisition = cgi.escape(source_of_aquisition)

    out = '<table border="0" width="100%"><tr class="blocknote">'
    out += '''<td valign="left">
    %s
    <small>''' % collection_indicator

    if subject != "XX":
        out += " / "+ subject

    out += subject_2
    out += "</small></td>"

    for report_number in additional_report_numbers:
        out += "<td><small><strong>" +cgi.escape(report_number) +" </strong></small></td>"

    if len(source_of_aquisition) > 0:
        out += '<td align="right"><strong>'+ source_of_aquisition + "</strong></td>"

    out += "</tr></table><br>"

    return out

def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0
