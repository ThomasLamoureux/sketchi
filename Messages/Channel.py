# Read me
# The channel_random_string is for keeping track of the channel updates. Everytime a channel is updated on the server in some way,
# this will be randomized as a 5 character string. If the string is different then what is on the client, then the client will update
# the channel and set that string as its random string.



class Channel():
    def request_from_database(self, request):
        return None



    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.message_cache = []
        self.message_cache_range = [0, 50]
        self.channel_loaded = False
        self.channel_random_string = "00000" # This is a weird thing and not very 'good' but its simple and effective; Long explanation at the top


    # This function will handle and overflows in range
    def load_cache(self, range_1, range_2):
        
        if (range_1 < 0):
            range_1 = 0


    def check_channel_updated(self)
        check = "AAAAA" # placeholder

        if self.channel_random_string != check:
            self.update_channel()


    def update_channel(self):
        pass


    def load_channel(self):
        pass


    def open_channel(self):
        if (self.channel_loaded == False):
            load_cache(0, 50)
            load_channel()

            if (self.channel_loaded == False):
                print("Error loading channel.")
                return 

        # Interact with GUI to load messages
        

    
    def load_messages_up():
        if (self.message_cache[0] + self.message_cache[1] > 150):
            load_cache(self.message_cache[0] + 50, self.message_cache[1] + 50)
        else:
            load_cache(self.message_cache[0], self.message_cache[1] + 50)

        load_channel()


    def load_messages_down():
        if (self.message_cache[0] == 0):
            return
            
        if (self.message_cache[1] > 150):
            load_cache(self.message_cache[0] - 50, self.message_cache - 50)
        else:
            load_cache(self.message_cache[0], self.message_cache[1] + 50)

        load_channel()
