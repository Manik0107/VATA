from manim import *

class Intro(Scene):
    def construct(self):
        title = Tex("Linear Regression Explained with Graphs")
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))
        self.wait(1)

class Outro(Scene):
    def construct(self):
        summary = Tex("Summary: Linear Regression Concepts and Graphs")
        takeaways = BulletedList(
            "Key concepts reviewed",
            "Formula overview",
            "Visual understanding with graphs"
        )
        group = VGroup(summary, takeaways).arrange(DOWN)
        self.play(Write(summary))
        self.play(FadeIn(takeaways))
        self.wait(3)
        self.play(FadeOut(group))
        self.wait(1)