import json
from googletrans import Translator
from fastapi import FastAPI, status, Query, Path
from fastapi.responses import Response
from api.db import client, db
from api.model import WordParams, WordDetailed, Wordlist, WordResponse, DeleteResponse

app = FastAPI()

async def get_translation(text: str, src: str, dest: str):

    """
    This function takes in a word, source language, and destination language and returns a dictionary of the following:
    - original_language: the language of the word passed in
    - translated_language: the language the word was translated to
    - primary_translation: the primary translation of the word
    - alternative_translations: alternative translations of the word
    - synonyms: synonyms of the word
    - primary_definition: the primary definition of the word
    - example_use: an example of the word used in a sentence

    ----------------
    Parameters:
    - text: the word to be translated
    - src: the language of the word passed in
    - dest: the language the word will be translated to

    """

    alternative_translations = None
    synonyms = None
    primary_definition = None
    example_to_use = None

    translator = Translator()
    result = translator.translate(text, src=src, dest=dest)

    all_info = result.extra_data

    #get the translation, synonyms, definitions,  and examples
    main_translation = all_info['translation'][0][0].lower()

    #source language
    original_language = all_info['original-language']

    #not all language combinations offer alternative translations
    if all_info['all-translations']:
        translations = all_info['all-translations'][0][1]
        alternative_translations = translations[:5] if len(translations) > 5 else translations

    #source language
    original_language = all_info['original-language']

    #not all language combinations offer synonyms
    if all_info['synonyms']:
        synonyms = all_info['synonyms'][0][1][0][0][:5] if len(all_info['synonyms'][0][1][0][0]) > 5 else all_info['synonyms'][0][1][0][0]
    else:
        synonyms = None

    #not all language combinations offer definitions
    if all_info['definitions']:
        primary_definition = all_info['definitions'][0][1][0][0]
    else:
        primary_definition = None

    #not all language combinations offer examples
    if all_info['examples']:
        example_to_use = all_info['examples'][0][1][0].replace('<b>', '').replace('</b>', '')                   
    else:
        example_to_use = None


    return {
        "original_language": original_language,
        "translated_language": dest,
        "primary_translation": main_translation, 
        "alternative_translations" : alternative_translations,
        "synonyms": synonyms,
        "primary_definition": primary_definition,
        "example_use": example_to_use,
    }



@app.on_event("startup")
def startup():

    app.mongo_client = client
    app.database = db




@app.get("/translations/{word}/", status_code=status.HTTP_200_OK, response_model=WordResponse)
async def get_word(word: str = Path(..., description="The word to be translated"),
                    src: str = Query(..., description="The language of the word passed in"),
                    dest: str = Query(..., description="The language the word will be translated to")):


    #check if the word exists in the database
    #not enough to check if the word exists, need to check if the word is in the correct language e.g. pain in french means bread in english means suffering
    try:
        word_from_db = await app.database.words.find_one({"word": word, 
                                                        "attributes.original_language": src,
                                                        "attributes.translated_language": dest
                                                      }) 
    except:
        word_from_db = None
        
    if word_from_db:

        del word_from_db["_id"]

        return {
            "status": status.HTTP_200_OK,
            "word": word,
            "attributes": word_from_db["attributes"]
        }
    
    else:
        try:
            googleTransApiResponse = await get_translation(word, src, dest)

            #validate the api response based on WordParams class before inserting into the database
            word_attributes = WordParams(**googleTransApiResponse).dict()

            word_db_object = {
                "word":word,
                "attributes":word_attributes
            }

            await app.database.words.insert_one(word_db_object)

            #change the default status code from 200 to 201
            Response.status_code = status.HTTP_201_CREATED

            return {
                "status": status.HTTP_201_CREATED,
                "word": word,
                "attributes": word_attributes
            }
        
        except:
            return {
                "status":status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error": "something went wrong with the translation, please try a different word/language combination"
            } 
        
# get all words in the database applying pagination
@app.get("/wordlist", status_code=status.HTTP_200_OK)
async def get_all_words(page: int  = Query(1, description="The page number to be returned"),
                        limit: int = Query(10, description="The number of words to be returned per page"),
                        keyword: str = Query(None, description="The keyword to be searched for"), 
                        detailed: bool = Query(False, description="Whether to return the detailed version of the word")):

    skip = (page - 1) * limit

    words = []

    try:
        #sort words in alphabetical order in database, apply pagination and use partial text search based on keyword
        filter_query = {"word": {"$regex": keyword[:3], "$options": "i"}} if keyword else None
        async for word in app.database.words.find(filter_query).sort("word").skip(skip).limit(limit):        

            del word["_id"]

            words.append(word["word"] if not detailed else word)

        if not detailed:
            worlistDict = {"wordlist": words}
            wordlist = Wordlist(**worlistDict).dict()
            wordlist["status"] = status.HTTP_200_OK

        else:
            worlistValidated = [WordDetailed(**word).dict() for word in words]
            wordlist = {"wordlist": worlistValidated}
            wordlist["status"] = status.HTTP_200_OK

        return wordlist

    except:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "error": "database operation failed, please try again later" 
        }

#delete a word from the database
@app.delete("/translations/{word}/", status_code=status.HTTP_200_OK, response_model=DeleteResponse)
async def delete_word(word: str = Path(..., description="The word to be deleted")):
    
        try:
            await app.database.words.delete_one({"word": word})
            return {
                "status": status.HTTP_200_OK,
                "message": f"{word} has been deleted from the database"
            }
        except:
            return {
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error": "database operation failed, please try again later" 
            }
    

@app.get("/health")
async def health_check():
    return {"status": "ok"}
