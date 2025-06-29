#!/usr/bin/env python3
"""
Translate text from stdin or URL using Gemini API
"""

import argparse
import os
import sys
import threading
import time

import google.generativeai as genai


def setup_gemini(api_key):
    """Initialize Gemini API"""
    genai.configure(api_key=api_key)

    model_name = os.environ.get("GTR_MODEL", "gemini-2.5-pro")

    return genai.GenerativeModel(model_name)


class Spinner:
    """Simple spinner for loading indication"""

    def __init__(self):
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.stop_spinner = False
        self.spinner_thread = None

    def _spin(self):
        """Spinner animation loop"""
        i = 0
        while not self.stop_spinner:
            sys.stderr.write(f"\r{self.spinner_chars[i % len(self.spinner_chars)]}  ")
            sys.stderr.flush()
            time.sleep(0.1)
            i += 1

    def start(self):
        """Start spinner in a separate thread"""
        self.stop_spinner = False
        self.spinner_thread = threading.Thread(target=self._spin)
        self.spinner_thread.daemon = True
        self.spinner_thread.start()

    def stop(self):
        """Stop spinner and clear the line"""
        self.stop_spinner = True
        if self.spinner_thread:
            self.spinner_thread.join()
        sys.stderr.write("\r" + " " * 30 + "\r")
        sys.stderr.flush()


def translate_text(model, text, target_lang="Japanese", is_url=False):
    """Translate text or URL content using Gemini API"""

    if is_url:
        prompt = f"""
        Access the following URL and translate its content to {target_lang}.
        Extract the main content (article text, blog post, etc.) and translate it.
        Ignore navigation menus, advertisements, and other non-content elements.
        Output only the translation without any explanations or additional text.

        URL: {text}
        """
    else:
        prompt = f"""
        Translate the following text to {target_lang}.
        Output only the translation without any explanations or additional text.
        IMPORTANT: Translate the ENTIRE text completely Do not abbreviate,
                   summarize, or omit any part of the content.

        Text:
        {text}
        """

    # Start spinner
    spinner = Spinner()
    spinner.start()

    try:
        response = model.generate_content(prompt)
        spinner.stop()
        return response.text.strip()
    except Exception as e:
        spinner.stop()
        sys.stderr.write(f"Translation error: {str(e)}\n")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Translate text from stdin or URL")
    parser.add_argument(
        "url", nargs="?", help="URL to translate (optional, uses stdin if not provided)"
    )
    parser.add_argument(
        "-t", "--target", default="Japanese", help="Target language (default: Japanese)"
    )

    args = parser.parse_args()

    api_key = os.environ.get("GTR_API_KEY")
    if not api_key:
        sys.stderr.write("Error: GTR_API_KEY environment variable is not set\n")
        sys.stderr.write("Please run: export GTR_API_KEY='your-api-key'\n")
        sys.exit(1)

    model = setup_gemini(api_key)

    if args.url:
        text = args.url
        is_url = True
    elif not sys.stdin.isatty():
        text = sys.stdin.read().strip()
        if not text:
            sys.stderr.write("Error: Input text is empty\n")
            sys.exit(1)
        is_url = False
    else:
        sys.stderr.write("Error: No input provided\n")
        sys.stderr.write("Usage: pbpaste | gtr\n")
        sys.stderr.write("   or: gtr <URL>\n")
        sys.exit(1)

    translated = translate_text(model, text, args.target, is_url)
    print(translated)


if __name__ == "__main__":
    main()
