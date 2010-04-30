<?php
/**
 * @package WordPress
 * @subpackage Default_Theme
 */
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" <?php language_attributes(); ?>>

<head profile="http://gmpg.org/xfn/11">
<meta http-equiv="Content-Type" content="<?php bloginfo('html_type'); ?>; charset=<?php bloginfo('charset'); ?>" />

<title><?php wp_title('&laquo;', true, 'right'); ?> <?php bloginfo('name'); ?></title>

<link rel="stylesheet" href="/media/screen.css" type="text/css" media="screen,projection" />
<link rel="stylesheet" href="/media/print.css" type="text/css" media="print" />
<link rel="stylesheet" href="/media/main.css" type="text/css" media="screen" />


<link rel="pingback" href="<?php bloginfo('pingback_url'); ?>" />

<?php if ( is_singular() ) wp_enqueue_script( 'comment-reply' ); ?>

<?php wp_head(); ?>
</head>
<body <?php body_class(); ?> id="section-tasks">

<div style="background:white"> 
        <div id="header" class="container"> 
            <div id="logo"> 
                <h1><a href="/"><img src='/media/images/logo.png' alt="Democracy Club"/></a></h1> 
            </div> 
            <ul id="links"> 
              
                <li><a href="/aboutus/">About us</a></li> 
              
                <li><a href="/projects/">What we&#39;re doing</a></li> 
              
                <li><a href="/contact/">Contact</a></li> 
              
                <li><a href="/faq/">FAQ</a></li> 

            </ul> 
            <span style="float:right;clear:right;"> 
                
            </span> 
        </div> 
      </div> 

<div style="background:#3a7bd3"> 
          <div id="navigation" class="container"> 
            
            <ul> 
              
                <li><a href="/welcome">Home</a></li> 
              
                <li><a href="/constituencies/">Constituency list</a></li> 
              
                <li><a href="/blog/">Blog</a></li> 
              
            </ul> 
            
          </div> 
      </div> 



      <div id="main" class="container"> 
        <div class="span-8"> 
	 <p class="notice"> 
	 <strong>NEW!</strong> Our candidate survey is online.  <a href="http://election.theyworkforyou.com/quiz">Find out what your candidates think about local and national issues</a>.
	</p> 
	</div> 
        <div class="clear"></div> 
              
         <div class="span-6"> 
         <div class="gradient-box"> 
