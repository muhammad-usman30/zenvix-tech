<?php
/**
 * SEO: document titles, meta description, Open Graph / Twitter tags and JSON-LD.
 *
 * Static pages use inc/seo-data.php (generated from the same data as the static site).
 * Posts and archives are built at runtime. Skipped automatically if Yoast or Rank Math is active.
 *
 * @package Zenvix
 */

defined( 'ABSPATH' ) || exit;

/** Is a dedicated SEO plugin handling meta tags? */
function zx_seo_plugin_active() {
	return defined( 'WPSEO_VERSION' ) || defined( 'RANK_MATH_VERSION' ) || defined( 'AIOSEO_VERSION' );
}

/** Generated per-page data. */
function zx_seo_data() {
	static $data = null;
	if ( null === $data ) {
		$data = require ZX_DIR . '/inc/seo-data.php';
		$data = is_array( $data ) ? $data : array();
	}
	return $data;
}

/** Key into zx_seo_data() for the current request, or null. */
function zx_seo_key() {
	if ( is_front_page() ) {
		return 'front';
	}
	if ( is_404() ) {
		return '404';
	}
	if ( is_page() ) {
		$slug = get_post_field( 'post_name', get_queried_object_id() );
		return isset( zx_seo_data()[ $slug ] ) ? $slug : null;
	}
	if ( is_home() || is_archive() || is_search() ) {
		return 'blog';
	}
	return null;
}

/** Replace {{HOME}} placeholders in generated schema. */
function zx_seo_home_placeholders( $value ) {
	$json = wp_json_encode( $value );
	$json = str_replace( '{{HOME}}', untrailingslashit( home_url() ), $json );
	return json_decode( $json, true );
}

/** Current page title/description/image. */
function zx_seo_current() {
	$key  = zx_seo_key();
	$data = $key ? zx_seo_data()[ $key ] : null;
	$site = get_bloginfo( 'name' );
	$out  = array(
		'title' => $data['title'] ?? $site, // never call wp_get_document_title() here: it runs our own title filter
		'desc'  => $data['desc'] ?? get_bloginfo( 'description' ),
		'image' => ZX_URI . '/' . ( $data['og'] ?? 'assets/img/og-image.jpg' ),
		'type'  => 'website',
	);

	if ( is_singular( 'post' ) ) {
		$post          = get_queried_object();
		$out['title']  = get_the_title( $post ) . ' | ' . $site;
		$out['desc']   = has_excerpt( $post ) ? get_the_excerpt( $post ) : wp_trim_words( wp_strip_all_tags( $post->post_content ), 28, '…' );
		$out['type']   = 'article';
		if ( has_post_thumbnail( $post ) ) {
			$out['image'] = get_the_post_thumbnail_url( $post, 'full' );
		}
	} elseif ( is_singular() && ! $data ) {
		$post         = get_queried_object();
		$out['title'] = get_the_title( $post ) . ' | ' . $site;
		$out['desc']  = has_excerpt( $post ) ? get_the_excerpt( $post ) : wp_trim_words( wp_strip_all_tags( $post->post_content ), 28, '…' );
	} elseif ( is_category() || is_tag() ) {
		$term         = get_queried_object();
		$out['title'] = sprintf( '%s Articles | %s Blog', single_term_title( '', false ), $site );
		$out['desc']  = $term->description ? wp_strip_all_tags( $term->description ) : sprintf( 'Guides and insights on %s from the %s team.', strtolower( $term->name ), $site );
	} elseif ( is_search() ) {
		$out['title'] = sprintf( 'Search results for “%s” | %s', get_search_query(), $site );
	} elseif ( is_paged() && $data ) {
		$out['title'] = sprintf( '%s — Page %d', $out['title'], (int) get_query_var( 'paged' ) );
	}
	$out['desc'] = wp_html_excerpt( $out['desc'], 160, '' );
	return $out;
}

add_filter(
	'pre_get_document_title',
	function ( $title ) {
		if ( zx_seo_plugin_active() ) {
			return $title;
		}
		return zx_seo_current()['title'];
	}
);

/** Organization schema built from Zenvix Settings. */
function zx_org_schema() {
	$same_as = array();
	foreach ( array( 'facebook', 'instagram', 'x', 'linkedin' ) as $k ) {
		if ( '#' !== zx_opt( $k ) ) {
			$same_as[] = zx_opt( $k );
		}
	}
	$home = home_url( '/' );
	return array(
		'@context'     => 'https://schema.org',
		'@type'        => 'ProfessionalService',
		'@id'          => $home . '#organization',
		'name'         => get_bloginfo( 'name' ),
		'url'          => $home,
		'logo'         => ZX_URI . '/assets/img/logo.png',
		'image'        => ZX_URI . '/assets/img/og-image.jpg',
		'email'        => zx_opt( 'email' ),
		'telephone'    => zx_opt( 'phone' ),
		'priceRange'   => '$$',
		'description'  => 'Zenvix Technologies is a software development and digital marketing company in Lahore, Pakistan, building custom software, websites, mobile apps, AI solutions and growth campaigns for clients worldwide.',
		'address'      => array(
			'@type'           => 'PostalAddress',
			'addressLocality' => zx_opt( 'address_1' ),
			'addressRegion'   => zx_opt( 'address_2' ),
			'addressCountry'  => 'PK',
		),
		'areaServed'   => array( 'Pakistan', 'United States', 'United Kingdom', 'United Arab Emirates', 'Saudi Arabia', 'Qatar', 'Worldwide' ),
		'openingHours' => 'Mo-Sa 09:00-19:00',
		'sameAs'       => $same_as,
		'contactPoint' => array(
			'@type'             => 'ContactPoint',
			'telephone'         => zx_opt( 'phone' ),
			'email'             => zx_opt( 'email' ),
			'contactType'       => 'sales',
			'availableLanguage' => array( 'English', 'Urdu' ),
		),
	);
}

add_action(
	'wp_head',
	function () {
		if ( zx_seo_plugin_active() ) {
			return;
		}
		$m   = zx_seo_current();
		$url = is_singular() ? get_permalink() : ( is_front_page() ? home_url( '/' ) : home_url( add_query_arg( array() ) ) );
		$e   = function ( $s ) {
			return esc_attr( wp_strip_all_tags( $s ) );
		};
		echo "\n<!-- Zenvix SEO -->\n";
		echo '<meta name="description" content="' . $e( $m['desc'] ) . '">' . "\n";
		echo '<meta property="og:type" content="' . $e( $m['type'] ) . '">' . "\n";
		echo '<meta property="og:site_name" content="' . $e( get_bloginfo( 'name' ) ) . '">' . "\n";
		echo '<meta property="og:title" content="' . $e( $m['title'] ) . '">' . "\n";
		echo '<meta property="og:description" content="' . $e( $m['desc'] ) . '">' . "\n";
		echo '<meta property="og:url" content="' . esc_url( $url ) . '">' . "\n";
		echo '<meta property="og:image" content="' . esc_url( $m['image'] ) . '">' . "\n";
		echo '<meta property="og:locale" content="en_US">' . "\n";
		echo '<meta name="twitter:card" content="summary_large_image">' . "\n";
		echo '<meta name="twitter:title" content="' . $e( $m['title'] ) . '">' . "\n";
		echo '<meta name="twitter:description" content="' . $e( $m['desc'] ) . '">' . "\n";
		echo '<meta name="twitter:image" content="' . esc_url( $m['image'] ) . '">' . "\n";
		echo '<meta name="geo.region" content="PK-PB">' . "\n" . '<meta name="geo.placename" content="Lahore">' . "\n";
		if ( is_singular( 'post' ) ) {
			echo '<meta property="article:published_time" content="' . esc_attr( get_the_date( 'c' ) ) . '">' . "\n";
			echo '<meta property="article:modified_time" content="' . esc_attr( get_the_modified_date( 'c' ) ) . '">' . "\n";
		}

		$schemas = array( zx_org_schema() );
		$key     = zx_seo_key();
		if ( $key && ! empty( zx_seo_data()[ $key ]['schema'] ) ) {
			foreach ( zx_seo_data()[ $key ]['schema'] as $s ) {
				$schemas[] = zx_seo_home_placeholders( $s );
			}
		}
		if ( is_singular( 'post' ) ) {
			$post      = get_queried_object();
			$cats      = get_the_category( $post->ID );
			$schemas[] = array(
				'@context'         => 'https://schema.org',
				'@type'            => 'BlogPosting',
				'headline'         => get_the_title( $post ),
				'description'      => $m['desc'],
				'image'            => $m['image'],
				'datePublished'    => get_the_date( 'c', $post ),
				'dateModified'     => get_the_modified_date( 'c', $post ),
				'author'           => array( '@type' => 'Organization', 'name' => get_bloginfo( 'name' ), 'url' => home_url( '/' ) ),
				'publisher'        => array( '@id' => home_url( '/' ) . '#organization' ),
				'mainEntityOfPage' => get_permalink( $post ),
				'articleSection'   => $cats ? $cats[0]->name : '',
				'wordCount'        => str_word_count( wp_strip_all_tags( $post->post_content ) ),
			);
			$schemas[] = array(
				'@context'        => 'https://schema.org',
				'@type'           => 'BreadcrumbList',
				'itemListElement' => array(
					array( '@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => home_url( '/' ) ),
					array( '@type' => 'ListItem', 'position' => 2, 'name' => 'Blog', 'item' => zx_url( 'blog' ) ),
					array( '@type' => 'ListItem', 'position' => 3, 'name' => get_the_title( $post ), 'item' => get_permalink( $post ) ),
				),
			);
		}
		foreach ( $schemas as $s ) {
			echo '<script type="application/ld+json">' . wp_json_encode( $s, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . "</script>\n";
		}
		echo "<!-- /Zenvix SEO -->\n";
	},
	2
);

/** Favicons (unless a Site Icon is set in Settings → General / Customizer). */
add_action(
	'wp_head',
	function () {
		if ( has_site_icon() ) {
			return;
		}
		echo '<link rel="icon" href="' . esc_url( ZX_URI . '/favicon.ico' ) . '" sizes="48x48">' . "\n";
		echo '<link rel="icon" type="image/png" sizes="32x32" href="' . esc_url( ZX_URI . '/assets/img/favicon-32.png' ) . '">' . "\n";
		echo '<link rel="apple-touch-icon" href="' . esc_url( ZX_URI . '/assets/img/favicon-180.png' ) . '">' . "\n";
	},
	3
);

/** Preload the hero image on the front page. */
add_action(
	'wp_head',
	function () {
		if ( is_front_page() ) {
			echo '<link rel="preload" as="image" href="' . esc_url( ZX_URI . '/assets/img/hero-bg.webp' ) . '" imagesrcset="' . esc_url( ZX_URI . '/assets/img/hero-bg-900.webp' ) . ' 900w, ' . esc_url( ZX_URI . '/assets/img/hero-bg.webp' ) . ' 1400w" imagesizes="100vw" fetchpriority="high">' . "\n";
		}
	},
	1
);

/** No-index search results and 404s. */
add_filter(
	'wp_robots',
	function ( $robots ) {
		if ( is_search() || is_404() ) {
			$robots['noindex'] = true;
			$robots['follow']  = true;
		}
		return $robots;
	}
);

/** Body classes used by the stylesheet. */
add_filter(
	'body_class',
	function ( $classes ) {
		$key = zx_seo_key();
		if ( $key && ! empty( zx_seo_data()[ $key ]['body'] ) ) {
			$classes[] = zx_seo_data()[ $key ]['body'];
		}
		if ( is_singular( 'post' ) ) {
			$classes[] = 'page-post';
		}
		return $classes;
	}
);
