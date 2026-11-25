from manim import *

# Consistent color palette across all scenes
BG_COLOR = "#0F172A"        # Clean deep slate
CARD_BG = "#1E293B"         # Subtle panel background
TEXT_COLOR = "#F8FAFC"      # Off-white text
MUTED_COLOR = "#94A3B8"     # Secondary labels / axes

F_COLOR = "#38BDF8"         # Sky blue for f(x) and df
G_COLOR = "#34D399"         # Emerald green for g(x) and dg
DF_STRIP_COLOR = "#60A5FA"  # Right strip: g(x) * df
DG_STRIP_COLOR = "#4ADE80"  # Top strip: f(x) * dg
CORNER_COLOR = "#F43F5E"    # Coral red for vanishing corner df * dg & errors
PROD_COLOR = "#FBBF24"      # Amber gold for product h(x) = f(x)g(x)


def make_section_header(title_text: str) -> VGroup:
    """Creates a clean top banner with an underline."""
    title = Text(title_text, font_size=32, color=TEXT_COLOR, weight=BOLD)
    title.to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.6)
    line = Line(
        title.get_left() + DOWN * 0.25,
        title.get_left() + RIGHT * 12.8 + DOWN * 0.25,
        color=MUTED_COLOR,
        stroke_width=1.5,
        stroke_opacity=0.5,
    )
    return VGroup(title, line)


def wrap_in_card(mobject: Mobject, buff: float = 0.28, stroke_color=MUTED_COLOR) -> VGroup:
    """Wraps a mobject inside a clean dark rounded card."""
    card = SurroundingRectangle(
        mobject,
        buff=buff,
        corner_radius=0.12,
        color=stroke_color,
        stroke_width=1.8,
        fill_color=CARD_BG,
        fill_opacity=0.9,
    )
    return VGroup(card, mobject)