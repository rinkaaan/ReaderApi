import re
import streamlit as st


def convert_to_ruby(japanese_text):
    # Find all instances of [漢字](ふりがな)
    pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    # Replace with <ruby> tags
    def replace_with_ruby(match):
        kanji = match.group(1)
        furigana = match.group(2)
        return f'<ruby>{kanji}<rt>{furigana}</rt></ruby>'

    html_text = pattern.sub(replace_with_ruby, japanese_text)
    return html_text


# Example usage
japanese_text = "[更](さら)に[言](い)えば、システムで[自動](じどう)で[出来](でき)ることが[増](ふ)えていっていませんか？"
html_output = convert_to_ruby(japanese_text)

st.markdown(html_output, unsafe_allow_html=True)
