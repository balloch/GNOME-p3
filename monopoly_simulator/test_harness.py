import os, sys
upper_path = '/'.join(os.getcwd().split('/')[:-1])
sys.path.append(upper_path)
import numpy as np
from monopoly_simulator import gameplay
from monopoly_simulator import gameplay_socket
from monopoly_simulator import novelty_generator
from monopoly_simulator import background_agent_v3_1
from monopoly_simulator.server_agent_serial import ServerAgent
from monopoly_simulator.logging_info import log_file_create
import os
import shutil
import json

agent_combination_1 = [[background_agent_v3_1, background_agent_v3_1, background_agent_v3_1]]


def play_tournament_without_novelty(tournament_log_folder=None, meta_seed=5, num_games=100):
    """
    Tournament logging is not currently supported, but will be soon.
    :param tournament_log_folder: String. The path to a folder.
    :param meta_seed: This is the seed we will use to generate a sequence of seeds, that will (in turn) spawn the games in gameplay/simulate_game_instance
    :param num_games: The number of games to simulate in a tournament
    :return: None. Will print out the win-loss metrics, and will write out game logs
    """

    if not tournament_log_folder:
        print("No logging folder specified, cannot log tournaments. Provide a logging folder path.")
        raise Exception

    np.random.seed(meta_seed)
    big_list = list(range(0,1000000))
    np.random.shuffle(big_list)
    tournament_seeds = big_list[0:num_games]
    winners = list()
    count = 1

    folder_name = "../tournament_logs" + tournament_log_folder
    try:
        os.makedirs(folder_name)
        print('Logging gameplay')
    except:
        print('Given logging folder already exists. Clearing folder before logging new files.')
        shutil.rmtree(folder_name)
        os.makedirs(folder_name)

    metadata_dict = {
        "function": "play_tournament_without_novelty",
        "parameters": {
            "meta_seed": meta_seed,
            "num_game": num_games
        }
    }

    json_filename = folder_name + "tournament_meta_data.json"
    out_file = open(json_filename, "w")
    json.dump(metadata_dict, out_file, indent=4)
    out_file.close()

    for t in tournament_seeds:
        print('Logging gameplay for seed: ', str(t), ' ---> Game ' + str(count))
        filename = folder_name + "meta_seed_" + str(meta_seed) + '_num_games_' + str(count) + '.log'
        logger = log_file_create(filename)
        winners.append(gameplay.play_game_in_tournament(t))
        handlers_copy = logger.handlers[:]
        for handler in handlers_copy:
            logger.removeHandler(handler)
            handler.close()
            handler.flush()
        count += 1

    print(winners)


def play_tournament_with_novelty_1(tournament_log_folder=None, meta_seed=5, num_games=100, novelty_index=23, novelty_info=False):
    """
    Use this function for the normal gameplay without socket communication
    :param tournament_log_folder:
    :param meta_seed:
    :param num_games:
    :param novelty_index: an integer between 1 and num_games-1. We will play this many games BEFORE introducing novelty.
    :param novelty_info: boolean that specifies if the agent will be notified when novelty is injected or not.
    :return:
    """

    if not tournament_log_folder:
        print("No logging folder specified, cannot log tournaments. Provide a logging folder path.")
        raise Exception

    np.random.seed(meta_seed)
    big_list = list(range(0, 1000000))
    np.random.shuffle(big_list)
    tournament_seeds = big_list[0:num_games]
    winners = list()
    count = 1

    folder_name = "../tournament_logs" + tournament_log_folder
    try:
        os.makedirs(folder_name)
        print('Logging gameplay')
    except:
        print('Given logging folder already exists. Clearing folder before logging new files.')
        shutil.rmtree(folder_name)
        os.makedirs(folder_name)

    metadata_dict = {
        "function": "play_tournament_with_novelty_1",
        "parameters": {
            "meta_seed": meta_seed,
            "novelty_index": novelty_index,
            "num_game": num_games
        }
    }

    json_filename = folder_name + "tournament_meta_data.json"
    out_file = open(json_filename, "w")
    json.dump(metadata_dict, out_file, indent=4)
    out_file.close()

    for t in range(0,novelty_index):
        print('Logging gameplay without novelty for seed: ', str(tournament_seeds[t]), ' ---> Game ' + str(count))
        filename = folder_name + "meta_seed_" + str(meta_seed) + '_without_novelty' + '_num_games_' + str(count) + '.log'
        logger = log_file_create(filename)
        winners.append(gameplay.play_game_in_tournament(tournament_seeds[t], novelty_info))
        handlers_copy = logger.handlers[:]
        for handler in handlers_copy:
            logger.removeHandler(handler)
            handler.close()
            handler.flush()
        count += 1

    new_winners = list()
    for t in range(novelty_index, len(tournament_seeds)):
        print('Logging gameplay with novelty for seed: ', str(tournament_seeds[t]), ' ---> Game ' + str(count))
        filename = folder_name + "meta_seed_" + str(meta_seed) + '_with_novelty' + '_num_games_' + str(count) + '.log'
        logger = log_file_create(filename)
        new_winners.append(gameplay.play_game_in_tournament(tournament_seeds[t], novelty_info, class_novelty_1))
        handlers_copy = logger.handlers[:]
        for handler in handlers_copy:
            logger.removeHandler(handler)
            handler.close()
            handler.flush()
        count += 1

    print('pre_novelty winners', winners)
    print('post_novelty_winners', new_winners)


def play_tournament_with_novelty_2(tournament_log_folder=None, nov=None, meta_seed=5, num_games=100, novelty_index=25, novelty_info=False):
    """
    Use this function when using the the server-clent agent to communicate over the socket
    :param tournament_log_folder: String. The path to a folder.
    :param meta_seed: This is the seed we will use to generate a sequence of seeds, that will (in turn) spawn the games in gameplay/simulate_game_instance
    :param novelty_index: game from which novelty will be injected
    :param num_games: The number of games to simulate in a tournament
    :param novelty_info: boolean that specifies if the agent will be notified when novelty is injected or not.
    :return: None. Will print out the win-loss metrics, and will write out game logs
    """

    if not tournament_log_folder:
        print("No logging folder specified, cannot log tournaments. Provide a logging folder path.")
        raise Exception

    np.random.seed(meta_seed)
    big_list = list(range(0,1000000))
    np.random.shuffle(big_list)
    tournament_seeds = big_list[0:num_games]
    winners = list()
    count = 1

    for i in range(len(agent_combination_1)):
        folder_name = "../tournament_logs" + tournament_log_folder + '_comb_' + str(i) + '/'
        try:
            os.makedirs(folder_name)
            print('Logging gameplay')
        except:
            print('Given logging folder already exists. Clearing folder before logging new files.')
            shutil.rmtree(folder_name)
            os.makedirs(folder_name)

        metadata_dict = {
            "function": "play_tournament_without_novelty",
            "parameters": {
                "meta_seed": meta_seed,
                "num_game": num_games,
                "novelty_index": novelty_index
            }
        }

        json_filename = folder_name + "tournament_meta_data.json"
        out_file = open(json_filename, "w")
        json.dump(metadata_dict, out_file, indent=4)
        out_file.close()

        # define agent
        agent = ServerAgent()
        f_name = 'play game without novelty'
        if not agent.start_tournament(f_name):
            print("Unable to start tournament")
            exit(0)
        else:
            pass

        for t in range(0,novelty_index):
            print('Logging gameplay without novelty for seed: ', str(tournament_seeds[t]), ' ---> Game ' + str(count))
            filename = folder_name + "meta_seed_" + str(meta_seed) + '_without_novelty' + '_num_games_' + str(count) + '.log'
            logger = log_file_create(filename)
            winners.append(gameplay_socket.play_game_in_tournament_socket(tournament_seeds[t], agent, agent_combination_1[i][0], agent_combination_1[i][1],
                                                                          agent_combination_1[i][2], novelty_info))
            handlers_copy = logger.handlers[:]
            for handler in handlers_copy:
                logger.removeHandler(handler)
                handler.close()
                handler.flush()
            count += 1

        new_winners = list()
        for t in range(novelty_index, len(tournament_seeds)):
            print('Logging gameplay with novelty for seed: ', str(tournament_seeds[t]), ' ---> Game ' + str(count))
            filename = folder_name + "meta_seed_" + str(meta_seed) + '_with_novelty' + '_num_games_' + str(count) + '.log'
            logger = log_file_create(filename)
            new_winners.append(gameplay_socket.play_game_in_tournament_socket(tournament_seeds[t], agent, agent_combination_1[i][0], agent_combination_1[i][1],
                                                                              agent_combination_1[i][2], novelty_info, class_novelty_1))
            handlers_copy = logger.handlers[:]
            for handler in handlers_copy:
                logger.removeHandler(handler)
                handler.close()
                handler.flush()
            count += 1

        print("Pre-novelty winners: ", winners)
        print("Post-novelty winners: ", new_winners)


def class_novelty_1(current_gameboard,novelty_type='price'):
    """
    Types: 'mortgage', 'bank', 'price', 'endpoints', 'sequence', 'endpoints',
            'cardquantity', 'colors', 'dice', 'carddestination', 'cardmoney'
    """
    ## price
    if novelty_type == 'price':
        inanimateNovelty = novelty_generator.InanimateAttributeNovelty()
        asset_lists = ["Mediterranean Avenue", "Baltic Avenue", "Reading Railroad", "Oriental Avenue", "Vermont Avenue",
                       "Connecticut Avenue", "St. Charles Place", "Electric Company", "States Avenue",
                       "Virginia Avenue", "Pennsylvania Railroad", "St. James Place", "Tennessee Avenue",
                       "New York Avenue", "Kentucky Avenue", "Indiana Avenue", "Illinois Avenue", "B&O Railroad",
                       "Atlantic Avenue", "Ventnor Avenue", "Water Works", "Marvin Gardens", "Pacific Avenue",
                       "North Carolina Avenue", "Pennsylvania Avenue", "Short Line", "Park Place", "Boardwalk"]
        num = 0
        for asset in asset_lists:
            num += 1
            if num >= 0 and num < 10:
                inanimateNovelty.price_novelty(current_gameboard['location_objects'][asset], 1499)

    ## Mortgage
    elif novelty_type == 'mortgage':
        morNovelty = novelty_generator.InanimateAttributeNovelty()
        mor_location = current_gameboard['location_objects']["Mediterranean Avenue"]
        morNovelty.mortgage_novelty(mor_location, 40)

    ## Bank
    elif novelty_type == 'bank':
        contingentattributenovelty = novelty_generator.ContingentAttributeNovelty()
        contingentattributenovelty.change_property_sell_percentage(current_gameboard,
                                                                   0.4)

    ## Reorder gameboard
    elif novelty_type == 'endpoints':
        granularityNovelty = novelty_generator.GranularityRepresentationNovelty()
        granularityNovelty.granularity_novelty(current_gameboard,
                                               current_gameboard['location_objects']['Baltic Avenue'],
                                               6)
        granularityNovelty.granularity_novelty(current_gameboard,
                                               current_gameboard['location_objects']['States Avenue'],
                                               20)
        granularityNovelty.granularity_novelty(current_gameboard,
                                               current_gameboard['location_objects']['Tennessee Avenue'],
                                               27)
        granularityNovelty.granularity_novelty(current_gameboard,
                                               current_gameboard['location_objects']['Park Place'],
                                               52)

    ## Reorder the sequence
    elif novelty_type == 'sequence':
        spaceordernovelty = novelty_generator.SpatialRepresentationNovelty()
        new_location_sequence = ["Go", "Community Chest", "Mediterranean Avenue", "Baltic Avenue", "Income Tax", "Reading Railroad",
                                 "Oriental Avenue", "Chance", "Vermont Avenue", "Connecticut Avenue", "In Jail/Just Visiting",
                                 "St. Charles Place", "Electric Company", "States Avenue", "Virginia Avenue", "Pennsylvania Railroad",
                                 "St. James Place", "Community Chest", "Tennessee Avenue", "New York Avenue", "Free Parking",
                                 "Kentucky Avenue", "Chance", "Indiana Avenue", "Illinois Avenue", "B&O Railroad", "Atlantic Avenue",
                                 "Ventnor Avenue", "Water Works", "Marvin Gardens", "Go to Jail", "Pacific Avenue",
                                 "North Carolina Avenue", "Community Chest", "Pennsylvania Avenue", "Short Line", "Chance",
                                 "Park Place", "Luxury Tax", "Boardwalk"]
        spaceordernovelty.global_reordering(current_gameboard,
                                            new_location_sequence)
        print(current_gameboard['location_sequence'])

    ## Reorder the colors
    elif novelty_type == 'colors':
        spatialNovelty = novelty_generator.SpatialRepresentationNovelty()
        spatialNovelty.color_reordering(current_gameboard, ['Boardwalk', 'Park Place'], 'Blue')

    ## Dice
    elif novelty_type == 'dice':
        numberDieNovelty = novelty_generator.NumberClassNovelty()
        numberDieNovelty.die_novelty(current_gameboard, 2, die_state_vector=[[1,2,3,4,5,6],[1,2,3,4,5,6]])
        classDieNovelty = novelty_generator.TypeClassNovelty()
        # die_state_distribution_vector = ['uniform','uniform','biased','biased']
        die_state_distribution_vector = ['biased', 'uniform']
        die_type_vector = ['odd_only','even_only']
        classDieNovelty.die_novelty(current_gameboard, die_state_distribution_vector, die_type_vector)

    ## Card Quantity
    elif novelty_type == 'cardquantity':
        numberCardNovelty = novelty_generator.NumberClassNovelty()
        community_chest_cards_num = {"go_to_jail":1}
        chance_cards_num = {"go_to_jail":1}
        numberCardNovelty.card_novelty(current_gameboard, community_chest_cards_num, chance_cards_num)

    ## Card - destination
    elif novelty_type == 'carddestination':
        desCardNovelty = novelty_generator.InanimateAttributeNovelty()
        community_chest_card_destinations, chance_card_destinations = dict(), dict()
        community_chest_card_destinations['advance_to_go'] = location.ActionLocation("action", 'Chance', 36, 37, "None", "pick_card_from_chance")
        desCardNovelty.card_destination_novelty(current_gameboard, community_chest_card_destinations, chance_card_destinations)

    ## Card - Amount
    elif novelty_type == 'cardmoney':
        cardamountNovelty = novelty_generator.InanimateAttributeNovelty()
        community_chest_card_amounts = dict()
        key = "sale_of_stock"
        community_chest_card_amounts[key] = 60
        cardamountNovelty.card_amount_novelty(current_gameboard, community_chest_card_amounts=community_chest_card_amounts)

    ## New Cards
    else:
        classCardNovelty = novelty_generator.TypeClassNovelty()
        novel_cc = dict()
        novel_cc["street_repairs"] = "alternate_contingency_function_1"
        novel_chance = dict()
        novel_chance["general_repairs"] = "alternate_contingency_function_1"
        classCardNovelty.card_novelty(current_gameboard,
                                      novel_cc,
                                      novel_chance)

#All the tournaments get logged in seperate folders inside ../tournament_logs folder
try:
    os.makedirs("../tournament_logs/")
except:
    pass

#Specify the name of the folder in which the tournament games has to be logged in the following format: "/name_of_your_folder/"
# play_tournament_without_novelty('/tournament_without_novelty_4/', meta_seed=10, num_games=10)
play_tournament_with_novelty_2(tournament_log_folder='/tournament_with_novelty/', meta_seed=15, num_games=20, novelty_index=10, novelty_info=True)
