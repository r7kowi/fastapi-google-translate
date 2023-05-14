# google-translate-api by koviTek solutions
=============================================

### Description

The purpose of this API is to provide word translations as well as some extra attributes such as;
 
- alternative translation
- synonyms (in source language)
- definition (in source language)
- example use (in source language)

The solution utilises googletrans python package an unofficial Google Translate API as the official
tool only provides translation, no additional characteristics. This API also keeps expanding its own
database so if a word is not already saved in the db it makes a call to googletrans API then saves the 
word and its attributes in its own database for future use.


