<?
## $Id$

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

//==========================================================================
//  File: FormatRetriever.inc (flexElink core)
//  Classes:    FormatRetriever
//              
//  Requires: 
//  Included: DB
//==========================================================================


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  Class: FormatRetriever
//  Purpose:
//  Attributes:
//  Visible Methods:
//	getInstance ----->
//	getFormatCode --->	
//	getParsedFormat ->
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class FormatRetriever {

  var $cache; //Contains parsed formats, indexed by their format name

  function FormatRetriever()
  {
    $this->cache=array();
  }

/*---------------------------------------------------------------------
  Method: getInstance (static)
  Description: Gives a reference to an FormatRetriever ensurring that is the 
  	only one that exists. For doing so, the Singleton pattern is followed. 
	Call always to this method instead of using the constructor
  Parameters:
  Return value: (FormatRetriever) Reference to the unique FormatRetriever 
		object
---------------------------------------------------------------------*/
  function & getInstance()
  {
    static $instance;

    if(!isset($instance))
    {
      $instance=new FormatRetriever();     
    }

    return $instance;
  }
  
/*---------------------------------------------------------------------
  Method: getFormatCode
  Description: 
  Parameters:
  Return value:
---------------------------------------------------------------------*/
  function getFormatCode( $fname )
  {
    $fname=strtoupper(trim($fname));

    include(DB);

    $db=mysql_connect( $DB_HOST, $DB_USER, $DB_PASSWD );
    mysql_selectdb( $DB_DB, $db );
    $qry="select value from flxFORMATS where name='".addslashes($fname)."'";
    $qh=mysql_query( $qry, $db );
    if(mysql_num_rows($qh)<1)
    {
      return array(0, "Format '$fname' not found");
    }
    $res=mysql_fetch_array( $qh );
    mysql_close($db);
    return array(1, $res["value"]);
  }
  
/*---------------------------------------------------------------------
  Method: getSerializedFormat
  Description: 
  Parameters:
  Return value:
---------------------------------------------------------------------*/
  function getSerializedFormat ( $fname )
  {
    $fname=strtoupper(trim($fname));
    if(isset($this->cache[$fname]))
    {
      return array(1, $this->cache[$fname]);
    }
    else
    {
      include(DB);

      $db=mysql_pconnect( $DB_HOST, $DB_USER, $DB_PASSWD );
      mysql_selectdb( $DB_DB, $db );
      $qry="select serialized from flxFORMATS where name='".addslashes($fname)."'";
      $qh=mysql_query( $qry, $db );
      if(mysql_num_rows($qh)<1)
      {
        return array(0, "Format '$fname' not found");
      }
      $res=mysql_fetch_array( $qh );
      $this->cache[$fname]=$res["serialized"];
      return array(1, $res["serialized"]);
    }
  }

/*---------------------------------------------------------------------
  Method: getParsedFormat
  Description: 
  Parameters:
  Return value:
---------------------------------------------------------------------*/
  function getParsedFormat( $fname )
  {
    $fname=strtoupper(trim($fname));
    if($fname=="")
    {
      return array(0, "Empty format name");
    }
    //First, check if we have the "compiled" format in local cache
      //If the format is not in chache, we should go for it to the 
      //  database, parse it, add compiled result (if succesful) to cache
      //  and return it
      list($ok, $fcode)=$this->getSerializedFormat( $fname );
      if($ok)
      {
	$tree=unserialize($fcode);
        if($tree==null)
        {
          return array(0, "Bad format");
        }
	return array(1, $tree);
      }
  }

  function applyFormat( $fname, $intvars )
  {
  }
}

?>
