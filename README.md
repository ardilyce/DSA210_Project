# Chess.com Data Analysis Project

## Overview
The aim of this project is to analyze and predict chess game outcomes based on key factors, such as the **rating differential** between players and their **opening choices**. Using a dataset of historical chess games, I employed various data analysis techniques, including statistical testing and machine learning, to identify patterns and build a predictive model for game outcomes. The presentation can be found in this link: [link]

## Project Description
I started with data obtained from my games on Chess.com, focusing on extracting important features like player ratings, game outcomes, and opening moves. The main goal was to assess the impact of **rating differential** and **opening choices** on whether a game results in a win or loss.

### Data Preprocessing
- I **cleaned the dataset** by handling missing values, ensuring the data was structured properly for analysis.
- **Rating Differential** was calculated for each game by subtracting my rating from my opponent's rating, and I used that as one of the features for prediction.
- **Game results** were encoded as Win = 2, Loss = 0, and Draw = 1 for use in machine learning.
- **One-hot encoding** was applied to categorical features like `Time Class` and `Main Opening` to prepare the data for the model.

### Statistical Analysis and Hypothesis Testing
I used **statistical testing** to explore the relationships between game outcomes and features like rating differential:
- **Z-tests** was performed to test the significance of rating differential on game outcomes (Win/Loss).

### Machine Learning
After preprocessing, I trained a **Random Forest Classifier** to predict the outcome of a game based on various features:
- **Features**: My Elo, Rival Elo, Rating Differential, Time Class, and Main Opening
- **Target**: Game Outcome: Win or Lose (Draw is included for one of the ML models. Since number of draws are limited, I included them in one model and not to other one.)
- I used **80% of the data for training** and **20% for testing** to evaluate the model's performance.
- **SMOTE** was applied for handling class imbalance in the dataset.
- The model was evaluated using metrics such as **accuracy**, **confusion matrix**.

### Visualization
Several **visualizations** were used to explore the data:
- **Line Plot**: To show the smotothed rating trends for different time formats.
- **Bar and Box plots**: To analyze win rates by rating differential and opening.
- **Confusion Matrix**: To evaluate the performance of the classification model.
- **Density Plot**: To visualize the distribution of the rating differential between Win and Loss outcomes.
  
### Hypothesis Testing Results
__Null Hypothesis (H₀):__ The rating differential between the two players does not significantly affect the outcome of the game. This means that the rating differential does not influence whether the result will be a win or a loss.

__Alternative Hypothesis (H₁):__ The rating differential between the two players significantly affects the outcome of the game. This means that the rating differential influences the likelihood of a win or a loss.

- I tested the hypothesis that **rating differential** influences the outcome of the game. Using Z-test, I found that rating differential **does** have a significant effect on game outcomes, with lower rating differentials (i.e I have greater rating than my opponent) correlating with a higher probability of winning. So I rejected the null hypothesis.

## Results and Insights
- **Rating Differential**: The analysis confirmed that a lower rating differential generally correlates with a higher win rate. Rating differential is calculated by subtracting my ELO from my opponent's ELO. (Lower difference means my rating is greater than my opponent.)
- **Machine Learning Model**: The Random Forest model was able to predict the outcome of the games with reasonable accuracy (~70%). It performed better in predicting wins, and whether including the draws or not only affected accuracy by 2% percent.
- I find that Reti and English are my most played openings but Italian has provided me better winning chances. (I excluded openings with less than 10 games.) In average I played more games at weekends but not a significant difference occured. Number of *online* games played is low while I'm in campus, but the reason is that I played more over the board (OTB) matches.  

## Model Evaluation
The trained model's **accuracy** was evaluated using a confusion matrix, which helped to assess the precision and recall of the model's predictions. Although the model was strong at predicting wins, its performance for losses could be further improved by adjusting class weights and trying different machine learning algorithms.

## Conclusion
This project provided a detailed analysis of my chess games, uncovering patterns in the rating differential and opening moves that affect game outcomes. By combining statistical analysis with machine learning, I was able to create a model that predicts game outcomes based on historical data. The project also highlighted some interesting trends, such as the impact of certain openings and the role of rating differential in determining the outcome.
