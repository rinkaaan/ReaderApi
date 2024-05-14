import subprocess


def add_furigana(text):
    # Run MeCab to get the morphological analysis
    result = subprocess.run(['mecab'], input=text, text=True,
                            capture_output=True)

    print(result.stdout)

    # # Process MeCab output
    # furigana_text = ""
    # for line in result.stdout.split("\n"):
    #     if line == "EOS":
    #         break
    #     parts = line.split("\t")
    #     if len(parts) < 2:
    #         continue
    #     word = parts[0]
    #     reading = parts[1].split(",")[-1] if len(
    #             parts[1].split(",")) > 7 else ""
    #     # Only add furigana for kanji (not katakana or hiragana)
    #     if word != reading and any(
    #             '\u4e00' <= char <= '\u9faf' for char in word):
    #         furigana_text += f"[{word}]({reading})"
    #     else:
    #         furigana_text += word
    #
    # return furigana_text


# Example usage
input_text = "更に言えば、システムで自動で出来ることが増えていっていませんか？"
output_text = add_furigana(input_text)
print(output_text)
