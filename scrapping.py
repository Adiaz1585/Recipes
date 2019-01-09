import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from uploadFiles import getAuthorization, uploadFile #used to upload files to
import os
import csv

#This will create a text file.
#It will name the file the recipe name and also if its ingrediants or steps
#then it will call the function that will upload the file to google drive
def createTextFile(fileName, content):
    file = open("{}.txt".format(fileName), 'w')
    file.writelines(content)
    file.close()



#definaition to scrape the data from 
#the website and store in variables.

def scrapeData():
    recipe = []
    steps = []
    
    url = 'https://www.allrecipes.com/recipe/237842/slow-cooker-pineapple-chicken/?internalSource=similar_recipe_banner&referringId=241813&referringContentType=Recipe&clickId=simslot_2'

    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'lxml')

    for my_tag in soup.find_all(class_ = "recipe-ingred_txt added"):
        ingrediant = my_tag.text
        recipe.append("{}\n".format(ingrediant))
    # print(my_tag.text)


    for my_tag in soup.find_all(class_ = "recipe-directions__list--item"):
        step = my_tag.text
        steps.append("{}\n".format(step))
    
    recipeName = soup.find(class_ = "recipe-summary__h1").text

    # #This variable creates the name of the file recipe will be stored in
    recipeName = str(recipeName.replace(' ' , ''))
    recipeFileName = ("{}Recipe".format(recipeName))
    stepFileName = ("{}Steps".format(recipeName))

    createTextFile(recipeFileName, recipe)
    createTextFile(stepFileName, steps)

    # # for x in range(len(recipe)): 
    # #     print (recipe[x])

    # # print ("\n")

    # # for x in range(len(steps)): 
    # #     print (steps[x])
    
    # print(stepFileName)
    uploadFile(recipeFileName, stepFileName, recipeName)

    os.remove("{}.txt".format(recipeFileName))
    os.remove("{}.txt".format(stepFileName))
    storeUrl(url)
    
    # url = soup.find(class_ = "slider-card")
    # print(url)

def storeUrl(url):
    file = open("useUrls.txt", 'a')
    file.write(url)
    file.close()

scrapeData()
