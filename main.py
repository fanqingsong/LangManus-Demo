from agent import LangManusAgent

if __name__ == '__main__':
    agent = LangManusAgent(task="Find a popular open-source project updated recently and summarize its new features with examples and charts.")
    agent.run()