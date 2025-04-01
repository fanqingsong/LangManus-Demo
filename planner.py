def plan_task(user_query):
    return [
        {'agent': 'researcher', 'task': 'Find trending repo'},
        {'agent': 'browser', 'task': 'Scrape GitHub activity'},
        {'agent': 'coder', 'task': 'Analyze recent commits and features'},
        {'agent': 'reporter', 'task': 'Generate Markdown report'}
    ]