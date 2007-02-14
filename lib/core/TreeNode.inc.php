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
//  File: TreeNode.inc (flexElink core)
//  Classes:    Condition
//              Atribs
//		Node
//  Requires:
//  Included:   
//==========================================================================

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  Class: Condition
//  Purpose:
//  Attributes:
//  Methods:
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

  class Condition {
    var $atname;
    var $atvalue;

    function Condition( $atname, $atvalue="" )
    {
      $this->atname=$atname;
      $this->atvalue=trim($atvalue);
    }

    function pass( $atname, $atvalue="" )
    {
      $atvalue=trim($atvalue);
      //$atname=strtoupper( trim( $atname ) );
      $atname=trim( $atname );
      return (($atname==$this->atname) && ($atvalue==$this->atvalue));
    }
    
  }

  
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  Class: Atribs
//  Purpose:
//  Attributes:
//  Methods:
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

  class Atribs {
    var $name="";
    var $vars;

    function Atribs($name, $var="")
    {
      $this->name=$name;
      $this->vars=array();
      if($var!="")
        $this->addVar($var);
    }

    function addVar($varname)
    {
      if(!in_array(trim($varname), array_values($this->vars)))
        array_push($this->vars, trim($varname));
    }
  }


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  Class: Node
//  Purpose:
//  Attributes:
//  Methods:
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

  class Node {
    var $tag; //string contining the tag name
    var $vars; //array which contains variable to set up with 
		   //  the text of the tag
    var $sons; //array which will keep all the references to son nodes 
    var $parent; //reference to the parent node
    var $atribs;  //array contianing references to atribute objects
    var $conditions; //array containing conditions needed for entering
			// this node
    
    function &Node($tagname, & $parent)
    {
      $this->tag=trim($tagname);
      $this->parent= & $parent;
      $this->sons=array();
      $this->atribs=array();
      $this->vars=array();
      $this->conditions=array();

      return $this;
    }

    function addAtrib( $name, $intvar)
    {
      //$atribname=strtoupper(trim($name));
      $atribname=trim($name);
      $intvar=strtoupper(trim($intvar));
      if(!in_array($atribname, array_keys($this->atribs)))
        $this->atribs[ $atribname ]=new Atribs( $atribname );
      $this->atribs[ $atribname ]->addVar( $intvar );
    }

    function addCondition( $atname, $atvalue="" )
    {
      //$atname=strtoupper(trim($atname));
      $atname=trim($atname);
      //As XML only allows an attribute to appear once in each TAG, 
      //  the condition list with more than one attrib that has the same 
      //  name, won't make sense, so the criteria for looking if a
      //  condition is already inserted is looking for the attrib name.
      //In case various attrib values are specified for one attribute name,
      //  the first one will remain
      if(!in_array($atname, array_keys($this->conditions)))
	$this->conditions[ $atname ]=new Condition( $atname, $atvalue );
    }

    function & son( $name, $conditions=null )
    {
      $idx=0;
      while($idx<=(count($this->sons)-1))
      {
        $temp=& $this->sons[$idx];
	if($temp->matchId( $name, $conditions ))
	{
	  return $temp;
        }
	$idx++;
      }
      return null;
    }

    function & atrib($name)
    {
      //return ($this->atribs[strtoupper(trim($name))]);
      return ($this->atribs[trim($name)]);
    }

    function matchId ( $tagname, $conditions=null )
    {
      //$tagname=trim(strtoupper($tagname));
      $tagname=trim($tagname);
      //First let's see if tag names match
      if ( $tagname!=$this->tag ) return 0;
      if ( $conditions==null )
	$conditions=array();
      $acond=array();
      foreach($conditions as $key=>$value)
      {
	//$acond[strtoupper($key)]=$value;
	$acond[$key]=$value;
      }
      //Then let's check if it has same conditions
      if($this->tag==$tagname)
      {
        //Then we have to see if the node has exactly the same conditions
	foreach($acond as $key=>$value)
	{
	  if (!($this->hasCondition($key, $value))) return 0;
	}
	 
	//Now we need to check if the node condition is in the parameter
	foreach($this->conditions as $cond)
	{ 
	  if (!(in_array($cond->atname, array_keys($acond))))
	    return 0;
          if (!($cond->pass($cond->atname, $acond[$cond->atname])))
	    return 0;
	}
      }
      return 1;
    }

    function addSon( $tagname, $conditions=null )
    {
      //$tag=strtoupper(trim($tagname));
      $tag=trim($tagname);
      if($conditions==null)
	$conditions=array();
      if(!$this->hasSon( $tagname, $conditions ))
      {
        $temp = & new Node( $tag, $this );
	  foreach($conditions as $key=>$value)
	    $temp->addCondition($key, $value);
        array_push($this->sons, & $temp);
      }
    }

    function addVariable( $varname )
    {
      if(!in_array( trim($varname), $this->vars))
        array_push($this->vars, trim($varname));
    }

    function hasSon( $tagname, $conditions=null )
    {
      //There could be more than one son with the same tagname
      foreach($this->sons as $temp)
      {
        if($temp->matchId( $tagname, $conditions))
          return 1;
      }
      return 0;
    }
    
    function hasVariables()
    {
      return (count($this->vars)>0);
    }

    function hasAtribs()
    {
      return (count($this->atribs));
    }

    function hasAtrib( $atname )
    {
      //$atname=strtoupper(trim($atname));
      $atname=trim($atname);
      return in_array($atname, array_keys($this->atribs));
    }

    function hasCondition( $atname, $atvalue="" )
    {
	//$atname=strtoupper(trim($atname));
	$atname=trim($atname);
	if(in_array($atname, array_keys($this->conditions)))
	  if(!$atvalue)
	    return 1;
          else
	    return ($this->conditions[$atname]->pass($atname, $atvalue));
        return 0;
    }

    function & descend( $tag, $cond )
    {
      foreach($this->sons as $key=>$temp)
      {
        //if(strtoupper(trim($tag))==$temp->tag)
        if(trim($tag)==$temp->tag)
	{
	  if($temp->passConditions( $cond ))
	  {
	    return $temp;
          }
        }
      }
      return null;
    }

    function passConditions( $a ) 
    { //This method tells if the node pass the conditions according with the
      //  assoc array which is passed as parameter. This array will contain
      //  the atribute names as indexes, and the atribute values as values.
      //To pass the conditions means that all the conditions in the node have
      //  be present in the array parameter

      //If there is no condition in the node, is passed
      if (!$this->conditions)
	return 1;
      //If there is any condition in the node but not in the parameter is
      // not passed
      if (($this->conditions) && (!$a))
	return 0;
      //Any other case, we'll have to compare individually
      foreach($this->conditions as $atname=>$atvalue)
      {
	if (!in_array($atname, array_keys( $a )))
	{
	  return 0;
        }
        if (!$atvalue->pass( $atname, $a[ $atname ]))
	{
	  return 0;
        }
      }
      return 1;
    }

    function output()
    {
      print "Actual node: ".$this->tag."(".$this->parent->tag.")<br>";
      print "Sons: ".array2str(array_keys($this->sons))."<br>";
      print "Variables: ".array2str(array_values($this->vars))."<br>";
      print "Atribs: ".array2str(array_keys($this->atribs))."<br>";
      print "Conditions: ".array2str(array_keys($this->conditions))."<br>";
      reset($this->sons);
      while(current($this->sons)){
	$temp=current($this->sons);
	$temp->output();
	next($this->sons);
      }
    }

  }


//----------------------------------------------------------------------

?>  
