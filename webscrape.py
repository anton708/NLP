#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 14:05:20 2021

@author: Anton
"""


# This method scrapes the professor's website 50 times, and stores the company 
# name and the company purpose to a data frame that can be shared with the group
def part1():
    company = []
    purpose = []

    # Looping 50 times
    for x in range(0,50):
        resp = requests.get("http://3.85.131.173:8000/random_company")
        soup = BeautifulSoup(resp.text, 'html.parser')
    
        #Acquired company name from "Title" section
        company.append(str.split(soup.title.string," - A Flask Website")[0])
    
        #Acquired purpose form the "li" section that started with "Purpose: "
        listLi = soup.find_all("li")
        for li in listLi:
            if "Purpose:" in li.string:
                purpose.append(str.split(li.string,"Purpose: ")[1])
                break

    #Combined two lists into a data frame and exported it
    d = {'Company': company, 'Purpose': purpose}
    data = pd.DataFrame(data=d)
    data.to_csv('anton.csv')
    return data


# This method should read in my group members' csv files and merge them all into one big data frame
def part2(myData):
    luke = pd.read_csv("luke.csv")
    neil = pd.read_csv("neil.csv")
    #renaming columns to match myData
    luke.rename(columns={"Names": "Company"},inplace=True)
    neil.rename(columns={"Name": "Company"},inplace=True)
    
    finalDF = pd.concat([myData, luke, neil])
    return finalDF

# This method will perform NLP on the combined files using the Vader Sentiment package. It will sort the companies
# by sentiment and then output the top 5 and bottom 5 companies by sentiment
def part3(finalDF):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    analyser = SentimentIntensityAnalyzer()
    sentiments = []
    for purpose in finalDF.Purpose:
        sentiments.append(analyser.polarity_scores(purpose)["compound"])
    finalDF["Sentiment"] = sentiments
    finalDF.sort_values(by=['Sentiment'], inplace=True)
    
    top5 = pd.DataFrame({"Company": finalDF.Company[(len(finalDF)-5):(len(finalDF))],
                         "Sentiment": finalDF.Sentiment[(len(finalDF)-5):(len(finalDF))]})
    bottom5 = pd.DataFrame({"Company": finalDF.Company[0:5],
                         "Sentiment": finalDF.Sentiment[0:5]})
    
    return (top5,bottom5)



if __name__ == '__main__':
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup
    
    myData = part1()
    finalDF = part2(myData)
    top5, bottom5 = part3(finalDF)
    print(top5)
    print(bottom5)
    
