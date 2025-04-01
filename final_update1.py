import requests
import csv
import time
import argparse
from pathlib import Path
import json
import os



def fetch_tweets(url, headers, params, max_pages=5):
    """Fetch tweets from the db of x with pagination support"""
    all_tweets = []
    next_token = None
    page_count = 0
    
    while page_count < max_pages:
        try:
            # Add pagination token if exists
            if next_token:
                params['next_token'] = next_token
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            response_data = response.json()

            tweets1 = response_data.get('tweets', [])
            all_tweets.extend(tweets1)
            # Check for more pages
            next_token = response_data.get('next_cursor')
            #print(next_token)            
            if not next_token:
                break
                
            page_count += 1
            time.sleep(1)  # Rate limit avoidance
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {params['query']}: {e}")
            break
            
    return all_tweets

def process_language_topics(topics, lang, output_file, url, headers, max_pages):
    """Process all topics for a specific language and save to CSV file"""
    # Check if file exists to determine write mode
    file_exists = os.path.isfile(output_file)
    
    with open(output_file, mode="a" if file_exists else "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header only if file is new
        if not file_exists:
            writer.writerow(["Topic", "Language", "Tweet ID", "Text"])
        
        # Process each topic
        for topic in topics:
            print(f"Fetching tweets for hashtag: '{topic}' in language: '{lang}'...")
            
            params = {
                "query": f"{topic} lang:{lang}",
                "max_results": 100,
                "start_time": "2020-01-01T00:00:00Z",
                "tweet.fields": "id,text,created_at"
            }
            
            tweets = fetch_tweets(url, headers, params, max_pages)
            
            # Write tweets to CSV
            tweet_count = 0
            for tweet in tweets:
                try:
                    tweet_text = tweet.get("text", "").replace("\n", " ").strip()
                    writer.writerow([
                        topic,
                        lang,
                        tweet.get("id", "N/A"),
                        tweet_text
                    ])
                    
                    tweet_count += 1
                except Exception as e:
                    print(f"Error processing tweet: {e}")
                    continue
            
            print(f"Saved {tweet_count} tweets for {topic}")
            csvfile.flush()  # Ensure data is written to disk
            
    print(f"All tweets saved to {output_file}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Fetch tweets by hashtag with pagination")
    parser.add_argument("--base_filename", default="tweets", help="Base name for output files")
    parser.add_argument("--max_pages", type=int, default=5, help="Max pages per topic")
    args = parser.parse_args()

    # API configuration
    url = "https://api.twitterapi.io/twitter/tweet/advanced_search"
    headers = {"X-API-Key": "my_api_key"}

    # Topic lists
    english_topics = [
        "#CulturalBias", "#CulturalStereotypes", "#MediaBias",
        "#DoubleStandards", "#WesternBias", "#Orientalism",
        "#Islamophobia", "#EthnicBias", "#RacistStereotypes",
        "#BiasedCoverage", "#StereotypicalMedia", "#RacialPrejudice",
        "#CulturalMisrepresentation", "#CulturalAppropriation", 
        "#BiasInFashion", "#CulturalClichés", "#Ethnocentrism", 
        "#FoodStereotypes", "#ClothingBias", "#BiasedNarratives",
        "#Culture", "#Media", "#Bias", "#Clothing", "#Racism", "#Black_lives_matter"
    ]
    
    arabic_topics = [
        "#التحيز_الثقافي", "#تمييز_ثقافي", "#التحيز_ضد_الثقافات",
        "#الفجوة_الثقافية", "#عدالة_ثقافية", "#التحيز_ضد_العرب",
        "#ازدواجية_المعايير", "#الصورة_النمطية_عن_العرب",
        "#تشويه_الثقافة_العربية", "#الهوية_العربية",
        "#حقوق_المرأة_في_العالم_العربي", "#الحجاب_والتمييز",
        "#الميراث_والتحيز", "#الرؤية_الغربية_للإسلام",
        "#العرب_في_الإعلام_الغربي", "#التحيز_في_القضايا_العربية",
        "#القضية_الفلسطينية_والتحيز", "#التاريخ_والسرد_الغربي",
        "#الصراع_الثقافي", "#التغطية_الإعلامية_المنحازة", "#المرأة " , "#العرب", "الثقافة", "الهوية",
    ]

    # Ensure output directory exists
    Path(args.base_filename).parent.mkdir(parents=True, exist_ok=True)

    # Process English topics
    process_language_topics(
        english_topics, 
        "en", 
        f"{args.base_filename}_en.csv", 
        url, 
        headers, 
        args.max_pages
    )
    
    # Process Arabic topics
    process_language_topics(
        arabic_topics, 
        "ar", 
        f"{args.base_filename}_ar.csv", 
        url, 
        headers, 
        args.max_pages
    )

if __name__ == "__main__":
    main()


