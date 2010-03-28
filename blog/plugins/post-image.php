<?php
/*
Plugin Name: Post Image
Plugin URI: http://guff.szub.net/post-image
Description: Display an image 'attached' to each post. Use post_image() or szub_post_image() in The Loop.
Version: R1.1.1
Author: Kaf Oseo, modified by Suprb (www.suprb.com)
Author URI: http://szub.net/

    Copyright (c) 2006, 2007 Kaf Oseo (http://szub.net)
    Post Image is released under the GNU General Public License (GPL)
    http://www.gnu.org/licenses/gpl.txt

    This is a WordPress 2 plugin (http://wordpress.org).

~Changelog:
R1.1.1 (Jan-04-2007)
Missed this bug fix: Avoid displaying "broken" img tag when no image
exists.

R1.1 (Jan-04-2007)
You can specify an image attachment to use by inserting 'post-image'
(or whatever is set for the 'customkey' parameter) somewhere in the
(upload) title field. Hit a few buggy bits such as with 'thumbnail'
filenames for language localization, and implemented pseudo-caching
on multi-post queries.

R1 (Mar-17-2006)
Along with bug swattings from 0.1 (beta), the following changes and
features provided with this full release: new query_string argument
wrapper function (szub_post_image()); override an attachment and/or
$default_image for individual posts through a custom field (default
key: post-image); if $img_tag is set to true/1 and display false/0,
now returns complete <img> element (previously it returned only the
image's url). Tentative support for WordPress 2.1.
*/

function szub_post_image($args='') {
    parse_str($args);
    if( !isset($default_image) ) $default_image = '';
    if( !isset($use_thumb) ) $use_thumb = false;
    if( !isset($img_tag) ) $img_tag = true;
    if( !isset($css_class) ) $css_class = 'post-image';
    if( !isset($customkey) ) $customkey = 'post-image';
    if( !isset($display) ) $display = true;

    return post_image($default_image, $use_thumb, $img_tag, $css_class, $customkey, $display);
}

function post_image($default_image='', $use_thumb=false, $img_tag=true, $css_class='post-image', $customkey='post-image', $display=true) {
    global $post, $posts, $wp_version, $wpdb;
    global $post_image_attachments;

    if( empty($post) )
        return;

    if( !empty($posts) ) {
        foreach($posts as $apost) {
            if( $posts[0] != $apost )
                $IN_ids .= ',';
            $IN_ids .= (int) $apost->ID;
        }
    }

    if( !empty($default_image) ) {
        $img_url = $default_image;
        $img_title = apply_filters('the_title', $post->post_title);
    }

    $post_custom = get_post_custom($post->ID);
    $meta_value = $post_custom["$customkey"][0];

    if( $meta_value ) {
        $img_url = $meta_value;
        $img_title = apply_filters('the_title', $post->post_title);
    } else {
        if( empty($post_image_attachments) ) {
            $record = ( $wp_version < 2.1 ) ? 'post_status' : 'post_type';
            $post_image_attachments = @$wpdb->get_results("SELECT ID, post_parent, post_title, post_content, guid FROM $wpdb->posts WHERE post_parent IN($IN_ids) AND $record = 'attachment' AND post_mime_type LIKE '%image%' ORDER BY post_date ASC");
        }

        foreach( $post_image_attachments as $attachment ) {
            if( $post->ID == $attachment->post_parent ) {
                    if( !$first_attachment ) {
                        $img_url = $attachment->guid;
                        $img_title = apply_filters('the_title', $attachment->post_title);
                        $first_attachment = 1;
                    }

                $postmarked = strpos(strtolower($attachment->post_title), strtolower($customkey));
                $fileimage = explode('.', basename($attachment->guid));

                if( $postmarked == true || $post->ID == $fileimage[0] || $post->post_name == $fileimage[0] ) {
                    $img_url = $attachment->guid;
                    $img_title = apply_filters('the_title', $attachment->post_title);

                    if($postmarked == true) {
                        $img_title = trim(str_replace($customkey, '', $img_title));
                        break;
                    }
                }
            }
        }

        if( $use_thumb && ($img_url != $default_image) )
            $img_url = preg_replace('!(\.[^.]+)?$!', __('.thumbnail') . '$1', $img_url, 1);
    }

    $img_path = ABSPATH . str_replace(get_settings('siteurl'), '', $img_url);

    if( !file_exists($img_path) ) {
        return;
    } else {
        if( $img_tag ) {
  /*          $imagesize = @getimagesize($img_url);
    
			list($width, $height, $type, $attr) = getimagesize($img_url);
			$temp_h = ($height*315)/$width;
	
        	//$image = '<img class="' . $css_class . '" src="' . $img_url . '" width="315" height="' . $temp_h . '" title="' . $img_title . '" alt="' . $img_title . '" />';
    */    	
        	$image = $img_url;
        } else {
            $image = $img_url;
        }
    }

    if( $display )
     
    return $image;
}

function post_height($default_image='', $use_thumb=false, $img_tag=true, $css_class='post-image', $customkey='post-image', $display=true) {
    global $post, $posts, $wp_version, $wpdb;
    global $post_image_attachments;

    if( empty($post) )
        return;

    if( !empty($posts) ) {
        foreach($posts as $apost) {
            if( $posts[0] != $apost )
                $IN_ids .= ',';
            $IN_ids .= (int) $apost->ID;
        }
    }

    if( !empty($default_image) ) {
        $img_url = $default_image;
        $img_title = apply_filters('the_title', $post->post_title);
    }

    $post_custom = get_post_custom($post->ID);
    $meta_value = $post_custom["$customkey"][0];

    if( $meta_value ) {
        $img_url = $meta_value;
        $img_title = apply_filters('the_title', $post->post_title);
    } else {
        if( empty($post_image_attachments) ) {
            $record = ( $wp_version < 2.1 ) ? 'post_status' : 'post_type';
            $post_image_attachments = @$wpdb->get_results("SELECT ID, post_parent, post_title, post_content, guid FROM $wpdb->posts WHERE post_parent IN($IN_ids) AND $record = 'attachment' AND post_mime_type LIKE '%image%' ORDER BY post_date ASC");
        }

        foreach( $post_image_attachments as $attachment ) {
            if( $post->ID == $attachment->post_parent ) {
                    if( !$first_attachment ) {
                        $img_url = $attachment->guid;
                        $img_title = apply_filters('the_title', $attachment->post_title);
                        $first_attachment = 1;
                    }

                $postmarked = strpos(strtolower($attachment->post_title), strtolower($customkey));
                $fileimage = explode('.', basename($attachment->guid));

                if( $postmarked == true || $post->ID == $fileimage[0] || $post->post_name == $fileimage[0] ) {
                    $img_url = $attachment->guid;
                    $img_title = apply_filters('the_title', $attachment->post_title);

                    if($postmarked == true) {
                        $img_title = trim(str_replace($customkey, '', $img_title));
                        break;
                    }
                }
            }
        }

        if( $use_thumb && ($img_url != $default_image) )
            $img_url = preg_replace('!(\.[^.]+)?$!', __('.thumbnail') . '$1', $img_url, 1);
    }

    $img_path = ABSPATH . str_replace(get_settings('siteurl'), '', $img_url);

    if( !file_exists($img_path) ) {
        return;
    } else {
        if( $img_tag ) {
            $imagesize = @getimagesize($img_url);
    
			list($width, $height, $type, $attr) = getimagesize($img_url);
			$temp_h = ($height*315)/$width;
	
        	$height_y = $temp_h;
        } else {
            $height_y= $img_url;
        }
    }

    return $height_y;
}

?>