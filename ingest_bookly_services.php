<?php
/**
 * Automated Bookly Service Catalog Matrix Ingestion Engine
 * Ingests all 7 sub-sites with complete atomic and compound services from master specifications.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

global $wpdb;

echo "=== Starting Full Bookly Service Catalog Matrix Ingestion ===\n";

$catalogs = array(
    // -------------------------------------------------------------
    // SITE 1: staging.garywallage.uk (Portrait & Headshots)
    // -------------------------------------------------------------
    1 => array(
        'name' => 'Portrait & Headshots (staging.garywallage.uk)',
        'staff' => array(
            'gary' => array( 'name' => 'Gary David Wallage', 'email' => 'gary@garywallage.uk' ),
            'hma'  => array( 'name' => 'HMA - Hair & Makeup Artist', 'email' => 'hma@garywallage.uk' ),
        ),
        'categories' => array( 'Consultations', 'Portrait Sessions', 'Corporate & Team', 'Hair & Makeup', 'Portrait Packages' ),
        'atomics' => array(
            'P00' => array( 'title' => 'P00 - Portrait Consultation', 'price' => 0.00, 'duration' => 1800, 'category' => 'Consultations', 'staff' => 'gary', 'color' => '#1A365D' ),
            'P01' => array( 'title' => 'P01 - Classic Portrait Session', 'price' => 145.00, 'duration' => 3600, 'category' => 'Portrait Sessions', 'staff' => 'gary', 'color' => '#1A365D' ),
            'P02' => array( 'title' => 'P02 - Extended Portrait Session', 'price' => 225.00, 'duration' => 7200, 'category' => 'Portrait Sessions', 'staff' => 'gary', 'color' => '#1A365D' ),
            'P03' => array( 'title' => 'P03 - Corporate Headshot Session', 'price' => 295.00, 'duration' => 5400, 'category' => 'Corporate & Team', 'staff' => 'gary', 'color' => '#1A365D' ),
            'P04' => array( 'title' => 'P04 - Team Headshots (Per Person)', 'price' => 85.00, 'duration' => 1200, 'category' => 'Corporate & Team', 'staff' => 'gary', 'color' => '#1A365D' ),
            'PH1' => array( 'title' => 'PH1 - Hair & Makeup — Natural/Radiant', 'price' => 195.00, 'duration' => 7200, 'category' => 'Hair & Makeup', 'staff' => 'hma', 'color' => '#4A90E2' ),
            'PH2' => array( 'title' => 'PH2 - Hair & Makeup — Full Glamour', 'price' => 245.00, 'duration' => 7200, 'category' => 'Hair & Makeup', 'staff' => 'hma', 'color' => '#4A90E2' ),
        ),
        'compounds' => array(
            'CP01' => array( 'title' => 'CP01 - The Professional Profile', 'price' => 295.00, 'category' => 'Portrait Packages', 'color' => '#1A365D', 'components' => array( 'PH1', 'P01' ) ),
            'CP02' => array( 'title' => 'CP02 - The Actor Portfolio', 'price' => 375.00, 'category' => 'Portrait Packages', 'color' => '#1A365D', 'components' => array( 'PH1', 'P02' ) ),
            'CP03' => array( 'title' => 'CP03 - The Executive Portrait', 'price' => 439.00, 'category' => 'Portrait Packages', 'color' => '#1A365D', 'components' => array( 'PH1', 'P03' ) ),
            'CP04' => array( 'title' => 'CP04 - The Personal Brand', 'price' => 419.00, 'category' => 'Portrait Packages', 'color' => '#1A365D', 'components' => array( 'PH2', 'P02' ) ),
        )
    ),

    // -------------------------------------------------------------
    // SITE 2: wedding.garywallage.uk (Luxury Wedding)
    // -------------------------------------------------------------
    2 => array(
        'name' => 'Wedding (wedding.garywallage.uk)',
        'staff' => array(
            'gary'       => array( 'name' => 'Gary David Wallage', 'email' => 'gary@garywallage.uk' ),
            'hma'        => array( 'name' => 'HMA - Hair & Makeup Artist', 'email' => 'hma@garywallage.uk' ),
            'second'     => array( 'name' => 'Second Photographer', 'email' => 'second@garywallage.uk' ),
            'photobooth' => array( 'name' => 'Photobooth Operator', 'email' => 'photobooth@garywallage.uk' ),
        ),
        'categories' => array( 'Consultations', 'Pre-Wedding', 'Wedding Day', 'Upgrades & Add-ons', 'Hair & Makeup', 'Wedding Packages' ),
        'atomics' => array(
            'W00' => array( 'title' => 'W00 - Wedding Planning Consultation', 'price' => 0.00, 'duration' => 2700, 'category' => 'Consultations', 'staff' => 'gary', 'color' => '#B08D55' ),
            'W01' => array( 'title' => 'W01 - Pre-Wedding / Engagement Session', 'price' => 395.00, 'duration' => 7200, 'category' => 'Pre-Wedding', 'staff' => 'gary', 'color' => '#B08D55' ),
            'W02' => array( 'title' => 'W02 - Half-Day Wedding Coverage', 'price' => 995.00, 'duration' => 14400, 'category' => 'Wedding Day', 'staff' => 'gary', 'color' => '#B08D55' ),
            'W03' => array( 'title' => 'W03 - Full-Day Wedding Coverage', 'price' => 1695.00, 'duration' => 28800, 'category' => 'Wedding Day', 'staff' => 'gary', 'color' => '#B08D55' ),
            'W04' => array( 'title' => 'W04 - Twilight & Evening Extension', 'price' => 350.00, 'duration' => 7200, 'category' => 'Wedding Day', 'staff' => 'gary', 'color' => '#B08D55' ),
            'W05' => array( 'title' => 'W05 - Second Photographer Coverage', 'price' => 450.00, 'duration' => 28800, 'category' => 'Upgrades & Add-ons', 'staff' => 'second', 'color' => '#C5A059' ),
            'W06' => array( 'title' => 'W06 - Drone Aerial Venue Coverage', 'price' => 295.00, 'duration' => 3600, 'category' => 'Upgrades & Add-ons', 'staff' => 'gary', 'color' => '#B08D55' ),
            'W07' => array( 'title' => 'W07 - Express 48-Hour Gallery Delivery', 'price' => 195.00, 'duration' => 900, 'category' => 'Upgrades & Add-ons', 'staff' => 'gary', 'color' => '#B08D55' ),
            'W08' => array( 'title' => 'W08 - Bespoke Heritage Leather Album (12x12)', 'price' => 550.00, 'duration' => 900, 'category' => 'Upgrades & Add-ons', 'staff' => 'gary', 'color' => '#B08D55' ),
            'W09' => array( 'title' => 'W09 - Parent Replica Album Pair (8x8)', 'price' => 395.00, 'duration' => 900, 'category' => 'Upgrades & Add-ons', 'staff' => 'gary', 'color' => '#B08D55' ),
            'W10' => array( 'title' => 'W10 - Handcrafted Folio Presentation Box', 'price' => 350.00, 'duration' => 900, 'category' => 'Upgrades & Add-ons', 'staff' => 'gary', 'color' => '#B08D55' ),
            'W11' => array( 'title' => 'W11 - Luxury Open-Air Photobooth Experience', 'price' => 495.00, 'duration' => 10800, 'category' => 'Upgrades & Add-ons', 'staff' => 'photobooth', 'color' => '#C5A059' ),
            'W12' => array( 'title' => 'W12 - Social Media Content Creator Coverage', 'price' => 395.00, 'duration' => 21600, 'category' => 'Upgrades & Add-ons', 'staff' => 'gary', 'color' => '#B08D55' ),
            'WH1' => array( 'title' => 'WH1 - Bridal Hair & Makeup Trial', 'price' => 195.00, 'duration' => 7200, 'category' => 'Hair & Makeup', 'staff' => 'hma', 'color' => '#C5A059' ),
            'WH2' => array( 'title' => 'WH2 - Bridal Hair & Makeup Wedding Day', 'price' => 350.00, 'duration' => 10800, 'category' => 'Hair & Makeup', 'staff' => 'hma', 'color' => '#C5A059' ),
            'WH3' => array( 'title' => 'WH3 - Bridesmaid / Mother Hair & Makeup', 'price' => 125.00, 'duration' => 3600, 'category' => 'Hair & Makeup', 'staff' => 'hma', 'color' => '#C5A059' ),
        ),
        'compounds' => array(
            'CW01' => array( 'title' => 'CW01 - The Registry & Micro-Wedding', 'price' => 650.00, 'category' => 'Wedding Packages', 'color' => '#B08D55', 'components' => array( 'W00', 'W02' ) ),
            'CW02' => array( 'title' => 'CW02 - The Classical Union', 'price' => 1695.00, 'category' => 'Wedding Packages', 'color' => '#B08D55', 'components' => array( 'W00', 'W03' ) ),
            'CW03' => array( 'title' => 'CW03 - The Complete Heritage', 'price' => 2450.00, 'category' => 'Wedding Packages', 'color' => '#B08D55', 'components' => array( 'W00', 'W01', 'W03', 'W08' ) ),
            'CW04' => array( 'title' => 'CW04 - The Estate Celebration', 'price' => 2895.00, 'category' => 'Wedding Packages', 'color' => '#B08D55', 'components' => array( 'W00', 'W01', 'W03', 'W05', 'W08', 'W11' ) ),
            'CW05' => array( 'title' => 'CW05 - The Grand Legacy', 'price' => 3650.00, 'category' => 'Wedding Packages', 'color' => '#B08D55', 'components' => array( 'W00', 'W01', 'W03', 'W04', 'W05', 'W06', 'W08', 'W09', 'W11' ) ),
            'CW06' => array( 'title' => 'CW06 - The Twilight Ceremony', 'price' => 1250.00, 'category' => 'Wedding Packages', 'color' => '#B08D55', 'components' => array( 'W00', 'W02', 'W04' ) ),
            'CW07' => array( 'title' => 'CW07 - The Two-Photographer Story', 'price' => 2095.00, 'category' => 'Wedding Packages', 'color' => '#B08D55', 'components' => array( 'W00', 'W03', 'W05' ) ),
            'CW08' => array( 'title' => 'CW08 - The Complete Morning', 'price' => 1995.00, 'category' => 'Wedding Packages', 'color' => '#B08D55', 'components' => array( 'W00', 'W03', 'WH2' ) ),
            'CW09' => array( 'title' => 'CW09 - The Bridal Heirloom', 'price' => 2795.00, 'category' => 'Wedding Packages', 'color' => '#B08D55', 'components' => array( 'W00', 'W01', 'W03', 'WH2', 'W08' ) ),
            'CW10' => array( 'title' => 'CW10 - The Destination / Multi-Day', 'price' => 3950.00, 'category' => 'Wedding Packages', 'color' => '#B08D55', 'components' => array( 'W00', 'W01', 'W03', 'W04', 'W05' ) ),
            'CW11' => array( 'title' => 'CW11 - The Intimate Gathering', 'price' => 1150.00, 'category' => 'Wedding Packages', 'color' => '#B08D55', 'components' => array( 'W00', 'W02', 'W10' ) ),
            'CW12' => array( 'title' => 'CW12 - The Modern Social Union', 'price' => 2050.00, 'category' => 'Wedding Packages', 'color' => '#B08D55', 'components' => array( 'W00', 'W03', 'W12' ) ),
            'CW13' => array( 'title' => 'CW13 - The Ultimate Heirloom', 'price' => 4450.00, 'category' => 'Wedding Packages', 'color' => '#B08D55', 'components' => array( 'W00', 'W01', 'W03', 'W04', 'W05', 'W06', 'W08', 'W09', 'W10', 'W11', 'WH2' ) ),
        )
    ),

    // -------------------------------------------------------------
    // SITE 3: family.garywallage.uk (Family & Generation)
    // -------------------------------------------------------------
    3 => array(
        'name' => 'Family (family.garywallage.uk)',
        'staff' => array(
            'gary' => array( 'name' => 'Gary David Wallage', 'email' => 'gary@garywallage.uk' ),
            'hma'  => array( 'name' => 'HMA - Hair & Makeup Artist', 'email' => 'hma@garywallage.uk' ),
        ),
        'categories' => array( 'Consultations', 'Family Sessions', 'Hair & Styling', 'Family Packages' ),
        'atomics' => array(
            'F00' => array( 'title' => 'F00 - Family Planning Consultation', 'price' => 0.00, 'duration' => 1800, 'category' => 'Consultations', 'staff' => 'gary', 'color' => '#2C5E3B' ),
            'F01' => array( 'title' => 'F01 - Classic Family Parkland Session', 'price' => 195.00, 'duration' => 3600, 'category' => 'Family Sessions', 'staff' => 'gary', 'color' => '#2C5E3B' ),
            'F02' => array( 'title' => 'F02 - Extended Generation Portrait', 'price' => 295.00, 'duration' => 7200, 'category' => 'Family Sessions', 'staff' => 'gary', 'color' => '#2C5E3B' ),
            'F03' => array( 'title' => 'F03 - At-Home Lifestyle Newborn & Family', 'price' => 245.00, 'duration' => 5400, 'category' => 'Family Sessions', 'staff' => 'gary', 'color' => '#2C5E3B' ),
            'FH1' => array( 'title' => 'FH1 - Hair & Makeup — Fresh & Natural', 'price' => 175.00, 'duration' => 5400, 'category' => 'Hair & Styling', 'staff' => 'hma', 'color' => '#7BB661' ),
            'FH2' => array( 'title' => 'FH2 - Family Refresh Touch-up', 'price' => 95.00, 'duration' => 2700, 'category' => 'Hair & Styling', 'staff' => 'hma', 'color' => '#7BB661' ),
        ),
        'compounds' => array(
            'CF01' => array( 'title' => 'CF01 - The Parkland Family Experience', 'price' => 329.00, 'category' => 'Family Packages', 'color' => '#2C5E3B', 'components' => array( 'FH1', 'F01' ) ),
            'CF02' => array( 'title' => 'CF02 - The Multi-Generation Heirloom', 'price' => 419.00, 'category' => 'Family Packages', 'color' => '#2C5E3B', 'components' => array( 'FH1', 'F02' ) ),
            'CF03' => array( 'title' => 'CF03 - The Welcomed Newborn', 'price' => 379.00, 'category' => 'Family Packages', 'color' => '#2C5E3B', 'components' => array( 'FH1', 'F03' ) ),
        )
    ),

    // -------------------------------------------------------------
    // SITE 4: fashion.garywallage.uk (Fashion & Commercial)
    // -------------------------------------------------------------
    4 => array(
        'name' => 'Fashion (fashion.garywallage.uk)',
        'staff' => array(
            'gary' => array( 'name' => 'Gary David Wallage', 'email' => 'gary@garywallage.uk' ),
            'hma'  => array( 'name' => 'HMA - Hair & Makeup Artist', 'email' => 'hma@garywallage.uk' ),
        ),
        'categories' => array( 'Consultations', 'Fashion & Editorial', 'Hair & Makeup', 'Production Packages' ),
        'atomics' => array(
            'FS00' => array( 'title' => 'FS00 - Commercial Campaign Briefing', 'price' => 0.00, 'duration' => 1800, 'category' => 'Consultations', 'staff' => 'gary', 'color' => '#1A1A1A' ),
            'FS01' => array( 'title' => 'FS01 - Studio Lookbook Session', 'price' => 350.00, 'duration' => 7200, 'category' => 'Fashion & Editorial', 'staff' => 'gary', 'color' => '#1A1A1A' ),
            'FS02' => array( 'title' => 'FS02 - Location Fashion Editorial', 'price' => 450.00, 'duration' => 10800, 'category' => 'Fashion & Editorial', 'staff' => 'gary', 'color' => '#1A1A1A' ),
            'FS03' => array( 'title' => 'FS03 - Designer Commercial Campaign', 'price' => 850.00, 'duration' => 21600, 'category' => 'Fashion & Editorial', 'staff' => 'gary', 'color' => '#1A1A1A' ),
            'FS04' => array( 'title' => 'FS04 - E-commerce Product & Apparel (Half-Day)', 'price' => 495.00, 'duration' => 14400, 'category' => 'Fashion & Editorial', 'staff' => 'gary', 'color' => '#1A1A1A' ),
            'FSH1' => array( 'title' => 'FSH1 - Hair & Makeup — Clean Commercial', 'price' => 195.00, 'duration' => 5400, 'category' => 'Hair & Makeup', 'staff' => 'hma', 'color' => '#D4AF37' ),
            'FSH2' => array( 'title' => 'FSH2 - Hair & Makeup — High-Concept Runway', 'price' => 295.00, 'duration' => 7200, 'category' => 'Hair & Makeup', 'staff' => 'hma', 'color' => '#D4AF37' ),
        ),
        'compounds' => array(
            'CFS01' => array( 'title' => 'CFS01 - The Lookbook Production', 'price' => 489.00, 'category' => 'Production Packages', 'color' => '#1A1A1A', 'components' => array( 'FSH1', 'FS01' ) ),
            'CFS02' => array( 'title' => 'CFS02 - The High-Fashion Campaign', 'price' => 669.00, 'category' => 'Production Packages', 'color' => '#1A1A1A', 'components' => array( 'FSH2', 'FS02' ) ),
            'CFS03' => array( 'title' => 'CFS03 - The Full Designer Launch', 'price' => 1049.00, 'category' => 'Production Packages', 'color' => '#1A1A1A', 'components' => array( 'FSH2', 'FS03' ) ),
        )
    ),

    // -------------------------------------------------------------
    // SITE 5: cosplay.garywallage.uk (Cosplay & Cinematic)
    // -------------------------------------------------------------
    5 => array(
        'name' => 'Cosplay (cosplay.garywallage.uk)',
        'staff' => array(
            'gary' => array( 'name' => 'Gary David Wallage', 'email' => 'gary@garywallage.uk' ),
            'hma'  => array( 'name' => 'HMA - Hair & Makeup Artist', 'email' => 'hma@garywallage.uk' ),
        ),
        'categories' => array( 'Consultations', 'Cosplay Sessions', 'Special FX & H&M', 'Cinematic Packages' ),
        'atomics' => array(
            'C00' => array( 'title' => 'C00 - Character & Concept Consultation', 'price' => 0.00, 'duration' => 1800, 'category' => 'Consultations', 'staff' => 'gary', 'color' => '#5B2C6F' ),
            'C01' => array( 'title' => 'C01 - Single Character Studio Session', 'price' => 195.00, 'duration' => 3600, 'category' => 'Cosplay Sessions', 'staff' => 'gary', 'color' => '#5B2C6F' ),
            'C02' => array( 'title' => 'C02 - Group / Guild Cosplay Session', 'price' => 325.00, 'duration' => 7200, 'category' => 'Cosplay Sessions', 'staff' => 'gary', 'color' => '#5B2C6F' ),
            'C03' => array( 'title' => 'C03 - Location / Cinematic Cosplay Session', 'price' => 295.00, 'duration' => 7200, 'category' => 'Cosplay Sessions', 'staff' => 'gary', 'color' => '#5B2C6F' ),
            'CH3' => array( 'title' => 'CH3 - Character Special FX Hair & Makeup', 'price' => 295.00, 'duration' => 7200, 'category' => 'Special FX & H&M', 'staff' => 'hma', 'color' => '#9B59B6' ),
        ),
        'compounds' => array(
            'CC01' => array( 'title' => 'CC01 - The Character Transformation', 'price' => 439.00, 'category' => 'Cinematic Packages', 'color' => '#5B2C6F', 'components' => array( 'CH3', 'C01' ) ),
            'CC02' => array( 'title' => 'CC02 - The Convention Portfolio', 'price' => 459.00, 'category' => 'Cinematic Packages', 'color' => '#5B2C6F', 'components' => array( 'C01', 'C02' ) ),
            'CC03' => array( 'title' => 'CC03 - The Epic Location Shoot', 'price' => 495.00, 'category' => 'Cinematic Packages', 'color' => '#5B2C6F', 'components' => array( 'CH3', 'C01', 'C03' ) ),
        )
    ),

    // -------------------------------------------------------------
    // SITE 6: glamour.garywallage.uk (Studio Glamour)
    // -------------------------------------------------------------
    6 => array(
        'name' => 'Glamour (glamour.garywallage.uk)',
        'staff' => array(
            'gary' => array( 'name' => 'Gary David Wallage', 'email' => 'gary@garywallage.uk' ),
            'hma'  => array( 'name' => 'HMA - Hair & Makeup Artist', 'email' => 'hma@garywallage.uk' ),
        ),
        'categories' => array( 'Consultations', 'Glamour Sessions', 'Hair & Makeup', 'Editorial Packages' ),
        'atomics' => array(
            'G00' => array( 'title' => 'G00 - Creative Direction Consultation', 'price' => 0.00, 'duration' => 1800, 'category' => 'Consultations', 'staff' => 'gary', 'color' => '#11110E' ),
            'G01' => array( 'title' => 'G01 - Studio Editorial Glamour Session', 'price' => 295.00, 'duration' => 5400, 'category' => 'Glamour Sessions', 'staff' => 'gary', 'color' => '#11110E' ),
            'G02' => array( 'title' => 'G02 - High-Fashion Lookbook Session', 'price' => 395.00, 'duration' => 9000, 'category' => 'Glamour Sessions', 'staff' => 'gary', 'color' => '#11110E' ),
            'G03' => array( 'title' => 'G03 - Vintage Hollywood / Retro Glamour', 'price' => 345.00, 'duration' => 7200, 'category' => 'Glamour Sessions', 'staff' => 'gary', 'color' => '#11110E' ),
            'GH1' => array( 'title' => 'GH1 - Hair & Makeup — Editorial Glow', 'price' => 195.00, 'duration' => 5400, 'category' => 'Hair & Makeup', 'staff' => 'hma', 'color' => '#B08D55' ),
            'GH2' => array( 'title' => 'GH2 - Hair & Makeup — High Fashion / Avant-Garde', 'price' => 275.00, 'duration' => 7200, 'category' => 'Hair & Makeup', 'staff' => 'hma', 'color' => '#B08D55' ),
        ),
        'compounds' => array(
            'CG01' => array( 'title' => 'CG01 - The Magazine Cover', 'price' => 439.00, 'category' => 'Editorial Packages', 'color' => '#11110E', 'components' => array( 'GH1', 'G01' ) ),
            'CG02' => array( 'title' => 'CG02 - The High Fashion Editorial', 'price' => 609.00, 'category' => 'Editorial Packages', 'color' => '#11110E', 'components' => array( 'GH2', 'G02' ) ),
            'CG03' => array( 'title' => 'CG03 - The Golden Age', 'price' => 569.00, 'category' => 'Editorial Packages', 'color' => '#11110E', 'components' => array( 'GH2', 'G03' ) ),
        )
    ),

    // -------------------------------------------------------------
    // SITE 7: boudoir.garywallage.uk (Boudoir & Dudoir)
    // -------------------------------------------------------------
    7 => array(
        'name' => 'Boudoir (boudoir.garywallage.uk)',
        'staff' => array(
            'gary' => array( 'name' => 'Gary David Wallage', 'email' => 'gary@garywallage.uk' ),
            'hma'  => array( 'name' => 'HMA - Hair & Makeup Artist', 'email' => 'hma@garywallage.uk' ),
        ),
        'categories' => array( 'Consultations', 'Boudoir & Dudoir Sessions', 'Hair & Makeup', 'Boutique Packages' ),
        'atomics' => array(
            'B00' => array( 'title' => 'B00 - Discovery & Styling Consultation', 'price' => 0.00, 'duration' => 1800, 'category' => 'Consultations', 'staff' => 'gary', 'color' => '#B08585' ),
            'B01' => array( 'title' => 'B01 - Classic Boudoir Studio Session', 'price' => 295.00, 'duration' => 5400, 'category' => 'Boudoir & Dudoir Sessions', 'staff' => 'gary', 'color' => '#B08585' ),
            'B02' => array( 'title' => 'B02 - Dudoir / Male Boudoir Session', 'price' => 295.00, 'duration' => 5400, 'category' => 'Boudoir & Dudoir Sessions', 'staff' => 'gary', 'color' => '#B08585' ),
            'B03' => array( 'title' => 'B03 - Couples Intimate Session', 'price' => 395.00, 'duration' => 7200, 'category' => 'Boudoir & Dudoir Sessions', 'staff' => 'gary', 'color' => '#B08585' ),
            'BH1' => array( 'title' => 'BH1 - Hair & Makeup — Soft Natural / Glow', 'price' => 195.00, 'duration' => 5400, 'category' => 'Hair & Makeup', 'staff' => 'hma', 'color' => '#C5A5A5' ),
            'BH2' => array( 'title' => 'BH2 - Hair & Makeup — Dramatic / Smokey Noir', 'price' => 245.00, 'duration' => 7200, 'category' => 'Hair & Makeup', 'staff' => 'hma', 'color' => '#C5A5A5' ),
        ),
        'compounds' => array(
            'CB01' => array( 'title' => 'CB01 - The Empowerment Experience', 'price' => 439.00, 'category' => 'Boutique Packages', 'color' => '#B08585', 'components' => array( 'BH1', 'B01' ) ),
            'CB02' => array( 'title' => 'CB02 - The Velvet Noir', 'price' => 489.00, 'category' => 'Boutique Packages', 'color' => '#B08585', 'components' => array( 'BH2', 'B01' ) ),
            'CB03' => array( 'title' => 'CB03 - The Intimate Duo', 'price' => 579.00, 'category' => 'Boutique Packages', 'color' => '#B08585', 'components' => array( 'BH1', 'B03' ) ),
        )
    )
);

foreach ( $catalogs as $blog_id => $cat_data ) {
    echo "\n>>> Ingesting Site {$blog_id}: {$cat_data['name']} <<<\n";
    switch_to_blog( $blog_id );
    $prefix = $wpdb->prefix;

    // 1. Staff Members
    $staff_map = array();
    foreach ( $cat_data['staff'] as $key => $sinfo ) {
        $existing = $wpdb->get_row( $wpdb->prepare( "SELECT id FROM {$prefix}bookly_staff WHERE full_name = %s OR email = %s LIMIT 1", $sinfo['name'], $sinfo['email'] ) );
        if ( $existing ) {
            $staff_id = $existing->id;
            $wpdb->update( "{$prefix}bookly_staff", array( 'full_name' => $sinfo['name'], 'email' => $sinfo['email'], 'visibility' => 'public' ), array( 'id' => $staff_id ) );
        } else {
            $wpdb->insert( "{$prefix}bookly_staff", array(
                'full_name' => $sinfo['name'],
                'email' => $sinfo['email'],
                'visibility' => 'public',
                'position' => 1
            ) );
            $staff_id = $wpdb->insert_id;
        }
        $staff_map[$key] = $staff_id;

        // Ensure schedule (Mon-Sun 09:00 - 20:00)
        for ( $day = 1; $day <= 7; $day++ ) {
            $has_sched = $wpdb->get_var( $wpdb->prepare( "SELECT id FROM {$prefix}bookly_staff_schedule_items WHERE staff_id = %d AND day_index = %d LIMIT 1", $staff_id, $day ) );
            if ( ! $has_sched ) {
                $wpdb->insert( "{$prefix}bookly_staff_schedule_items", array(
                    'staff_id' => $staff_id,
                    'day_index' => $day,
                    'start_time' => '09:00:00',
                    'end_time' => '20:00:00'
                ) );
            }
        }
        echo "  - Staff configured: {$sinfo['name']} (ID: {$staff_id})\n";
    }

    // 2. Categories
    $category_map = array();
    $pos = 1;
    foreach ( $cat_data['categories'] as $cname ) {
        $existing_cat = $wpdb->get_row( $wpdb->prepare( "SELECT id FROM {$prefix}bookly_categories WHERE name = %s LIMIT 1", $cname ) );
        if ( $existing_cat ) {
            $cat_id = $existing_cat->id;
        } else {
            $wpdb->insert( "{$prefix}bookly_categories", array( 'name' => $cname, 'position' => $pos ) );
            $cat_id = $wpdb->insert_id;
        }
        $category_map[$cname] = $cat_id;
        $pos++;
    }

    // 3. Atomic Services
    $atomic_service_map = array();
    foreach ( $cat_data['atomics'] as $code => $sdata ) {
        $cat_id = isset( $category_map[$sdata['category']] ) ? $category_map[$sdata['category']] : null;
        $staff_id = isset( $staff_map[$sdata['staff']] ) ? $staff_map[$sdata['staff']] : reset( $staff_map );

        $existing_svc = $wpdb->get_row( $wpdb->prepare( "SELECT id FROM {$prefix}bookly_services WHERE title = %s OR title LIKE %s LIMIT 1", $sdata['title'], $code . ' %' ) );
        if ( $existing_svc ) {
            $service_id = $existing_svc->id;
            $wpdb->update( "{$prefix}bookly_services", array(
                'title' => $sdata['title'],
                'duration' => $sdata['duration'],
                'price' => $sdata['price'],
                'category_id' => $cat_id,
                'color' => $sdata['color'],
                'type' => 'simple',
                'visibility' => 'public'
            ), array( 'id' => $service_id ) );
        } else {
            $wpdb->insert( "{$prefix}bookly_services", array(
                'title' => $sdata['title'],
                'duration' => $sdata['duration'],
                'price' => $sdata['price'],
                'category_id' => $cat_id,
                'color' => $sdata['color'],
                'type' => 'simple',
                'visibility' => 'public',
                'position' => 10
            ) );
            $service_id = $wpdb->insert_id;
        }
        $atomic_service_map[$code] = $service_id;

        // Bind Staff Service
        $has_staff_svc = $wpdb->get_var( $wpdb->prepare( "SELECT id FROM {$prefix}bookly_staff_services WHERE staff_id = %d AND service_id = %d LIMIT 1", $staff_id, $service_id ) );
        if ( ! $has_staff_svc ) {
            $wpdb->insert( "{$prefix}bookly_staff_services", array(
                'staff_id' => $staff_id,
                'service_id' => $service_id,
                'price' => $sdata['price'],
                'capacity_min' => 1,
                'capacity_max' => 1
            ) );
        } else {
            $wpdb->update( "{$prefix}bookly_staff_services", array( 'price' => $sdata['price'] ), array( 'id' => $has_staff_svc ) );
        }
        echo "  - Atomic service: [{$code}] {$sdata['title']} (£{$sdata['price']}) -> ID: {$service_id}\n";
    }

    // 4. Compound Services
    foreach ( $cat_data['compounds'] as $code => $cdata ) {
        $cat_id = isset( $category_map[$cdata['category']] ) ? $category_map[$cdata['category']] : null;

        // Calculate total duration from components
        $total_duration = 0;
        $component_ids = array();
        foreach ( $cdata['components'] as $comp_code ) {
            if ( isset( $atomic_service_map[$comp_code] ) ) {
                $comp_id = $atomic_service_map[$comp_code];
                $component_ids[] = $comp_id;
                $comp_dur = $wpdb->get_var( $wpdb->prepare( "SELECT duration FROM {$prefix}bookly_services WHERE id = %d", $comp_id ) );
                $total_duration += intval( $comp_dur );
            }
        }

        $existing_cmp = $wpdb->get_row( $wpdb->prepare( "SELECT id FROM {$prefix}bookly_services WHERE title = %s OR title LIKE %s LIMIT 1", $cdata['title'], $code . ' %' ) );
        if ( $existing_cmp ) {
            $compound_id = $existing_cmp->id;
            $wpdb->update( "{$prefix}bookly_services", array(
                'title' => $cdata['title'],
                'duration' => $total_duration ?: 3600,
                'price' => $cdata['price'],
                'category_id' => $cat_id,
                'color' => $cdata['color'],
                'type' => 'compound',
                'visibility' => 'public'
            ), array( 'id' => $compound_id ) );
        } else {
            $wpdb->insert( "{$prefix}bookly_services", array(
                'title' => $cdata['title'],
                'duration' => $total_duration ?: 3600,
                'price' => $cdata['price'],
                'category_id' => $cat_id,
                'color' => $cdata['color'],
                'type' => 'compound',
                'visibility' => 'public',
                'position' => 1
            ) );
            $compound_id = $wpdb->insert_id;
        }

        // Link Sub-Services
        $wpdb->delete( "{$prefix}bookly_sub_services", array( 'service_id' => $compound_id ) );
        $sub_pos = 1;
        foreach ( $component_ids as $sub_id ) {
            $wpdb->insert( "{$prefix}bookly_sub_services", array(
                'type' => 'service',
                'service_id' => $compound_id,
                'sub_service_id' => $sub_id,
                'position' => $sub_pos
            ) );
            $sub_pos++;
        }

        // Bind all active staff to compound service
        foreach ( $staff_map as $sid ) {
            $has_bind = $wpdb->get_var( $wpdb->prepare( "SELECT id FROM {$prefix}bookly_staff_services WHERE staff_id = %d AND service_id = %d LIMIT 1", $sid, $compound_id ) );
            if ( ! $has_bind ) {
                $wpdb->insert( "{$prefix}bookly_staff_services", array(
                    'staff_id' => $sid,
                    'service_id' => $compound_id,
                    'price' => $cdata['price'],
                    'capacity_min' => 1,
                    'capacity_max' => 1
                ) );
            }
        }

        echo "  - Compound package: [{$code}] {$cdata['title']} (£{$cdata['price']}) [Components: " . implode( ', ', $cdata['components'] ) . "] -> ID: {$compound_id}\n";
    }

    restore_current_blog();
}

echo "\n=== All 7 Sub-Sites Successfully Ingested! ===\n";
