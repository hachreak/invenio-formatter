# -*- coding: utf-8 -*-
## $Id$
## Administration of Bibformat config files
                                              
## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005 CERN.
##
## The CDSware is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## The CDSware is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with CDSware; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
"""HTML Templates for BibFormat administration"""                                           
__lastupdated__ = """$Date$"""

# non Invenio imports
import cgi

# Invenio imports                
from invenio.messages import gettext_set_language
from invenio.textutils import indent_text
from invenio.config import weburl, sweburl
from invenio.messages import language_list_long

class Template:
    """Templating class, refer to bibformat.py for examples of call"""

    def tmpl_admin_index(self, use_old_bibformat, ln, warnings):
        """
        Returns the main BibFormat admin page.

        The page offers for some times the choice between the old and new BibFormat.
        This is the only page where the code needs to be cleaned
        when the migration kit will be removed. #FIXME: remove when removing migration kit

        @param ln language
        @param use_old_bibformat if True use old BibFormat. If False, use new.
        @param warnings a list of warnings to display at top of page. None if no warning
        @return main BibFormat admin page
        """

        _ = gettext_set_language(ln)    # load the right message language

        if use_old_bibformat:
            old_bibformat_checked = "checked"
            new_bibformat_checked = ""
        else:
            old_bibformat_checked = ""
            new_bibformat_checked = "checked"

        out = ''' For the time being it is recommended to use
        <a href="%s/admin/bibformat">this BibFormat administration interface</a><br/><br/><br/><br/><br/>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        ''' % weburl

        if warnings:
            out += '''
            <table width="66%%" class="errorbox" style="margin-left: auto; margin-right: auto;">
            <tr>
            <th class="errorboxheader">
            %(warnings)s
            </th>
            </tr>
            </table>
            ''' % {'warnings': '<br/>'.join(warnings)}

        out += '''
        <table width="66%%" class="errorbox" style="margin-left: auto; margin-right: auto;">
        <tr>
        <th class="errorboxheader">
        <big>Bibformat has changed!</big>
        <p>You will need to migrate your formats. You can read the <a href="">documentation</a> to learn how to write
        formats, or use the <a href="%(weburl)s/admin/bibformat/bibformat_migration_kit_assistant.py">migration assistant</a>.</p>
        <p>However for some time the old Bibformat will still run along the new one, so that you can
        transition smoothly. Choose which one to run:</p>
        <div style="text-align: center;">
        <form  action="" method="post">

        <input type="radio" name="version" id="old" value="old" %(old_bibformat_checked)s/><label for="old">Old version (php)</label>
        <input type="radio" name="version" id="new" value="new" %(new_bibformat_checked)s/><label for="new">New version (python)</label>
        <input type="submit" value="Apply change"/>
        </form>
        </div>
        </th>
        </tr>
        </table>
        ''' % {'old_bibformat_checked':old_bibformat_checked,
               'new_bibformat_checked':new_bibformat_checked,
               'weburl':weburl}
        
        out += '''
        <p>
         This is where you can edit the formatting style available for the collections. You need to 
         <a href="%(weburl)s/youraccount.py/login?referer=%(weburl)s/admin/webcomment/">login</a> to enter.
        </p>

        <dl>
        <dt><a href="%(weburl)s/admin/bibformat/bibformatadmin.py/output_formats_manage?ln=%(ln)s">Manage Output Formats</a></dt>
        <dd>Create, edit and delete output formats, the rules that define which format template must be used for a given record.</dd>
        </dl>
        <dl>
        <dt><a href="%(weburl)s/admin/bibformat/bibformatadmin.py/format_templates_manage?ln=%(ln)s">Manage Format Templates</a></dt>
        <dd>Create, edit and delete format templates, which define how to format a record.</dd>
        </dl>
        <dl>
        <dt><a href="%(weburl)s/admin/bibformat/bibformatadmin.py/format_elements_doc?ln=%(ln)s">Format Elements Documentation</a></dt>
        <dd>Documentation of the format elements to be used inside format templates.</dd>
        </dl>
        <dl>
        <dt><a href="%(weburl)s/admin/bibformat/bibformatadmin.py/kb_manage?ln=%(ln)s">Manage Knowledge Bases</a></dt>
        <dd>Specify how an incomplete or non standard record has to be transformed into a nice standard text.</dd>
        </dl>
        <dl>
        <dt><a href="%(weburl)s/admin/bibformat/guide.html">BibFormat Admin Guide</a></dt>
        <dd>Everything you want to know about BibFormat administration</dd>
        </dl>

        <div style="background-color:rgb(204, 204, 204)";>

        <p><b>OLD BIBFORMAT ADMIN FOLLOWS:</b>
        <em>
        <p>The BibFormat admin interface enables you to specify how the
        bibliographic data is presented to the end user in the search
        interface and search results pages.  For example, you may specify that
        titles should be printed in bold font, the abstract in small italic,
        etc.  Moreover, the BibFormat is not only a simple bibliographic data
        <em>output formatter</em>, but also an automated <em>link
        constructor</em>.  For example, from the information on journal name
        and pages, it may automatically create links to publisher's site based
        on some configuration rules.

        <h2>Configuring BibFormat</h2>

        <p>By default, a simple HTML format based on the most common fields
        (title, author, abstract, keywords, fulltext link, etc) is defined.
        You certainly want to define your own ouput formats in case you have a
        specific metadata structure.

        <p>Here is a short guide of what you can configure:

        <blockquote>
        <dl>

        <dt><a href="BEH_display.php">Behaviours</a>

        <dd>Define one or more output BibFormat behaviours.  These are then
        passed as parameters to the BibFormat modules while executing
        formatting. 

        <br><em>Example:</em> You can tell BibFormat that is has to enrich the
        incoming metadata file by the created format, or that it only has to
        print the format out.

        <dt><a href="OAIER_display.php">Extraction Rules</a>

        <dd>Define how the metadata tags from input are mapped into internal
        BibFormat variable names.  The variable names can afterwards be used
        in formatting and linking rules.

        <br><em>Example:</em> You can tell that <code>100 $a</code> field
        should be mapped into <code>$100.a</code> internal variable that you
        could use later.

        <dt><a href="LINK_display.php">Link Rules</a> 

        <dd>Define rules for automated creation of URI links from mapped
        internal variables.

        <br><em>Example:</em> You can tell a rule how to create a link to
        People database out of the <code>$100.a</code> internal variable
        repesenting author's name.  (The <code>$100.a</code> variable was mapped
        in the previous step, see the Extraction Rules.)

        <dt><a href="LINK_FORMAT_display.php">File Formats</a>

        <dd>Define file format types based on file extensions.  This will be
        used when proposing various fulltext services.

        <br><em>Example:</em> You can tell that <code>*.pdf</code> files will
        be treated as PDF files.  

        <dt><a href="UDF_display.php">User Defined Functions (UDFs)</a>

        <dd>Define your own functions that you can reuse when creating your
        own output formats.  This enables you to do complex formatting without
        ever touching the BibFormat core code.

        <br><em>Example:</em> You can define a function how to match and
        extract email addresses out of a text file.

        <dt><a href="FORMAT_display.php">Formats</a>

        <dd>Define the output formats, i.e. how to create the output out of
        internal BibFormat variables that were extracted in a previous step.
        This is the functionality you would want to configure most of the
        time.  It may reuse formats, user defined functions, knowledge bases,
        etc.

        <br><em>Example:</em> You can tell that authors should be printed in
        italic, that if there are more than 10 authors only the first three
        should be printed, etc.

        <dt><a href="KB_display.php">Knowledge Bases (KBs)</a>

        <dd>Define one or more knowledge bases that enables you to transform
        various forms of input data values into the unique standard form on
        the output.

        <br><em>Example:</em> You can tell that <em>Phys Rev D</em> and
        <em>Physical Review D</em> are both the same journal and that these
        names should be standardized to <em>Phys Rev : D</em>.

        <dt><a href="test.php">Execution Test</a>

        <dd>Enables you to test your formats on your sample data file.  Useful
        when debugging newly created formats.

        </dl>
        </blockquote>

        <p>To learn more on BibFormat configuration, you can consult the <a
        href="guide.html">BibFormat Admin Guide</a>.</small>

        <h2>Running BibFormat</h2>

        <h3>From the Web interface</h3>
        <p>
        Run <a href="BIBREFORMAT_display.php">Reformat Records</a> tool.
        This tool permits you to update stored formats for bibliographic records.
        <br>
        It should normally be used after configuring BibFormat's
        <a href="BEH_display.php">Behaviours</a> and
        <a href="FORMAT_display.php">Formats</a>.
        When these are ready, you can choose to rebuild formats for selected
        collections or you can manually enter a search query and the web interface
        will accomplish all necessary formatting steps.
        <br>
        <i>Example:</i> You can request Photo collections to have their HTML 
        brief formats rebuilt, or you can reformat all the records written by Ellis.

        <h3>From the command-line interface</h3>

        <p>Consider having an XML MARC data file that is to be uploaded into
        the CDS Invenio.  (For example, it might have been harvested from other
        sources and processed via <a href="../bibconvert/">BibConvert</a>.)
        Having configured BibFormat and its default output type behaviour, you
        would then run this file throught BibFormat as follows:

        <blockquote>
        <pre>
        $ bibformat < /tmp/sample.xml > /tmp/sample_with_fmt.xml
        <pre>
        </blockquote>

        that would create default HTML formats and would "enrich" the input
        XML data file by this format.  (You would then continue the upload
        procedure by calling successively <a
        href="../bibupload/">BibUpload</a> and <a
        href="../bibwords/">BibWords</a>.)

        <p>Now consider a different situation.  You would like to add a new
        possible format, say "HTML portfolio" and "HTML captions" in order to
        nicely format multiple photographs in one page.  Let us suppose that
        these two formats are called <code>hp</code> and <code>hc</code> and
        are already loaded in the <code>collection_format</code> table.
        (TODO: describe how this is done via WebAdmin.)  You would then
        proceed as follows: firstly, you would prepare the corresponding <a
        href="BEH_display.php">output behaviours</a> called <code>HP</code>
        and <code>HC</code> (TODO: note the uppercase!) that would not enrich
        the input file but that would produce an XML file with only
        <code>001</code> and <code>FMT</code> tags.  (This is in order not to
        update the bibliographic information but the formats only.)  You would
        also prepare corresponding <a href="FORMAT_display.php">formats</a>
        at the same time.  Secondly, you would launch the formatting as
        follows:

        <blockquote>
        <pre>
        $ bibformat otype=HP,HC < /tmp/sample.xml > /tmp/sample_fmts_only.xml
        <pre>
        </blockquote>

        that should give you an XML file containing only 001 and FMT tags.
        Finally, you would upload the formats:

        <blockquote>
        <pre>
        $ bibupload < /tmp/sample_fmts_only.xml
        <pre>
        </blockquote>

        and that's it. The new formats should now appear in <a
        href="%(weburl)s">WebSearch</a>.
        </em>
        </div>

        ''' % {'weburl':weburl, 'ln':ln}

        return indent_text(out)

    def tmpl_admin_format_template_show_attributes(self, ln, name, description, filename, editable):
        """
        Returns a page to change format template name and description

        @param ln language
        @param name the name of the format
        @param description the description of the format
        @param filename the filename of the template
        @param editable True if we let user edit, else False
        @return editor for 'format'
        """
        _ = gettext_set_language(ln)    # load the right message language


        out = ""

        out += '''
        <table class="admin_wvar">
        <tr><th colspan="4" class="adminheaderleft">%(menu)s</th></tr>
        <tr>
        <td>0.&nbsp;<small><a href="format_templates_manage?ln=%(ln)s">%(close_editor)s</a></small>&nbsp;</td>
        <td>1.&nbsp;<small><a href="format_template_show?ln=%(ln)s&amp;bft=%(filename)s">%(template_editor)s</a></small>&nbsp;</td>
        <td>2.&nbsp;<small>%(modify_template_attributes)s</small>&nbsp;</td>
        <td>3.&nbsp;<small><a href="format_template_show_dependencies?ln=%(ln)s&amp;bft=%(filename)s">%(check_dependencies)s</a></small>&nbsp;</td>
        </tr>
        </table><br/>
        ''' % {'ln':ln,
               'menu':_("Menu"),
               'filename':filename,
               'close_editor': _("Close Editor"),
               'modify_template_attributes': _("Modify Template Attributes"),
               'template_editor': _("Template Editor"),
               'check_dependencies': _("Check Dependencies")
               }
        
        disabled = ""
        readonly = ""
        if not editable:
            disabled = 'disabled="disabled"'
            readonly = 'readonly="readonly"'
            
        out += '''
        <form action="format_template_update_attributes?ln=%(ln)s&amp;bft=%(filename)s" method="POST">
        <table><tr>
        <th colspan="2" class="adminheaderleft">%(name)s attributes&nbsp;[<a href="%(weburl)s/admin/bibformat/guide.html#attrsFormatTemplate">?</a>]</th>
        </tr>
        <tr>
        <td class="admintdright">
        
        <input type="hidden" name="key" value="%(name)s"/>
        <label for="name">%(name_label)s</label>:&nbsp;</td>
        <td><input tabindex="4" name="name" type="text" id="name" size="25" value="%(name)s" %(readonly)s/>
        <input type="hidden" value="%(filename)s"/>
        </td>
        </tr>
        <tr>
        <td class="admintdright" valign="top"><label for="description">%(description_label)s</label>:&nbsp;</td>
        <td><textarea tabindex="5" name="description" id="description" rows="4" cols="25" %(readonly)s>%(description)s</textarea> </td>
        </tr>
        <tr>
        <td>&nbsp;</td>
        <td align="right"><input tabindex="6" class="adminbutton" type="submit" value="%(update_format_attributes)s" %(disabled)s/></td>
        </tr>
        </table></form>
        ''' % {"name": name,
               "description": description,
               'ln':ln,
               'filename':filename,
               'disabled':disabled,
               'readonly':readonly,
               'description_label': _("Description"),
               'name_label': _("Name"),
               'update_format_attributes': _("Update Format Attributes"),
               'weburl':weburl
               }

        return out

    def tmpl_admin_format_template_show_dependencies(self, ln, name, filename, output_formats, format_elements, tags):
        """
        Shows the dependencies (on elements) of the given format.

        @param name the name of the template
        @param filename the filename of the template
        @param format_elements the elements (and list of tags in each element) this template depends on
        @param output_formats the output format that depend on this template
        @param tags the tags that are called by format elements this template depends on.
        """
        _ = gettext_set_language(ln)    # load the right message language
        
        out = '''
        <table class="admin_wvar">
        <tr><th colspan="4" class="adminheaderleft">%(menu)s</th></tr>
        <tr>
        <td>0.&nbsp;<small><a href="format_templates_manage?ln=%(ln)s">%(close_editor)s</a></small>&nbsp;</td>
        <td>1.&nbsp;<small><a href="format_template_show?ln=%(ln)s&amp;bft=%(filename)s">%(template_editor)s</a></small>&nbsp;</td>
        <td>2.&nbsp;<small><a href="format_template_show_attributes?ln=%(ln)s&amp;bft=%(filename)s">%(modify_template_attributes)s</a></small>&nbsp;</td>
        <td>3.&nbsp;<small>%(check_dependencies)s</small>&nbsp;</td>
        </tr>
        </table>
        <table width="90%%" class="admin_wvar"><tr>
        <th class="adminheaderleft">Output Formats that use %(name)s</th>
        <th class="adminheaderleft">Format Elements used by %(name)s*</th>
        <th class="adminheaderleft">All Tags Called*</th>
        </tr>
        <tr>
        <td valign="top">&nbsp;<br/>
        ''' % {'ln':ln,
               'filename':filename,
               'menu': _("Menu"),
               'close_editor': _("Close Editor"),
               'modify_template_attributes': _("Modify Template Attributes"),
               'template_editor': _("Template Editor"),
               'check_dependencies': _("Check Dependencies"),
               'name': name }

        #Print output formats
        if len(output_formats) == 0:
            out += '<p align="center"><i>No output format uses this format template.</i></p>'
            
        for output_format in output_formats:
            name = output_format['names']['generic']
            filename = output_format['filename']
            out += ''' <a href="output_format_show?ln=%(ln)s&amp;bfo=%(filename)s">%(name)s</a>''' % {'filename':filename,
                                                                                                  'name':name,
                                                                                                  'ln':ln}
            if len(output_format['tags']) > 0:
                out += "("+", ".join(output_format['tags'])+")"
            out += "<br/>"
            
        #Print format elements (and tags)
        out += '</td><td valign="top">&nbsp;<br/>'
        if len(format_elements) == 0:
            out += '<p align="center"><i>This format template uses no format element.</i></p>'
        for format_element in format_elements:
            name = format_element['name']
            out += ''' <a href="format_elements_doc?ln=%(ln)s#%(anchor)s">%(name)s</a>''' % {'name':"bfe_"+name.lower(),
                                                                                           'anchor':name.upper(),
                                                                                           'ln':ln}
            if len(format_element['tags']) > 0:
                out += "("+", ".join(format_element['tags'])+")"
            out += "<br/>"
        #Print tags
        out += '</td><td valign="top">&nbsp;<br/>'
        if len(tags) == 0:
            out += '<p align="center"><i>This format template uses no tag.</i></p>'
        for tag in tags:
            out += '''%(tag)s<br/>''' % { 'tag':tag}
        out += '''
        </td>
        </tr>
        </table>
        <b>*Note</b>: Some tags linked with this format template might not be shown. Check manually.
        '''
        return out
    
    def tmpl_admin_format_template_show(self, ln, name, description, code, filename, ln_for_preview, pattern_for_preview, editable):
        """
        Returns the editor for format templates. Edit 'format'

        @param ln language
        @param format the format to edit
        @param filename the filename of the template
        @param ln_for_preview the language for the preview (for bfo)
        @param pattern_for_preview the search pattern to be used for the preview (for bfo)
        @param editable True if we let user edit, else False
        @return editor for 'format'
        """
        _ = gettext_set_language(ln)    # load the right message language
        
        out = ""

        out += '''
        <table class="admin_wvar">
        <tr><th colspan="4" class="adminheaderleft">%(menu)s</th></tr>
        <tr>
        <td>0.&nbsp;<small><a href="format_templates_manage?ln=%(ln)s">%(close_editor)s</a></small>&nbsp;</td>
        <td>1.&nbsp;<small>%(template_editor)s</small>&nbsp;</td>
        <td>2.&nbsp;<small><a href="format_template_show_attributes?ln=%(ln)s&amp;bft=%(filename)s">%(modify_template_attributes)s</a></small>&nbsp;</td>
        <td>3.&nbsp;<small><a href="format_template_show_dependencies?ln=%(ln)s&amp;bft=%(filename)s">%(check_dependencies)s</a></small>&nbsp;</td>
        </tr>
        </table>

        <script type="text/javascript">

        function toggle_doc_visibility(){
        var doc = document.getElementById('docTable');
        var link = document.getElementById('docLink');
        if (doc.style.display=='none'){
        doc.style.display = '';
        link.innerHTML = "%(label_hide_doc)s"
        } else {
        doc.style.display = 'none';
        link.innerHTML = "%(label_show_doc)s"
        } 
        }
   
        </script>

        ''' % {'ln': ln, 'filename': filename,
               'menu': _("Menu"),
               'label_show_doc': _("Show Documentation"),
               'label_hide_doc': _("Hide Documentation"),
               'close_editor': _("Close Editor"),
               'modify_template_attributes': _("Modify Template Attributes"),
               'template_editor': _("Template Editor"),
               'check_dependencies': _("Check Dependencies")
               }

        disabled = ""
        readonly = ""
        if not editable:
            disabled = 'disabled="disabled"'
            readonly = 'readonly="readonly"'
            

        #First column: template code and preview
        out += '''
        <table width="90%%" cellspacing="5">
        <tr>
        <td>
        <form action="format_template_show_preview_or_save?ln=%(ln)s&amp;bft=%(filename)s" method="POST" target="previewiframe">
        <table width="100%%" id="mainTable"><tr>
        <th class="adminheaderleft"><div style="float:left;">Format template code</div>
        <div style="float:right;">
        <a id="docLink" href="#" onclick="toggle_doc_visibility()">%(label_hide_doc)s</a>
        </div>
        </th>
        </tr>
        <tr><td colspan="2">
        <textarea name="code" id="code" rows="25" %(readonly)s
        style="width:100%%">%(code)s</textarea>
        </td></tr>
        <tr><td align="right" valign="top">
        <input type="submit" class="adminbutton" name="save_action" value="Save Changes" %(disabled)s/>
        </td>
        </tr>
        </table>
        <table width="100%%">
        <tr><th class="adminheaderleft">
        Preview
        </th>
        </tr>
        <tr><td class="admintdright">
        <label for="ln_for_preview">Language:</label> <select id="ln_for_preview" name="ln_for_preview">
        ''' %  {'ln':ln,
                'weburl':weburl,
                'filename':filename,
                'label_hide_doc':_("Hide Documentation"),
                'code':code,
                'readonly':readonly,
                'disabled':disabled,
                'ln_for_preview':ln_for_preview,
                'pattern_for_preview':pattern_for_preview}
        
        for lang in language_list_long():
            if lang[0] == ln_for_preview:
                out += '''<option value="%(ln)s" selected="selected">%(language)s</option>''' % {'ln':lang[0],
                                                                                                 'language':lang[1]}
            else:
                out += '''<option value="%(ln)s">%(language)s</option>''' % {'ln':lang[0], 'language':lang[1]}
       

        out += '''
        </select>
        &nbsp;
        <label for="pattern_for_preview">Search Pattern: </label><input type="text" value="%(pattern_for_preview)s" size="8" name="pattern_for_preview" id="pattern_for_preview"/>&nbsp;
        
        <input type="submit" class="adminbutton" name="preview_action" value="Reload Preview"/>
        </td>
        </tr>
        <tr><td>
        <iframe src ="%(weburl)s/admin/bibformat/bibformatadmin.py/format_template_show_preview_or_save?ln=%(ln)s&amp;ln_for_preview=%(ln_for_preview)s&amp;pattern_for_preview=%(pattern_for_preview)s&amp;bft=%(filename)s" name="previewiframe"
        width="100%%" height="400"></iframe>
   
        </td></tr>
        </table>
        </form>
        </td>

        ''' % {'code':code, 'ln':ln,
               'weburl':weburl, 'filename':filename,
               'ln_for_preview':ln_for_preview,
               'pattern_for_preview':pattern_for_preview
               }


        #Second column Print documentation 
            
        out += '''
        <td valign="top" id="docTable">
        <table width="100%%"><tr>
        <th class="adminheaderleft">Elements Documentation</th>
        </tr>
        </table>
        <table width="100%%"><tr>
        <td class="admintdright">
        <form action="format_template_show_short_doc?ln=%(ln)s" method="POST" target="shortDocFrame">
        <label for="search_doc_pattern">Search for:&nbsp;</label><input type="text" size="20" name="search_doc_pattern" id="search_doc_pattern" value=""/> <input type="submit" class="adminbutton" name="search_in_doc" value="Search" />
        </form>
        </td>
        </tr>
        </table>
        
        <iframe name="shortDocFrame"
        src ="%(weburl)s/admin/bibformat/bibformatadmin.py/format_template_show_short_doc?ln=%(ln)s"
        height="90%%" width="98%%">
        </iframe>

        </td>
        </tr>
        </table>
        ''' % {'weburl':weburl, 'ln':ln}

        return out

    def tmpl_admin_format_template_show_short_doc(self, ln, format_elements):
        """
        Prints the format element documentation in a condensed way to display
        inside format template editor.
        
        This page is different from others: it is displayed inside a <iframe>
        tag in template tmpl_admin_format_template_show.

        @param ln language
        @param format_elements a list of format elements structures as returned by get_format_elements
        """
        out = '''
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
        <html>
        <head>
        <title>BibFormat Short Documentation of Format Elements</title>
        <link rel="stylesheet" href="%(cssurl)s/img/cds.css">
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        </head>
        <body>

        <script type="text/javascript">

	function toggle_visibility(element, show, r,g,b){
	var children = element.childNodes
	var child
	for(x=0; x<children.length; x++){
	  if (children[x].id == 'params'){
	    child = children[x]
	  }
	}
	if (show=='show'){
	element.style.background='rgb(201, 218, 255)'
	element.style.cursor='text'
	child.style.display=''
	} else {
	element.style.background="rgb("+r+","+g+","+b+")"
	child.style.display='none'
	} 
	}

        
   
        </script>
        ''' % {'cssurl': sweburl or weburl}
        
        if len(format_elements) == 0:
            out += '''
            <em>No format elements found</em>
            '''
        else:
            line = 0
  
            #Print elements doc
            for format_element in format_elements:
                format_attributes = format_element['attrs']
                row_content = ""
                if line % 2:
                    row_content += '''<div onmouseover="toggle_visibility(this, 'show', 235, 247, 255);"
                    onmouseout="toggle_visibility(this, 'hide', 235, 247, 255);"
                    style="background-color: rgb(235, 247, 255);"><hr/>'''
                else:
                    row_content += '''<div onmouseover="toggle_visibility(this, 'show', 255, 255, 255);"
                    onmouseout="toggle_visibility(this, 'hide', 255, 255, 255);"
                    >'''
                name = format_attributes['name']
                description = format_attributes['description']
                
                params_names = ""
                for param in format_attributes['params']:
                    params_names += "<b>"+param['name'] +'</b> '

                row_content += '''
                <code> <b>&lt;BFE_%(name)s/&gt;</b><br/></code>
                <small>%(description)s.</small>
                <div id="params" style="display:none;">
                <ul>
                ''' % {'params_names':params_names, 'name':name, 'description':description}

                for param in format_attributes['params']:
                    row_content += '''
                    <li><small><b>%(name)s</b>:&nbsp;%(description)s</small></li>
                    ''' % {'name':param['name'],
                           'description':param['description']}
                for param in format_attributes['builtin_params']:
                    row_content += '''
                    <li><small><b>%(name)s</b>:&nbsp;%(description)s</small></li>
                    ''' % {'name':param['name'],
                           'description':param['description']}

                row_content += '</ul></div>'
                if line % 2:
                    row_content += '''<hr/></div>'''
                else:
                    row_content += '</div>'
                line += 1
              
                out += row_content


        out += '''</body></html>'''
        return indent_text(out)
    
    def tmpl_admin_format_templates_management(self, ln, formats):
        """
        Returns the management console for formats. Includes list of formats and
        associated administration tools.
        
        @param ln language
        @param formats a list of dictionaries with formats attributes
        @return format management console as html
        """
        
        _ = gettext_set_language(ln)    # load the right message language


        #top of the page and table header
        out = '''
        <table class="admin_wvar">
        <tr><th colspan="4" class="adminheaderleft">%(menu)s</th></tr>
        <tr>
        <td>0.&nbsp;<small><a href="output_formats_manage?ln=%(ln)s">%(manage_output_formats)s</a></small>&nbsp;</td>
        <td>1.&nbsp;<small>%(manage_format_templates)s</small>&nbsp;</td>
        <td>2.&nbsp;<small><a href="format_elements_doc?ln=%(ln)s">%(format_elements_documentation)s</a></small>&nbsp;</td>
        <td>3.&nbsp;<small><a href="kb_manage?ln=%(ln)s">%(manage_knowledge_bases)s</a></small>&nbsp;</td>
        </tr>
        </table>

        <p>From here you can create, edit or delete formats templates.
        Have a look at the <a href="format_elements_doc?ln=%(ln)s">format elements documentation</a> to
        learn which elements you can use in your templates.</p>

  
        <table class="admin_wvar" width="95%%">
        <tr>
        <th class="adminheaderleft" >&nbsp;</th>
        <th class="adminheaderleft" >%(name)s</th>
        <th class="adminheaderleft" >%(description)s</th>
        <th class="adminheaderleft" >%(status)s</th>
        <th class="adminheaderleft" >%(last_modification_date)s</th>
        <th class="adminheadercenter" >%(action)s&nbsp;&nbsp;&nbsp;[<a href="%(weburl)s/admin/bibformat/guide.html#formatTemplates">?</a>]</th>
        </tr>
        ''' % {'name':_("Name"),
               'description':_("Description"),
               'menu': _("Menu"),
               'status':_("Status"),
               'last_modification_date':_("Last Modification Date"),
               'action':_("Action"),
               'ln':ln,
               'manage_output_formats':_("Manage Output Formats"),
               'manage_format_templates':_("Manage Format Templates"),
               'format_elements_documentation':_("Format Elements Documentation"),
               'manage_knowledge_bases':_("Manage Knowledge Bases"),
               'weburl':weburl}
        
        #table content: formats names, description and buttons
        if len(formats) == 0:
            out += '''<tr>
            <td colspan="6" class="admintd" align="center"><em>No format</em></td>
            </tr>'''
        else:
            line = 0
            for attrs in formats:
                filename = attrs['filename']
                if filename == "":
                    filename = "&nbsp;"
                name = attrs['name']
                if name == "":
                    name = "&nbsp;"
                description = attrs['description']
                if description == "":
                    description = "&nbsp;"
                last_mod_date = attrs['last_mod_date']
                status = attrs['status']
                
                disabled = ""
                if attrs['editable'] == False:
                    disabled = 'disabled="disabled"'
                     
                style = 'style="vertical-align: middle;'
                if line % 2:
                    style = 'style="vertical-align: middle;background-color: rgb(235, 247, 255);'
                line += 1

                row_content = '''<tr>
                <td class="admintdright" %(style)s">&nbsp;</td>
                <td class="admintdleft" %(style)s white-space: nowrap;"><a href="format_template_show?bft=%(filename)s&amp;ln=%(ln)s">%(name)s</a></td>
                <td class="admintdleft" %(style)s" >%(description)s</td>
                <td class="admintdleft" %(style)s white-space: nowrap;" >%(status)s</td>
                <td class="admintdleft" %(style)s white-space: nowrap;" >%(last_mod_date)s</td>
                <td class="admintd" %(style)s white-space: nowrap;">
                <form method="post" action="format_template_delete?ln=%(ln)s&amp;bft=%(filename)s">
                <input class="adminbutton" type="submit" value="%(delete)s" %(disabled)s/>
                </form>
                </td>
                </tr>
                ''' % {'filename':filename,
                       'name':name,
                       'description':description,
                       'ln':ln,
                       'style':style,
                       'disabled':disabled,
                       'last_mod_date':last_mod_date,
                       'status':status,
                       'delete':_("Delete")
                       }
                out += row_content
            
        #table footer, buttons and bottom of the page
        out += '''
        <tr>
        <td align="left" colspan="3">
        <form action="format_templates_manage?ln=%(ln)s">
        <input type="hidden" name="checking" value="1"></input>
        <input class="adminbutton" type="submit" value="%(extensive_checking)s"/>
        </form>
        </td>
        <td align="right" colspan="3">
        <form action="format_template_add?ln=%(ln)s">
        <input class="adminbutton" type="submit" value="%(add_format_template)s"/>
        </form>

        </td>
        </tr>
        </table>
        
        ''' % {'ln':ln,
               'add_format_template':_("Add New Format Template"),
               'extensive_checking':_("Check Format Templates Extensively")}

        return indent_text(out)
        
    def tmpl_admin_output_formats_management(self, ln, output_formats):
        """
        Returns the main management console for formats. Includes list of formats and
        associated administration tools.
        @param ln language
        @param output_formats a list of output formats
        @return main management console as html
        """
        
        _ = gettext_set_language(ln)    # load the right message language


        #top of the page and table header
        out = '''
        <table class="admin_wvar">
        <tr><th colspan="4" class="adminheaderleft">%(menu)s</th></tr>
        <tr>
        <td>0.&nbsp;<small>%(manage_output_formats)s</small>&nbsp;</td>
        <td>1.&nbsp;<small><a href="format_templates_manage?ln=%(ln)s">%(manage_format_templates)s</a></small>&nbsp;</td>
        <td>2.&nbsp;<small><a href="format_elements_doc?ln=%(ln)s">%(format_elements_documentation)s</a></small>&nbsp;</td>
        <td>3.&nbsp;<small><a href="kb_manage?ln=%(ln)s">%(manage_knowledge_bases)s</a></small>&nbsp;</td>
        </tr>
        </table>

        <p>From here you can add, edit or delete output formats available for collections. Output formats define which template to use. <br/>To edit templates go to the <a href="format_templates_manage?ln=%(ln)s">template administration page</a>.</p>
 
        <table class="admin_wvar" width="95%%">
        <tr>
        <th class="adminheaderleft" >&nbsp;</th>
        <th class="adminheaderleft" ><a href="output_formats_manage?ln=%(ln)s&amp;sortby=code">%(code)s</a></th>
        <th class="adminheaderleft" ><a href="output_formats_manage?ln=%(ln)s&amp;sortby=name">%(name)s</a></th>
        <th class="adminheaderleft" >%(description)s</th>
        <th class="adminheaderleft" >%(status)s</th>
        <th class="adminheaderleft" >%(last_modification_date)s</th>
        <th class="adminheadercenter" >%(action)s&nbsp;&nbsp;&nbsp;[<a href="%(weburl)s/admin/bibformat/guide.html#outputFormats">?</a>]</th>
        </tr>
        ''' %  {'code':_("Code"),
                'name':_("Name"),
                'description':_("Description"),
                'status':_("Status"),
                'last_modification_date':_("Last Modification Date"),
                'action':_("Action"),
                'ln':ln,
                'manage_output_formats':_("Manage Output Formats"),
                'manage_format_templates':_("Manage Format Templates"),
                'format_elements_documentation':_("Format Elements Documentation"),
                'manage_knowledge_bases':_("Manage Knowledge Bases"),
                'menu': _("Menu"),
                'weburl':weburl}
        
        #table content: formats names, description and buttons
        if len(output_formats) == 0:
            out += '''<tr>
            <td colspan="5" class="admintd" align="center"><em>No format</em></td>
            </tr>'''
        else:
            line = 0
            for output_format in output_formats:
                format_attributes = output_format['attrs']
                name = format_attributes['names']['generic']
                if name == "":
                    name = "&nbsp;"
                description = format_attributes['description']
                if description == "":
                    description = "&nbsp;"
                code = format_attributes['code']
                if code == "":
                    code = "&nbsp;"
                    
                last_mod_date = output_format['last_mod_date']
                status = output_format['status']
                disabled = ""
                if output_format['editable'] == False:
                    disabled = 'disabled="disabled"'
   
                style = "vertical-align: middle;"
                if line % 2:
                    style = 'vertical-align: middle; background-color: rgb(235, 247, 255);'
                line += 1
                row_content = '''<tr>
                <td class="admintdright" style="%(style)s">&nbsp;</td>
                <td class="admintdleft" style="white-space: nowrap; %(style)s">
                    <a href="output_format_show?bfo=%(code)s">%(code)s</a>
                </td>
                <td class="admintdleft" style="white-space: nowrap; %(style)s">
                    <a href="output_format_show?bfo=%(code)s">%(name)s</a>
                </td>
                <td class="admintdleft"style="%(style)s" >
                      %(description)s
                </td>
                <td class="admintd" style="white-space: nowrap; %(style)s" >%(status)s</td>
                <td class="admintdleft" style="white-space: nowrap;%(style)s" >%(last_mod_date)s</td>
                <td class="admintd" style="white-space: nowrap; %(style)s">
                <form method="POST" action="output_format_delete?ln=%(ln)s&amp;bfo=%(code)s">
                <input class="adminbutton" type="submit" value="Delete" %(disabled)s />
                </form>
                </td>
                </tr>
                ''' % {'style':style,
                       'code':code,
                       'description':description,
                       'name':name,
                       'ln':ln,
                       'disabled':disabled,
                       'last_mod_date':last_mod_date,
                       'status':status}
                
                out += row_content
                          
        #table footer, buttons and bottom of the page
        out += '''
        <tr>
        <td align="right" colspan="7">
        <form method="GET" action="output_format_add?ln=%(ln)s">
        <input class="adminbutton" type="submit" value="%(add_output_format)s"/>
        </form>
        </td>
        </tr>
        </table>
        ''' % {'ln':ln,
               'add_output_format':_("Add New Output Format")}
        
        return indent_text(out)

    def tmpl_admin_output_format_show(self, ln, code, name, rules, default, format_templates, editable):
        """
        Returns the content of an output format

        rules is an ordered list of dict (sorted by evaluation order),
        with keys 'field', 'value' and 'template'

        IMPORTANT: we display rules evaluation index starting at 1 in
        interface, but we start internally at 0
        
        @param ln language
        @param code the code of the output to show
        @param name the name of this output format
        @param rules the list of rules for this output format
        @param default the default format template of the output format
        @param format_templates the list of format_templates
        @param editable True if we let user edit, else False
        @return the management console for this output format
        """
        _ = gettext_set_language(ln)
        out = '''
          <table class="admin_wvar">
        <tr><th colspan="4" class="adminheaderleft">%(menu)s</th></tr>
        <tr>
        <td>0.&nbsp;<small><a href="output_formats_manage?ln=%(ln)s">%(close_output_format)s</a></small>&nbsp;</td>
        <td>1.&nbsp;<small>%(rules)s</small>&nbsp;</td>
        <td>2.&nbsp;<small><a href="output_format_show_attributes?ln=%(ln)s&amp;bfo=%(code)s">%(modify_output_format_attributes)s</a></small>&nbsp;</td>
        <td>3.&nbsp;<small><a href="output_format_show_dependencies?ln=%(ln)s&amp;bfo=%(code)s">%(check_dependencies)s</a></small>&nbsp;</td>
        </tr>
        </table>
        <p>Define here the rules the specifies which template to use for a given record.</p>

        ''' % {'code':code,
               'ln':ln,
               'menu':_("menu"),
               'close_output_format':_("Close Output Format"),
               'rules':_("Rules"),
               'modify_output_format_attributes':_("Modify Output Format Attributes"),
               'check_dependencies':_("Check Dependencies")
               }
        
        out += '''
        <form name="rules" action="output_format_show?ln=%(ln)s&amp;bfo=%(code)s" method="post">
        <table>
        <tr>
        <td>
        ''' % {'ln': ln, 'code':code}
        
        disabled = ""
        readonly = ""
        if not editable:
            disabled = 'disabled="disabled"'
            readonly = 'readonly="readonly"'
        
        if len(rules) == 0:
            out += '''<p align="center"><em>No special rule</em></p>'''
        
        line = 1
        for rule in rules:
            out += '''
            <table align="center" class="admin_wvar">
            <tr>
            '''  

            out += '''
            <td rowspan="2" class="adminheader" style="vertical-align: middle;">'''
            if line > 1:
                out += '''
                <input type="image" src="%(weburl)s/img/smallup.gif" alt="Increase priority of rule %(row)s" name="+ %(row)s" value="+ %(row)s" %(disabled)s/></div>
                ''' % {'weburl':weburl, 'row':line, 'disabled':disabled}
              
            out += '''<div>%(row)s</div>''' % { 'row':line}
            if line < len(rules):
                out += '''
                <input type="image" src="%(weburl)s/img/smalldown.gif" alt="Decrease priority of rule %(row)s" name="- %(row)s" value="- %(row)s" %(disabled)s/>
                ''' % {'weburl':weburl,
                       'row':line,
                       'disabled':disabled}

            out += '''</td>
            <td class="adminheaderleft">&nbsp;</td>
            '''
    
            out += '''
            <td class="adminheaderleft" style="white-space: nowrap;">
            Use template&nbsp;<select name="r_tpl" %(disabled)s>''' % {'disabled':disabled}

           
            for template in format_templates:
                attrs = format_templates[template]['attrs']
                attrs['template'] = template
                
                if template != rule['template']:
                    out += '''<option value="%(template)s">%(name)s</option>''' % attrs
                else:
                    out += '''<option value="%(template)s" selected="selected">%(name)s</option>''' % attrs
            
            if not format_templates.has_key(rule['template']) and rule['template'] != "":
                #case where a non existing format tempate is use in output format
                #we need to add it as option
                out += '''<option value="%s" selected="selected">%s</option>''' % (rule['template'],
                                                                                   rule['template'])
                
            out += '''</select>&nbsp;if field
            &nbsp;<input type="text" name="r_fld" value="%(field)s" size="10" %(readonly)s/>&nbsp;is equal to&nbsp;<input type="text" value="%(value)s" name="r_val" %(readonly)s/>
            </td>
            <td class="adminheaderright" style="vertical-align: middle;">
            &nbsp;[<a href="%(weburl)s/admin/bibformat/guide.html#rulesOutputFormat">?</a>]
            </td>
            </tr>
            ''' % {'weburl':weburl,
                   'field': rule['field'],
                   'value':rule['value'],
                   'readonly':readonly}

            out += '''
            <tr>
            <td colspan ="3" class="adminheaderright" style="vertical-align: middle; white-space: nowrap;">
            <input type="submit" class="adminbutton" name="r_upd" value="%(remove_rule_label)s %(row)s" %(disabled)s/>&nbsp;
            </td>
            </tr>
            </table>
            ''' % {'remove_rule_label': _("Remove Rule"),
                   'row':line,
                   'disabled':disabled}
            line += 1
            
        out += '''
        <table width="100%" align="center" class="admin_wvar">
        <tr>
        '''

        out += '''
        <td width="30" class="adminheaderleft">&nbsp;</td>
        <td class="adminheaderleft">By default use <select id="default" name="default" %(disabled)s>''' % {'disabled':disabled}

        for template in format_templates:
            attrs = format_templates[template]['attrs']
            attrs['template'] = template
            if template  != default:
                out += '''<option value="%(template)s">%(name)s</option>''' % attrs
            else:
                out += '''<option value="%(template)s" selected="selected">%(name)s</option>''' % attrs

        if not format_templates.has_key(default) and default!= "":
            #case where a non existing format tempate is use in output format
            #we need to add it as option (only if it is not empty string)
            out += '''<option value="%s" selected="selected">%s</option>''' % (default,default)
        out += '''</select></td>
        </tr>
        </table>
        <div align="right">
        <input tabindex="6" class="adminbutton" type="submit" name="r_upd" value="%(add_new_rule_label)s" %(disabled)s/>
        <input tabindex="7" class="adminbutton" type="submit" name="r_upd" value="%(save_changes_label)s" %(disabled)s/>
        </div>
        </td>
        </tr>
        </table>
        </form>
        ''' % {'add_new_rule_label':_("Add New Rule"),
             'save_changes_label':_("Save Changes"),
             'disabled':disabled
             }
      
        return indent_text(out)

    def tmpl_admin_output_format_show_attributes(self, ln, name, description, content_type, code, names_trans, editable):
        """
        Returns a page to change output format name and description

        names_trans is an ordered list of dicts with keys 'lang' and 'trans'

        @param ln language
        @param name the name of the format
        @param description the description of the format
        @param code the code of the format
        @param content_type the (MIME) content type of the ouput format
        @param names_trans the translations in the same order as the languages from get_languages()
        @param editable True if we let user edit, else False
        @return editor for output format attributes
        """
        _ = gettext_set_language(ln)    # load the right message language

        out = ""

        out += '''
        <table class="admin_wvar">
        <tr><th colspan="4" class="adminheaderleft">%(menu)s</th></tr>
        <tr>
        <td>0.&nbsp;<small><a href="output_formats_manage?ln=%(ln)s">%(close_output_format)s</a></small>&nbsp;</td>
        <td>1.&nbsp;<small><a href="output_format_show?ln=%(ln)s&amp;bfo=%(code)s">%(rules)s</a></small>&nbsp;</td>
        <td>2.&nbsp;<small>%(modify_output_format_attributes)s</small>&nbsp;</td>
        <td>3.&nbsp;<small><a href="output_format_show_dependencies?ln=%(ln)s&amp;bfo=%(code)s">%(check_dependencies)s</a></small>&nbsp;</td>
        </tr>
        </table><br/>
        ''' % {'ln':ln,
               'code':code,
               'close_output_format':_("Close Output Format"),
               'rules':_("Rules"),
               'modify_output_format_attributes':_("Modify Output Format Attributes"),
               'check_dependencies':_("Check Dependencies"),
               'menu':_("Menu")
               }

        disabled = ""
        readonly = ""
        if not editable:
            disabled = 'disabled="disabled"'
            readonly = 'readonly="readonly"'
        
        out += '''
        <form action="output_format_update_attributes?ln=%(ln)s&amp;bfo=%(code)s" method="POST">
        <table class="admin_wvar">
        <tr>
        <th colspan="2" class="adminheaderleft">
        Output Format Attributes&nbsp;[<a href="%(weburl)s/admin/bibformat/guide.html#attrsOutputFormat">?</a>]</th>
        </tr>
        <tr>
        <td class="admintdright"><label for="outputFormatCode">Code</label>:&nbsp;</td>
        <td><input tabindex="1" name="code" type="text" id="outputFormatCode" maxlength="6" size="6" value="%(code)s" %(readonly)s/></td>
        </tr>
        <td class="admintdright"><label for="outputFormatContentType">Content type</label>:&nbsp;</td>
        <td><input tabindex="2" name="content_type" type="text" id="outputFormatContentType" size="25"  value="%(content_type)s" %(readonly)s/> <small>Mime content-type. Specifies how the browser should handle this output.</small></td> 
        <tr>
        <td class="admintdright"><label for="outputFormatName">Name</label>:&nbsp;</td>
        <td><input tabindex="3" name="name" type="text" id="outputFormatName" size="25" value="%(name)s" %(readonly)s/></td>
        </tr>
        ''' % {'name': name,
               'ln':ln,
               'code':code,
               'content_type':content_type,
               'readonly':readonly,
               'weburl':weburl}
        
        #Add translated names
        i = 3
        for name_trans in names_trans:
            i += 1
            out += '''
            <tr>
            <td class="admintdright"><label for="outputFormatName%(i)s">%(lang)s Name</label>:&nbsp;</td>
            <td><input tabindex="%(i)s" name="names_trans" type="text" id="outputFormatName%(i)s" size="25" value="%(name)s" %(readonly)s/></td>
            </tr>''' % {'name':name_trans['trans'],
                        'lang':name_trans['lang'],
                        'i':i,
                        'readonly':readonly}
        #Description and end of page
        out += '''
        <tr>
        <td  class="admintdright" valign="top"><label for="outputFormatDescription">Description</label>:&nbsp;</td>
        <td><textarea tabindex="%(tabindexdesc)s" name="description" id="outputFormatDescription" rows="4" cols="25" %(readonly)s>%(description)s</textarea> </td>
        </tr>
        <tr>
        <td colspan="2" align="right"><input tabindex="%(tabindexbutton)s" class="adminbutton" type="submit" value="Update Output Format Attributes" %(disabled)s/></td>
        </tr>
        </table>
        </form>
     
        ''' % {'description': description,
               'tabindexdesc': i + 1,
               'tabindexbutton': i + 2,
               'readonly':readonly,
               'disabled':disabled}

        return out


    def tmpl_admin_output_format_show_dependencies(self, ln, name, code, format_templates):
        """
        Shows the dependencies of the given format.

        @param name the name of the output format
        @param code the code of the output format
        @param format_templates format templates that depend on this format (and also elements and tags)
        """
        _ = gettext_set_language(ln)    # load the right message language
        out = '''
        <table class="admin_wvar">
        <tr><th colspan="4" class="adminheaderleft">%(menu)s</th></tr>
        <tr>
        <td>0.&nbsp;<small><a href="output_formats_manage?ln=%(ln)s">%(close_output_format)s</a></small>&nbsp;</td>
        <td>1.&nbsp;<small><a href="output_format_show?ln=%(ln)s&amp;bfo=%(code)s">%(rules)s</a></small>&nbsp;</td>
        <td>2.&nbsp;<small><a href="output_format_show_attributes?ln=%(ln)s&amp;bfo=%(code)s">%(modify_output_format_attributes)s</a></small>&nbsp;</td>
        <td>3.&nbsp;<small>%(check_dependencies)s</small>&nbsp;</td>
        </tr>
        </table><br/>
        <table width="90%%" class="admin_wvar"><tr>

        <th class="adminheaderleft">Output Formats that use %(name)s</th>
        <th class="adminheaderleft">Format Elements used by %(name)s</th>
        <th class="adminheaderleft">Tags Called*</th>
        </tr>
        ''' % {'name': name,
               'code': code,
               'ln':ln,
               'close_output_format':_("Close Output Format"),
               'rules':_("Rules"),
               'modify_output_format_attributes':_("Modify Output Format Attributes"),
               'check_dependencies':_("Check Dependencies"),
               'menu': _("Menu")
               }
        
        if len(format_templates) == 0:
            out += '''<tr><td colspan="3"><p align="center">
            <i>This output format uses no format template.</i></p></td></tr>'''
            
        for format_template in format_templates:
            name = format_template['name']
            filename = format_template['filename']
            out += '''<tr><td><a href="format_template_show?bft=%(filename)s&amp;ln=%(ln)s">%(name)s</a></td>
            <td>&nbsp</td><td>&nbsp</td></tr>''' % {'filename':filename,
                                                    'name':name,
                                                    'ln':ln}
            for format_element in format_template['elements']:
                name = format_element['name']
                filename = format_element['filename']
                out += '''<tr><td>&nbsp</td>
                <td><a href="format_elements_doc?ln=%(ln)s#%(anchor)s">%(name)s</a></td>
                <td>&nbsp</td></tr>''' % {'anchor':name.upper(),
                                          'name':name,
                                          'ln':ln}
                for tag in format_element['tags']:
                    out += '''<tr><td>&nbsp</td><td>&nbsp</td>
                    <td>%(tag)s</td></tr>''' % {'tag':tag}
        
        out += '''
        </table>
        <b>*Note</b>: Some tags linked with this format template might not be shown. Check manually.
        '''
        return out
        
    def tmpl_admin_format_elements_documentation(self, ln, format_elements):
        """
        Returns the main management console for format elements. Includes list of formats elements and
        associated administration tools.
        
        @param ln language
        @param formats a list of dictionaries with formats elements attributes
        @return main management console as html
        """
        
        _ = gettext_set_language(ln)    # load the right message language


        #top of the page and table header
        out = '''
        <table class="admin_wvar">
        <tr><th colspan="4" class="adminheaderleft">%(menu)s</th></tr>
        <tr>
        <td>0.&nbsp;<small><a href="output_formats_manage?ln=%(ln)s">%(manage_output_formats)s</a></small>&nbsp;</td>
        <td>1.&nbsp;<small><a href="format_templates_manage?ln=%(ln)s">%(manage_format_templates)s</a></small>&nbsp;</td>
        <td>2.&nbsp;<small>%(format_elements_documentation)s</small>&nbsp;</td>
        <td>3.&nbsp;<small><a href="kb_manage?ln=%(ln)s">%(manage_knowledge_bases)s</a></small>&nbsp;</td>
        </tr>
        </table>

        
        <p>Here you can manage the formats elements, the elementary bricks for formats.</p>
        ''' % {'ln':ln,
               'menu': _("Menu"),
               'manage_output_formats':_("Manage Output Formats"),
               'manage_format_templates':_("Manage Format Templates"),
               'format_elements_documentation':_("Format Elements Documentation"),
               'manage_knowledge_bases':_("Manage Knowledge Bases")
               }

 
        #table content: formats names, description and actions
        if len(format_elements) == 0:
            out += '''
            <em>No format elements found</em>
            '''
        else:
            
            #Print summary of elements (name + decription)
            out += '''<h2>Summary table of elements</h2>'''
            out += '''<table width="90%">'''
            for format_element in format_elements:
                format_attributes = format_element['attrs']
                out += '''
                <tr>
                <td>
                <code><a href="#%(name)s">&lt;BFE_%(name)s/&gt;</a></code>
                </td>
                <td>
                %(description)s
                </td>
                </tr>
                ''' % format_attributes
            out += "</table>"
            
            #Print details of elements
            out += '''<h2>Details of elements</h2>'''
            for format_element in format_elements:
                format_attributes = format_element['attrs']
                element_name = format_attributes['name']
                out += self.tmpl_admin_print_format_element_documentation(ln, element_name, format_attributes)
            
        #table footer, buttons and bottom of the page
        out += ''' 
        <table align="center" width="95%">
        </table>'''
        return indent_text(out)

    def tmpl_admin_print_format_element_documentation(self, ln, name, attributes, print_see_also=True):
        """
        Prints the formatted documentation of a single element

        @param ln language
        @param name the name of the element
        @param attributes the attributes of the element, as returned by get_format_element_attrs_from_*
        @param print_see_also if True, prints links to other sections related to element
        """
        params_names = ""
        for param in attributes['params']:
            params_names += "<b>"+param['name'] +'</b>="..." '

        out = '''
        <a name="%(name)s"></a><h3>%(name)s</h3>

        <b>&lt;BFE_%(name)s</b> %(params_names)s<b>/&gt;</b><br/><br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>%(description)s.</em><br/><br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Parameters:</b><br/>
        ''' % {'params_names': params_names,
               'name':name,
               'description': attributes['description']}
        for param in attributes['params']:
            out += '''
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <code>%(name)s</code> - %(description)s. ''' % param
            if param['default'] != "":
                default = cgi.escape(param['default'])
                if default.strip() == "":
                    default = "&nbsp;"
                out += '''
                Default value is &laquo;<code>%s</code>&raquo;
                ''' % default

            out += '<br/>'

        for param in attributes['builtin_params']:
            out += '''
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <code>%(name)s</code> - %(description)s. ''' % param
            if param['default'] != "":
                default = cgi.escape(param['default'])
                if default.strip() == "":
                    default = "&nbsp;"
                out += '''
                Default value is &laquo;<code>%s</code>&raquo;
                ''' % default
                
            out += '<br/>'

        if print_see_also:
            out += '''<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <b>See also:</b><br/>'''

            for element in attributes['seealso']:
                element_name = element.split('.')[0].upper()
                out += '''
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <a href="#%(name)s">Element <em>%(name)s</em></a><br/>''' % {'name':element_name}
            out += '''
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <a href ="format_element_show_dependencies?ln=%(ln)s&amp;bfe=%(bfe)s">Dependencies of this element</a><br/>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <a href ="validate_format?ln=%(ln)s&amp;bfe=%(bfe)s">The correctness of this element</a><br/>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <a href ="format_element_test?ln=%(ln)s&amp;bfe=%(bfe)s">Test this element</a><br/>
            ''' % {'ln':ln, 'bfe':name}

        return out
            
    def tmpl_admin_format_element_show_dependencies(self, ln, name, format_templates, tags):
        """
        Shows the dependencies of the given format element

        @param name the name of the element
        @param format_templates format templates that depend on this element
        @param tags the tags that are called by this format element
        """
        out = '''
        <p>Go back to <a href="format_elements_doc?ln=%(ln)s#%(name)s">documentation</a></p>
        ''' % {'ln':ln, 'name':name.upper()}
        
        out += ''' <table width="90%" class="admin_wvar"><tr>'''
        out += '''
        <th class="adminheaderleft">Format Templates that use %(name)s</th>
        <th class="adminheaderleft">Tags Called*</th>
        </tr>
        <tr>
        <td>&nbsp;<br/>''' % {"name": name}

        
        #Print format elements (and tags)
        if len(format_templates) == 0:
            out += '''<p align="center">
            <i>This format element is not used in any format template.</i></p>'''
        for format_template in format_templates:
            name = format_template['name']
            filename = format_template['filename']
            out += '''<a href="format_template_show?ln=%(ln)s&amp;bft=%(filename)s">%(name)s</a><br/>''' % {'filename':filename,
                                                                                                        'name':name,
                                                                                                        'ln':ln}

        #Print tags
        out += "</td><td>&nbsp;<br/>"
        if len(tags) == 0:
            out += '''<p align="center">
            <i>This format element uses no tag.</i></p>'''
        for tag in tags:
            out += '''%(tag)s<br/>''' % {'tag':tag}
        out += '''
        </td>
        </tr>
        </table>
        <b>*Note</b>: Some tags linked with this format template might not be shown. Check manually.
        '''
        return out

    def tmpl_admin_format_element_test(self, ln, bfe, description, param_names, param_values, param_descriptions, result):
        """
        Prints a page where the user can test the given format element with his own parameters.

        @param ln language
        @param bfe the format element name
        @param description a description of the element
        @param param_names a list of parameters names/labels
        @param param_values a list of values for parameters
        @param param_descriptions a list of description for parameters
        @param result the result of the evaluation
        """

        out = '''
        <p>Go back to <a href="format_elements_doc?ln=%(ln)s#%(name)s">documentation</a></p>
        ''' % {'ln':ln, 'name':bfe.upper()}

        out += '''
        <h3>&lt;BFE_%(bfe)s /&gt;</h3>
        <p>%(description)s</p>
        <table width="100%%"><tr><td>
        <form method="post" action="format_element_test?ln=%(ln)s&amp;bfe=%(bfe)s">
        <table>
        ''' % {'bfe':bfe, 'ln':ln, 'description':description }
        
        for i in range(len(param_names)):
            out += '''
            <tr>
            <td class="admintdright">%(name)s</td>
            <td class="admintdright"><input type="text" name="param_values" value="%(value)s"/></td>
            <td class="admintdleft">%(description)s&nbsp;</td>
            </tr>
            ''' % {'name':param_names[i],
                   'value':param_values[i],
                   'description':param_descriptions[i]}

        out += '''
        <tr><td colspan="2" class="admintdright"><input type="submit" class="adminbutton" value="Test!"/></td>
        <td>&nbsp;</td>
        </tr>
        </table>
        </form>
        <fieldset style="display:inline;margin-left:auto;margin-right:auto;">
        <legend>Result:</legend>%(result)s</fieldset>
        
        ''' % {'result':result}

        out += '''
        </td></tr><tr><td>
        '''
        #out += self.tmpl_admin_print_format_element_documentation(ln, bfe, attributes, False)
        out += '''</td></tr></table>'''
        return out
        
    def tmpl_admin_add_format_element(self, ln):
        """
        Shows how to add a format element (mainly doc)

        @param ln language
        """
        _ = gettext_set_language(ln)    # load the right message language

        out = '''
        <p>To add a new basic element (only fetch the value of a field, without special post-processing), go to the <a href="%(weburl)sadmin/bibindex/bibindexadmin.py/field">BibEdit "Manage Logical Fields"</a> page and add a name for a field. Make sure that the name is unique and corresponds well to the field. For example, to add an element that fetch the value of field 245__%, add a new logical field with name "title" and field "245__%". Then in your template, call BFE_TITLE to print the title.</p>
        <p>To add a new complex element (for eg. special formatting of the field, condition on the value, etc.) you must go to the lib/python/invenio/bibformat_elements directory of your Invenio installation, and add a new format element file. Read documentation for more information.</p>
        ''' % {'weburl':weburl}

        return out
        
    def tmpl_admin_kbs_management(self, ln, kbs):
        """
        Returns the main management console for knowledge bases.
        
        @param ln language
        @param kbs a list of dictionaries with knowledge bases attributes
        @return main management console as html
        """
        
        _ = gettext_set_language(ln)    # load the right message language

        #top of the page and table header
        out = '''
        <table class="admin_wvar">
        <tr><th colspan="4" class="adminheaderleft">%(menu)s</th></tr>
        <tr>
        <td>0.&nbsp;<small><a href="output_formats_manage?ln=%(ln)s">%(manage_output_formats)s</a></small>&nbsp;</td>
        <td>1.&nbsp;<small><a href="format_templates_manage?ln=%(ln)s">%(manage_format_templates)s</a></small>&nbsp;</td>
        <td>2.&nbsp;<small><a href="format_elements_doc?ln=%(ln)s">%(format_elements_documentation)s</a></small>&nbsp;</td>
        <td>3.&nbsp;<small>%(manage_knowledge_bases)s</small>&nbsp;</td>
        </tr>
        </table>
        <table class="admin_wvar" width="95%%">
        <tr>
        <th class="adminheaderleft" >&nbsp;</th>
        <th class="adminheaderleft" >Name</th>
        <th class="adminheaderleft" >Description</th>
        <th class="adminheadercenter" >Action&nbsp;&nbsp;&nbsp;[<a href="%(weburl)s/admin/bibformat/guide.html#KBs">?</a>]</th>
        </tr>''' % {'ln':ln,
                    'menu':_("Menu"),
                    'manage_output_formats':_("Manage Output Formats"),
                    'manage_format_templates':_("Manage Format Templates"),
                    'format_elements_documentation':_("Format Elements Documentation"),
                    'manage_knowledge_bases':_("Manage Knowledge Bases"),
                    'weburl':weburl}
                
        #table content: kb names, description and actions
        if len(kbs) == 0:
            out += '''<tr>
            <td colspan="5" class="admintd" align="center"><em>No Knowledge Base</em></td>
            </tr>'''
        else:
            line = 0
            for kb_attributes in kbs :
                kb_attributes['style'] = ""
                if line % 2:
                    kb_attributes['style'] = 'background-color: rgb(235, 247, 255);'
                line += 1
                kb_attributes['ln'] = ln
                kb_attributes['weburl'] = weburl
                row_content = '''<tr>
                <td class="admintdright" style="vertical-align: middle; %(style)s">&nbsp;</td>
                <td class="admintdleft" style="vertical-align: middle; %(style)s white-space: nowrap;"><a href="kb_show?ln=%(ln)s&amp;amp;kb=%(id)s">%(name)s</a></td>
                <td class="admintdleft"style="vertical-align: middle; %(style)s">%(description)s</td>
                <td class="admintd" style="vertical-align: middle; %(style)s white-space: nowrap;">
                <form action="kb_delete?ln=%(ln)s" type="POST">
                <input type="submit" class="adminbutton" value="Delete">
                <input type="hidden" id="kb" name="kb" value="%(id)s">
                </form>
                </td>
                </tr>
                ''' % kb_attributes
                out += row_content
            
        #table footer, buttons and bottom of the page
        out += ''' </table>
        <table align="center" width="95%">
        <tr>
        <td align="left" valign="top">&nbsp;</td>
        '''
        out += '''
        <td align="right">
        <form action="kb_add?ln=%(ln)s">
        <input class="adminbutton" type="submit" value="Add New Knowledge Base"/>
        </form>
        </td>
        </tr>
        </table>''' % {'ln': ln}
        
        return indent_text(out)

    def tmpl_admin_kb_show(self, ln, kb_id, kb_name, mappings, sortby):
        """
        Returns the content of a knowledge base.
        
        @param ln language
        @param kb_id the id of the kb
        @param kb_name the name of the kb
        @param content a list of dictionaries with mappings
        @param sortby the sorting criteria ('from' or 'to')
        @return main management console as html
        """
     
        _ = gettext_set_language(ln)    # load the right message language
        
        #top of the page and  main table that split screen in two parts
        out = '''
        <table class="admin_wvar">
        <tr><th colspan="4" class="adminheaderleft">%(menu)s</th></tr>
        <tr>
        <td>0.&nbsp;<small><a href="kb_manage?ln=%(ln)s&amp;sortby=%(sortby)s">%(close)s</a></small>&nbsp;</td>
        <td>1.&nbsp;<small>%(mappings)s</small>&nbsp;</td>
        <td>2.&nbsp;<small><a href="kb_show_attributes?ln=%(ln)s&amp;kb=%(kb_id)s&amp;sortby=%(sortby)s">%(attributes)s</a></small>&nbsp;</td>
        <td>3.&nbsp;<small><a href="kb_show_dependencies?ln=%(ln)s&amp;kb=%(kb_id)s&amp;sortby=%(sortby)s">%(dependencies)s</a></small>&nbsp;</td>
        </tr>
        </table> ''' % {'ln':ln,
                        'kb_id':kb_id,
                        'sortby':sortby,
                        'close': _("Close Editor"),
                        'mappings': _("Knowledge Base Mappings"),
                        'attributes':_("Knowledge Base Attributes"),
                        'dependencies':_("Knowledge Base Dependencies"),
                        'menu': _("Menu")}

        
        out += '''
        <p>Here you can add new mappings to this base and change the base attributes.</p>
        <table width="100%" align="center">
        <tr>
        '''

        #First column of table: add mapping form
        out += '''
        <td width="300" valign="top">
        
        <form name="addNewMapping"
        action="kb_add_mapping?ln=%(ln)s&amp;kb=%(kb_id)s&amp;sortby=%(sortby)s" method="post">''' % {'ln':ln,
                                                                                                      'kb_id':kb_id,
                                                                                                      'sortby':sortby}
        out += '''
        <table class="admin_wvar" width="100%%">
        <tr>
        <th colspan="2" class="adminheaderleft">Add New Mapping &nbsp;[<a href="%(weburl)s/admin/bibformat/guide.html#addMappingKB">?</a>]</th>
        </tr>
        <tr>
        <td class="admintdright"><label for="mapFrom"><span style="white-space: nowrap;">Map From</span></label>:&nbsp;</td>
        <td><input tabindex="1" name="mapFrom" type="text" id="mapFrom" size="25"/></td>
        </tr>
        <tr>
        <td class="admintdright"><label for="mapTo">To</label>:&nbsp;</td>
        <td><input tabindex="2" name="mapTo" type="text" id="mapTo" size="25"/></td>
        </tr>
        <tr>
        <td colspan="2" align="right"><input tabindex="3" class="adminbutton" type="submit" value="Add new Mapping"/></td>
        </tr>
        </table>
        </form>
        </td>
        ''' % {'weburl':weburl}
                
        #Second column: mappings table
        #header and footer
        out += '''
        <td valign="top">
            
        <table class="admin_wvar">
        <thead>
        <tr>
        <th class="adminheaderleft" width="25">&nbsp;</th>
        <th class="adminheaderleft" width="34%%"><a href="kb_show?ln=%(ln)s&amp;kb=%(kb_id)s&amp;sortby=from">Map From</a></th>
        <th class="adminheaderleft">&nbsp;</th>
        <th class="adminheaderleft" width="34%%"><a href="kb_show?ln=%(ln)s&amp;kb=%(kb_id)s&amp;sortby=to">To</a></th>
        <th class="adminheadercenter" width="25%%">Action&nbsp;&nbsp;&nbsp;[<a href="%(weburl)s/admin/bibformat/guide.html#removeMappingKB">?</a>]</th>
        </tr>
        </thead>
        <tfoot>
        <tr>
        <td colspan="5">&nbsp;</td>
        </tr>
        </tfoot>
        <tbody>
        ''' % {'ln':ln,
               'kb_id':kb_id,
               'weburl':weburl}
        
        #table content: key, value and actions
        if len(mappings) == 0:
            out += '''
            <tr>
            <td colspan="5" class="admintd" align="center"><em>Knowledge base is empty</em></td>
            </tr></tbody>'''
        else:
            line = 0
            tabindex_key = 6
            tabindex_value = 7
            tabindex_save_button = 8
            for mapping in mappings:
                style = "vertical-align: middle;"
                if line % 2:
                    style += 'background-color: rgb(235, 247, 255);'
                line += 1
                tabindex_key += 3
                tabindex_value += 3
                tabindex_save_button += 3

                row_content = '''
                <tr>
                <td colspan="5">
                <form action="kb_edit_mapping?ln=%(ln)s&amp;kb=%(kb_id)s&amp;sortby=%(sortby)s" name="%(key)s" method="post">
                <table>
                <tr>
                <td class="admintdright" style="%(style)s" width="5">
                &nbsp;
                <input type="hidden" name="key" value="%(key)s"/>
                </td>
                <td class="admintdleft" style="%(style)s">
                    <input type="text" name="mapFrom" size="30" maxlength="255" value="%(key)s" tabindex="%(tabindex_key)s"/>
                </td>
                <td class="admintdleft" style="%(style)s white-space: nowrap;" width="5">=&gt;</td> 
                <td class="admintdleft"style="%(style)s">
                     <input type="text" name="mapTo" size="30" value="%(value)s" tabindex="%(tabindex_value)s">
                </td>
                <td class="admintd" style="%(style)s white-space: nowrap;">
                     <input class="adminbutton" type="submit" name="update" value="Save" tabindex="%(tabindex_save_button)s"/>
                     <input class="adminbutton" type="submit" name="delete"value="Delete"/></td>
                </tr></table></form></td></tr>
                ''' % {'key': mapping['key'],
                       'value':mapping['value'],
                       'ln':ln,
                       'style':style, 
                       'tabindex_key': tabindex_key,
                       'tabindex_value': tabindex_value,
                       'tabindex_save_button': tabindex_save_button,
                       'kb_id':kb_id,
                       'sortby':sortby}
                
                out += row_content
            
        #End of tables
        out += '''</tbody></table>
        </td>
        '''
        out+= '''
        <td width="20%">&nbsp;</td>
        </tr>
        </table>
        '''

        #add script that will put focus on first field of "add mapping" form
        out += '''
        <script type="text/javascript">
        self.focus();document.addNewMapping.mapFrom.focus()
        </script>
        '''

        return indent_text(out)


    def tmpl_admin_kb_show_attributes(self, ln, kb_id, kb_name, description, sortby):
        """
        Returns the attributes of a knowledge base.
        
        @param ln language
        @param kb_id the id of the kb
        @param kb_name the name of the kb
        @param description the description of the kb
        @param sortby the sorting criteria ('from' or 'to')
        @return main management console as html
        """
     
        _ = gettext_set_language(ln)    # load the right message language
        
        out = '''
        <table class="admin_wvar">
        <tr><th colspan="4" class="adminheaderleft">%(menu)s</th></tr>
        <tr>
        <td>0.&nbsp;<small><a href="kb_manage?ln=%(ln)s&amp;sortby=%(sortby)s">%(close)s</a></small>&nbsp;</td>
        <td>1.&nbsp;<small><a href="kb_show?ln=%(ln)s&amp;kb=%(kb_id)s&amp;sortby=%(sortby)s">%(mappings)s</a></small>&nbsp;</td>
        <td>2.&nbsp;<small>%(attributes)s</small>&nbsp;</td>
        <td>3.&nbsp;<small><a href="kb_show_dependencies?ln=%(ln)s&amp;kb=%(kb_id)s&amp;sortby=%(sortby)s">%(dependencies)s</a></small>&nbsp;</td>
        </tr>
        </table> ''' % {'ln':ln,
                        'kb_id':kb_id,
                        'sortby':sortby,
                        'close': _("Close Editor"),
                        'menu': _("Menu"),
                        'mappings': _("Knowledge Base Mappings"),
                        'attributes':_("Knowledge Base Attributes"),
                        'dependencies':_("Knowledge Base Dependencies")}
                
        out += '''
        <form name="updateAttributes"
        action="kb_update_attributes?ln=%(ln)s&amp;kb=%(kb_id)s&amp;sortby=%(sortby)s" method="post">
        <table class="admin_wvar">
        <tr>

        ''' % {'ln':ln,
               'kb_id':kb_id,
               'sortby':sortby}

        out += '''
        <th colspan="2" class="adminheaderleft">%(kb_name)s attributes&nbsp;[<a href="%(weburl)s/admin/bibformat/guide.html#attrsKB">?</a>]</th>''' % {'kb_name': kb_name,
                                                                                                                                                       'weburl': weburl}

        out += '''
         </tr>
        <tr>
        <td class="admintdright">
        <input type="hidden" name="key" value="%(kb_id)s"/>
        <label for="name">Name</label>:&nbsp;</td>
        <td><input tabindex="4" name="name" type="text" id="name" size="25" value="%(kb_name)s"/></td>
        </tr>
        <tr>
        <td  class="admintdright" valign="top"><label for="description">Description</label>:&nbsp;</td>
        <td><textarea tabindex="5" name="description" id="description" rows="4" cols="25">%(kb_description)s</textarea> </td>
        </tr>
        <tr>
        <td>&nbsp;</td>
        <td align="right"><input tabindex="6" class="adminbutton" type="submit" value="Update Base Attributes"/></td>
        </tr>
        </table>
        </form></td>''' % {'kb_name': kb_name,
                           'kb_description': description,
                           'kb_id':kb_id}

        return indent_text(out)

    def tmpl_admin_kb_show_dependencies(self, ln, kb_id, kb_name, sortby, format_elements):
        """
        Returns the attributes of a knowledge base.
        
        @param ln language
        @param kb_id the id of the kb
        @param kb_name the name of the kb
        @param sortby the sorting criteria ('from' or 'to')
        @param format_elements the elements that use this kb
        """
     
        _ = gettext_set_language(ln)    # load the right message language
        
        out = '''
        <table class="admin_wvar">
        <tr><th colspan="4" class="adminheaderleft">%(menu)s</th></tr>
        <tr>
        <td>0.&nbsp;<small><a href="kb_manage?ln=%(ln)s&amp;sortby=%(sortby)s">%(close)s</a></small>&nbsp;</td>
        <td>1.&nbsp;<small><a href="kb_show?ln=%(ln)s&amp;kb=%(kb_id)s&amp;sortby=%(sortby)s">%(mappings)s</a></small>&nbsp;</td>
        <td>2.&nbsp;<small><a href="kb_show_attributes?ln=%(ln)s&amp;kb=%(kb_id)s&amp;sortby=%(sortby)s">%(attributes)s</a></small>&nbsp;</td>
        <td>3.&nbsp;<small>%(dependencies)s</small>&nbsp;</td>
        </tr>
        </table> <br/>''' % {'ln':ln,
                             'kb_id':kb_id,
                             'sortby':sortby,
                             'close': _("Close Editor"),
                             'menu' : _("Menu"),
                             'mappings': _("Knowledge Base Mappings"),
                             'attributes':_("Knowledge Base Attributes"),
                             'dependencies':_("Knowledge Base Dependencies")}

        out += ''' <table width="90%" class="admin_wvar"><tr>'''
        out += '''
        <th class="adminheaderleft">Format Elements used by %(name)s*</th>
        </tr>
        <tr>
        <td valign="top">&nbsp;''' % {"name": kb_name}

        if len(format_elements) == 0:
            out += '<p align="center"><i>This knowledge base is not used in any format elements.</i></p>'
        for format_element in format_elements:
            name = format_element['name']
            out += '''<a href="format_elements_doc?ln=%(ln)s#%(anchor)s">%(name)s</a><br/>''' % {'name':"bfe_"+name.lower(),
                                                                                                 'anchor':name.upper(),
                                                                                                 'ln':ln}
        out += '''
        </td>
        </tr>
        </table>
        <b>*Note</b>: Some knowledge base usages might not be shown. Check manually.
        '''
        
        return indent_text(out)

    def tmpl_admin_validate_format(self, ln, errors):
        """
        Prints the errors of the validation of a format (might be any
        kind of format)

        @param ln language
        @param errors a list of tuples (error code, string error message)
        """
        _ = gettext_set_language(ln)    # load the right message language
        out = ""
 
        if len(errors) == 0:
            out += '''<span style="color: rgb(0, 255, 0);" >%s.</span>''' % _('No problem found with format')
        elif len(errors) == 1:
            out += '''<span style="color: rgb(255, 0, 0);" >%s:</span><br/>''' % _('An error has been found')
        else:
            out += '''<span style="color: rgb(255, 0, 0);" >%s:</span><br/>''' % _('The following errors have been found')
            
        for error in errors:
            out += error + "<br/>"

        return indent_text(out)
    
    def tmpl_admin_dialog_box(self, url, ln, title, message, options):
        """
        Prints a dialog box with given title, message and options

        @param url the url of the page that must process the result of the dialog box
        @param ln language
        @param title the title of the dialog box
        @param message a formatted message to display inside dialog box
        @param options a list of string options to display as button to the user
        """
        
        out = ""
        out += '''
        <div style="text-align:center;">
        <fieldset style="display:inline;margin-left:auto;margin-right:auto;">
        <legend>%(title)s:</legend>
        <p>%(message)s</p>
        <form method="post" action="%(url)s">
        ''' % {'title':title,
               'message':message,
               'url':url}
        
        for option in options:
            out += '''<input type="submit" class="adminbutton" name="chosen_option" value="%(value)s" />&nbsp;''' % {'value':option}

        out += '''</form></fieldset></div>'''
        return indent_text(out)