# CS410-Movie-Review-Rating-System

Instructions
```
cd backend
python3 -m venv venv
source venv/bin/activate
pip3 install flask
pip3 install selenium
pip3 install numpy
pip3 install nltk
python3 api.py
```

```
cd frontend
npm install axios
npm start
(sometimes you have to do 'npx create-react-app frontend' and migrate all the files from the current frontend folder to the new frontend folder and rerun the commands above to run the react app)
```

Abstract: \
We are planning on making a system that can recommend whether or not to watch a movie that a user inputs. We want to do this by taking in movie reviews from Rotten Tomatoes and IMDB and sorting the reviews based on positive reviews and negative reviews. We will do this by looking at key words within the reviews and sorting based on an algorithm. This algorithm will use data to train a model and assign probabilities to words on how often they appear in positive or negative reviews. Then, based on those probabilities, we will scan through new reviews and label them as positive or negative. We will then create a percentage based on how many positive reviews there are and how many negative reviews there are for a given movie. This percentage will be how likely we are to recommend this movie to the user.

Introduction: \
Another week means another cycle of scrolling through Netflix summaries and rotten tomatoes reviews - just to fall asleep on the couch without having even started a movie. Is this you too? Through our movie recommender system, you are able to take away your need to make decisions - at least for a nice night in. This is your time to relax. Based on all the reviews collected from the same sites you spend hours searching through, we’ll come up with a simple answer for you: yes or no. One less thing to worry about.

We want to create this system to make life easier for users. By clearly recommending whether a user will enjoy a movie based on other users' movie reviews, we help an individual simplify a mundane task.

Link to IMDB Dataset in CSV Format: \
https://uillinoisedu-my.sharepoint.com/:x:/g/personal/khushim2_illinois_edu/EbJg-geF865Fp6v9mDnU8AABTpbEFlIk3Yd5pRi_Ns7WCg?e=2MfjzS&nav=MTVfe0Q4NTFBQUMzLUY5MzctNEU0Ny1BOTI5LTkxOTdFOTAxMDU1Q30
>>>>>>> 866e0df416dde1f29d924f469231e3085c50de1a
