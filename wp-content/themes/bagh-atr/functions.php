<?php
add_action('wp_enqueue_scripts', function () {
    wp_enqueue_style('bagh-atr-fonts', 'https://fonts.googleapis.com/css2?family=Aref+Ruqaa:wght@700&family=Vazirmatn:wght@400;500;700&display=swap', [], null);
    wp_enqueue_style('bagh-atr', get_theme_file_uri('assets/style.css'), [], wp_get_theme()->get('Version'));
});
add_action('after_setup_theme', function () {
    add_theme_support('wp-block-styles');
});
