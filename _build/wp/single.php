<?php
/**
 * Single blog post.
 *
 * @package Zenvix
 */

get_header();

while ( have_posts() ) :
	the_post();
	$zx_cat     = zx_post_cat();
	$zx_url     = get_permalink();
	$zx_title   = get_the_title();
	$zx_content = apply_filters( 'the_content', get_the_content() ); // phpcs:ignore
	$zx_content = str_replace( ']]>', ']]&gt;', $zx_content );
	$zx_toc     = zx_toc( $zx_content );
	$zx_share   = zx_share_links( $zx_url, $zx_title );
	?>
<article <?php post_class( 'post' ); ?>>
	<header class="post-hero">
		<div class="ph-grid" aria-hidden="true"></div>
		<div class="container narrow-lg">
			<nav aria-label="Breadcrumb"><ol class="crumbs dark">
				<li><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Home</a></li>
				<li><a href="<?php echo esc_url( zx_url( 'blog' ) ); ?>">Blog</a></li>
				<li aria-current="page"><?php echo esc_html( $zx_cat ? $zx_cat->name : 'Article' ); ?></li>
			</ol></nav>
			<?php if ( $zx_cat ) : ?>
				<a class="post-cat static anim-up" href="<?php echo esc_url( get_category_link( $zx_cat ) ); ?>"><?php echo esc_html( $zx_cat->name ); ?></a>
			<?php endif; ?>
			<h1 class="anim-up" style="--d:.06s"><?php echo esc_html( $zx_title ); ?></h1>
			<?php if ( has_excerpt() ) : ?>
				<p class="post-excerpt anim-up" style="--d:.12s"><?php echo esc_html( get_the_excerpt() ); ?></p>
			<?php endif; ?>
			<div class="post-byline anim-up" style="--d:.18s">
				<span class="byline-avatar"><img src="<?php echo esc_url( ZX_URI . '/assets/img/favicon-192.png' ); ?>" alt="" width="40" height="40"></span>
				<span><b>Zenvix Editorial Team</b><small><time datetime="<?php echo esc_attr( get_the_date( 'c' ) ); ?>"><?php echo esc_html( get_the_date( 'M d, Y' ) ); ?></time> · <?php echo (int) zx_reading_time(); ?> min read</small></span>
				<div class="share"><?php echo $zx_share; // phpcs:ignore ?></div>
			</div>
		</div>
	</header>

	<?php if ( has_post_thumbnail() ) : ?>
		<div class="container narrow-lg">
			<figure class="post-cover anim-fade" style="--d:.2s"><?php the_post_thumbnail( 'full', array( 'loading' => 'eager', 'fetchpriority' => 'high', 'alt' => $zx_title ) ); ?></figure>
		</div>
	<?php endif; ?>

	<div class="container post-layout">
		<aside class="post-aside">
			<?php if ( count( $zx_toc ) > 1 ) : ?>
				<div class="toc" data-toc>
					<h2><?php echo zx_icon( 'list', 'ic ic-sm' ); // phpcs:ignore ?> On this page</h2>
					<ol>
						<?php foreach ( $zx_toc as $zx_item ) : ?>
							<li><a href="#<?php echo esc_attr( $zx_item[0] ); ?>"><?php echo esc_html( $zx_item[1] ); ?></a></li>
						<?php endforeach; ?>
					</ol>
				</div>
			<?php endif; ?>
			<div class="aside-cta"><span class="ic-badge"><?php echo zx_icon( 'rocket' ); // phpcs:ignore ?></span><h3>Need a quote?</h3><p>Get a free, no-obligation estimate for your project.</p><a class="btn btn-primary btn-sm btn-block" href="<?php echo esc_url( zx_url( 'contact' ) ); ?>">Talk to an expert</a></div>
		</aside>

		<div class="post-content prose">
			<?php
			echo $zx_content; // phpcs:ignore
			wp_link_pages();
			$zx_tags = get_the_tags();
			?>
			<div class="post-foot">
				<?php if ( $zx_tags ) : ?>
					<ul class="tags">
						<?php foreach ( $zx_tags as $zx_tag ) : ?>
							<li><a href="<?php echo esc_url( get_tag_link( $zx_tag ) ); ?>">#<?php echo esc_html( $zx_tag->name ); ?></a></li>
						<?php endforeach; ?>
					</ul>
				<?php else : ?>
					<span></span>
				<?php endif; ?>
				<div class="share"><span>Share:</span><?php echo $zx_share; // phpcs:ignore ?></div>
			</div>

			<div class="author-box">
				<img src="<?php echo esc_url( ZX_URI . '/assets/img/favicon-192.png' ); ?>" alt="" width="64" height="64" loading="lazy">
				<div><b>Written by the Zenvix Editorial Team</b><p>Engineers, designers and strategists at Zenvix Technologies in Lahore, sharing what we learn building software, apps and websites for clients worldwide. Need help with this topic? <a href="<?php echo esc_url( zx_category_service_url( $zx_cat ) ); ?>">See our <?php echo esc_html( $zx_cat ? strtolower( $zx_cat->name ) : '' ); ?> services</a>.</p></div>
			</div>

			<?php
			$zx_prev = get_previous_post();
			$zx_next = get_next_post();
			if ( $zx_prev || $zx_next ) :
				?>
				<nav class="post-nav" aria-label="More articles">
					<?php if ( $zx_prev ) : ?>
						<a class="pn prev" href="<?php echo esc_url( get_permalink( $zx_prev ) ); ?>"><small><?php echo zx_icon( 'arrow-left', 'ic ic-xs' ); // phpcs:ignore ?> Previous</small><b><?php echo esc_html( get_the_title( $zx_prev ) ); ?></b></a>
					<?php else : ?>
						<span></span>
					<?php endif; ?>
					<?php if ( $zx_next ) : ?>
						<a class="pn next" href="<?php echo esc_url( get_permalink( $zx_next ) ); ?>"><small>Next <?php echo zx_icon( 'arrow-right', 'ic ic-xs' ); // phpcs:ignore ?></small><b><?php echo esc_html( get_the_title( $zx_next ) ); ?></b></a>
					<?php endif; ?>
				</nav>
			<?php endif; ?>
		</div>
	</div>
</article>

	<?php
	$zx_related = get_posts(
		array(
			'posts_per_page' => 2,
			'post__not_in'   => array( get_the_ID() ),
			'category__in'   => $zx_cat ? array( $zx_cat->term_id ) : array(),
		)
	);
	if ( count( $zx_related ) < 2 ) {
		$zx_related = array_merge(
			$zx_related,
			get_posts(
				array(
					'posts_per_page' => 2 - count( $zx_related ),
					'post__not_in'   => array_merge( array( get_the_ID() ), wp_list_pluck( $zx_related, 'ID' ) ),
				)
			)
		);
	}
	if ( $zx_related ) :
		?>
<section class="section bg-soft">
	<div class="container">
		<div class="sec-head center"><span class="eyebrow reveal"><?php echo zx_icon( 'sparkle', 'ic ic-xs' ); // phpcs:ignore ?> Keep reading</span><h2 class="reveal" style="--d:.06s">Related <span class="grad-text">Articles</span></h2></div>
		<div class="grid-2 related-posts">
			<?php
			foreach ( $zx_related as $zx_r ) {
				echo zx_blog_card( $zx_r ); // phpcs:ignore
			}
			?>
		</div>
	</div>
</section>
		<?php
	endif;
endwhile;

get_footer();
