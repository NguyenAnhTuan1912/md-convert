import configparser

config = configparser.ConfigParser()
config.read("config.ini")

total_of_workers = int(config["program"]["total_of_workers"])
total_of_concurrent_processed_files = int(config["program"]["total_of_concurrent_processed_files"])
ori_folder_name = config["program"]["ori_folder_name"]
out_folder_name = config["program"]["out_folder_name"]