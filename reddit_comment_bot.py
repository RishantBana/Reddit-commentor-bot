import praw
import config
import time
import os


SUBREDDIT_NAME = 'Sample subreddit'
SEARCH_TERMS = "Sample comment"
SLEEP_TIME = 60  

def bot_login():

    reddit_instance = praw.Reddit(
        username=config.username,
        password=config.password,
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent="Reddit_comment_bot"
    )
    print("Logged in!")
    return reddit_instance

def fetch_replied_comments(file_path):
    
    if not os.path.isfile(file_path):
        return []
    
    with open(file_path, "r") as file:
        replied_comments = file.read().splitlines()
    
    return list(filter(None, replied_comments))

def save_replied_comment(file_path, comment_id):
    
    with open(file_path, "a") as file:
        file.write(comment_id + "\n")

def run_bot(reddit_instance, replied_comments):
    
    print("Searching the latest comments...")

    found_matching_comment = False  

    try:
        for comment in reddit_instance.subreddit(SUBREDDIT_NAME).comments(limit=2000):  
            if (SEARCH_TERMS in comment.body.lower() and  
                comment.id not in replied_comments and 
                comment.author != reddit_instance.user.me()):
                found_matching_comment = True 
                print(f'Found a matching comment: {comment.id}')
                
                
                response = comment.reply("Hey, I like your comment!")
                print(f'Replied to comment: {comment.id} by {comment.author}')
                print(f'Bot commented: "{response.body}"')

                replied_comments.append(comment.id)
                save_replied_comment("comments_replied_to.txt", comment.id)

        if not found_matching_comment:
            print("No matching comments found.")

    except Exception as e:
        print(f"An error occurred: {e}")

    print("Search completed.")
    
    print(f"Sleeping for {SLEEP_TIME} seconds...")
    time.sleep(SLEEP_TIME)

def main():

    reddit_instance = bot_login()
    replied_comments = fetch_replied_comments("comments_replied_to.txt")
    print(replied_comments)

    while True:
        run_bot(reddit_instance, replied_comments)

if __name__ == "__main__":
    main()
