# 乾杯 かんぱい - Kanpai! wordgame

## Application Purpose

Purpose of the **乾杯 かんぱい - Kanpai wordgame** is to learn to read top  Japanese words in a fun and interactive way. The game covers most common Japanese words for e.g. greetings, food, and verbs.

Japanese uses three different syllabary - kanji, hiragana, and katakana (and in some cases the Latin script (known as roomaji)). The words are presented in all these versions, depending on which version is used in real life.

The game is a modified version of a standard word game, and assumes that the players do not necessarily have previous knowledge in Japanese. The player is presented with the different readings of the word and he/she needs to select the correct translation in English (or vice versa).

## User Groups

There are two types of roles in the application, a normal user, i.e. the player, and an admin user.

## User Interface Draft

Below is an updated draft of the user interface.

![Game design document picture](./documentation/pictures/game_design_doc_pic.jpg) 

## Basic Version Functionalities

* User can create a new player, and log in and out as a player or as an admin user.
* User can select which type of words to learn, e.g. greetings, numbers, months, adjectives, verbs, or food.
* User will see different writings in Japanese for a particular word, and select which of the shown translations in English is the correct one.
* There are tips/hints to help the learning process (e.g. words are presented in a standard order).
* User sees their statistics for the particular game (e.g. number of words to learn, number of words learnt).
* User sees statistics for their games over time (games player, number of words to learn / learnt, best time in solving a particular game).
* User sees statistics for other players in the game (e.g. best times to solve particular games, best players in the game, most active players in the application).
* Statistics are presented in a visually pleasing manner.
* User can give feedback on the game and see the feedbacks given by others.
* Error messages are shown on the same page where relevant.
* Admin user can review all feedbacks, answer to them, and delete feedbacks given (hide from view).

## Future Development Ideas
* User sees a word in English and selects the correct Japanese translation. 
* Words are continuously shuffled in the game, within a word category and/or between word categories.
* To add pressure in the game, a clock tracking time spent on the game is shown.
* Statistics are enhanced further. E.g. if there is plenty of usage, it is presented over time in e.g. a line graph by weekday.

## Release and testing

The application is available for testing in [Heroku](https://kanpaiwordgame.herokuapp.com/).

Updated 4.9.2021