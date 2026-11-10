<?php
/**
 * Contact Form 7 integration.
 *
 * - Creates the "Zenvix Contact Form" (styled markup) once CF7 is active.
 * - Recipient is the email from Appearance → Zenvix Settings ([_zx_email] mail tag).
 * - "Which service do you need?" is required when Service = Other.
 * - Every submission is saved under Inquiries in the admin, even if email delivery fails.
 * - On localhost without SMTP configured, emails are captured (not sent) so the form can be tested.
 *
 * @package Zenvix
 */

defined( 'ABSPATH' ) || exit;

const ZX_CF7_TITLE = 'Zenvix Contact Form';

/** Is Contact Form 7 active? */
function zx_cf7_active() {
	return class_exists( 'WPCF7_ContactForm' );
}

/** ID of the theme's CF7 form (0 if missing). */
function zx_cf7_form_id() {
	$id = (int) get_option( 'zx_cf7_form_id' );
	if ( $id && 'wpcf7_contact_form' === get_post_type( $id ) ) {
		return $id;
	}
	return 0;
}

/** Form template (CF7 tags inside the theme's field markup). */
function zx_cf7_form_template() {
	$services = array( 'Web Development', 'Software Development', 'Mobile App Development', 'Social Media Marketing', 'SEO Services', 'Email Marketing', 'UI/UX Design', 'AI Solutions', 'Other' );
	$q        = function ( $items ) {
		return '"' . implode( '" "', $items ) . '"';
	};
	return implode(
		"\n",
		array(
			'<div class="f-row">',
			'<div class="field"><label for="fname">First Name <span class="req">*</span></label>[text* first-name id:fname autocomplete:given-name]</div>',
			'<div class="field"><label for="lname">Last Name <span class="req">*</span></label>[text* last-name id:lname autocomplete:family-name]</div>',
			'</div>',
			'<div class="f-row">',
			'<div class="field"><label for="email">Email Address <span class="req">*</span></label>[email* your-email id:email autocomplete:email]</div>',
			'<div class="field"><label for="phone">Phone Number</label>[tel phone id:phone autocomplete:tel]</div>',
			'</div>',
			'<div class="field"><label for="company">Company / Organization</label>[text company id:company autocomplete:organization]</div>',
			'<div class="field"><label for="service">Service Needed <span class="req">*</span></label>[select* service id:service first_as_label "Select a service..." ' . $q( $services ) . ']</div>',
			'<div class="field-reveal" data-other-wrap><div><div class="field"><label for="service_other">Which service do you need? <span class="req">*</span></label>[text service-other id:service_other placeholder "e.g. Shopify store, Chrome extension, IT consultancy..."]</div></div></div>',
			'<div class="f-row">',
			'<div class="field"><label for="budget">Project Budget</label>[select budget id:budget first_as_label "Select a budget range..." ' . $q( array( 'Under $1,000', '$1,000 – $5,000', '$5,000 – $15,000', '$15,000 – $50,000', '$50,000+' ) ) . ']</div>',
			'<div class="field"><label for="timeline">Timeline</label>[select timeline id:timeline first_as_label "Select a timeline..." ' . $q( array( 'ASAP (within 1 month)', '1–3 months', '3–6 months', '6+ months', 'Not sure yet' ) ) . ']</div>',
			'</div>',
			'<div class="field"><label for="details">Project Details <span class="req">*</span></label>[textarea* details id:details minlength:20 maxlength:1000 x5]<div class="field-foot"><small class="counter"><span data-counter>0</span> / 1000 characters</small></div></div>',
			'<div class="field check">[acceptance consent id:consent] I agree to be contacted by Zenvix Technologies about this inquiry. [/acceptance]</div>',
			'[submit class:btn class:btn-primary class:btn-block "Send Message"]',
		)
	);
}

/** Mail settings for the form. */
function zx_cf7_mail() {
	$body = implode(
		"\n",
		array(
			'New project inquiry from the website',
			'',
			'Name: [first-name] [last-name]',
			'Email: [your-email]',
			'Phone: [phone]',
			'Company: [company]',
			'Service: [service] [service-other]',
			'Budget: [budget]',
			'Timeline: [timeline]',
			'',
			'Project details:',
			'[details]',
			'',
			'--',
			'Sent from [_site_title] ([_site_url]) on [_date] at [_time]',
		)
	);
	return array(
		'active'             => true,
		'subject'            => 'New inquiry: [service] — [first-name] [last-name]',
		'sender'             => '[_site_title] <wordpress@[_site_domain]>',
		'recipient'          => '[_zx_email]',
		'body'               => $body,
		'additional_headers' => 'Reply-To: [first-name] [last-name] <[your-email]>',
		'attachments'        => '',
		'use_html'           => false,
		'exclude_blank'      => true,
	);
}

/** Create the theme's form if CF7 is active and it doesn't exist yet. */
function zx_cf7_ensure_form() {
	if ( ! zx_cf7_active() || zx_cf7_form_id() ) {
		return zx_cf7_form_id();
	}
	$form = WPCF7_ContactForm::get_template( array( 'title' => ZX_CF7_TITLE ) );
	$form->set_properties(
		array(
			'form'     => zx_cf7_form_template(),
			'mail'     => zx_cf7_mail(),
			'mail_2'   => array( 'active' => false ),
			'messages' => array_merge(
				(array) $form->prop( 'messages' ),
				array(
					'mail_sent_ok'     => 'Thank you! Your message has been sent. We will get back to you within 24 hours.',
					'validation_error' => 'Please check the highlighted fields and try again.',
					'accept_terms'     => 'Please tick the consent box to continue.',
				)
			),
		)
	);
	$id = $form->save();
	if ( $id ) {
		update_option( 'zx_cf7_form_id', (int) $id );
	}
	return (int) $id;
}
add_action( 'admin_init', 'zx_cf7_ensure_form' );

/** Contact page: render the form (or a fallback until CF7 is installed). */
function zx_contact_form() {
	$id = zx_cf7_active() ? zx_cf7_ensure_form() : 0;
	if ( $id ) {
		echo do_shortcode( '[contact-form-7 id="' . (int) $id . '" html_class="contact-form" html_id="zx-contact-form"]' ); // phpcs:ignore
		return;
	}
	echo '<div class="contact-form-fallback">';
	if ( current_user_can( 'install_plugins' ) ) {
		echo '<p class="notice-admin"><strong>Admin note:</strong> install and activate <a href="' . esc_url( admin_url( 'plugin-install.php?s=contact+form+7&tab=search&type=term' ) ) . '">Contact Form 7</a> to show the contact form here. Only administrators see this message.</p>';
	}
	echo '<p>Email us at <a href="mailto:' . esc_attr( zx_opt( 'email' ) ) . '">' . esc_html( zx_opt( 'email' ) ) . '</a> or <a href="' . esc_url( zx_opt( 'whatsapp_url' ) ) . '" target="_blank" rel="noopener">message us on WhatsApp</a> and we will reply within one business day.</p>';
	echo '</div>';
}

// No <p>/<br> auto-formatting inside the theme's form markup.
add_filter( 'wpcf7_autop_or_not', '__return_false' );

// [_zx_email] → email from Zenvix Settings.
add_filter(
	'wpcf7_special_mail_tags',
	function ( $output, $name ) {
		return '_zx_email' === $name ? zx_opt( 'email' ) : $output;
	},
	10,
	2
);

// "Which service do you need?" is required when Service = Other.
add_filter(
	'wpcf7_validate_text',
	function ( $result, $tag ) {
		if ( 'service-other' !== $tag->name ) {
			return $result;
		}
		$service = isset( $_POST['service'] ) ? sanitize_text_field( wp_unslash( $_POST['service'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification
		$other   = isset( $_POST['service-other'] ) ? trim( sanitize_text_field( wp_unslash( $_POST['service-other'] ) ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification
		if ( 'Other' === $service && '' === $other ) {
			$result->invalidate( $tag, 'Please tell us which service you need.' );
		}
		return $result;
	},
	20,
	2
);

/* ------------------------------------------------------------------ Inquiries log */

add_action(
	'init',
	function () {
		register_post_type(
			'zx_inquiry',
			array(
				'labels'          => array(
					'name'          => 'Inquiries',
					'singular_name' => 'Inquiry',
					'edit_item'     => 'Inquiry',
					'search_items'  => 'Search inquiries',
					'not_found'     => 'No inquiries yet',
				),
				'public'          => false,
				'show_ui'         => true,
				'show_in_menu'    => true,
				'menu_icon'       => 'dashicons-email-alt',
				'menu_position'   => 26,
				'supports'        => array( 'title' ),
				'capability_type' => 'post',
				'capabilities'    => array( 'create_posts' => 'do_not_allow' ),
				'map_meta_cap'    => true,
			)
		);
	}
);

/** Field labels stored with each inquiry. */
function zx_inquiry_fields() {
	return array(
		'first-name'    => 'First name',
		'last-name'     => 'Last name',
		'your-email'    => 'Email',
		'phone'         => 'Phone',
		'company'       => 'Company',
		'service'       => 'Service',
		'service-other' => 'Other service',
		'budget'        => 'Budget',
		'timeline'      => 'Timeline',
		'details'       => 'Project details',
	);
}

// Save the submission before CF7 sends the email.
add_action(
	'wpcf7_before_send_mail',
	function ( $contact_form ) {
		if ( (int) $contact_form->id() !== zx_cf7_form_id() || ! class_exists( 'WPCF7_Submission' ) ) {
			return;
		}
		$submission = WPCF7_Submission::get_instance();
		if ( ! $submission ) {
			return;
		}
		$data = $submission->get_posted_data();
		$val  = function ( $k ) use ( $data ) {
			$v = $data[ $k ] ?? '';
			return is_array( $v ) ? implode( ', ', $v ) : (string) $v;
		};
		$service = $val( 'service' ) === 'Other' && $val( 'service-other' ) ? 'Other: ' . $val( 'service-other' ) : $val( 'service' );
		$id      = wp_insert_post(
			array(
				'post_type'   => 'zx_inquiry',
				'post_status' => 'publish',
				'post_title'  => sanitize_text_field( trim( $val( 'first-name' ) . ' ' . $val( 'last-name' ) ) . ' — ' . $service ),
			)
		);
		if ( $id && ! is_wp_error( $id ) ) {
			foreach ( array_keys( zx_inquiry_fields() ) as $k ) {
				update_post_meta( $id, '_zx_' . $k, 'details' === $k ? sanitize_textarea_field( $val( $k ) ) : sanitize_text_field( $val( $k ) ) );
			}
			update_post_meta( $id, '_zx_mail', 'pending' );
			$GLOBALS['zx_last_inquiry'] = $id;
		}
	}
);

add_action(
	'wpcf7_mail_sent',
	function () {
		if ( ! empty( $GLOBALS['zx_last_inquiry'] ) ) {
			update_post_meta( $GLOBALS['zx_last_inquiry'], '_zx_mail', ! empty( $GLOBALS['zx_mail_captured'] ) ? 'captured' : 'sent' );
		}
	}
);
add_action(
	'wpcf7_mail_failed',
	function () {
		if ( ! empty( $GLOBALS['zx_last_inquiry'] ) ) {
			update_post_meta( $GLOBALS['zx_last_inquiry'], '_zx_mail', 'failed' );
		}
	}
);

// Inquiry screen: read-only details box.
add_action(
	'add_meta_boxes_zx_inquiry',
	function () {
		add_meta_box(
			'zx-inquiry',
			'Inquiry details',
			function ( $post ) {
				$status = get_post_meta( $post->ID, '_zx_mail', true );
				$labels = array(
					'sent'     => 'Email sent',
					'failed'   => 'Email failed — check WP Mail SMTP settings',
					'captured' => 'Local test — email captured, not sent',
					'pending'  => 'Pending',
				);
				echo '<table class="widefat striped"><tbody>';
				foreach ( zx_inquiry_fields() as $k => $label ) {
					$v = get_post_meta( $post->ID, '_zx_' . $k, true );
					if ( '' === $v ) {
						continue;
					}
					if ( 'your-email' === $k ) {
						$v = '<a href="mailto:' . esc_attr( $v ) . '">' . esc_html( $v ) . '</a>';
					} else {
						$v = nl2br( esc_html( $v ) );
					}
					echo '<tr><th style="width:160px">' . esc_html( $label ) . '</th><td>' . $v . '</td></tr>'; // phpcs:ignore
				}
				echo '<tr><th>Received</th><td>' . esc_html( get_the_date( 'M d, Y H:i', $post ) ) . '</td></tr>';
				echo '<tr><th>Email status</th><td>' . esc_html( $labels[ $status ] ?? '—' ) . '</td></tr>';
				echo '</tbody></table>';
			},
			'zx_inquiry',
			'normal',
			'high'
		);
	}
);

// Inquiries list columns.
add_filter(
	'manage_zx_inquiry_posts_columns',
	function () {
		return array(
			'cb'         => '<input type="checkbox">',
			'title'      => 'Name — Service',
			'zx_email'   => 'Email',
			'zx_phone'   => 'Phone',
			'zx_budget'  => 'Budget',
			'zx_mail'    => 'Email status',
			'date'       => 'Received',
		);
	}
);
add_action(
	'manage_zx_inquiry_posts_custom_column',
	function ( $col, $id ) {
		$map = array(
			'zx_email'  => '_zx_your-email',
			'zx_phone'  => '_zx_phone',
			'zx_budget' => '_zx_budget',
			'zx_mail'   => '_zx_mail',
		);
		if ( isset( $map[ $col ] ) ) {
			echo esc_html( get_post_meta( $id, $map[ $col ], true ) );
		}
	},
	10,
	2
);

/* ------------------------------------------------------------------ Local testing */

/** Running on a local development host? */
function zx_is_local() {
	$host = wp_parse_url( home_url(), PHP_URL_HOST );
	return in_array( $host, array( 'localhost', '127.0.0.1', '::1' ), true ) || ( $host && preg_match( '/\.(test|local|localhost)$/', $host ) );
}

/** Has WP Mail SMTP been configured with a real mailer? */
function zx_smtp_configured() {
	$o = get_option( 'wp_mail_smtp' );
	return is_array( $o ) && ! empty( $o['mail']['mailer'] ) && 'mail' !== $o['mail']['mailer'];
}

// On localhost (no SMTP configured) capture emails in wp-content/zx-mail-log.txt instead of sending.
add_filter(
	'pre_wp_mail',
	function ( $return, $atts ) {
		if ( null !== $return || ! zx_is_local() || zx_smtp_configured() ) {
			return $return;
		}
		$GLOBALS['zx_mail_captured'] = true;
		$to   = is_array( $atts['to'] ) ? implode( ', ', $atts['to'] ) : $atts['to'];
		$hdrs = is_array( $atts['headers'] ) ? implode( "\n", $atts['headers'] ) : (string) $atts['headers'];
		$log  = sprintf( "==== %s\nTo: %s\nSubject: %s\n%s\n\n%s\n\n", gmdate( 'c' ), $to, $atts['subject'], $hdrs, $atts['message'] );
		@file_put_contents( WP_CONTENT_DIR . '/zx-mail-log.txt', $log, FILE_APPEND | LOCK_EX ); // phpcs:ignore
		return true;
	},
	10,
	2
);
