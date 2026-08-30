# 🎨 Handover & Live Design Directives for Claude (Aesthetic & Editorial Lead)

**Version**: 3.0 (Verified Against Live Child Theme CSS)  
**Lead DevOps / Infrastructure**: Antigravity  
**Lead Aesthetic & Editorial Editor**: Claude  

---

## 🎨 1. Live Color Token Reference Table (Exact Live CSS Parity)

| Sub-Site | Domain | Primary (`--brand-accent`) | Accent / Gold (`--brand-gold-light`) | Background (`--brand-bg`) | Atmosphere |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Wedding** | `wedding.garywallage.uk` | `#B08D55` (Champagne Gold) | `#C5A059` (Light Gold) | `#FFFFFF` (Pure White) | Timeless, editorial, documentary luxury |
| **Boudoir** | `boudoir.garywallage.uk` | `#B08585` (Dusty Rose) | `#C5A5A5` (Rose Mist) | `#FAF7F5` (Warm Alabaster) | Soft, intimate, empowering |
| **Glamour** | `glamour.garywallage.uk` | `#B08D55` (Burnished Gold) | `#D4AF37` (Metallic Gold) | `#11110E` (Studio Onyx) | High-contrast, moody couture |
| **Family** | `family.garywallage.uk` | `#2C5E3B` (Forest Green) | `#7BB661` (Meadow Green) | `#F7F9F6` (Meadow Alabaster) | Natural, warm, generational |
| **Fashion** | `fashion.garywallage.uk` | `#1A1A1A` (Graphite Black) | `#D4AF37` (Metallic Gold) | `#F8F8F8` (Studio Gray) | High-fashion editorial, clean, sharp |
| **Cosplay** | `cosplay.garywallage.uk` | `#5B2C6F` (Imperial Purple) | `#9B59B6` (Neon Amethyst) | `#0F0A17` (Cosmic Void) | Cinematic character, sci-fi neon cyan |
| **Portraits** | `staging.garywallage.uk` | `#1A365D` (Executive Navy) | `#4A90E2` (Sky Blue) | `#F5F7FA` (Crisp Platinum) | Corporate authority, headshots |

---

## 📐 2. Structural & Layout Mandates

1. **10-80-10 Rule**: Desktop containers use `max-width: 1200px; padding: 0 10%; margin: 0 auto;`.
2. **Never-Crop Rule**: Portrait orientation photography must never be forced into landscape letterbox crops.
3. **Template Parity**:
   * `/services-packages` ➔ `page-services.php` (Interleaved package and individual grids).
   * Individual Service Pages ➔ `page-service-detail.php` (66/33 editorial overview + sticky investment plaque).
