#from input import Input
import re
import time
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk import pos_tag,download,help
from collections import Counter
import copy
import numpy

contraction_mapping = {
    "ain't": "is not",
    "aren't": "are not",
    "can't": "cannot",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "didn't": "did not",  "doesn't": "does not", "don't": "do not", "hadn't": "had not", "hasn't": "has not", "haven't": "have not",
    "he'd": "he would", "he'll": "he will", "he's": "he is", "how'd": "how did", "how'd'y": "how do you", "how'll": "how will", "how's": "how is",
    "I'd": "I would", "I'd've": "I would have", "I'll": "I will", "I'll've": "I will have", "I'm": "I am", "I've": "I have", "i'd": "i would",
    "i'd've": "i would have", "i'll": "i will",  "i'll've": "i will have", "i'm": "i am", "i've": "i have", "isn't": "is not", "it'd": "it would",
    "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have", "it's": "it is", "let's": "let us", "ma'am": "madam",
    "mayn't": "may not", "might've": "might have", "mightn't": "might not", "mightn't've": "might not have", "must've": "must have",
    "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have", "o'clock": "of the clock",
    "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not", "sha'n't": "shall not", "shan't've": "shall not have",
    "she'd": "she would", "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have", "she's": "she is",
    "should've": "should have", "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have", "so's": "so as",
    "this's": "this is", "that'd": "that would", "that'd've": "that would have", "that's": "that is", "there'd": "there would",
    "there'd've": "there would have", "there's": "there is", "here's": "here is", "they'd": "they would", "they'd've": "they would have",
    "they'll": "they will", "they'll've": "they will have", "they're": "they are", "they've": "they have", "to've": "to have",
    "wasn't": "was not", "we'd": "we would", "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", "we're": "we are",
    "we've": "we have", "weren't": "were not", "what'll": "what will", "what'll've": "what will have", "what're": "what are",
    "what's": "what is", "what've": "what have", "when's": "when is", "when've": "when have", "where'd": "where did", "where's": "where is",
    "where've": "where have", "who'll": "who will", "who'll've": "who will have", "who's": "who is", "who've": "who have",
    "why's": "why is", "why've": "why have", "will've": "will have", "won't": "will not", "won't've": "will not have",
    "would've": "would have", "wouldn't": "would not", "wouldn't've": "would not have", "y'all": "you all",
    "y'all'd": "you all would", "y'all'd've": "you all would have", "y'all're": "you all are", "y'all've": "you all have",
    "you'd": "you would", "you'd've": "you would have", "you'll": "you will", "you'll've": "you will have",
    "you're": "you are", "you've": "you have"
}


#wordnet_lemmatizer = WordNetLemmatizer()

# data="""Hello my name is 32.5 Kuldeep economy. I am playing football.  scarves     I like to play cricket also. I started liking ice cream also."""
#input_article=Input().get_article()
#data=input_article 
""" def __get_lemmatize_words(self):
        lemmatizer=WordNetLemmatizer()
        lematize_words=[]
        
        l=[]
        for word in self.words:
            l.append(word)
            pos=pos_tag(l)
            if re.search(r'(^NN+)',pos[0][1]) is not None:
                lematize_words.append(lemmatizer.lemmatize(word))
            elif re.search(r'(^VB+)',pos[0][1]) is not None:
                lematize_words.append(lemmatizer.lemmatize(word,pos='v'))
            l.pop()
        return lematize_words """

class Summarize:
    def __init__(self,title,article,lines):
        self.article=article.replace('\n',' ')
        self.title=title
        self.corpus=""
        self.sentences=[]
        self.words=[]
        self.lines=lines
        self.punctuations = '''!()[]{};:,"\<>/@'’#$%^&*_~+'''
        
    def __custom_word_tokenize(self,string):
        l=[]
        word=[]
        for char in string:
            if char==" ":
                l.append("".join(word))
                word=[]
            else:
                word.append(char)
        if len(word)!=0:
            l.append("".join(word))
        return l

    def __remove_contractions(self, string):
        contractions_removed = ""
        selected_words = contraction_mapping.keys()
        
        words = self.__custom_word_tokenize(string)

        for char in words:
            if char in selected_words:
                contractions_removed = contractions_removed+" " + \
                    contraction_mapping[char]
            else:
                contractions_removed = contractions_removed +" "+ char
        string = contractions_removed
        

        return string
    
    def __get_lemmated_word(self,word,pos):
        lemmatizer=WordNetLemmatizer()
        if re.search(r'(^NN+)',pos) is not None:
            return lemmatizer.lemmatize(word)
        elif re.search(r'(^VB+)',pos) is not None:
            return lemmatizer.lemmatize(word,pos='v')
        else:
            return lemmatizer.lemmatize(word,pos='v')
    
    def __get_lemmated_corpus(self):
        corpus=""
        l=[]
        for word in self.corpus.split():
            l.append(word)
            lw=self.__get_lemmated_word(word, pos_tag(l)[0][1]) 
            corpus=corpus+" "+lw
            #print("l= ",l," pos= ",pos_tag(l)[0][1]," lemmated=",lw)
            l.pop()

        return corpus
    
    def __remove_punctuations(self, string):
        no_punct = ""
        other_punctuations='''/_~'''
        last_char=""
        for char in string:
            if char in other_punctuations:
                no_punct = no_punct + " "
                last_char=char
                continue
            if char=="." and (last_char==" " or last_char=="."):
                continue

            if char not in self.punctuations:
                no_punct = no_punct + char
                last_char=char
        string = no_punct
        return string
    
    def __clean_data(self):
        self.article=re.sub(' +',' ',self.article)
        self.corpus=self.article.lower()
        self.corpus=self.__remove_contractions(self.corpus)
        self.corpus=self.__remove_punctuations(self.corpus)
        self.corpus=self.__get_lemmated_corpus()



    def __get_words(self,corpus):
        tokenizer=RegexpTokenizer(r'\w+')
        words=tokenizer.tokenize(corpus)
        return words
        
    
    def __get_frequency_counts(self, sentences, vector):
        '''
        This functon returns the frquency counts for each row
        '''
        f = copy.deepcopy(vector)       
        x = []
        bullet_point_pattern=r'[0-9](\.)$'
  
        for sentence in sentences:
            words = self.__get_words(sentence)
            flag=0

            for word in words:
                if re.search(bullet_point_pattern,word) is None:
                    flag=1
                    if word[-1]=='.':
                        f[word[:-1]]+=1
                    else:
                        f[word] += 1
            if flag==1:
                x.append(f)
          
            f = copy.deepcopy(vector)

        return x



    def __get_row_lengths(self, sentences):
        '''
        Returns the lenth of each document in corpus
        '''
        l = []
        for sentence in sentences:
            x = self.__get_words(sentence)
            l.append(len(x))
        return l

    def __compute_tf(self, sentences, fc):
        '''
        Returns the Tf calculated matrix
        '''
        row_lengths = self.__get_row_lengths(sentences)
        k = 0
        for row in fc:
          
            for value in row:
                row[value] /= float(row_lengths[k])
            k += 1
       
        return fc

    
    def __get_ni(self, sentences, vector):
        '''
        Returns the value, each feature present in how many documents
        '''
        k = 0
        count = 0
        unique_words = list(vector)
        
        li_count = []
        for unique_word in unique_words:
           
            for sentence in sentences:
               
                words = self.__get_words(sentence)
                if unique_word in words:
                   
                    count += 1
            li_count.append(count + 1)
            count = 0
        return li_count

    def __compute_idf(self, sentences, vector, fc, n):
        '''
        computes the idf and returns a dictionary
        '''
        k = 0
        x = []
        idf = copy.deepcopy(vector)
        ni = self.__get_ni(sentences, vector) #return list of values, each describing in how many documents a word is present 
        for i in ni:
            x.append(numpy.log(n / ni[k]) + 1)
            k += 1
        k = 0
        for i in idf:
            idf[i] = x[k]
            k += 1
        #print("\n\n The IDF values calculated are :\n\n")
        # print(idf)
        return idf

    
    def __get_unique_features(self, li):
        '''
        This returns the unique feature names in the list
        '''
        unique = []
        for i in li:
            if i not in unique:
                unique.append(i)
        return unique


    def __preprocess(self):
        unique_words = self.__get_unique_features(self.words)

        dim = []
        dim = [0 for i in range(len(unique_words))]
        n=len(self.sentences)

        vector = dict(zip(unique_words, dim))
        
        fc = self.__get_frequency_counts(self.sentences, vector) # returns [#sentence * #unique_words] matrix
        
        tf = self.__compute_tf(self.sentences, fc)
        
        idf = self.__compute_idf(self.sentences, vector, fc, n + 1)
        
        return tf,idf
        

    def __compute_tf_idf(self, tf, idf, title):
        '''
        This returns computed tf-idf dictionary for the given vocab
        '''
        x = {}
        tf_idf = []
        for key in tf:
            for word in key:
                x[word] = key[word] * idf[word]
                if word in self.title:
                    x[word] += 0.01
            tf_idf.append(x)
            x = {}
        
        return tf_idf

    def __transform(self, tf, idf, title):
        '''
        returns a normalized sparse matrix
        '''
        tf_idf = self.__compute_tf_idf(tf, idf, self.title)
        return tf_idf

    def __score_sentences(self, tf, tf_idf, sent_word_count):
        sentenceValue = {}
        x = 0
        i = 0
        for sent in tf_idf:
            total_score_per_sentence = 0
            for word, score in sent.items():
                total_score_per_sentence += score
            sentenceValue[x] = total_score_per_sentence / sent_word_count[i]
            i += 1
            x += 1
        return sentenceValue
    
    def __find_average_score(self, sentenceValues):
        sumValues = 0
        l=100000
        for entry in sentenceValues:
            if l>sentenceValues[entry]:
                l=sentenceValues[entry]
            sumValues += sentenceValues[entry]
        # Average value of a sentence from original summary_text
        if len(sentenceValues)>0:
            average = (sumValues / len(sentenceValues))
        else: 
            average=1000
        self.__LOWEST_SCORE=l
        return average
    
    def __get_summary(self, sentences, sentenceValues, threshold, lines=0):
        summary = ""
        if lines<=0:
            for sent, score in sentenceValues.items():
                if score >= threshold:
                    summary =summary+" "+sentences[sent]
        else:
            for sent, score in sentenceValues.items():
                if score >= threshold and lines>0:
                    summary =summary+" "+sentences[sent]
                    lines-=1
        return summary
    
    def generate_summary(self):
        self.__clean_data()

        self.sentences=sent_tokenize(self.corpus)
        self.words=self.__get_words(self.corpus)

        self.tf_, self.idf_ = self.__preprocess()
        self.tf_idf_ = self.__transform(self.tf_, self.idf_, self.title)
        
        sentences=sent_tokenize(self.article)
        sent_word_count= self.__get_row_lengths(sentences)
        self.sentenceScores_ = self.__score_sentences(self.tf_, self.tf_idf_, sent_word_count)

        threshold = self.__find_average_score(self.sentenceScores_)
        #self.THRESHOLD=threshold
        threshold=(threshold+self.__LOWEST_SCORE)/2
        self.summary = self.__get_summary(sentences, self.sentenceScores_, threshold,self.lines)

        #print(self.sentenceScores_)
        values={"summary":self.summary,"threshold":threshold}
        return values


if __name__ == "__main__":
    s=Summarize("Hello","introduction")
    summ=s.generate_summary()
    print(summ["summary"])
    print(summ["threshold"])

    start=time.time()
    end=time.time()
    print("execution tim in ms: ",(end-start)*10**3)