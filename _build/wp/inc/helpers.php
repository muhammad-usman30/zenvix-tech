<?php
/**
 * Template helpers: settings values, URLs, nav state, icons.
 *
 * @package Zenvix
 */

defined( 'ABSPATH' ) || exit;

/**
 * Default contact details (used until changed in Appearance → Zenvix Settings).
 */
function zx_defaults() {
	return array(
		'email'     => 'zenvixtechnologies7@gmail.com',
		'phone'     => '+92 326 4549778',
		'whatsapp'  => '923264549778',
		'address_1' => 'Gulberg, Lahore',
		'address_2' => 'Punjab, Pakistan',
		'map_url'   => 'https://share.google/JHnFjofZhqNVF7J7r',
		'map_query' => 'Gulberg, Lahore, Punjab, Pakistan',
		'hours'     => 'Mon–Sat, 9am–7pm PKT',
		'facebook'  => '',
		'instagram' => '',
		'x'         => '',
		'linkedin'  => '',
	);
}

/**
 * Get a setting (or a value derived from one).
 *
 * @param string $key Setting key.
 * @return string
 */
function zx_opt( $key ) {
	$saved    = get_option( 'zx_settings', array() );
	$defaults = zx_defaults();
	$get      = function ( $k ) use ( $saved, $defaults ) {
		if ( isset( $saved[ $k ] ) && '' !== trim( (string) $saved[ $k ] ) ) {
			return trim( (string) $saved[ $k ] );
		}
		return $defaults[ $k ] ?? '';
	};

	switch ( $key ) {
		case 'phone_href':
			return '+' . preg_replace( '/\D+/', '', $get( 'phone' ) );
		case 'whatsapp_url':
			return 'https://wa.me/' . preg_replace( '/\D+/', '', $get( 'whatsapp' ) );
		case 'map_embed':
			return 'https://www.google.com/maps?q=' . rawurlencode( $get( 'map_query' ) ) . '&output=embed';
		case 'facebook':
		case 'instagram':
		case 'x':
		case 'linkedin':
			$v = isset( $saved[ $key ] ) ? trim( (string) $saved[ $key ] ) : '';
			return '' === $v ? '#' : $v;
	}
	return $get( $key );
}

/** Echo a setting, HTML-escaped. */
function zx_e( $key ) {
	echo esc_html( zx_opt( $key ) );
}

/** Echo a URL setting, URL-escaped. */
function zx_eu( $key ) {
	echo esc_url( zx_opt( $key ) );
}

/**
 * URL for a site page or post.
 *
 * ''            → home
 * 'blog'        → posts page
 * 'post:slug'   → blog post by slug
 * 'path/slug'   → page by path (e.g. 'services/web-development')
 *
 * @param string $key Page key.
 * @return string
 */
function zx_url( $key ) {
	static $cache = array();
	if ( isset( $cache[ $key ] ) ) {
		return $cache[ $key ];
	}
	if ( '' === $key ) {
		$url = home_url( '/' );
	} elseif ( 'blog' === $key && get_option( 'page_for_posts' ) ) {
		$url = get_permalink( (int) get_option( 'page_for_posts' ) );
	} elseif ( 0 === strpos( $key, 'post:' ) ) {
		$slug = substr( $key, 5 );
		$post = get_page_by_path( $slug, OBJECT, 'post' );
		$url  = $post ? get_permalink( $post ) : home_url( '/' . $slug . '/' );
	} else {
		$page = get_page_by_path( $key );
		$url  = $page ? get_permalink( $page ) : home_url( '/' . trim( $key, '/' ) . '/' );
	}
	$cache[ $key ] = $url;
	return $url;
}

/**
 * Echo the active-state attributes for a header nav item.
 *
 * @param string $key home|about|services|blog|contact.
 */
function zx_nav_class( $key ) {
	$active = false;
	switch ( $key ) {
		case 'home':
			$active = is_front_page();
			break;
		case 'about':
		case 'contact':
			$active = is_page( $key );
			break;
		case 'services':
			$services = get_page_by_path( 'services' );
			$active   = is_page( 'services' ) || ( $services && is_page() && (int) wp_get_post_parent_id( get_queried_object_id() ) === (int) $services->ID );
			break;
		case 'blog':
			$active = is_home() || is_singular( 'post' ) || is_category() || is_tag() || is_search() || is_author() || is_date();
			break;
	}
	if ( $active ) {
		echo ' class="is-active" aria-current="page"';
	}
}

/**
 * Inline SVG icon from the sprite printed in header.php.
 *
 * @param string $name Icon name.
 * @param string $cls  CSS class.
 * @return string
 */
function zx_icon( $name, $cls = 'ic' ) {
	return '<svg class="' . esc_attr( $cls ) . '" aria-hidden="true"><use href="#i-' . esc_attr( $name ) . '"/></svg>';
}

/**
 * Inner-page hero (same markup as the static site).
 *
 * @param array $args eyebrow, title (HTML), text, crumbs [[label, url|null]], bg (theme-relative image path).
 */
function zx_page_hero( $args ) {
	$args = wp_parse_args( $args, array( 'eyebrow' => '', 'title' => '', 'text' => '', 'crumbs' => array(), 'bg' => '' ) );
	?>
	<section class="page-hero">
		<?php if ( $args['bg'] ) : ?>
			<div class="ph-bg"><img src="<?php echo esc_url( ZX_URI . '/' . $args['bg'] ); ?>" alt="" width="1600" height="900" fetchpriority="high" decoding="async"></div>
		<?php endif; ?>
		<div class="ph-grid" aria-hidden="true"></div>
		<div class="container ph-inner">
			<nav aria-label="Breadcrumb"><ol class="crumbs">
				<?php foreach ( $args['crumbs'] as $c ) : ?>
					<?php if ( ! empty( $c[1] ) ) : ?>
						<li><a href="<?php echo esc_url( $c[1] ); ?>"><?php echo esc_html( $c[0] ); ?></a></li>
					<?php else : ?>
						<li aria-current="page"><?php echo esc_html( $c[0] ); ?></li>
					<?php endif; ?>
				<?php endforeach; ?>
			</ol></nav>
			<?php if ( $args['eyebrow'] ) : ?>
				<span class="eyebrow light anim-up"><?php echo zx_icon( 'sparkle', 'ic ic-xs' ); // phpcs:ignore ?> <?php echo esc_html( $args['eyebrow'] ); ?></span>
			<?php endif; ?>
			<h1 class="anim-up" style="--d:.08s"><?php echo wp_kses_post( $args['title'] ); ?></h1>
			<?php if ( $args['text'] ) : ?>
				<p class="anim-up" style="--d:.16s"><?php echo wp_kses_post( $args['text'] ); ?></p>
			<?php endif; ?>
		</div>
	</section>
	<?php
}
