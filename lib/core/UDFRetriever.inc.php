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
//  File: UDFRetriever.inc (flexElink core)
//  Classes:    UDFRetriever
//  Requires: 
//  Included: DB   
//==========================================================================

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  Class: UDFRetriever
//  Purpose: Retrieves UDFs from the database providing services for validating
//	and getting the reults of an existing one. All the UDF database access
//	is encapsulated here; besides, it implements an internal cache which is
//	trasparent to clients and that minimizes DB accesses. It follows the 
//	Singleton pattern so it will only be one instance of this class.
//  Attributes:
//	cache --> Array that implements an internal cache for keeping UDFs 
//		retrieved from the DB (minimizes DB acceses)
//	db -----> Persistent MySQL connection
//  Visible methods:
//	getInstance (static)--> returns an instance of the class ensurring 
//		that is unique
//	validate -----> cheks that the UDF with the given name exists and has 
//		the number of parameters indicated. 
//	execute ------> evaluates the UDF with the parameter values given and
//		returns the result if the execution was succesful
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

  class UDFRetriever {
    var $cache;
    var $db;
    
    function UDFRetriever()
    {
      $this->cache=array();

      include( DB );

      $this->db=mysql_pconnect( $DB_HOST, $DB_USER, $DB_PASSWD );
      mysql_selectdb( $DB_DB, $this->db );
    }

    function destroy()
    {
      //mysql_close( $this->db );
    }

/*---------------------------------------------------------------------
  Method: getInstance (static)
  Description: Gives a reference to an UDFRetriever ensurring that is the only
  	one that exists. For doing so, the Singleton pattern is followed. Call
	always to this method instead of using the constructor
  Parameters:
  Return value: (UDFRetriever) Reference to the unique UDFRetriever object
---------------------------------------------------------------------*/
    function & getInstance()
    {
      static $instance;

      if(!isset($instance))
      {
	$instance=new UDFRetriever();
      }
      return $instance;
    }

/*---------------------------------------------------------------------
  Method: validate
  Description: Checks if a UDF is defined in the FlexElink configuration and
  	if the number of parameters is correct for it
  Parameters:
  	udf_name (String) ---------> identifier of the UDF
	udf_param_count (Integer) -> number of parameters of the UDF
  Return value: (Array) Contains two values:
  	1) The first one is <=0 if the validation wasn't OK, and any other
	value in case of succesful validation
	2) The second one contains a text explaining why the validation wasn't
	possible. (It's not meaningful when the validation is OK)
---------------------------------------------------------------------*/
    function validate( $udf_name, $udf_param_count)
    {
      if(!$this->db)
	return array(0, "Couldn't connect to database");
      $udf_name=strtoupper(trim($udf_name));
      //Check if the function is in cache
      if(in_array($udf_name, array_keys($this->cache)))
      {
	if($udf_param_count==count($this->cache[$udf_name][0]))
	{
	  return array(1, $this->cache[$udf_name]);
	}
	return array(0, "Function '$udf_name' error: wrong number of parameters");
      }
      else
      {
	//If the function is not cached we have to look for it on the DB
	$qry="select code from flxUDFS where fname='".addslashes($udf_name)."'";
	$qh=mysql_query( $qry, $this->db );
	if(mysql_num_rows($qh)>0)
	{
	  $row=mysql_fetch_array($qh);
	  $code=$row["code"];
	  $qry="select pname from flxUDFPARAMS 
		where fname='".addslashes($udf_name)."' 
		order by ord";
          $qh=mysql_query($qry, $this->db);
	  $params=array();
	  while($row=mysql_fetch_array($qh))
	  {
	    array_push($params, $row["pname"]);
	  }
	  if(count($params)==$udf_param_count)
	  {
	    //Add to cache
	    $this->cache[$udf_name]=array($params, $code);
	    return array(1, $this->cache[$udf_name]);
          }
	  return array(0, "Function '$udf_name' error: wrong number of parameters");
	}
      }
      return array(0, "Function '$udf_name' not found");
    }


/*---------------------------------------------------------------------
  Method: execute
  Description: Gives the result of evaluating the UDF with the parameter values 
  	indicated.
  Parameters:
  	name (String) --> UDF identifier
	param_values (Array) --> Contains the parameter values with which the
		UDF has to be executed. The order is important because the 
		values will be assigned to parameters in the order they come
		in the array to the order they where defined in the UDF.
       last (Bool) -----------> Value of the a special variable to be used 
       		inside the UDF code (LAST_ITERATION)
       first (Bool) ----------> Value of the a special variable to be used 
       		inside the UDF code (FIRST_ITERATION)
  Return value: (Array) Contains two values:
  	1) The first one is <=0 if it occured any problem during execution, any
	other value in case of success
	2) The second one contains a text explaining why the execution wasn't
	possible. (It's not meaningful when it is OK)
---------------------------------------------------------------------*/
    function execute( $name, $param_values, $last, $first )
    {
      list($ok, $udf)=$this->validate( $name, count($param_values) );
      if(!$ok)
        return array(0, $udf);
      $excode="\$LAST_ITERATION=$last;";
      $excode.="\$FIRST_ITERATION=$first;";
      list($param_names, $code)=$udf;
      $counter=0;
      foreach($param_names as $pname)
      {
        //$val=addslashes($param_values[$counter]);
        $val=str_replace("\\", "\\\\", $param_values[$counter]);
        $val=str_replace("\"", "\\\"", $val);
	$val=str_replace("\$", "\\\$", $val);
        $excode.='$'."$pname=\"".$val."\";\n";
        $counter++;
      }
      $excode.=$code;
      $res=eval($excode);
      return array(1, $res);
    }


  
  }//end class: 

?>
