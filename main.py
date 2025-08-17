
'''import youtube_comment_scraper
import pandas as pd
from pysentimiento import create_analyzer
import sys

def main(youtube_url):
    print(f"Scraping comments from: {youtube_url}")
    comments = youtube_comment_scraper.scrape_comments(youtube_url)
    print(f"Found {len(comments)} comments.")

    if comments:
        print("Analyzing sentiment...")
        analyzer = create_analyzer(task="sentiment", lang="en") # Using English model, will handle multilingual comments to the best of its ability.
                                                              # For true multilingual, a language detection step and language-specific models would be ideal.
        analyzed_comments = []
        for comment in comments:
            text = comment.get("text")
            if text:
                try:
                    output = analyzer.predict(text)
                    sentiment = output.output
                    if sentiment == "POS":
                        comment["sentiment"] = "Positive"
                    elif sentiment == "NEG":
                        comment["sentiment"] = "Negative"
                    else:
                        comment["sentiment"] = "Neutral"
                except Exception as e:
                    print(f"Error analyzing sentiment for comment \'{text}\': {e}")
                    comment["sentiment"] = "Undetermined"
            else:
                comment["sentiment"] = "Undetermined"
            analyzed_comments.append(comment)

        print("Sentiment analysis complete.")

        df = pd.DataFrame(analyzed_comments)
        # Select and reorder columns as requested by the user
        df = df[["author", "author_id", "text", "sentiment"]]
        output_file = "youtube_comments_with_sentiment.xlsx"
        df.to_excel(output_file, index=False)
        print(f"Categorized comments saved to {output_file}")
    else:
        print("No comments to analyze.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        youtube_link = sys.argv[1]
        main(youtube_link)
    else:
        print("Usage: python3 main.py <youtube_link>")
        print("Example: python3 main.py https://www.youtube.com/watch?v=M7lc1UVf-VE")

'''
import youtube_comment_scraper
import pandas as pd
from pysentimiento import create_analyzer
from langdetect import detect
from googletrans import Translator
import sys

def main(youtube_url):
    print(f"Scraping comments from: {youtube_url}")
    comments = youtube_comment_scraper.scrape_comments(youtube_url)
    print(f"Found {len(comments)} comments.")

    if not comments:
        print("No comments to analyze.")
        return

    print("Initializing analyzers...")
    analyzer_en = create_analyzer(task="sentiment", lang="en")
    translator = Translator()

    analyzed_comments = []
    for comment in comments:
        text = comment.get("text")
        if text:
            try:
                lang = detect(text)
                original_text = text

                if lang == "te":
                    translated = translator.translate(text, src="te", dest="en").text
                    output = analyzer_en.predict(translated)
                    text_for_analysis = translated
                elif lang == "en":
                    output = analyzer_en.predict(text)
                    text_for_analysis = text
                else:
                    translated = translator.translate(text, dest="en").text
                    output = analyzer_en.predict(translated)
                    text_for_analysis = translated

                sentiment_map = {"POS": "Positive", "NEG": "Negative", "NEU": "Neutral"}
                comment["sentiment"] = sentiment_map.get(output.output, "Undetermined")
                comment["language"] = lang
                comment["translated_text"] = text_for_analysis if lang != "en" else ""
            except Exception as e:
                print(f"Error analyzing sentiment for '{text}': {e}")
                comment["sentiment"] = "Undetermined"
                comment["language"] = "Unknown"
                comment["translated_text"] = ""
        else:
            comment["sentiment"] = "Undetermined"
            comment["language"] = "Unknown"
            comment["translated_text"] = ""

        analyzed_comments.append(comment)

    print("Sentiment analysis complete.")

    df = pd.DataFrame(analyzed_comments)
    df = df[["author", "author_id", "text", "language", "translated_text", "sentiment"]]
    output_file = "youtube_comments_with_sentiment.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Categorized comments saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        youtube_link = sys.argv[1]
        main(youtube_link)
    else:
        print("Usage: python main.py <youtube_link>")
        print("Example: python main.py https://www.youtube.com/watch?v=M7lc1UVf-VE")
