import pandas as pd
import numpy as np


def format_hisory_new_providers(name):
    import flair
    flair_sentiment = flair.models.TextClassifier.load('en-sentiment')

    import nltk
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')

    path =r'/Users/tom/Documents/StockSharks/{}.csv'.format(name)
    main = pd.read_csv(r'/Users/tom/Documents/StockSharks/history.csv', encoding='utf-8')
    source= pd.read_csv(path)
    target_df = pd.DataFrame(columns=main.columns, index=source.index)
    for ind, row in source.iterrows():
        if isinstance(row.text, str):
            s = flair.data.Sentence(row.text)
            flair_sentiment.predict(s)
            total_sentiment = s.labels
            if len(total_sentiment)>0:
                print(total_sentiment)
                print(type(total_sentiment))
                target_df['Time'].iloc[ind]= row.date
                target_df['Text'].iloc[ind] =row.text
                target_df['Source'].iloc[ind]=row.username
                target_df['Organisations'].iloc[ind] = {(' '.join(c[0] for c in chunk), chunk.label() ) for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(row.text))) if hasattr(chunk, 'label') and chunk.label()in['ORGANIZATION', 'PERSON']}

                target_df['Sentiment'].iloc[ind]= total_sentiment[0].value
                target_df['Sentiment_Score'].iloc[ind] = total_sentiment[0].score
                target_df['URL'].iloc[ind] = np.nan
    main = pd.concat([main, target_df], axis=0)
    main=main.set_index(keys='Time', drop=True)
    main.to_csv(r'/Users/tom/Documents/StockSharks/history.csv', encoding='utf-8')
name='KimbleCharting'
format_hisory_new_providers(name)