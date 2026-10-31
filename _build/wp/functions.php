<?php
/**
 * Zenvix Technologies theme bootstrap.
 *
 * @package Zenvix
 */

defined( 'ABSPATH' ) || exit;

define( 'ZX_VERSION', '1.0.0' );
define( 'ZX_DIR', get_template_directory() );
define( 'ZX_URI', get_template_directory_uri() );

require ZX_DIR . '/inc/helpers.php';
require ZX_DIR . '/inc/settings.php';
require ZX_DIR . '/inc/seo.php';
require ZX_DIR . '/inc/blog.php';
require ZX_DIR . '/inc/contact-form.php';
require ZX_DIR . '/inc/setup.php';

add_action(
	'after_setup_theme',
	function () {
		add_theme_support( 'title-tag' );
		add_theme_support( 'post-thumbnails' );
		add_theme_support( 'responsive-embeds' );
		add_theme_support( 'html5', array( 'search-form', 'gallery', 'caption', 'style', 'script' ) );
		add_image_size( 'zx-card', 800, 533, true );
	}
);

/**
 * Styles & scripts. Versions follow file modification time so edits bust caches.
 */
add_action(
	'wp_enqueue_scripts',
	function () {
		$ver = function ( $rel ) {
			$file = ZX_DIR . $rel;
			return file_exists( $file ) ? (string) filemtime( $file ) : ZX_VERSION;
		};
		wp_enqueue_style( 'zx-fonts', 'https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap', array(), null );
		wp_enqueue_style( 'zx-main', ZX_URI . '/assets/css/style.css', array(), $ver( '/assets/css/style.css' ) );
		wp_enqueue_script( 'zx-main', ZX_URI . '/assets/js/main.js', array(), $ver( '/assets/js/main.js' ), array( 'strategy' => 'defer', 'in_footer' => true ) );
		wp_enqueue_script( 'zx-wp', ZX_URI . '/assets/js/wp.js', array(), $ver( '/assets/js/wp.js' ), array( 'strategy' => 'defer', 'in_footer' => true ) );

		// The theme doesn't use block styles on the front end.
		if ( ! is_singular( 'post' ) ) {
			wp_dequeue_style( 'wp-block-library' );
			wp_dequeue_style( 'wp-block-library-theme' );
		}
		wp_dequeue_style( 'global-styles' );
		wp_dequeue_style( 'classic-theme-styles' );
	},
	20
);

add_filter(
	'wp_resource_hints',
	function ( $urls, $relation ) {
		if ( 'preconnect' === $relation ) {
			$urls[] = 'https://fonts.googleapis.com';
			$urls[] = array( 'href' => 'https://fonts.gstatic.com', 'crossorigin' );
		}
		return $urls;
	},
	10,
	2
);

// Leaner <head>.
remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
remove_action( 'wp_print_styles', 'print_emoji_styles' );
remove_action( 'wp_head', 'wp_generator' );
remove_action( 'wp_head', 'wlwmanifest_link' );
remove_action( 'wp_head', 'rsd_link' );
remove_action( 'wp_head', 'wp_shortlink_wp_head' );
