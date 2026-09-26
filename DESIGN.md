---
name: Tactile Modernist OS
colors:
  surface: '#f9f9f9'
  surface-dim: '#dadada'
  surface-bright: '#f9f9f9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3f3'
  surface-container: '#eeeeee'
  surface-container-high: '#e8e8e8'
  surface-container-highest: '#e2e2e2'
  on-surface: '#1a1c1c'
  on-surface-variant: '#46464b'
  inverse-surface: '#2f3131'
  inverse-on-surface: '#f0f1f1'
  outline: '#76777b'
  outline-variant: '#c7c6cb'
  surface-tint: '#5e5e62'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#1b1b1f'
  on-primary-container: '#848387'
  inverse-primary: '#c7c6ca'
  secondary: '#566500'
  on-secondary: '#ffffff'
  secondary-container: '#d3ef51'
  on-secondary-container: '#5b6b00'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#141e18'
  on-tertiary-container: '#7c867f'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e3e2e6'
  primary-fixed-dim: '#c7c6ca'
  on-primary-fixed: '#1b1b1f'
  on-primary-fixed-variant: '#46464a'
  secondary-fixed: '#d3ef51'
  secondary-fixed-dim: '#b8d236'
  on-secondary-fixed: '#181e00'
  on-secondary-fixed-variant: '#404c00'
  tertiary-fixed: '#dae5dc'
  tertiary-fixed-dim: '#bec9c1'
  on-tertiary-fixed: '#141e18'
  on-tertiary-fixed-variant: '#3f4943'
  background: '#f9f9f9'
  on-background: '#1a1c1c'
  surface-variant: '#e2e2e2'
typography:
  headline-xl:
    fontFamily: Plus Jakarta Sans
    fontSize: 44px
    fontWeight: '700'
    lineHeight: 52px
    letterSpacing: -0.03em
  headline-xl-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 30px
    fontWeight: '700'
    lineHeight: 38px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.025em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0em
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.04em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  gutter: 1.25rem
  gutter-desktop: 1.5rem
  margin: 0.75rem
  margin-desktop: 1.25rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.875rem
  space-lg: 1.25rem
  space-xl: 2rem
---

## Brand & Style

The design system projects high-order operational intelligence, spatial calm, and physical software precision. Engineered for an advanced placement and orchestration platform, the interface balances an architectural, utilitarian ethos with hyper-contemporary warmth. It delivers the focused sensory feedback of physical industrial hardware translated into a fluid digital operating system.

The design movement synthesizes **Tactile Minimalism** and **Modern Skeuomorphic Realism**. Rather than flat, sterile SaaS dashboards, the interface uses an atmospheric canvas of muted sage-slate, deeply radiused floating porcelain surfaces, tactile dark matte islands, and vivid chartreuse micro-accents. The emotional response is one of supreme competence, unhurried focus, and surgical clarity.

## Colors

The palette operates via four distinct tonal planes:

- **Atmospheric Outer Canvas (`#a1aca4`)**: A dusty, natural sage-slate that envelopes the viewport, giving the software an organic, physical perimeter that softens screen fatigue.
- **Porcelain Work Surface (`#fbfbfb` / `#ffffff`)**: Crisp, elevated primary viewports with pure white inner cards (`#ffffff`) and faint zinc structural borders (`rgba(18, 19, 22, 0.06)`).
- **Matte Charcoal Structural Elements (`#121316`, `#18191c`, `#1c1e22`)**: Dense, deep graphite used for the primary navigation dock, persistent command capsules, key action states, and high-impact micro-surfaces.
- **Electric Chartreuse Accent (`#d6f254`, `#e8fa8c`)**: An ultra-vivid optical lime deployed sparingly for primary action triggers, positive placement thresholds, system health, and active selection states.

### Secondary Functional Accents
- **Muted Sage Tint**: `#8d9990` for secondary canvas borders and ghost dividers.
- **Surface Elevation Dark**: `#26292f` for hover states within dark matte surfaces.
- **Muted Indicator Fill**: `#e4e8ea` for empty tracks in progress bars and capsule meters.
- **Success Tone**: `#22c55e` (used strictly for validated statuses where chartreuse is non-standard).
- **Warning & Danger**: Amber `#f59e0b` and Crimson `#ef4444`, adapted with high-contrast charcoal text pairing.

## Typography

The typographical structure utilizes **Plus Jakarta Sans** for structural, expressive, and conversational clarity, paired with **JetBrains Mono** for technical telemetry, key metrics, status indicators, and operational metadata.

- **Headlines**: Tight letter-spacing with deliberate, rounded geometry gives headlines a tech-forward architectural presence without mechanical stiffness.
- **Labels & Numbers**: Numerical data, status capsules, IDs, and percentage allocations always render in `JetBrains Mono` to emphasize deterministic computation and precise alignment.
- **Inline Pill Embeds**: Badges, status markers, and operational tags maintain vertical parity with typography line heights, avoiding layout jitter.

## Layout & Spacing

The interface embraces a "viewport-in-canvas" approach:

- **Desktop (1024px+)**: The outermost frame is a full-bleed muted sage/slate backdrop (`#a1aca4`) with a fixed padding (`margin-desktop: 1.25rem`). Sitting within this field are two principal units:
  1. An independent vertical charcoal navigation dock (`width: 72px`).
  2. The primary application workspace: an expansive, unified `#fbfbfb` floating card with deep `2rem` rounded corners (`rounded-3xl`) holding the entire main dashboard, toolbars, and contextual panels.
- **Tablet / Mobile (<1024px)**: Outer canvas margins diminish to `0.75rem`. The vertical dock collapses into a floating horizontal bottom capsule island. Main workspace retains maximum corner curvature of `1.25rem` to optimize usable screen estate.
- **Content Grid**: Inside the porcelain work area, elements adhere to a 12-column layout with fluid gutters (`gutter: 1.25rem`) and modular component padding anchored strictly to the `0.25rem` scale.

## Elevation & Depth

Visual hierarchy uses physical stacking, deliberate contrast, and deep atmospheric shadows:

1. **Outer Slate Canvas**: Baseline level zero. Recessed, quiet, and matte.
2. **Porcelain Application Shell**: Floating over the canvas with an extra-diffused low-elevation shadow:
   `0 20px 48px -12px rgba(18, 19, 22, 0.14), 0 1px 2px rgba(18, 19, 22, 0.04)`.
3. **Internal Nested Cards**: Crisp pure-white (`#ffffff`) surfaces positioned over the `#fbfbfb` main floor, outlined with a hairline border: `1px solid rgba(18, 19, 22, 0.05)`, cast with a soft ambient shadow `0 2px 8px rgba(18, 19, 22, 0.03)`.
4. **Charcoal Navigation Dock & Control Pods**: High-contrast matte charcoal surfaces (`#121316`) that cast deep directional drop-shadows:
   `0 16px 36px -6px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(255, 255, 255, 0.06) inset`.
5. **Chartreuse Accents & Focus States**: Electric lime elements emit an energetic ambient glow when active: `0 0 20px rgba(214, 242, 84, 0.38)`.

## Shapes

The design language is defined by deliberate pill geometries, soft radii, and dramatic outer curves (`roundedness: 3`):

- **Main Workspaces**: `32px` (`rounded-3xl`) for the primary floating application container.
- **Primary Interactive Cards**: `20px` to `24px` radius with soft interior nesting.
- **Pills, Badges, Dock Items, and Action Buttons**: Completely rounded pill forms (`9999px` / `rounded-full`).
- **Capsule Meters & Range Bars**: Fully rounded tracks and segmented inner bars.

## Components

### Buttons
- **Primary Action**: Electric lime background (`#d6f254`), high-contrast charcoal text (`#121316`), pill-shaped (`rounded-full`), `h-11`, horizontal padding `1.25rem`. Subtle tactile active state (`scale(0.98)`).
- **Secondary Charcoal**: Matte charcoal surface (`#1c1e22`), white text, faint white inner rim (`border border-white/10`), pill-shaped.
- **Ghost / Neutral**: Soft zinc background (`rgba(18, 19, 22, 0.04)`), dark charcoal text, transitioning to `#e8fa8c` on hover.

### Navigation Dock
- **Vertical Dock**: Fixed `#121316` matte housing, `72px` wide, full container height or floating pill format.
- **Icons**: Enclosed in circular or squircle pods (`44px × 44px`), soft grey idle state (`#8a8f98`), turning `#d6f254` with white/black icon treatment when active. Contains an animated chartreuse indicator pip.

### Cards & Content Surfaces
- **Porcelain Metric Tiles**: `#ffffff` background with `20px` border-radius, thin light border (`#eceeed`), inner padding `1.25rem`.
- **Charcoal Feature Cards**: Alternating high-priority pods featuring dark matte fills (`#18191c`), pale grey labels, and chartreuse callouts.

### Capsule Bar Meters & Gauges
- **Track**: Muted recessed track (`#ecefed`), `8px` or `12px` height, `rounded-full`.
- **Fill**: Solid electric lime (`#d6f254`) or segmented pills showing status increments.
- **Inline Pill Badges**: Integrated alongside metrics; containing an emoji or monochrome icon + mono percentage/score (e.g., `⚡ 98.4%`), framed in a `border border-black/5` capsule.

### Inputs & Form Fields
- **Container**: `h-12`, pill-shaped or soft-pill (`16px`), background `#f3f4f6`, zero hard exterior borders, faint focus ring using `#d6f254` (`ring-2 ring-[#d6f254]`).
- **Typography**: Input text uses `Plus Jakarta Sans`, metadata and search shortcut chips render in `JetBrains Mono`.

### Checkboxes & Segmented Controls
- **Segmented Switch**: Capsule track in `#e9ece9` containing a sliding active pill in pure white or `#121316` with smooth spring transitions.
- **Checkboxes**: Smooth squircle (`rounded-lg`) checking into full electric lime `#d6f254` with a dark charcoal check icon.