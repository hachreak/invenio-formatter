## $Id$
##
## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006 CERN.
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

__revision__ = "$Id$"

from cStringIO import StringIO
from invenio.bibformat_bfx_engine import format_with_bfx

def format(bfo, template='DC'):
    """
    An entry point to the BibFormat BFX engine, when used as an element.
    Formats the record according to a template.

    For further details, please read the documentation.
    
    @param template the name of the template file without the bfx extension
    """
    output = ""
    recIDs=[bfo.recID]
    outFile=StringIO() # a virtual file-like object to write in
    format_with_bfx(recIDs, outFile, template)
    output=outFile.getvalue()        
    return output
