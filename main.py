import requests
import csv
import argparse
import time

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Fetch tweets by hashtag and save to a CSV file.")
    parser.add_argument("output_file", help="Path to the output CSV file (e.g., 'tweets.csv')")
    args = parser.parse_args()

    # API endpoint (note: this is a placeholder URL; replace with the real API)
    url = "https://api.twitterapi.io/twitter/tweet/advanced_search"

    # Your API key (replace with a valid key)
    headers = {"X-API-Key": "yourapi"}

    # Hashtags to search for (updated to include '#')
    topics = ["#CulturalBias",
    "#CulturalStereotypes",
    "#MediaBias",
    "#DoubleStandards",
    "#WesternBias",
    "#Orientalism",
    "#Islamophobia",
    "#EthnicBias",
    "#RacistStereotypes",
    "#BiasedCoverage",
    "#StereotypicalMedia",
    "#RacialPrejudice",
    "#CulturalMisrepresentation",
    "#CulturalAppropriation",
    "#BiasInFashion",
    "#CulturalClichés",
    "#Ethnocentrism",
    "#FoodStereotypes",
    "#ClothingBias",
    "#BiasedNarratives"]
    topics2 = [
    "#التحيز_الثقافي",
    "#تمييز_ثقافي",
    "#التحيز_ضد_الثقافات",
    "#الفجوة_الثقافية",
    "#عدالة_ثقافية",
    "#التحيز_ضد_العرب",
    "#ازدواجية_المعايير",
    "#الصورة_النمطية_عن_العرب",
    "#تشويه_الثقافة_العربية",
    "#الهوية_العربية",
    "#حقوق_المرأة_في_العالم_العربي",
    "#الحجاب_والتمييز",
    "#الميراث_والتحيز",
    "#الرؤية_الغربية_للإسلام",
    "#العرب_في_الإعلام_الغربي",
    "#التحيز_في_القضايا_العربية",
    "#القضية_الفلسطينية_والتحيز",
    "#التاريخ_والسرد_الغربي",
    "#الصراع_الثقافي",
    "#التغطية_الإعلامية_المنحازة",
    "#التحيز_في_الإعلام",
    "#الإعلام_المنحاز",
    "#الصورة_النمطية_في_هوليوود",
    "#تشويه_العرب",
    "#الإسلام_في_الإعلام_الغربي",
    "#الصورة_النمطية_عن_الإسلام",
    "#الرقابة_الإعلامية",
    "#ازدواجية_المعايير_في_السوشيال_ميديا",
    "#التاريخ_بعيون_غربية",
    "#التاريخ_الاستعماري",
    "#العلم_الإسلامي_والتجاهل",
    "#إسهامات_العرب_في_العلوم",
    "#الاستشراق",
    "#الاستشراق_والتحيز",
    "#الانتداب_والاستعمار",
    "#الإرث_الاستعماري",
    "#طمس_اللغة_العربية",
    "#هيمنة_المصطلحات_الغربية",
    "#سرقة_الثقافة",
    "#الاستيلاء_الثقافي",
    "#التحيز_في_الترجمة",
    "#التلاعب_بالمفاهيم",
    "#حقوق_الإنسان_والتحيز",
    "#ازدواجية_المعايير_في_الحقوق",
    "#حقوق_المرأة_العربية",
    "#المرأة_العربية_في_الإعلام",
    "#التحيز_الأكاديمي",
    "#المنهجية_الغربية_المتحيزة",
    "#الإسلاموفوبيا",
    "#القوانين_التمييزية_ضد_المسلمين",
    "#الحجاب_والتمييز_في_مكان_العمل",
    "#الميراث_والتفاوت",
    "#تغطية_الإعلام_للصراعات_العربية",
    "#التحيز_في_الذكاء_الاصطناعي",
    "#التمييز_الرقمي"
]
    # Languages to search in
    #  # Arabic (ar) and English (en)
    lang="ar"
    # Open the CSV file for writing (creates the file if it doesn't exist)
    with open(args.output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["Topic", "Language", "Tweet ID", "Text"])

        # Loop through each topic and language
        for topic in topics2:
            
            print(f"Fetching tweets for hashtag: '{topic}' in language: '{lang}'...")

            # Query parameters (no change needed; hashtags work like regular keywords)
            params = {
                "query": f"{topic} lang:{lang}",  # Search for the hashtag in the specified language
                "max_results": 500,
                "start_time": "2020-01-01T00:00:00Z",  # Start from Jan 1, 2024
                "end_time": "2024-03-01T00:00:00Z",    # Until March 1, 2024  # Number of tweets to fetch
            }

            # Make the API request
            response = requests.get(url, headers=headers, params=params)
            time.sleep(1)
            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                tweets = data.get("tweets", [])

                # Write tweets to the CSV file
                for tweet in tweets:
                    # Replace newlines in the tweet text with spaces
                    tweet_text = tweet["text"].replace("\n", " ").strip()
                    writer.writerow([topic, lang, tweet["id"], tweet_text])
            else:
                print(f"Error fetching tweets for hashtag '{topic}' in language '{lang}': {response.status_code} - {response.text}")

    print(f"Tweets saved to {args.output_file}")

if __name__ == "__main__":
    main()
