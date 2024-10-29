import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download stopwords if not already done
nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Define the text
text = """Moderator: Ladies and gentlemen, good day and welcome to the Voltas Limited Q1 FY '25 Earnings
Conference Call, hosted by Nirmal Bang Equities Private Limited.
As a reminder, all participant lines will be in the listen-only mode and there will be an
opportunity for you to ask questions after the presentation concludes. Should you need assistance
during the conference call, please signal an operator by pressing star then zero on your touchtone
telephone. Please note that this conference is being recorded.
I now hand the conference over to Ms. Natasha Jain from Nirmal Bang Equities. Thank you and
over to you, ma'am."""

# Define stop words in English
stop_words = set(stopwords.words('english'))

# Tokenize the text into words
words = word_tokenize(text)

# Remove stop words
filtered_text = [word for word in words if word.lower() not in stop_words]

# Join words back into a string
result = " ".join(filtered_text)

print("Original text:", text)
print("Text without stopwords:", result)
