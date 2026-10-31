<?php
/**
 * Appearance → Zenvix Settings: contact details, location and social links.
 *
 * @package Zenvix
 */

defined( 'ABSPATH' ) || exit;

/**
 * Field definitions grouped by section.
 */
function zx_settings_fields() {
	return array(
		'contact'  => array(
			'title'  => __( 'Contact details', 'zenvix' ),
			'fields' => array(
				'email'    => array( __( 'Email address', 'zenvix' ), 'email', __( 'Shown on the site and used as the contact form recipient.', 'zenvix' ) ),
				'phone'    => array( __( 'Phone number', 'zenvix' ), 'text', __( 'As displayed, e.g. +92 326 4549778', 'zenvix' ) ),
				'whatsapp' => array( __( 'WhatsApp number', 'zenvix' ), 'text', __( 'International format, digits only, e.g. 923264549778', 'zenvix' ) ),
				'hours'    => array( __( 'Working hours', 'zenvix' ), 'text', '' ),
			),
		),
		'location' => array(
			'title'  => __( 'Location', 'zenvix' ),
			'fields' => array(
				'address_1' => array( __( 'Address line 1', 'zenvix' ), 'text', __( 'e.g. Gulberg, Lahore', 'zenvix' ) ),
				'address_2' => array( __( 'Address line 2', 'zenvix' ), 'text', __( 'e.g. Punjab, Pakistan', 'zenvix' ) ),
				'map_url'   => array( __( 'Google Maps link', 'zenvix' ), 'url', __( 'Used for "Get directions" links.', 'zenvix' ) ),
				'map_query' => array( __( 'Map location (embed)', 'zenvix' ), 'text', __( 'Address or place name shown in the map on the Contact page.', 'zenvix' ) ),
			),
		),
		'social'   => array(
			'title'  => __( 'Social links', 'zenvix' ),
			'fields' => array(
				'facebook'  => array( 'Facebook', 'url', '' ),
				'instagram' => array( 'Instagram', 'url', '' ),
				'x'         => array( 'X (Twitter)', 'url', '' ),
				'linkedin'  => array( 'LinkedIn', 'url', __( 'Leave empty to keep the icon without a link.', 'zenvix' ) ),
			),
		),
	);
}

add_action(
	'admin_menu',
	function () {
		add_theme_page( __( 'Zenvix Settings', 'zenvix' ), __( 'Zenvix Settings', 'zenvix' ), 'manage_options', 'zx-settings', 'zx_render_settings_page' );
	}
);

add_action(
	'admin_init',
	function () {
		register_setting(
			'zx_settings_group',
			'zx_settings',
			array(
				'type'              => 'array',
				'sanitize_callback' => 'zx_sanitize_settings',
				'default'           => array(),
			)
		);
	}
);

/**
 * Sanitize settings on save.
 *
 * @param mixed $input Raw input.
 * @return array
 */
function zx_sanitize_settings( $input ) {
	$out = array();
	if ( ! is_array( $input ) ) {
		return $out;
	}
	foreach ( zx_settings_fields() as $section ) {
		foreach ( $section['fields'] as $key => $f ) {
			if ( ! isset( $input[ $key ] ) ) {
				continue;
			}
			$v = wp_unslash( $input[ $key ] );
			switch ( $f[1] ) {
				case 'email':
					$out[ $key ] = sanitize_email( $v );
					break;
				case 'url':
					$out[ $key ] = esc_url_raw( trim( $v ) );
					break;
				default:
					$out[ $key ] = sanitize_text_field( $v );
			}
		}
	}
	if ( isset( $out['whatsapp'] ) ) {
		$out['whatsapp'] = preg_replace( '/\D+/', '', $out['whatsapp'] );
	}
	return $out;
}

/**
 * Settings page markup.
 */
function zx_render_settings_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$saved    = get_option( 'zx_settings', array() );
	$defaults = zx_defaults();
	?>
	<div class="wrap">
		<h1><?php esc_html_e( 'Zenvix Settings', 'zenvix' ); ?></h1>
		<p><?php esc_html_e( 'These details appear in the header, footer, contact page, WhatsApp button and structured data. Empty fields use the default shown in grey.', 'zenvix' ); ?></p>
		<form method="post" action="options.php">
			<?php settings_fields( 'zx_settings_group' ); ?>
			<?php foreach ( zx_settings_fields() as $section ) : ?>
				<h2 class="title"><?php echo esc_html( $section['title'] ); ?></h2>
				<table class="form-table" role="presentation">
					<?php foreach ( $section['fields'] as $key => $f ) : ?>
						<tr>
							<th scope="row"><label for="zx-<?php echo esc_attr( $key ); ?>"><?php echo esc_html( $f[0] ); ?></label></th>
							<td>
								<input class="regular-text" type="<?php echo esc_attr( 'url' === $f[1] ? 'url' : ( 'email' === $f[1] ? 'email' : 'text' ) ); ?>"
									id="zx-<?php echo esc_attr( $key ); ?>" name="zx_settings[<?php echo esc_attr( $key ); ?>]"
									value="<?php echo esc_attr( $saved[ $key ] ?? '' ); ?>"
									placeholder="<?php echo esc_attr( $defaults[ $key ] ?? '' ); ?>">
								<?php if ( $f[2] ) : ?>
									<p class="description"><?php echo esc_html( $f[2] ); ?></p>
								<?php endif; ?>
							</td>
						</tr>
					<?php endforeach; ?>
				</table>
			<?php endforeach; ?>
			<?php submit_button(); ?>
		</form>
	</div>
	<?php
}
