from googleapiclient.discovery import build
import re
from textblob import TextBlob
from langdetect import detect
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import datetime
from visualisation import timestamp_graph,Pie_chart,engagement_graph
from data_manuplation import monthly,csv_file
api_key = 'AIzaSyAfT9Of2AXi8O-WyDoeRYl4wy6GJ0KKyZ0'


def get_upload_date_from_web(video_id):
    try:
        youtube = build('youtube', 'v3',developerKey=api_key)
        response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        # Extract the publication date from the response
        if 'items' in response and len(response['items']) > 0:
            video_info = response['items'][0]
            if 'snippet' in video_info and 'publishedAt' in video_info['snippet']:
                publish_date = video_info['snippet']['publishedAt']
                publish_date = datetime.datetime.strptime(publish_date, '%Y-%m-%dT%H:%M:%SZ').date()
                return publish_date
            else:
                print("Publication date not found for the video.")
                
        else:
            print("Video not found or API key is invalid.")
    except Exception as e:
        print("An error occurred:", str(e))
    return None



def get_date_range(start_date, end_date):
    # Initialize an empty dictionary to store the dates
    date_dict = {}

    # Iterate through each date from start_date to end_date
    current_date = start_date
    while current_date <= end_date:
        date_dict[current_date] =  {'positive': 0, 'negative': 0,'neutral':0,'total':0}  # Use None as placeholder value
        current_date += datetime.timedelta(days=1)  # Increment current_date by 1 day

    return date_dict



def sentiment_scores(sentence):
 
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
 
    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    
 
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        return 'positive'
 
    elif sentiment_dict['compound'] <= - 0.05 :
        return 'negative'
 
    else :
        return 'neutral'
        
        
def detect_language(text):
    try:
        language = detect(text)
        return language
    except:
        return "unknown"

def hinglish_to_english(text):
    translator = Translator()
    try:
        translated_text = translator.translate(text, dest='en')
        return translated_text.text
    except:
        print(text)
        return text

    
    
def clean_comm(comment):


    return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", comment).split())

def get_comment_sentiment(comment):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_comm(comment))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'
    
def video_comments(video_id):
    youtube = build('youtube', 'v3',developerKey=api_key)
    video_response=youtube.commentThreads().list(part='snippet,replies',videoId=video_id).execute()
    count = 0
    upload_date = get_upload_date_from_web(video_id)
    data_dict = get_date_range(upload_date,datetime.date.today())
    total_dict = {'Positive':0,'Negative':0,'Neutral':0}
    
    comment_dict = {'Positive_comments':[],'Negative_comments':[],'Neutral_comments':[]}
    while video_response:
        for item in video_response['items']:
            try:
                
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                date = item['snippet']['topLevelComment']['snippet']['publishedAt']
                likes = item['snippet']['topLevelComment']['snippet']['likeCount']
                date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').date()

                detected_lang = detect_language(comment)
                # english_text = hinglish_to_english(comment)
                if detected_lang == 'hi':
                    english_text = hinglish_to_english(comment)
                else:
                    english_text = comment
                # sentiment = get_comment_sentiment(english_text)#text blob
                sentiment = sentiment_scores(english_text) #vader_sentiment
                count +=1
                data_dict[date]['total'] += 1 
                if sentiment == 'positive':
                    data_dict[date]['positive'] += 1
                    total_dict['Positive'] += 1
                    comment_dict['Positive_comments'].append(comment)
                elif sentiment == 'negative':
                    data_dict[date]['negative'] += 1
                    comment_dict['Negative_comments'].append(comment)
                    total_dict['Negative'] += 1
                else:
                    data_dict[date]['neutral'] += 1
                    total_dict['Neutral'] += 1
                    comment_dict['Neutral_comments'].append(comment)
            except:
                pass
            # print(comment , end = '\n\n')
            # print(english_text , end = '\n\n')
            print(count,end='\n\n')  

            # print(sentiment,detected_lang, end='\n\n')
        # Again repeat
        if 'nextPageToken' in video_response:
            video_response =youtube.commentThreads().list(part='snippet,replies',videoId = video_id,pageToken = video_response['nextPageToken']).execute()
        else:
            # for com in comm:
            #     print(com)
            # print(data_dict)
            break
    monthly_data=monthly(data_dict)
    csv_file(comment_dict)
    engagement_graph(monthly_data)
    Pie_chart(total_dict)
    
            
if __name__ == "__main__":

    video_id = "HWjCStB6k4o"
    # Call function
    video_comments(video_id)

 