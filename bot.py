
from nps import chatBot

def main():
    print("Welcome to the chatbot. Please wait while the system trains hard!")
    bot = chatBot()
    bot.trainSet()
    bot.statistics()
    print()
    print("Begining interactive chat. To exit, press Ctrl-D")
    print()
    bot.talk()

if __name__ == "__main__":
    main()
