<?php
/**
 * Blog listing: posts page, category/tag archives and search results.
 *
 * @package Zenvix
 */

defined( 'ABSPATH' ) || exit;

$zx_blog_url = zx_url( 'blog' );
$zx_crumbs   = array( array( 'Home', home_url( '/' ) ) );
$zx_title    = 'Insights to Build, Launch &amp; <span class="grad-text-light">Grow Smarter</span>';
$zx_text     = 'Practical guides on custom software, mobile app costs, websites and digital marketing — written by the engineers and strategists at Zenvix Technologies.';
$zx_eyebrow  = 'Blog & Insights';

if ( is_category() || is_tag() ) {
	$zx_term     = get_queried_object();
	$zx_crumbs[] = array( 'Blog', $zx_blog_url );
	$zx_crumbs[] = array( $zx_term->name, null );
	$zx_title    = esc_html( $zx_term->name ) . ' <span class="grad-text-light">Articles</span>';
	$zx_text     = $zx_term->description ? esc_html( $zx_term->description ) : 'Guides and insights on ' . esc_html( strtolower( $zx_term->name ) ) . ' from the Zenvix team.';
	$zx_eyebrow  = is_category() ? 'Category' : 'Tag';
} elseif ( is_search() ) {
	$zx_crumbs[] = array( 'Blog', $zx_blog_url );
	$zx_crumbs[] = array( 'Search', null );
	$zx_title    = 'Search results for <span class="grad-text-light">“' . esc_html( get_search_query() ) . '”</span>';
	$zx_text     = sprintf( '%d article(s) found.', (int) $GLOBALS['wp_query']->found_posts );
	$zx_eyebrow  = 'Search';
} elseif ( is_author() || is_date() ) {
	$zx_crumbs[] = array( 'Blog', $zx_blog_url );
	$zx_crumbs[] = array( wp_strip_all_tags( get_the_archive_title() ), null );
	$zx_title    = esc_html( wp_strip_all_tags( get_the_archive_title() ) );
	$zx_text     = '';
	$zx_eyebrow  = 'Archive';
} else {
	$zx_crumbs[] = array( 'Blog', null );
}

get_header();

zx_page_hero(
	array(
		'eyebrow' => $zx_eyebrow,
		'title'   => $zx_title,
		'text'    => $zx_text,
		'crumbs'  => $zx_crumbs,
		'bg'      => 'assets/img/un/flatlay.webp',
	)
);

$zx_cats    = get_categories( array( 'hide_empty' => true ) );
$zx_current = is_category() ? get_queried_object_id() : 0;
$zx_feature = is_home() && ! is_paged();
?>
<section class="section">
	<div class="container">
		<div class="blog-toolbar reveal">
			<nav class="filters left" aria-label="Blog categories">
				<a class="chip<?php echo is_home() ? ' is-active' : ''; ?>" href="<?php echo esc_url( $zx_blog_url ); ?>"<?php echo is_home() ? ' aria-current="page"' : ''; ?>>All Articles</a>
				<?php foreach ( $zx_cats as $zx_cat ) : ?>
					<?php $zx_on = $zx_current === $zx_cat->term_id; ?>
					<a class="chip<?php echo $zx_on ? ' is-active' : ''; ?>" href="<?php echo esc_url( get_category_link( $zx_cat ) ); ?>"<?php echo $zx_on ? ' aria-current="page"' : ''; ?>><?php echo esc_html( $zx_cat->name ); ?></a>
				<?php endforeach; ?>
			</nav>
			<form class="search" role="search" method="get" action="<?php echo esc_url( home_url( '/' ) ); ?>">
				<label for="blog-search" class="sr-only">Search articles</label>
				<?php echo zx_icon( 'search', 'ic ic-sm' ); // phpcs:ignore ?>
				<input id="blog-search" type="search" name="s" placeholder="Search articles..." value="<?php echo esc_attr( get_search_query() ); ?>">
				<input type="hidden" name="post_type" value="post">
			</form>
		</div>

		<?php if ( have_posts() ) : ?>
			<div class="blog-grid<?php echo $zx_feature ? '' : ' is-filtered'; ?>">
				<?php
				$zx_i = 0;
				while ( have_posts() ) :
					the_post();
					echo zx_blog_card( get_post(), $zx_feature && 0 === $zx_i ); // phpcs:ignore
					$zx_i++;
				endwhile;
				?>
			</div>
			<?php
			the_posts_pagination(
				array(
					'mid_size'  => 1,
					'prev_text' => zx_icon( 'arrow-left', 'ic ic-sm' ) . '<span class="sr-only">Previous</span>',
					'next_text' => '<span class="sr-only">Next</span>' . zx_icon( 'arrow-right', 'ic ic-sm' ),
				)
			);
			?>
		<?php else : ?>
			<p class="empty-state"><?php echo zx_icon( 'search', 'ic' ); // phpcs:ignore ?> No articles match your search. Try another keyword.</p>
		<?php endif; ?>
	</div>
</section>
<?php
get_template_part( 'template-parts/blog-extras' );
get_footer();
