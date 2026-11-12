"""Application entry point."""

from dotenv import load_dotenv

load_dotenv()

from ui.dashboard import render_dashboard


if __name__ == "__main__":
    render_dashboard()