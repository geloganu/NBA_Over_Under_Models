# NBA_Playoffs

Over/Under prediction model using neural networks/random forest models. Trained on historical NBA game data and trends. Given that the playing styles of current NBA teams have gone through tremendous changes in the past into an offensive focused game, I decided to omit games before 2017. 

## Install

In Mac OS, clone the repository using the following command:

```
$ npm git clone https://github.com/geloganu/NBA_Over_Under_Models.git
```

In the same directory, install the required packages.

```
$ pip install -r requirements.txt
```

To run the program:

```
$ pip python run.py
```

## Usage

To initialize the boxscore, select 'Build/Update Database' page from the main menu and run the 'Build Database (stats.nba.com)' option followed by the 'Build Trailing Boxscore Data' option. This will create a SQL database file containing the relevant boxscore data since 2017. 

To create a trailing boxscore dataset, run the 'Build Trailing Boxscore Data' with the desired number of games trailed by. To update the boxscore dataset with the most current game data, run 'Update Boxscores'. 

(Work in progress) To fine tune the model, enter the 'Run Model Backtest' menu to fine tune the desired ML model. This will run a simulation for the entire season desired. For example, you may run the model for the entirety of the 2022 season and test the accuracy of the prediction output as the season is played out. You can also change various parameters of the model.

## License

MIT © [geloganu](https://github.com/geloganu)