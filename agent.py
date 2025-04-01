from planner import plan_task
from agents.researcher import find_trending_repo
from agents.browser import scrape_github_activity
from agents.coder import analyze_code_activity
from agents.reporter import generate_report

class LangManusAgent:
    def __init__(self, task):
        self.task = task
        self.context = {}

    def run(self):
        steps = plan_task(self.task)
        for step in steps:
            agent = step['agent']
            task = step['task']

            if agent == 'researcher':
                self.context['repo'] = find_trending_repo()

            elif agent == 'browser':
                self.context['repo_data'] = scrape_github_activity(self.context['repo'])

            elif agent == 'coder':
                self.context['analysis'], self.context['chart_path'] = analyze_code_activity(self.context['repo_data'])

            elif agent == 'reporter':
                report = generate_report(
                    self.context['repo'],
                    self.context['repo_data'],
                    self.context['analysis'],
                    self.context['chart_path']
                )
                print(report)

    def run_and_return(self):
        self.run()
        report = generate_report(
            self.context['repo'],
            self.context['repo_data'],
            self.context['analysis'],
            self.context['chart_path']
        )
        return report, self.context['chart_path']