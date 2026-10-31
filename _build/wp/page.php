<?php
/**
 * Generic page (any page without its own page-{slug}.php template).
 *
 * @package Zenvix
 */

get_header();

while ( have_posts() ) :
	the_post();
	zx_page_hero(
		array(
			'title'  => esc_html( get_the_title() ),
			'text'   => has_excerpt() ? esc_html( get_the_excerpt() ) : '',
			'crumbs' => array( array( 'Home', home_url( '/' ) ), array( get_the_title(), null ) ),
		)
	);
	?>
	<section class="section">
		<div class="container narrow">
			<div class="prose page-content">
				<?php the_content(); ?>
			</div>
		</div>
	</section>
	<?php
endwhile;

get_footer();
