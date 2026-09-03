<?php
/**
 * Plugin Name: Gary Wallage Network Legal Sync
 * Plugin URI: https://garywallage.uk
 * Description: Universal network-level policy manager for the Gary Wallage Photography multisite network. Define Terms & Conditions, Privacy Policy, and Cookie Policy once in Network Admin, and automatically synchronize them across all 7 sites.
 * Version: 1.0.0
 * Author: Gary David Wallage
 * Author URI: https://garywallage.uk
 * License: GPL-2.0+
 * Network: true
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class GW_Network_Legal_Sync {

    const OPT_TERMS   = 'gw_legal_sync_terms';
    const OPT_PRIVACY = 'gw_legal_sync_privacy';
    const OPT_COOKIES = 'gw_legal_sync_cookies';

    private static $instance = null;

    public static function get_instance() {
        if ( null === self::$instance ) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    public function __construct() {
        // Network Admin settings menu
        add_action( 'network_admin_menu', array( $this, 'add_network_admin_menu' ) );
        add_action( 'network_admin_edit_gw_legal_sync_save', array( $this, 'handle_network_save' ) );

        // Dynamic footer legal page filter fallback
        add_filter( 'theme_mod_legal_page_terms', array( $this, 'filter_terms_page_id' ) );
        add_filter( 'theme_mod_legal_page_privacy', array( $this, 'filter_privacy_page_id' ) );
        add_filter( 'theme_mod_legal_page_cookies', array( $this, 'filter_cookies_page_id' ) );
    }

    public function add_network_admin_menu() {
        add_submenu_page(
            'settings.php',
            'Network Legal Policies',
            'Legal Policies Sync',
            'manage_network_options',
            'gw-legal-sync',
            array( $this, 'render_network_settings_page' )
        );
    }

    public function render_network_settings_page() {
        if ( ! current_user_can( 'manage_network_options' ) ) {
            wp_die( 'Access denied.' );
        }

        $terms   = get_site_option( self::OPT_TERMS, $this->get_default_terms() );
        $privacy = get_site_option( self::OPT_PRIVACY, $this->get_default_privacy() );
        $cookies = get_site_option( self::OPT_COOKIES, $this->get_default_cookies() );

        $updated = isset( $_GET['updated'] ) && $_GET['updated'] === 'true';
        ?>
        <div class="wrap">
            <h1>Universal Legal Policies — Network Manager</h1>
            <p class="description">Edit the universal policy text below. Clicking <strong>Save &amp; Synchronize Network-Wide</strong> updates these master templates and automatically pushes the content to the corresponding pages across all sites on this network.</p>

            <?php if ( $updated ) : ?>
                <div class="notice notice-success is-dismissible">
                    <p><strong>Success:</strong> Universal legal policies saved and synchronized across all network sites!</p>
                </div>
            <?php endif; ?>

            <form method="post" action="<?php echo esc_url( network_admin_url( 'edit.php?action=gw_legal_sync_save' ) ); ?>">
                <?php wp_nonce_field( 'gw_legal_sync_verify', 'gw_legal_sync_nonce' ); ?>

                <table class="form-table" role="presentation">
                    <tr>
                        <th scope="row"><label for="gw_terms_content">Terms &amp; Conditions Content</label></th>
                        <td>
                            <?php wp_editor( $terms, 'gw_terms_content', array( 'textarea_name' => 'gw_terms_content', 'textarea_rows' => 12 ) ); ?>
                            <p class="description">Applies to <code>/terms-and-conditions/</code> across all sites.</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row"><label for="gw_privacy_content">Privacy Policy Content</label></th>
                        <td>
                            <?php wp_editor( $privacy, 'gw_privacy_content', array( 'textarea_name' => 'gw_privacy_content', 'textarea_rows' => 12 ) ); ?>
                            <p class="description">Applies to <code>/privacy-policy/</code> across all sites.</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row"><label for="gw_cookies_content">Cookie Policy Content</label></th>
                        <td>
                            <?php wp_editor( $cookies, 'gw_cookies_content', array( 'textarea_name' => 'gw_cookies_content', 'textarea_rows' => 12 ) ); ?>
                            <p class="description">Applies to <code>/cookie-policy/</code> across all sites.</p>
                        </td>
                    </tr>
                </table>

                <?php submit_button( 'Save & Synchronize Network-Wide' ); ?>
            </form>
        </div>
        <?php
    }

    public function handle_network_save() {
        check_admin_referer( 'gw_legal_sync_verify', 'gw_legal_sync_nonce' );

        if ( ! current_user_can( 'manage_network_options' ) ) {
            wp_die( 'Access denied.' );
        }

        $terms   = isset( $_POST['gw_terms_content'] ) ? wp_kses_post( wp_unslash( $_POST['gw_terms_content'] ) ) : '';
        $privacy = isset( $_POST['gw_privacy_content'] ) ? wp_kses_post( wp_unslash( $_POST['gw_privacy_content'] ) ) : '';
        $cookies = isset( $_POST['gw_cookies_content'] ) ? wp_kses_post( wp_unslash( $_POST['gw_cookies_content'] ) ) : '';

        update_site_option( self::OPT_TERMS, $terms );
        update_site_option( self::OPT_PRIVACY, $privacy );
        update_site_option( self::OPT_COOKIES, $cookies );

        // Push to all sites in network
        $this->sync_network_pages( $terms, $privacy, $cookies );

        wp_safe_redirect( add_query_arg( array( 'page' => 'gw-legal-sync', 'updated' => 'true' ), network_admin_url( 'settings.php' ) ) );
        exit;
    }

    public function sync_network_pages( $terms = null, $privacy = null, $cookies = null ) {
        if ( null === $terms )   $terms   = get_site_option( self::OPT_TERMS, $this->get_default_terms() );
        if ( null === $privacy ) $privacy = get_site_option( self::OPT_PRIVACY, $this->get_default_privacy() );
        if ( null === $cookies ) $cookies = get_site_option( self::OPT_COOKIES, $this->get_default_cookies() );

        $sites = get_sites( array( 'number' => 100 ) );
        foreach ( $sites as $s ) {
            switch_to_blog( $s->blog_id );

            // 1. Terms & Conditions
            $p_terms = get_page_by_path( 'terms-and-conditions' );
            if ( ! $p_terms ) {
                $tid = wp_insert_post( array(
                    'post_title'   => 'Terms & Conditions',
                    'post_name'    => 'terms-and-conditions',
                    'post_content' => $terms,
                    'post_status'  => 'publish',
                    'post_type'    => 'page'
                ) );
            } else {
                $tid = $p_terms->ID;
                wp_update_post( array( 'ID' => $tid, 'post_content' => $terms, 'post_status' => 'publish' ) );
            }
            set_theme_mod( 'legal_page_terms', $tid );

            // 2. Privacy Policy
            $p_priv = get_page_by_path( 'privacy-policy' );
            if ( ! $p_priv ) $p_priv = get_page_by_path( 'privacy-policy-2' );
            if ( ! $p_priv ) {
                $pid = wp_insert_post( array(
                    'post_title'   => 'Privacy Policy',
                    'post_name'    => 'privacy-policy',
                    'post_content' => $privacy,
                    'post_status'  => 'publish',
                    'post_type'    => 'page'
                ) );
            } else {
                $pid = $p_priv->ID;
                wp_update_post( array( 'ID' => $pid, 'post_content' => $privacy, 'post_status' => 'publish' ) );
            }
            set_theme_mod( 'legal_page_privacy', $pid );

            // 3. Cookie Policy
            $p_cookie = get_page_by_path( 'cookie-policy' );
            if ( ! $p_cookie ) {
                $cid = wp_insert_post( array(
                    'post_title'   => 'Cookie Policy',
                    'post_name'    => 'cookie-policy',
                    'post_content' => $cookies,
                    'post_status'  => 'publish',
                    'post_type'    => 'page'
                ) );
            } else {
                $cid = $p_cookie->ID;
                wp_update_post( array( 'ID' => $cid, 'post_content' => $cookies, 'post_status' => 'publish' ) );
            }
            set_theme_mod( 'legal_page_cookies', $cid );

            restore_current_blog();
        }
    }

    public function filter_terms_page_id( $id ) {
        if ( ! empty( $id ) && get_post_status( $id ) === 'publish' ) return $id;
        $page = get_page_by_path( 'terms-and-conditions' );
        return $page ? $page->ID : $id;
    }

    public function filter_privacy_page_id( $id ) {
        if ( ! empty( $id ) && get_post_status( $id ) === 'publish' ) return $id;
        $page = get_page_by_path( 'privacy-policy' );
        if ( ! $page ) $page = get_page_by_path( 'privacy-policy-2' );
        return $page ? $page->ID : $id;
    }

    public function filter_cookies_page_id( $id ) {
        if ( ! empty( $id ) && get_post_status( $id ) === 'publish' ) return $id;
        $page = get_page_by_path( 'cookie-policy' );
        return $page ? $page->ID : $id;
    }

    private function get_default_terms() {
        return "<!-- wp:heading -->\n<h2 class=\"wp-block-heading\">Terms &amp; Conditions — Gary Wallage Photography</h2>\n<!-- /wp:heading -->\n\n<!-- wp:paragraph -->\n<p>These terms apply to all bookings, consultations, and commissioned photography services provided by Gary Wallage Photography.</p>\n<!-- /wp:paragraph -->\n\n<!-- wp:heading {\"level\":3} -->\n<h3 class=\"wp-block-heading\">1. Booking &amp; Retainer</h3>\n<!-- /wp:heading -->\n<!-- wp:paragraph -->\n<p>Dates are reserved upon receipt of booking confirmation and agreed retainer. Pre-shoot consultations are complimentary and allow full customization of your session.</p>\n<!-- /wp:paragraph -->\n\n<!-- wp:heading {\"level\":3} -->\n<h3 class=\"wp-block-heading\">2. Rescheduling &amp; Cancellations</h3>\n<!-- /wp:heading -->\n<!-- wp:paragraph -->\n<p>We understand life happens. Sessions may be rescheduled with at least 48 hours notice without penalty.</p>\n<!-- /wp:paragraph -->\n\n<!-- wp:heading {\"level\":3} -->\n<h3 class=\"wp-block-heading\">3. Delivery of Master Files</h3>\n<!-- /wp:heading -->\n<!-- wp:paragraph -->\n<p>High-resolution, fully retouched digital images are delivered via private online gallery within agreed delivery timeframes.</p>\n<!-- /wp:paragraph -->\n\n<!-- wp:heading {\"level\":3} -->\n<h3 class=\"wp-block-heading\">4. Studio &amp; Contact Information</h3>\n<!-- /wp:heading -->\n<!-- wp:paragraph -->\n<p>63 Twinehame Road<br>Swindon SN25 2AG<br>Email: <a href=\"mailto:photographer@garywallage.uk\">photographer@garywallage.uk</a></p>\n<!-- /wp:paragraph -->";
    }

    private function get_default_privacy() {
        return "<!-- wp:heading -->\n<h2 class=\"wp-block-heading\">Privacy Policy — Gary Wallage Photography</h2>\n<!-- /wp:heading -->\n\n<!-- wp:paragraph -->\n<p>Gary Wallage Photography is committed to protecting your personal data, privacy, and photographic rights. This policy sets out how we handle your personal information, consultation records, and digital imagery.</p>\n<!-- /wp:paragraph -->\n\n<!-- wp:heading {\"level\":3} -->\n<h3 class=\"wp-block-heading\">1. Information We Collect</h3>\n<!-- /wp:heading -->\n<!-- wp:paragraph -->\n<p>When you book a session, request details, or schedule a consultation, we collect your name, email address (photographer@garywallage.uk), phone number, session date, and shoot preferences.</p>\n<!-- /wp:paragraph -->\n\n<!-- wp:heading {\"level\":3} -->\n<h3 class=\"wp-block-heading\">2. Photographic Privacy &amp; Image Rights</h3>\n<!-- /wp:heading -->\n<!-- wp:paragraph -->\n<p>Your privacy is paramount. Images are never published online or shared on social media without explicit, written model release consent.</p>\n<!-- /wp:paragraph -->\n\n<!-- wp:heading {\"level\":3} -->\n<h3 class=\"wp-block-heading\">3. Contact &amp; Data Access</h3>\n<!-- /wp:heading -->\n<!-- wp:paragraph -->\n<p>To request access to or deletion of your personal records, please contact <a href=\"mailto:photographer@garywallage.uk\">photographer@garywallage.uk</a>.</p>\n<!-- /wp:paragraph -->";
    }

    private function get_default_cookies() {
        return "<!-- wp:heading -->\n<h2 class=\"wp-block-heading\">Cookie Policy — Gary Wallage Photography</h2>\n<!-- /wp:heading -->\n\n<!-- wp:paragraph -->\n<p>Gary Wallage Photography uses essential cookies to ensure our website functions correctly and to deliver a seamless client experience.</p>\n<!-- /wp:paragraph -->\n\n<!-- wp:heading {\"level\":3} -->\n<h3 class=\"wp-block-heading\">1. What Are Cookies</h3>\n<!-- /wp:heading -->\n<!-- wp:paragraph -->\n<p>Cookies are small text files placed on your device to ensure secure navigation, maintain booking session state, and remember your display preferences.</p>\n<!-- /wp:paragraph -->\n\n<!-- wp:heading {\"level\":3} -->\n<h3 class=\"wp-block-heading\">2. Essential &amp; Functional Cookies</h3>\n<!-- /wp:heading -->\n<!-- wp:paragraph -->\n<p>We only deploy essential cookies required for calendar bookings, client inquiries, and core security. We do not use intrusive third-party cross-site advertising trackers.</p>\n<!-- /wp:paragraph -->\n\n<!-- wp:heading {\"level\":3} -->\n<h3 class=\"wp-block-heading\">3. Inquiries</h3>\n<!-- /wp:heading -->\n<!-- wp:paragraph -->\n<p>For any questions regarding our cookie or privacy practices, please contact <a href=\"mailto:photographer@garywallage.uk\">photographer@garywallage.uk</a>.</p>\n<!-- /wp:paragraph -->";
    }
}

// Instantiate
GW_Network_Legal_Sync::get_instance();
