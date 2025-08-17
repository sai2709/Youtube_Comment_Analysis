
import youtube_comment_downloader
import json
import time
import pandas as pd
from pysentimiento import create_analyzer

def get_video_id(url):
    if "youtube.com/watch?v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("&")[0]
    else:
        return None

def scrape_comments(youtube_url):
    video_id = get_video_id(youtube_url)
    if not video_id:
        print("Invalid YouTube URL.")
        return []

    downloader = youtube_comment_downloader.YoutubeCommentDownloader()
    comments = []
    try:
        for comment in downloader.get_comments(video_id):
            comments.append({
                'author': comment.get('author'),
                'author_id': comment.get('author_id'),
                'text': comment.get('text'),
                'time': comment.get('time'),
                'timestamp': comment.get('timestamp'),
                'votes': comment.get('votes'),
                'cid': comment.get('cid')
            })
            time.sleep(0.1) # Small delay to avoid rate limiting
    except Exception as e:
        print(f"Error scraping comments: {e}")
        return []
    return comments

def analyze_sentiment(comments):
    analyzer = create_analyzer(task="sentiment", lang="en") # Default to English, will handle multilingual later
    # For multilingual, pysentimiento can auto-detect language if model supports it.
    # For now, let's use a general sentiment model.
    # A more robust solution would involve language detection first, then applying the correct model.
    
    # For demonstration, we'll use a simple approach. For true multilingual, a more complex setup is needed.
    # Pysentimiento's `create_analyzer` can take `lang` as a list or 'auto' for some models.
    # For this example, we'll assume the default model handles multiple languages to some extent or we'll need to iterate.
    
    # Let's use the default 'sentiment' analyzer which is often trained on multiple languages or can be fine-tuned.
    # For a truly robust multilingual solution, one might need to detect language per comment and then use a language-specific model.
    # However, pysentimiento's base models are often multilingual.

    analyzed_comments = []
    for comment in comments:
        text = comment.get('text')
        if text:
            try:
                # Pysentimiento can often handle multiple languages with its base models.
                # For more precise multilingual, one would use a language detection library first.
                output = analyzer.predict(text)
                sentiment = output.output # 'POS', 'NEG', 'NEU'
                if sentiment == 'POS':
                    comment['sentiment'] = 'Positive'
                elif sentiment == 'NEG':
                    comment['sentiment'] = 'Negative'
                else:
                    comment['sentiment'] = 'Neutral'
            except Exception as e:
                print(f"Error analyzing sentiment for comment '{text}': {e}")
                comment['sentiment'] = 'Undetermined'
        else:
            comment['sentiment'] = 'Undetermined'
        analyzed_comments.append(comment)
    return analyzed_comments


if __name__ == '__main__':
    youtube_url = "https://www.youtube.com/watch?v=M7lc1UVf-VE"  # Example URL
    print(f"Scraping comments from: {youtube_url}")
    comments = scrape_comments(youtube_url)
    print(f"Found {len(comments)} comments.")

    if comments:
        print("Analyzing sentiment...")
        analyzed_comments = analyze_sentiment(comments)
        print("Sentiment analysis complete.")

        # Convert to DataFrame and save to Excel
        df = pd.DataFrame(analyzed_comments)
        output_file = "youtube_comments_with_sentiment.xlsx"
        df.to_excel(output_file, index=False)
        print(f"Categorized comments saved to {output_file}")
    else:
        print("No comments to analyze.")


