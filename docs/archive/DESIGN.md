# Visual Design Guide (moved)

This file has been moved to docs/design/visual-design.md. The docs/ version will be the active one — this file remains as a historical copy during the migration.

---

# Visual Design Guide

## Color Scheme

### Primary Colors
- **Primary Blue**: `#0d6efd` (Bootstrap primary)
- **Success Green**: `#198754` (Bootstrap success)
- **Info Cyan**: `#0dcaf0` (Bootstrap info)
- **Warning Yellow**: `#ffc107` (Bootstrap warning)
- **Danger Red**: `#dc3545` (Bootstrap danger)

### Neutral Colors
- **Dark Text**: `#212529`
- **Muted Text**: `#6c757d`
- **Light Background**: `#f8f9fa`
- **White**: `#ffffff`

### Diff Colors
- **Added Lines**: `#d4edda` (light green background)
- **Removed Lines**: `#f8d7da` (light red background)
- **Context Lines**: `#495057` (gray text)

## Typography

### Font Family
- **Default**: System fonts stack
- **Monospace**: 'Courier New', monospace (for diffs)

### Font Sizes
- **H1**: 2.5rem (40px)
- **H2**: 2rem (32px)
- **H3**: 1.75rem (28px)
- **H4**: 1.5rem (24px)
- **H5**: 1.25rem (20px)
- **Body**: 1rem (16px)

## Component Styles

### Cards
```css
.card {
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
```

### Buttons
- **Primary**: Blue with white text
- **Success**: Green with white text
- **Outline**: Border only, fills on hover
- **Large**: `btn-lg` class for emphasis

### Forms
- **Inputs**: Rounded corners, focus state with blue outline
- **Labels**: Bold, above inputs
- **Validation**: Red border and text for errors
- **Help Text**: Muted color below inputs

### Navigation
- **Navbar**: Dark blue background
- **Active Link**: White text, no underline
- **Hover**: Slightly lighter blue
- **Dropdown**: White background with shadow

## Layout Patterns

### Page Structure
```
┌─────────────────────────────────────┐
│         Navigation Bar               │
├─────────────────────────────────────┤
│                                      │
│         Page Header (h2)             │
│         Subtitle (muted)             │
│                                      │
├─────────────────────────────────────┤
│                                      │
│         Main Content                 │
│         (Cards, Forms, etc.)         │
│                                      │
├─────────────────────────────────────┤
│            Footer                    │
└─────────────────────────────────────┘
```

### Grid System
- **Container**: Centered, max-width responsive
- **Row**: Flexbox row
- **Columns**: 12-column grid
  - Desktop: Full width columns
  - Tablet: 2 columns per row
  - Mobile: 1 column per row

### Spacing
- **Section Margins**: `mt-4` (1.5rem top margin)
- **Card Spacing**: `mb-3` (1rem bottom margin)
- **Content Padding**: `p-3` to `p-4` (1rem to 1.5rem)

## Icons

### Bootstrap Icons Used
- `bi-tools` - Platform logo
- `bi-speedometer2` - Dashboard
- `bi-bar-chart-line` - Analytics
- `bi-file-earmark-diff` - Diff Checker
- `bi-clock-history` - History
- `bi-person-circle` - User profile
- `bi-box-arrow-in-right` - Login
- `bi-person-plus` - Register
- `bi-puzzle` - Modular features
- `bi-arrow-right-circle` - Action buttons

### Icon Usage
- **Size**: Default 1rem, larger in headers
- **Color**: Inherits from parent or custom
- **Spacing**: `me-2` class for right margin

## Responsive Breakpoints

### Bootstrap Breakpoints
- **xs**: < 576px (phones)
- **sm**: ≥ 576px (phones landscape)
- **md**: ≥ 768px (tablets)
- **lg**: ≥ 992px (desktops)
- **xl**: ≥ 1200px (large desktops)
- **xxl**: ≥ 1400px (extra large)

### Mobile Adaptations
- Navigation collapses to hamburger menu
- Cards stack vertically
- Forms full width
- Charts maintain aspect ratio
- Text sizes adjust

## Page-Specific Designs

### Homepage (index.html)
- **Hero Section**: Jumbotron with title and CTA buttons
- **Feature Cards**: 3-column grid on desktop
- **Icons**: Large display-1 size
- **Colors**: Mix of primary, success, and info

### Dashboard (dashboard.html)
- **Tool Cards**: Grid of available tools
- **Recent Activity**: Table with timestamps
- **Empty State**: Helpful message when no activity

### Analytics (analytics.html)
- **Chart Cards**: Three separate cards
- **Chart Canvas**: Responsive Chart.js
- **Headers**: Colored backgrounds (primary, success, info)
- **Hover Effects**: Tooltips on data points

### Diff Checker (diff_checker.html)
- **Split Layout**: Two columns for texts
- **Compare Button**: Large, centered
- **Results**: Monospace font with color coding
- **History Link**: Prominent button

### Diff History (diff_history.html)
- **Table Layout**: Sortable columns
- **Actions**: View button per row
- **Empty State**: Helpful message with link

### Login/Register (auth/)
- **Centered Card**: Single column, max 500px
- **Form Fields**: Stacked vertically
- **Submit Button**: Full width
- **Links**: Centered below form

## Animation & Transitions

### Hover Effects
```css
transition: all 0.2s ease-in-out;
```

### Card Hover
- Lift up 5px
- Increase shadow
- Smooth transition

### Button Hover
- Slightly darker background
- Maintain shape and size

### Link Hover
- Underline appears
- Color slightly darker

## Accessibility

### Color Contrast
- Text on background: Minimum 4.5:1 ratio
- Large text: Minimum 3:1 ratio
- Links: Distinguishable from text

### Focus States
- Visible outline on keyboard focus
- Blue outline for inputs
- Consistent across all interactive elements

### Form Labels
- Always associated with inputs
- Visible (not just placeholders)
- Clear error messages

### ARIA Labels
- Screen reader friendly
- Semantic HTML
- Proper heading hierarchy

## Browser Compatibility

### Tested On
- Chrome 120+
- Firefox 120+
- Safari 17+
- Edge 120+

### Fallbacks
- CSS Grid with flexbox fallback
- Modern features with polyfills
- Progressive enhancement

## Dark Mode (Future)

### Proposed Colors
```css
/* Dark mode variables */
--bg-dark: #1a1a1a;
--text-dark: #e0e0e0;
--card-dark: #2d2d2d;
--border-dark: #404040;
```

### Implementation
```css
@media (prefers-color-scheme: dark) {
  /* Dark mode styles */
}
```

## Custom CSS Classes

### Diff Output
```css
.diff-output {
  font-family: 'Courier New', monospace;
  background: #f8f9fa;
  padding: 15px;
  border-radius: 5px;
  overflow-x: auto;
  max-height: 600px;
}

.diff-add { background: #d4edda; color: #155724; }
.diff-remove { background: #f8d7da; color: #721c24; }
.diff-context { color: #495057; }
```

### Jumbotron
```css
.jumbotron {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 3rem;
}
```

## Print Styles

### Hidden on Print
- Navigation bar
- Footer
- Action buttons
- Sidebar (if added)

### Visible on Print
- Content area
- Charts (static image)
- Text content
- Headers

## Performance

### CSS Loading
- Bootstrap from CDN (cached)
- Custom CSS minified
- Critical CSS inline (future)

### Font Loading
- System fonts (no download)
- Icon fonts from CDN

### Image Optimization
- No heavy images currently
- SVG for logos (future)
- Lazy loading (future)

## Maintenance

### Adding New Colors
1. Define in CSS variables
2. Use consistently
3. Check contrast ratios
4. Test in dark mode (future)

### Adding New Components
1. Follow Bootstrap patterns
2. Use existing utilities
3. Add custom CSS only if needed
4. Document in this guide

### Updating Dependencies
1. Test Bootstrap updates
2. Check icon availability
3. Verify Chart.js compatibility
4. Update documentation

## Resources

- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- [Bootstrap Icons](https://icons.getbootstrap.com/)
- [Chart.js Docs](https://www.chartjs.org/docs/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
