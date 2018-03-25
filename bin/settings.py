import bin.my_lib.json_read_write as json_read_write
config = json_read_write.read("c:\\printer\\config.json")
SITE = config["site"]
SHOP_TEL = config["shop_tel"]
WORKPLACE = config["workplace"]
PROJECT_NAME = "cloud_printing_client"
