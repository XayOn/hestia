from aiohttp import web
from gql import gql
from random import randint
from datetime import datetime
from collections import Counter
from itertools import chain


class Rule:
    def __init__(self, rule, recipes, calendar):
        # Split the calendar into the days this rule will have to apply for
        self.rule = rule
        self.recipes = [
            a for a in recipes if a['rule']['id'] == self.rule['id']
        ]
        if len(recipes) < rule['frecuency_times']:
            raise Exception('Not enough recipes to satisfy rules')

        self.days_chunks = [
            calendar[b:b + rule['frecuency_days']]
            for b in range(0, len(calendar), rule['frecuency_days'])
        ]

    def chunk_complete(self, days):
        # In the whole chunk it should be.
        iterable = [[b['rule']['id'] for b in a['recipes']] for a in days]
        for a in days:
            print(a)
            for rule in a['recipes']:
                print(rule)
        counter = Counter(chain.from_iterable(iterable))
        return counter[self.rule['id']] >= self.rule['frecuency_times']

    def execute_rule(self):
        while not all(self.chunk_complete(days) for days in self.days_chunks):
            for days in self.days_chunks:
                if not self.chunk_complete(days):
                    rlen = len(self.recipes) - 1
                    day = randint(0, len(days) - 1) if len(days) > 0 else 0
                    rec = randint(0, rlen) if len(self.recipes) > 0 else 0
                    days[day]['recipes'].append(self.recipes.pop(rec))

class Calendar:
    """Each <frecuency_days> we need to have eaten, from a specific rule
    (<id>), <> times. Ranging from date_from to date_to and
    with times_day eating times.
    """
    def __init__(self, from_date, to_date):
        from_dt = datetime.strptime(from_date, '%Y-%m-%d')
        to_dt = datetime.strptime(to_date, '%Y-%m-%d')
        self.days = [dict(recipes=[]) for _ in range((from_dt - to_dt).days)]

    def generate(self, recipes):
        """Aggregate recipes's rules by duration """
        rules = {tuple(recipe['rule'].items()) for recipe in recipes}
        rules = [Rule(dict(rule), recipes, self.days) for rule in rules]
        for rule in rules:
            rule.execute_rule()
        return self.days


async def index(request):
    """Generate a weekly menu.

    Query hasura for recipes and rules, and generate a set of per-day recipes.
    Return it in the following format:

    {"day": [recipe_id, recipe_id, recipe_id]}
    """
    input = await request.json()
    recipes = await request.app['hasura'].execute_async(
        gql("""query RecipeRules {recipe {
            id rule {id frecuency_days frecuency_times}}}"""))
    recipes = recipes['recipe']

    return web.json_response(
        dict(ids=Calendar(input['from'], input['to']).generate(recipes)))
