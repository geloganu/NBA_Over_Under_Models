#!/usr/bin/env python
import sys
import time
from simple_term_menu import TerminalMenu

sys.path.insert(0, './src/build/')
from nba_stats_retrieval import *
from build_trailing_database import *

sys.path.insert(0, './src/misc/')
from webscraping_tools import *


def main():
    db = "./src/sql/database.db"
    trailing_db = "./src/sql/trailing.db"
    main_menu_title = "===============================\nNBA Over/Under Prediction Model\n=============================== \nMain Menu.\nPress Q or Esc to quit. \n"
    main_menu_items = ['Build/Update Database', 'Run Model Backtest','Info Page', 'Quit']
    main_menu_cursor = "> "
    main_menu_cursor_style = ("fg_red", "bold")
    main_menu_style = ("bg_red", "fg_yellow")
    main_menu_exit = False
    
    main_menu = TerminalMenu(
        menu_entries=main_menu_items,
        title=main_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )
    build_menu_title = "  Build/Update Database Menu.\n  Press Q or Esc to back to main menu. \n"
    build_menu_items = ["Update Boxscores", "Build Database (stats.nba.com)","Build Trailing Boxscore Data","Back"]
    build_menu_back = False
    build_menu = TerminalMenu(
        build_menu_items,
        title=build_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )
    
    backtest_menu_title = "  Backtesting Menu.\n  Press Q or Esc to back to main menu. \n"
    backtest_menu_items = ["Backtest Neural Network Model", "Backtest Random Forest Model","Back"]
    backtest_menu_back = False
    backtest_menu = TerminalMenu(
        backtest_menu_items,
        title=backtest_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )
    
    info_menu_title = "  Info Page\n  Press Q or Esc to back to main menu. \n\nTo initialize the boxscore, select 'Build/Update Database' page from the main menu and run \nthe 'Build Database (stats.nba.com)' option followed by the 'Build Trailing Boxscore Data' \noption. To create a trailing boxscore dataset, run the 'Build Trailing Boxscore Data' with \nthe desired number of games trailed by. \n \nTo run backtests and simulation, enter the 'Backtesting Menu' and select the desired model."
    info_menu_items = ["Back"]
    info_menu_back = False
    info_menu = TerminalMenu(
        info_menu_items,
        title=info_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )
    
    while not main_menu_exit:
        main_sel = main_menu.show()

        #build menu
        if main_sel == 0:
            while not build_menu_back:
                edit_sel = build_menu.show()
                if edit_sel == 0:
                    print("================================")
                    
                    #update boxscore
                    tables = read_table_names(db)
                    tables = [t for t in tables if t.find('boxscore') != -1]
                    season = tables[-1][-7::]
                    
                    print(f"Fetching statistics from stats.nba.com and updating boxscore for {season} season...\n")
                    
                    update_data(db, season)
                    print("Boxscore updated.")

                    #updates odds data
                    
                    update_database(db, "odds", access_odds_data())
                    print("O/U data updated.")
                    time.sleep(2)
                    
                elif edit_sel == 1:
                    print("================================")
                    seasons = season_range(2017,2022)
                    print(f"Fetching statistics from stats.nba.com and building database for seasons {seasons[0]} to {seasons[-1]}...")
                    for season in tqdm.tqdm(seasons):                       
                        update_data(db, season)
                    print("\nBoxscore database built.")
                    
                    #build odds data
                    update_database(db, "odds", access_odds_data())
                    print("O/U database built.")
                    time.sleep(2)
                    
                elif edit_sel == 2:
                    print("================================")
                    seasons = season_range(2017,2022)
                    n = int(input("Trail by (int): "))
                    
                    trailing_data = build_trailing(trailing_db, seasons, n )
                    print("Trailing database")
                    
                    update_database(trailing_db,  f"{n}_game_trailing", trailing_data)
                    print(f"{n} game trailing database built.")
                    time.sleep(2)
                    
                elif edit_sel == 3 or edit_sel == None:
                    build_menu_back = True
            build_menu_back = False
            
        #backtest menu
        elif main_sel == 1:
            while not backtest_menu_back:
                backtest_sel = backtest_menu.show()
                if backtest_sel == 0:
                    
                    print("To implement")
                    time.sleep(2)
                elif backtest_sel == 1:
                    print("To implement")
                    time.sleep(2)
                elif backtest_sel == 2 or backtest_sel == None:
                    backtest_menu_back = True
                    print("Back Selected")
            backtest_menu_back = False\
                
        #info page
        elif main_sel == 2:
            while not info_menu_back:
                info_sel = info_menu.show()
                if info_sel == 0 or info_sel == None:
                    info_menu_back = True
                    print("Back Selected")
            info_menu_back = False
            
        elif main_sel == 3 or main_sel == None:
            main_menu_exit = True
            print("Quit Selected")

    
if __name__ == '__main__':
    main()