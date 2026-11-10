<?php
/**
 * Blog helpers: cards, reading time, table of contents, content filters.
 *
 * @package Zenvix
 */

defined( 'ABSPATH' ) || exit;

/** Primary category of a post. */
function zx_post_cat( $post = null ) {
	$cats = get_the_category( $post ? $post->ID : get_the_ID() );
	return $cats ? $cats[0] : null;
}

/** Estimated reading time in minutes. */
function zx_reading_time( $post = null ) {
	$post  = get_post( $post );
	$words = str_word_count( wp_strip_all_tags( $post->post_content ) );
	return max( 3, (int) round( $words / 220 ) );
}

/** Card image (featured image or brand fallback). */
function zx_card_image( $post ) {
	if ( has_post_thumbnail( $post ) ) {
		return get_the_post_thumbnail(
			$post,
			'large',
			array(
				'alt'      => get_the_title( $post ),
				'loading'  => 'lazy',
				'decoding' => 'async',
			)
		);
	}
	return '<img src="' . esc_url( ZX_URI . '/assets/img/og-image.jpg' ) . '" alt="" width="1200" height="630" loading="lazy" decoding="async">';
}

/**
 * Blog card markup (same as the static site).
 *
 * @param WP_Post $post     Post.
 * @param bool    $featured Large horizontal layout.
 * @return string
 */
function zx_blog_card( $post, $featured = false ) {
	$cat   = zx_post_cat( $post );
	$url   = get_permalink( $post );
	$title = get_the_title( $post );
	$exc   = has_excerpt( $post ) ? get_the_excerpt( $post ) : wp_trim_words( wp_strip_all_tags( $post->post_content ), 22, '…' );
	ob_start();
	?>
	<article class="post-card reveal<?php echo $featured ? ' is-featured' : ''; ?>">
		<a class="post-media" href="<?php echo esc_url( $url ); ?>" tabindex="-1" aria-hidden="true"><?php echo zx_card_image( $post ); // phpcs:ignore ?>
			<?php if ( $cat ) : ?><span class="post-cat"><?php echo esc_html( $cat->name ); ?></span><?php endif; ?>
		</a>
		<div class="post-body">
			<div class="post-meta"><span><?php echo zx_icon( 'calendar', 'ic ic-xs' ); // phpcs:ignore ?> <?php echo esc_html( get_the_date( 'M d, Y', $post ) ); ?></span><span><?php echo zx_icon( 'clock', 'ic ic-xs' ); // phpcs:ignore ?> <?php echo (int) zx_reading_time( $post ); ?> min read</span></div>
			<h3><a href="<?php echo esc_url( $url ); ?>"><?php echo esc_html( $title ); ?></a></h3>
			<p><?php echo esc_html( $exc ); ?></p>
			<a class="link-arrow" href="<?php echo esc_url( $url ); ?>" aria-label="<?php echo esc_attr( 'Read article: ' . $title ); ?>">Read Article <?php echo zx_icon( 'arrow-right', 'ic ic-sm' ); // phpcs:ignore ?></a>
		</div>
	</article>
	<?php
	return ob_get_clean();
}

/** Echo the latest posts as cards (home page). */
function zx_latest_posts( $count = 3 ) {
	$q = new WP_Query(
		array(
			'posts_per_page'      => $count,
			'ignore_sticky_posts' => true,
			'no_found_rows'       => true,
		)
	);
	foreach ( $q->posts as $p ) {
		echo zx_blog_card( $p ); // phpcs:ignore
	}
	wp_reset_postdata();
}

/**
 * Table of contents from <h2 id="..."> headings.
 *
 * @param string $content Filtered post content.
 * @return array [ [id, text], ... ]
 */
function zx_toc( $content ) {
	preg_match_all( '/<h2[^>]*\sid="([^"]+)"[^>]*>(.*?)<\/h2>/is', $content, $m, PREG_SET_ORDER );
	return array_map(
		function ( $x ) {
			return array( $x[1], wp_strip_all_tags( $x[2] ) );
		},
		$m
	);
}

/** Share buttons. */
function zx_share_links( $url, $title ) {
	$u = rawurlencode( $url );
	$t = rawurlencode( $title );
	$links = array(
		array( 'https://www.facebook.com/sharer/sharer.php?u=' . $u, 'Share on Facebook', 'facebook' ),
		array( 'https://x.com/intent/post?url=' . $u . '&text=' . $t, 'Share on X', 'x-twitter' ),
		array( 'https://www.linkedin.com/sharing/share-offsite/?url=' . $u, 'Share on LinkedIn', 'linkedin' ),
		array( 'https://wa.me/?text=' . $t . '%20' . $u, 'Share on WhatsApp', 'whatsapp' ),
	);
	$html = '';
	foreach ( $links as $l ) {
		$html .= '<a href="' . esc_url( $l[0] ) . '" target="_blank" rel="noopener" aria-label="' . esc_attr( $l[1] ) . '">' . zx_icon( $l[2], 'ic ic-sm' ) . '</a>';
	}
	$html .= '<button data-copy="' . esc_attr( $url ) . '" aria-label="Copy link">' . zx_icon( 'copy', 'ic ic-sm' ) . '</button>';
	return $html;
}

/** CTA box inserted where posts contain <!--CTA-->. */
function zx_post_cta() {
	return '<div class="post-cta"><div><h3>Ready to start your project?</h3><p>Tell us about your idea and get a free consultation and estimate from the Zenvix team — we reply within one business day.</p></div>'
		. '<div class="post-cta-actions"><a class="btn btn-light btn-sm" href="' . esc_url( zx_url( 'contact' ) ) . '">Get a Free Quote ' . zx_icon( 'arrow-right', 'ic ic-sm' ) . '</a>'
		. '<a class="btn btn-ghost-light btn-sm" href="' . esc_url( zx_opt( 'whatsapp_url' ) ) . '" target="_blank" rel="noopener">' . zx_icon( 'whatsapp', 'ic ic-sm' ) . ' WhatsApp</a></div></div>';
}

/**
 * Post content: heading anchors for the TOC, CTA marker, scrollable tables.
 */
add_filter(
	'the_content',
	function ( $content ) {
		if ( ! is_singular( 'post' ) || ! in_the_loop() || ! is_main_query() ) {
			return $content;
		}
		// Add ids to h2 headings written in the editor.
		$used    = array();
		$content = preg_replace_callback(
			'/<h2(\s[^>]*)?>(.*?)<\/h2>/is',
			function ( $m ) use ( &$used ) {
				$attrs = $m[1] ?? '';
				if ( preg_match( '/\sid="([^"]+)"/', $attrs, $id ) ) {
					$used[] = $id[1];
					return $m[0];
				}
				$base = sanitize_title( wp_strip_all_tags( $m[2] ) );
				$id   = $base;
				$i    = 2;
				while ( in_array( $id, $used, true ) ) {
					$id = $base . '-' . $i++;
				}
				$used[] = $id;
				return '<h2' . $attrs . ' id="' . esc_attr( $id ) . '">' . $m[2] . '</h2>';
			},
			$content
		);
		// CTA marker (imported posts) — first one becomes the CTA box.
		$content = preg_replace( '/<!--CTA-->/', zx_post_cta(), $content, 1 );
		$content = str_replace( '<!--CTA-->', '', $content );
		// Wrap bare tables (classic editor) so they scroll on mobile.
		$content = preg_replace( '/(?<!<div class="table-wrap">)(<table(?![^>]*wp-block)[^>]*>.*?<\/table>)/is', '<div class="table-wrap">$1</div>', $content );
		$content = str_replace( '<div class="table-wrap"><div class="table-wrap">', '<div class="table-wrap">', $content );
		return $content;
	},
	20
);

add_filter(
	'excerpt_length',
	function () {
		return 26;
	}
);
add_filter(
	'excerpt_more',
	function () {
		return '…';
	}
);

/** Service page that matches a blog category (for the author box link). */
function zx_category_service_url( $cat ) {
	$map = array(
		'custom-software' => 'services/software-development',
		'mobile-apps'     => 'services/mobile-app-development',
		'web-development' => 'services/web-development',
	);
	return zx_url( $cat && isset( $map[ $cat->slug ] ) ? $map[ $cat->slug ] : 'services' );
}
