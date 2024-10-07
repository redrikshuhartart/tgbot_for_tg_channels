from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN") 
ADMINS = env.list("ADMINS") 
CHANNELS = env.list("CHANNELS")
TARGET_CHANNEl = env.str("TARGET_CHANNEl")
TEST_CHANNEL = env.str("TEST_CHANNEL")
