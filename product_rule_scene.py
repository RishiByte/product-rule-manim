from manim import *
import numpy as np
from helpers import (
    BG_COLOR,
    TEXT_COLOR,
    MUTED_COLOR,
    F_COLOR,
    G_COLOR,
    DF_STRIP_COLOR,
    DG_STRIP_COLOR,
    CORNER_COLOR,
    PROD_COLOR,
    make_section_header,
    wrap_in_card,
)

config.background_color = BG_COLOR


class BaseProductRuleScene(Scene):
    """Shared acts so you can render each part individually or all together."""

    def construct_intro(self):
        title = Text(
            "The Product Rule of Differentiation",
            font_size=44,
            color=TEXT_COLOR,
            weight=BOLD,
        )
        subtitle = Text(
            "Geometric Proof & Specific Example",
            font_size=26,
            color=MUTED_COLOR,
        )
        header_group = VGroup(title, subtitle).arrange(DOWN, buff=0.25)

        self.play(FadeIn(title, shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(subtitle), run_time=0.8)
        self.wait(1.0)
        self.play(header_group.animate.to_edge(UP, buff=0.5))

        # Pose the common misconception
        prod_eq = MathTex(
            r"h(x)", r"=", r"f(x)", r"\cdot", r"g(x)",
            font_size=46,
        )
        prod_eq[0].set_color(PROD_COLOR)
        prod_eq[2].set_color(F_COLOR)
        prod_eq[4].set_color(G_COLOR)

        question = MathTex(
            r"\text{Does } h'(x) = f'(x) \cdot g'(x)\text{ ?}",
            font_size=40,
            color=TEXT_COLOR,
        )

        ex_intro = MathTex(
            r"\text{Test with } f(x) = x^2 \text{ and } g(x) = x + 2",
            font_size=34,
            color=MUTED_COLOR,
        )
        wrong_try = MathTex(
            r"f'(x) \cdot g'(x) = (2x)(1) = 2x",
            font_size=36,
            color=CORNER_COLOR,
        )
        verdict = Text(
            "Wait—let's see what actually happens geometrically!",
            font_size=28,
            color=PROD_COLOR,
        )

        body = VGroup(prod_eq, question, ex_intro, wrong_try, verdict).arrange(
            DOWN, buff=0.45
        )
        body.next_to(header_group, DOWN, buff=0.6)

        self.play(Write(prod_eq), run_time=1.2)
        self.wait(0.8)
        self.play(Write(question), run_time=1.2)
        self.wait(1.0)
        self.play(FadeIn(ex_intro, shift=UP * 0.15))
        self.play(Write(wrong_try), run_time=1.2)
        self.wait(1.0)
        self.play(FadeIn(verdict, shift=UP * 0.15))
        self.wait(2.0)

    def construct_geometric_proof(self):
        header = make_section_header("1. Visual Derivation: Area of a Growing Rectangle")
        self.play(FadeIn(header), run_time=0.8)

        # Anchor bottom-left corner so growth moves cleanly RIGHT and UP
        base_bl = np.array([-5.2, -1.7, 0.0])
        w_base = 2.6
        h_base = 2.0

        base_rect = Rectangle(
            width=w_base,
            height=h_base,
            color=PROD_COLOR,
            stroke_width=2.5,
            fill_color=PROD_COLOR,
            fill_opacity=0.22,
        ).move_to(base_bl + RIGHT * (w_base / 2) + UP * (h_base / 2))

        brace_f = Brace(base_rect, DOWN, buff=0.15, color=F_COLOR)
        lbl_f = MathTex(r"f(x)", font_size=30, color=F_COLOR).next_to(brace_f, DOWN, buff=0.12)

        brace_g = Brace(base_rect, LEFT, buff=0.15, color=G_COLOR)
        lbl_g = MathTex(r"g(x)", font_size=30, color=G_COLOR).next_to(brace_g, LEFT, buff=0.12)

        area_lbl = MathTex(r"A = f(x)g(x)", font_size=28, color=PROD_COLOR).move_to(
            base_rect.get_center()
        )

        self.play(Create(base_rect), run_time=1.0)
        self.play(
            GrowFromCenter(brace_f),
            Write(lbl_f),
            GrowFromCenter(brace_g),
            Write(lbl_g),
            Write(area_lbl),
            run_time=1.3,
        )
        self.wait(1.0)

        # ValueTracker controls step dx -> 0
        dx = ValueTracker(1.0)

        right_strip = always_redraw(
            lambda: Rectangle(
                width=0.95 * dx.get_value(),
                height=h_base,
                color=DF_STRIP_COLOR,
                stroke_width=2,
                fill_color=DF_STRIP_COLOR,
                fill_opacity=0.55,
            ).move_to(
                base_bl
                + RIGHT * (w_base + (0.95 * dx.get_value()) / 2)
                + UP * (h_base / 2)
            )
        )

        top_strip = always_redraw(
            lambda: Rectangle(
                width=w_base,
                height=0.70 * dx.get_value(),
                color=DG_STRIP_COLOR,
                stroke_width=2,
                fill_color=DG_STRIP_COLOR,
                fill_opacity=0.55,
            ).move_to(
                base_bl
                + RIGHT * (w_base / 2)
                + UP * (h_base + (0.70 * dx.get_value()) / 2)
            )
        )

        corner_box = always_redraw(
            lambda: Rectangle(
                width=0.95 * dx.get_value(),
                height=0.70 * dx.get_value(),
                color=CORNER_COLOR,
                stroke_width=2,
                fill_color=CORNER_COLOR,
                fill_opacity=0.80,
            ).move_to(
                base_bl
                + RIGHT * (w_base + (0.95 * dx.get_value()) / 2)
                + UP * (h_base + (0.70 * dx.get_value()) / 2)
            )
        )

        # Labels when dx = 1.0 (faded cleanly before shrinking dx)
        brace_df = Brace(right_strip, DOWN, buff=0.15, color=F_COLOR)
        lbl_df = MathTex(r"\Delta f", font_size=28, color=F_COLOR).next_to(brace_df, DOWN, buff=0.12)

        brace_dg = Brace(top_strip, LEFT, buff=0.15, color=G_COLOR)
        lbl_dg = MathTex(r"\Delta g", font_size=28, color=G_COLOR).next_to(brace_dg, LEFT, buff=0.12)

        lbl_right = MathTex(r"g\,\Delta f", font_size=24, color=TEXT_COLOR).move_to(
            right_strip.get_center()
        )
        lbl_top = MathTex(r"f\,\Delta g", font_size=24, color=TEXT_COLOR).move_to(
            top_strip.get_center()
        )
        lbl_corner = MathTex(r"\Delta f \Delta g", font_size=20, color=TEXT_COLOR).move_to(
            corner_box.get_center()
        )

        dx_caption = always_redraw(
            lambda: MathTex(
                rf"\Delta x = {dx.get_value():.2f}",
                font_size=28,
                color=MUTED_COLOR,
            ).next_to(base_rect, DOWN, buff=1.15).align_to(base_rect, LEFT)
        )

        self.play(FadeIn(dx_caption))
        self.play(Create(right_strip), GrowFromCenter(brace_df), Write(lbl_df), Write(lbl_right))
        self.wait(0.8)
        self.play(Create(top_strip), GrowFromCenter(brace_dg), Write(lbl_dg), Write(lbl_top))
        self.wait(0.8)
        self.play(Create(corner_box), Write(lbl_corner))
        self.wait(1.0)

        # Right-hand algebra derivation (step by step)
        eq_anchor = np.array([-0.7, 2.0, 0.0])

        eq1 = MathTex(
            r"\Delta A =",
            r"g(x)\,\Delta f",
            r"+",
            r"f(x)\,\Delta g",
            r"+",
            r"\Delta f\,\Delta g",
            font_size=30,
        ).move_to(eq_anchor, aligned_edge=LEFT)
        eq1[1].set_color(DF_STRIP_COLOR)
        eq1[3].set_color(DG_STRIP_COLOR)
        eq1[5].set_color(CORNER_COLOR)

        eq2_note = Text("Divide both sides by Δx:", font_size=22, color=MUTED_COLOR)
        eq2 = MathTex(
            r"\frac{\Delta A}{\Delta x} =",
            r"g(x)\frac{\Delta f}{\Delta x}",
            r"+",
            r"f(x)\frac{\Delta g}{\Delta x}",
            r"+",
            r"\frac{\Delta f}{\Delta x}\,\Delta g",
            font_size=30,
        )
        eq2[1].set_color(DF_STRIP_COLOR)
        eq2[3].set_color(DG_STRIP_COLOR)
        eq2[5].set_color(CORNER_COLOR)

        eq2_note.next_to(eq1, DOWN, buff=0.35, aligned_edge=LEFT)
        eq2.next_to(eq2_note, DOWN, buff=0.22, aligned_edge=LEFT)

        self.play(Write(eq1), run_time=1.6)
        self.wait(1.0)
        self.play(FadeIn(eq2_note), Write(eq2), run_time=1.6)
        self.wait(1.2)

        # Fade out interior labels so shrinking strips stay crisp
        self.play(
            FadeOut(brace_df),
            FadeOut(lbl_df),
            FadeOut(brace_dg),
            FadeOut(lbl_dg),
            FadeOut(lbl_right),
            FadeOut(lbl_top),
            FadeOut(lbl_corner),
            run_time=0.6,
        )

        limit_note = Text("Let Δx → 0  (corner vanishes faster!):", font_size=22, color=PROD_COLOR)
        limit_note.next_to(eq2, DOWN, buff=0.35, aligned_edge=LEFT)
        self.play(FadeIn(limit_note))

        # Shrink dx -> 0.02 smoothly
        self.play(dx.animate.set_value(0.02), run_time=3.5, rate_func=smooth)
        self.wait(0.8)

        # Show vanishing corner term
        vanish_arrow = MathTex(r"\longrightarrow 0", font_size=28, color=CORNER_COLOR).next_to(
            eq2[5], DOWN, buff=0.12
        )
        eq_final = MathTex(
            r"\frac{d}{dx}\big[f(x)g(x)\big] =",
            r"f'(x)\,g(x)",
            r"+",
            r"f(x)\,g'(x)",
            font_size=33,
        )
        eq_final[1].set_color(DF_STRIP_COLOR)
        eq_final[3].set_color(DG_STRIP_COLOR)
        final_card = wrap_in_card(eq_final, buff=0.24, stroke_color=PROD_COLOR)
        final_card.next_to(limit_note, DOWN, buff=0.45, aligned_edge=LEFT)

        self.play(Write(vanish_arrow), run_time=0.8)
        self.play(FadeIn(final_card, shift=UP * 0.15), run_time=1.3)
        self.wait(2.5)

    def construct_worked_example(self):
        header = make_section_header("2. Specific Example: h(x) = x² · (x + 2) at x = 2")
        self.play(FadeIn(header), run_time=0.8)

        # Left side: Concrete 4 x 4 square at x = 2
        base_bl = np.array([-5.3, -1.7, 0.0])
        side = 2.4

        sq = Rectangle(
            width=side,
            height=side,
            color=PROD_COLOR,
            stroke_width=2.5,
            fill_color=PROD_COLOR,
            fill_opacity=0.22,
        ).move_to(base_bl + RIGHT * (side / 2) + UP * (side / 2))

        b_f = Brace(sq, DOWN, buff=0.14, color=F_COLOR)
        t_f = MathTex(r"f(2) = 2^2 = 4", font_size=26, color=F_COLOR).next_to(b_f, DOWN, buff=0.1)

        b_g = Brace(sq, LEFT, buff=0.14, color=G_COLOR)
        t_g = MathTex(r"g(2) = 4", font_size=26, color=G_COLOR).next_to(b_g, LEFT, buff=0.1)

        t_area = MathTex(r"\text{Area} = 16", font_size=28, color=PROD_COLOR).move_to(sq.get_center())

        # Strips scaled proportionally to rates: f'(2)=4 (right), g'(2)=1 (top)
        r_strip = Rectangle(
            width=0.95,
            height=side,
            color=DF_STRIP_COLOR,
            fill_color=DF_STRIP_COLOR,
            fill_opacity=0.55,
        ).next_to(sq, RIGHT, buff=0)

        t_strip = Rectangle(
            width=side,
            height=0.50,
            color=DG_STRIP_COLOR,
            fill_color=DG_STRIP_COLOR,
            fill_opacity=0.55,
        ).next_to(sq, UP, buff=0)

        r_rate = MathTex(r"4 \cdot 4 = 16", font_size=24, color=TEXT_COLOR).move_to(r_strip.get_center())
        t_rate = MathTex(r"4 \cdot 1 = 4", font_size=24, color=TEXT_COLOR).move_to(t_strip.get_center())

        self.play(Create(sq), GrowFromCenter(b_f), Write(t_f), GrowFromCenter(b_g), Write(t_g), Write(t_area))
        self.wait(0.8)

        # Right side: Step-by-step symbolic + numeric Product Rule
        col_x = -0.6
        step1 = MathTex(r"f(x) = x^2 \implies f'(x) = 2x", font_size=30, color=F_COLOR)
        step2 = MathTex(r"g(x) = x + 2 \implies g'(x) = 1", font_size=30, color=G_COLOR)
        step3 = MathTex(
            r"h'(x) =", r"f'(x)g(x)", r"+", r"f(x)g'(x)",
            font_size=30,
        )
        step3[1].set_color(DF_STRIP_COLOR)
        step3[3].set_color(DG_STRIP_COLOR)

        step4 = MathTex(
            r"h'(x) =", r"(2x)(x+2)", r"+", r"(x^2)(1)",
            font_size=30,
        )
        step4[1].set_color(DF_STRIP_COLOR)
        step4[3].set_color(DG_STRIP_COLOR)

        step5 = MathTex(
            r"h'(x) = 2x^2 + 4x + x^2 = 3x^2 + 4x",
            font_size=30,
            color=TEXT_COLOR,
        )

        step6 = MathTex(
            r"\text{At } x=2:\;\; h'(2) =", r"16", r"+", r"4", r"= 20",
            font_size=32,
        )
        step6[1].set_color(DF_STRIP_COLOR)
        step6[3].set_color(DG_STRIP_COLOR)
        step6[4].set_color(PROD_COLOR)
        step6_card = wrap_in_card(step6, buff=0.2, stroke_color=PROD_COLOR)

        steps = VGroup(step1, step2, step3, step4, step5, step6_card).arrange(
            DOWN, buff=0.32, aligned_edge=LEFT
        )
        steps.move_to(np.array([col_x, 2.25, 0.0]), aligned_edge=UL)

        self.play(Write(step1), run_time=1.0)
        self.play(Write(step2), run_time=1.0)
        self.wait(0.6)
        self.play(Write(step3), run_time=1.0)
        self.play(Write(step4), run_time=1.2)
        self.play(Write(step5), run_time=1.2)
        self.wait(0.8)

        # Highlight strips together with the final numeric sum 16 + 4 = 20
        self.play(Create(r_strip), Write(r_rate), run_time=1.0)
        self.play(Create(t_strip), Write(t_rate), run_time=1.0)
        self.play(FadeIn(step6_card, shift=UP * 0.15), run_time=1.2)
        self.wait(2.5)

    def construct_graph_verification(self):
        header = make_section_header("3. Graphical Check & Independent Paper Verification")
        self.play(FadeIn(header), run_time=0.8)

        axes = Axes(
            x_range=[0, 3.0, 0.5],
            y_range=[0, 32, 5],
            x_length=5.4,
            y_length=4.6,
            axis_config={"color": MUTED_COLOR, "include_numbers": True, "font_size": 20},
            tips=True,
        ).move_to(LEFT * 3.3 + DOWN * 0.35)

        x_lbl = axes.get_x_axis_label(MathTex("x", font_size=26, color=TEXT_COLOR))
        y_lbl = axes.get_y_axis_label(
            MathTex("h(x)", font_size=26, color=PROD_COLOR), edge=UP, direction=UP, buff=0.15
        )

        curve = axes.plot(lambda x: (x ** 2) * (x + 2), x_range=[0, 2.55], color=PROD_COLOR, stroke_width=3.2)
        pt = Dot(axes.c2p(2, 16), color=TEXT_COLOR, radius=0.07)
        pt_lbl = MathTex(r"(2, 16)", font_size=24, color=TEXT_COLOR).next_to(pt, UL, buff=0.12)
        guide_lines = axes.get_lines_to_point(axes.c2p(2, 16), color=MUTED_COLOR)

        tangent_line = axes.plot(
            lambda x: 16 + 20 * (x - 2),
            x_range=[1.25, 2.72],
            color=F_COLOR,
            stroke_width=3.0,
        )
        tan_lbl = MathTex(r"\text{Tangent slope} = 20", font_size=24, color=F_COLOR).next_to(
            axes.c2p(2.6, 28), LEFT, buff=0.15
        )

        wrong_line = DashedVMobject(
            axes.plot(lambda x: 16 + 4 * (x - 2), x_range=[0.8, 2.85], color=CORNER_COLOR, stroke_width=2.5),
            num_dashes=16,
        )
        wrong_lbl = MathTex(r"\text{Naive slope } 4\;\times", font_size=22, color=CORNER_COLOR).next_to(
            axes.c2p(2.7, 18.8), DOWN, buff=0.15
        )

        self.play(Create(axes), Write(x_lbl), Write(y_lbl), run_time=1.3)
        self.play(Create(curve), run_time=1.5)
        self.play(Create(guide_lines), FadeIn(pt), Write(pt_lbl))
        self.wait(0.6)

        # Show wrong slope briefly, then contrast with true tangent
        self.play(Create(wrong_line), Write(wrong_lbl), run_time=1.0)
        self.wait(1.0)
        self.play(Create(tangent_line), Write(tan_lbl), run_time=1.2)
        self.wait(1.0)
        self.play(FadeOut(wrong_line), FadeOut(wrong_lbl), run_time=0.7)

        # Right-hand independent verification panel
        v_title = Text("Independent Check (Direct Expansion)", font_size=26, color=TEXT_COLOR, weight=BOLD)
        v1 = MathTex(r"h(x) = x^2(x + 2) = x^3 + 2x^2", font_size=28, color=PROD_COLOR)
        v2 = MathTex(r"h'(x) = 3x^2 + 4x", font_size=30, color=G_COLOR)
        v3 = MathTex(r"h'(2) = 3(2)^2 + 4(2) = 12 + 8 = 20\;\checkmark", font_size=28, color=TEXT_COLOR)
        v4 = Text("Matches Product Rule & Tangent Slope!", font_size=23, color=F_COLOR)

        verify_group = VGroup(v_title, v1, v2, v3, v4).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        verify_card = wrap_in_card(verify_group, buff=0.3, stroke_color=G_COLOR)
        verify_card.move_to(RIGHT * 3.25 + DOWN * 0.25)

        self.play(FadeIn(verify_card[0]), Write(v_title), run_time=0.9)
        self.play(Write(v1), run_time=1.1)
        self.play(Write(v2), run_time=1.0)
        self.play(Write(v3), run_time=1.2)
        self.play(FadeIn(v4, shift=UP * 0.1))
        self.wait(3.0)


class Scene1Intro(BaseProductRuleScene):
    def construct(self):
        self.construct_intro()


class Scene2GeometricProof(BaseProductRuleScene):
    def construct(self):
        self.construct_geometric_proof()


class Scene3WorkedExample(BaseProductRuleScene):
    def construct(self):
        self.construct_worked_example()


class Scene4GraphVerification(BaseProductRuleScene):
    def construct(self):
        self.construct_graph_verification()


class ProductRuleFull(BaseProductRuleScene):
    """Renders the complete continuous video from start to finish."""

    def construct(self):
        self.construct_intro()
        self.play(FadeOut(*self.mobjects), run_time=0.7)

        self.construct_geometric_proof()
        self.play(FadeOut(*self.mobjects), run_time=0.7)

        self.construct_worked_example()
        self.play(FadeOut(*self.mobjects), run_time=0.7)

        self.construct_graph_verification()
        self.play(FadeOut(*self.mobjects), run_time=0.8)