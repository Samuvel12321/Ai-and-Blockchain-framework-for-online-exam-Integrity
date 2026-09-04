import reflex as rx


def index():
    return rx.center(
        rx.vstack(
            rx.heading("EduView Test"),
            rx.text("Reflex frontend is working"),
            spacing="4",
        ),
        height="100vh",
    )


app = rx.App()
app.add_page(index)