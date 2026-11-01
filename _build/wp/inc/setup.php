<?php
/**
 * One-time site setup (runs on theme activation; can be re-run from Appearance → Zenvix Setup).
 *
 * Non-destructive: existing pages/posts with the same slug are reused, nothing is deleted.
 *
 * @package Zenvix
 */

defined( 'ABSPATH' ) || exit;

/** Service pages created under /services/. */
function zx_service_pages() {
	return array(
		'web-development'        => 'Web Development',
		'software-development'   => 'Software Development',
		'mobile-app-development' => 'Mobile App Development',
		'social-media-marketing' => 'Social Media Marketing',
		'seo-services'           => 'SEO Services',
		'email-marketing'        => 'Email Marketing',
		'ui-ux-design'           => 'UI/UX Design',
		'ai-solutions'           => 'AI Solutions',
	);
}

/**
 * Find a page by path or create it.
 *
 * @return int Page ID.
 */
function zx_ensure_page( $slug, $title, $parent = 0, &$log = array() ) {
	$path = $parent ? get_post_field( 'post_name', $parent ) . '/' . $slug : $slug;
	$page = get_page_by_path( $path );
	if ( $page ) {
		if ( 'publish' !== $page->post_status ) {
			wp_update_post( array( 'ID' => $page->ID, 'post_status' => 'publish' ) );
		}
		$log[] = "Using existing page “{$page->post_title}” (/{$path}/)";
		return (int) $page->ID;
	}
	$id    = wp_insert_post(
		array(
			'post_type'   => 'page',
			'post_status' => 'publish',
			'post_title'  => $title,
			'post_name'   => $slug,
			'post_parent' => $parent,
		)
	);
	$log[] = "Created page “{$title}” (/{$path}/)";
	return (int) $id;
}

/** Import the bundled blog posts (skips posts whose slug already exists). */
function zx_import_posts( &$log ) {
	$file = ZX_DIR . '/inc/demo/posts.json';
	if ( ! file_exists( $file ) ) {
		return;
	}
	$posts = json_decode( file_get_contents( $file ), true ); // phpcs:ignore
	require_once ABSPATH . 'wp-admin/includes/media.php';
	require_once ABSPATH . 'wp-admin/includes/file.php';
	require_once ABSPATH . 'wp-admin/includes/image.php';

	foreach ( (array) $posts as $p ) {
		if ( get_page_by_path( $p['slug'], OBJECT, 'post' ) ) {
			$log[] = "Post “{$p['title']}” already exists — skipped";
			continue;
		}
		$cat = term_exists( $p['category'], 'category' );
		if ( ! $cat ) {
			$cat = wp_insert_term( $p['category'], 'category' );
		}
		$cat_id = is_array( $cat ) ? (int) $cat['term_id'] : (int) $cat;

		$id = wp_insert_post(
			array(
				'post_type'     => 'post',
				'post_status'   => 'publish',
				'post_title'    => $p['title'],
				'post_name'     => $p['slug'],
				'post_excerpt'  => $p['excerpt'],
				'post_content'  => $p['content'], // links resolved below once all posts exist
				'post_date'     => $p['date'],
				'post_category' => $cat_id ? array( $cat_id ) : array(),
				'tags_input'    => $p['tags'],
			),
			true
		);
		if ( is_wp_error( $id ) ) {
			$log[] = "Could not create “{$p['title']}”: " . $id->get_error_message();
			continue;
		}
		update_post_meta( $id, '_zx_demo', 1 );

		// Featured image from the theme's assets.
		$src = ZX_DIR . '/' . $p['image'];
		if ( file_exists( $src ) ) {
			$tmp = wp_tempnam( basename( $src ) );
			copy( $src, $tmp );
			$file_array = array(
				'name'     => $p['slug'] . '.' . pathinfo( $src, PATHINFO_EXTENSION ),
				'tmp_name' => $tmp,
			);
			$att = media_handle_sideload( $file_array, $id, $p['title'] );
			if ( is_wp_error( $att ) ) {
				@unlink( $tmp ); // phpcs:ignore
				$log[] = "Image for “{$p['title']}” failed: " . $att->get_error_message();
			} else {
				update_post_meta( $att, '_wp_attachment_image_alt', $p['title'] );
				set_post_thumbnail( $id, $att );
			}
		}
		$log[] = "Imported post “{$p['title']}”";
	}

	// Resolve {{url:...}} placeholders now that all pages and posts exist.
	foreach ( get_posts( array( 'meta_key' => '_zx_demo', 'posts_per_page' => -1, 'post_status' => 'any' ) ) as $post ) {
		if ( false === strpos( $post->post_content, '{{url:' ) ) {
			continue;
		}
		$content = preg_replace_callback(
			'/\{\{url:([^}]*)\}\}/',
			function ( $m ) {
				return esc_url( zx_url( $m[1] ) );
			},
			$post->post_content
		);
		wp_update_post( array( 'ID' => $post->ID, 'post_content' => wp_slash( $content ) ) );
	}
}

/**
 * Run setup. Returns a log of what happened.
 */
function zx_run_setup() {
	global $wpdb;

	// One setup at a time. After a theme switch, several admin requests can fire
	// after_switch_theme together; INSERT IGNORE is atomic, so only one gets the lock.
	$wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->options} WHERE option_name = 'zx_setup_lock' AND option_value < %d", time() - 300 ) );
	$locked = $wpdb->query( $wpdb->prepare( "INSERT IGNORE INTO {$wpdb->options} (option_name, option_value, autoload) VALUES ('zx_setup_lock', %s, 'no')", (string) time() ) );
	if ( ! $locked ) {
		return array( 'Setup is already running in another request — skipped this run' );
	}

	try {
		return zx_do_setup();
	} finally {
		$wpdb->delete( $wpdb->options, array( 'option_name' => 'zx_setup_lock' ) );
	}
}

/**
 * The setup steps (called by zx_run_setup() while holding the lock).
 */
function zx_do_setup() {
	$log = array();
	require_once ABSPATH . 'wp-admin/includes/file.php'; // get_home_path()
	require_once ABSPATH . 'wp-admin/includes/misc.php'; // got_url_rewrite(), save_mod_rewrite_rules()

	$home     = zx_ensure_page( 'home', 'Home', 0, $log );
	zx_ensure_page( 'about', 'About', 0, $log );
	$services = zx_ensure_page( 'services', 'Services', 0, $log );
	zx_ensure_page( 'contact', 'Contact', 0, $log );
	$blog     = zx_ensure_page( 'blog', 'Blog', 0, $log );
	foreach ( zx_service_pages() as $slug => $title ) {
		zx_ensure_page( $slug, $title, $services, $log );
	}

	update_option( 'show_on_front', 'page' );
	update_option( 'page_on_front', $home );
	update_option( 'page_for_posts', $blog );
	$log[] = 'Set “Home” as the front page and “Blog” as the posts page';

	// Post-name URLs. Only replaces WordPress's install defaults (empty, date-based or the
	// /index.php/ fallback WordPress picks when URL rewriting isn't available) — never a structure you chose.
	$current  = (string) get_option( 'permalink_structure' );
	$defaults = array( '', '/%year%/%monthnum%/%day%/%postname%/', '/index.php/%year%/%monthnum%/%day%/%postname%/', '/index.php/%postname%/' );
	if ( in_array( $current, $defaults, true ) && '/%postname%/' !== $current ) {
		if ( got_url_rewrite() ) {
			global $wp_rewrite; // set via WP_Rewrite so the flush below writes matching .htaccess rules
			$wp_rewrite->set_permalink_structure( '/%postname%/' );
			$log[] = 'Set permalinks to Post name (/%postname%/)';
		} else {
			$log[] = 'Permalinks left as ' . ( $current ? $current : 'Plain' ) . ': URL rewriting (Apache mod_rewrite) is not enabled on this server. Enable it, then choose Post name in Settings → Permalinks';
		}
	}

	// Hide WordPress's default "Hello world!" post if it is untouched.
	$hello = get_page_by_path( 'hello-world', OBJECT, 'post' );
	if ( $hello && 'publish' === $hello->post_status && false !== strpos( $hello->post_content, 'Welcome to WordPress' ) ) {
		wp_update_post( array( 'ID' => $hello->ID, 'post_status' => 'draft' ) );
		$log[] = 'Moved the default “Hello world!” post to drafts';
	}

	zx_import_posts( $log );

	if ( zx_cf7_active() ) {
		zx_cf7_ensure_form();
		$log[] = 'Contact Form 7 form ready';
	}

	flush_rewrite_rules( true ); // hard flush: also writes .htaccess
	$htaccess = get_home_path() . '.htaccess';
	if ( got_mod_rewrite() && ( ! file_exists( $htaccess ) || false === strpos( (string) file_get_contents( $htaccess ), 'RewriteRule' ) ) ) { // phpcs:ignore
		$log[] = 'Could not write .htaccess — go to Settings → Permalinks and click “Save Changes” once so page links work';
	}
	update_option( 'zx_setup_done', ZX_VERSION );
	update_option( 'zx_setup_log', $log );
	return $log;
}

add_action(
	'after_switch_theme',
	function () {
		if ( current_user_can( 'manage_options' ) ) {
			zx_run_setup();
			set_transient( 'zx_setup_notice', 1, 60 );
		}
	}
);

/* ------------------------------------------------------------------ Admin: setup page & notices */

add_action(
	'admin_menu',
	function () {
		add_theme_page( 'Zenvix Setup', 'Zenvix Setup', 'manage_options', 'zx-setup', 'zx_render_setup_page' );
	}
);

/** Plugin status rows for the setup page. */
function zx_plugin_rows() {
	if ( ! function_exists( 'get_plugins' ) ) {
		require_once ABSPATH . 'wp-admin/includes/plugin.php';
	}
	$installed = get_plugins();
	$rows      = array();
	foreach (
		array(
			'contact-form-7/wp-contact-form-7.php' => array( 'Contact Form 7', 'contact form 7', 'Powers the contact form.' ),
			'wp-mail-smtp/wp_mail_smtp.php'        => array( 'WP Mail SMTP', 'wp mail smtp', 'Delivers form emails reliably (configure with your Gmail on the live site).' ),
		) as $file => $p
	) {
		if ( is_plugin_active( $file ) ) {
			$status = '<span style="color:#15803d">✔ Active</span>';
		} elseif ( isset( $installed[ $file ] ) ) {
			$status = '<a class="button" href="' . esc_url( wp_nonce_url( admin_url( 'plugins.php?action=activate&plugin=' . rawurlencode( $file ) ), 'activate-plugin_' . $file ) ) . '">Activate</a>';
		} else {
			$status = '<a class="button button-primary" href="' . esc_url( admin_url( 'plugin-install.php?s=' . rawurlencode( $p[1] ) . '&tab=search&type=term' ) ) . '">Install</a>';
		}
		$rows[] = array( $p[0], $p[2], $status );
	}
	return $rows;
}

/** Appearance → Zenvix Setup. */
function zx_render_setup_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$log = null;
	if ( isset( $_POST['zx_run_setup'] ) && check_admin_referer( 'zx_run_setup' ) ) {
		$log = zx_run_setup();
	}
	$log = $log ?? get_option( 'zx_setup_log', array() );
	?>
	<div class="wrap">
		<h1>Zenvix Setup</h1>
		<h2 class="title">1. Plugins</h2>
		<table class="widefat striped" style="max-width:760px"><tbody>
			<?php foreach ( zx_plugin_rows() as $r ) : ?>
				<tr><td style="width:180px"><strong><?php echo esc_html( $r[0] ); ?></strong></td><td><?php echo esc_html( $r[1] ); ?></td><td style="width:120px"><?php echo $r[2]; // phpcs:ignore ?></td></tr>
			<?php endforeach; ?>
		</tbody></table>

		<h2 class="title">2. Pages, menu &amp; blog posts</h2>
		<p>Creates any missing pages (Home, About, Services + 8 service pages, Contact, Blog), sets the front page and imports the 3 blog articles. Safe to run again — existing content is reused, never deleted.</p>
		<form method="post">
			<?php wp_nonce_field( 'zx_run_setup' ); ?>
			<p><button class="button button-primary" name="zx_run_setup" value="1">Run setup</button>
			<a class="button" href="<?php echo esc_url( home_url( '/' ) ); ?>" target="_blank">View site</a>
			<a class="button" href="<?php echo esc_url( admin_url( 'themes.php?page=zx-settings' ) ); ?>">Zenvix Settings</a></p>
		</form>
		<?php if ( $log ) : ?>
			<h3>Last run</h3>
			<ul style="list-style:disc;padding-left:20px">
				<?php foreach ( $log as $line ) : ?>
					<li><?php echo esc_html( $line ); ?></li>
				<?php endforeach; ?>
			</ul>
		<?php endif; ?>
	</div>
	<?php
}

add_action(
	'admin_notices',
	function () {
		if ( ! current_user_can( 'manage_options' ) ) {
			return;
		}
		if ( get_transient( 'zx_setup_notice' ) ) {
			delete_transient( 'zx_setup_notice' );
			echo '<div class="notice notice-success is-dismissible"><p><strong>Zenvix theme is ready.</strong> Pages, front page and blog posts are set up. <a href="' . esc_url( admin_url( 'themes.php?page=zx-setup' ) ) . '">See what was done</a></p></div>';
		}
		if ( ! zx_cf7_active() ) {
			echo '<div class="notice notice-warning"><p><strong>Zenvix:</strong> install and activate <strong>Contact Form 7</strong> to enable the contact form. <a href="' . esc_url( admin_url( 'themes.php?page=zx-setup' ) ) . '">Open Zenvix Setup</a></p></div>';
		}
	}
);
