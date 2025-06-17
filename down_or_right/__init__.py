from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'down_or_right'
    PLAYERS_PER_GROUP = None 
    NUM_ROUNDS = 1
    DOWN_PERCENT = 90
    LARGE_PILE = cu(4)
    SMALL_PILE = cu(1)

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass 

class Player(BasePlayer):
    level = models.IntegerField()

    choice = models.StringField(
        choices=['Down', 'Right'],
        widget=widgets.RadioSelect,
        label="Choose an option:"
    )

    quiz_q1 = models.StringField(
        choices=[
            ['A', 'Player 2, Player3, Player1'],
            ['B', 'Player 1, Player 3, Player 2'],
            ['C', 'Player 1, Player 2, Player 3'],
            ['D', 'None of the above'],
        ],
        label='Q1. Which of the sequences below is in the correct order?',
        widget=widgets.RadioSelect
    )

    quiz_q2 = models.StringField(
        choices=[
            ['A', '2'],
            ['B', '1'],
            ['C', '3'],
            ['D', '4'],
        ],
        label=f'Q2. How many possible actions can a player select from?',
        widget=widgets.RadioSelect
    )

    quiz_q3 = models.StringField(
        choices=[
            ['A', 'The game continues to the next player'],
            ['B', 'The game ends, and everyone receives money'],
            ['C', 'The game ends. The player receives the large pile, and previous players get the small pile'],
            ['D', 'The game ends. Only the current player gets the small pile'],
        ],
        label='Q3. What happens if a player chooses the action "right"?',
        widget=widgets.RadioSelect
    )

    quiz_q4 = models.StringField(
        choices=[
            ['A', 'The game ends immediately'],
            ['B', 'The game continues, and both piles of money double'],
            ['C', 'Only the small pile doubles, and the game ends'],
            ['D', 'The current player receives no money'],
        ],
        label=f'Q4. What happens if a player chooses "down" and the random number is ≤ {C.DOWN_PERCENT}?',
        widget=widgets.RadioSelect
    )

    quiz_q5 = models.StringField(
        choices=[
            ['A', 'The game continues, and both piles of money double'],
            ['B', 'The game ends. The current and previous players receive the doubled small pile'],
            ['C', 'The game ends. The current player receives nothing, and previous players get the small pile'],
            ['D', 'The game ends. All players get the large pile'],
        ],
        label=f'Q5. What happens if a player chooses "down" and the random number is > {C.DOWN_PERCENT}?',
        widget=widgets.RadioSelect
    )

    quiz_q6 = models.StringField(
        choices=[
            ['A', 'Player X and all previous players'],
            ['B', 'Player X and all subsequent players'],
            ['C', 'Only Player X'],
            ['D', 'No Player'],
        ],
        label='Q6. When the game ends at the choice of player X, who will receive at least some money?',
        widget=widgets.RadioSelect
    )


    quiz_q7 = models.StringField(
        choices=[
            ['A', 'It is randomly assigned after the game starts'],
            ['B', 'It is pre-determined and communicated to you before starting the game'],
            ['C', 'You choose your own position at the beginning'],
            ['D', 'Your position depends on how fast you make decisions'],
        ],
        label='Q7. How is your position in the game sequence determined?',
        widget=widgets.RadioSelect
    )


    quiz_q8 = models.StringField(
        choices=[
            ['A', 'Player 1 chose "down", Player 2-4 chose "right"'],
            ['B', 'Player 1 chose "right", Player 2-4 chose "down"'],
            ['C', 'All of the previous players chose "right"'],
            ['D', 'All of the previous players chose "down"'],
        ],
        label='Q8. If you are Player 5, what have previous players in the sequence chosen?',
        widget=widgets.RadioSelect
    )

    quiz_q9 = models.StringField(
        choices=[
            ['A', 'Immediately after your turn in the game'],
            ['B', 'A few days after completing the study'],
            ['C', 'Before you make your first decision'],
            ['D', 'Depending on your decision'],
        ],
        label='Q9. When will you receive information about other participants’ decisions and your final earnings?',
        widget=widgets.RadioSelect
    )

def creating_session(self):
    for p in self.get_players():
        p.level = (p.participant.id_in_session-1) // 100 + 1

## PAGES 
class Introduction(Page):
    pass
class Instructions1(Page):
    form_model = 'player'
    form_fields = ['quiz_q1', 'quiz_q2']

    def error_message(self, values):
        errors = []

        if values['quiz_q1'] != 'C':
            errors.append("Q1 is incorrect. Please review the rules and try again.")
        if values['quiz_q2'] != 'A':
            errors.append("Q2 is incorrect. Please review the rules and try again.")
        if errors:
            return errors

class Instructions2(Page):
    form_model = 'player'
    form_fields = ['quiz_q3', 'quiz_q4', 'quiz_q5','quiz_q6']
    #template_name = 'down_or_right/Instructions.html'
    def vars_for_template(self):
        return {
            'down_percent': C.DOWN_PERCENT,
            'end_percent': 100 - C.DOWN_PERCENT
        }
    def error_message(self, values):
        errors = []

        if values['quiz_q3'] != 'C':
            errors.append("Q3 is incorrect. Please review the rules and try again.")
        if values['quiz_q4'] != 'B':
            errors.append("Q4 is incorrect. Please review the rules and try again.")
        if values['quiz_q5'] != 'B':
            errors.append("Q5 is incorrect. Please review the rules and try again.")
        if values['quiz_q6'] != 'A':
            errors.append("Q6 is incorrect. Please review the rules and try again.")
        if errors:
            return errors
        
class Instructions3(Page):
    form_model = 'player'
    form_fields = ['quiz_q7','quiz_q8','quiz_q9']

    def error_message(self, values):
        errors = []

        if values['quiz_q7'] != 'B':
            errors.append("Q7 is incorrect. Please review the rules and try again.")
        if values['quiz_q8'] != 'D':
            errors.append("Q8 is incorrect. Please review the rules and try again.")
        if values['quiz_q9'] != 'B':
            errors.append("Q9 is incorrect. Please review the rules and try again.")
        if errors:
            return errors



class Decision(Page):
    def vars_for_template(self):
        return {
            'down_percent': C.DOWN_PERCENT,
            'end_percent': 100 - C.DOWN_PERCENT,
            'large_pile': C.LARGE_PILE * 2**(self.level - 1),
            'small_pile': C.SMALL_PILE * 2**(self.level - 1),
            'doubled_small_pile': C.SMALL_PILE * 2**(self.level)
        }
    form_model = 'player'
    form_fields = ['choice']

class End(Page):
    pass


page_sequence = [Introduction, Instructions1, Instructions2, Instructions3, Decision, End]