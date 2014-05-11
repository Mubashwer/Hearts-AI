# 16/5/13: update to second test case for is_valid_play(), to correct 'broken' value
# 20/5/13: added a test case for pass_cards(), and modified/greatly expanded the test cases for is_valid_play()

# dictionary of tests, one for each function in the project spec; in each case, list a number of function calls (as a str), and the correct output for each
test_cases = {
    "pass_cards":
        [("""submission.pass_cards(['5S', '4S', '7C'])""",['5S', '4S', '7C']),
        ],

    "is_valid_play":
        [
         # can lead '0D' whether hearts are broken or not
         ("""submission.is_valid_play([], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6C', '7D', '6H', 'JH'],'0D',True)""",True), 
         ("""submission.is_valid_play([], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6C', '7D', '6H', 'JH'],'0D',False)""",True),

         # must follow suit if card of that suit held
         ("""submission.is_valid_play(['KH'], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6C', '7D', '6H', 'JH'],'JH',True)""",True),
         ("""submission.is_valid_play(['KS'], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6C', '7D', '6H', 'JH'],'JH',False)""",False),

         # must play card actually held in hand
         ("""submission.is_valid_play([], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6C', '7D', '6H', 'JH'],'KS',False)""",False),

         # can discard penalty card if no card of the suit lead is held
         ("""submission.is_valid_play(['KC'], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6D', '7D', '6H', 'JH'],'JH',True)""",True),
         ("""submission.is_valid_play(['KC'], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6D', '7D', '6H', 'JH'],'JH',False)""",True),
         ("""submission.is_valid_play(['KC'], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6D', '7D', '6H', 'QS'],'QS',True)""",True),
         ("""submission.is_valid_play(['KC'], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6D', '7D', '6H', 'QS'],'QS',False)""",True),

         # can discard non-penalty card if no card of the suit lead is held
         ("""submission.is_valid_play(['KC'], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6D', '7D', '6H', 'JH'],'9S',True)""",True),
         ("""submission.is_valid_play(['KC'], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6D', '7D', '6H', 'JH'],'9S',False)""",True),

         # can't lead with penalty card if hearts not broken and non-penalty cards in hand
         ("""submission.is_valid_play([], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6D', '7D', '6H', 'JH'],'JH',False)""",False),
         ("""submission.is_valid_play([], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6D', '7D', '6H', 'QS'],'QS',False)""",False),

         # can lead with penalty card if hearts are broken
         ("""submission.is_valid_play([], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6D', '7D', '6H', 'JH'],'JH',True)""",True),
         ("""submission.is_valid_play([], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6D', '7D', '6H', 'QS'],'QS',True)""",True),

         # can lead with a penalty card even if hearts isn't broken, if no non-penalty cards held in hand
         ("""submission.is_valid_play([], ['0H', '9H', '3H', '5H', 'AH', '6H', '7H', 'QS'],'0H',False)""",True),
         ("""submission.is_valid_play([], ['0H', '9H', '3H', '5H', 'AH', '6H', '7H', 'QS'],'QS',False)""",True),
        ],

    "get_valid_plays":
        [("""submission.get_valid_plays([], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6C', '7D', '6H', 'JH', '7S', '2S'],True)""",['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6C', '7D', '6H', 'JH', '7S', '2S']),
         ("""submission.get_valid_plays(['QH'], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6C', '7D', '6H', 'JH', '7S', '2S'],True)""",['3H', '6H', 'JH']),
         ("""submission.get_valid_plays(['QS'], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6C', '7D', '6H', 'JH', '7S', '2S'],True)""",['9S', '3S', '7S', '2S']),
         ("""submission.get_valid_plays(['QC'], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6D', '7D', '6H', 'JH', '7S', '2S'],False)""",['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6D', '7D', '6H', 'JH', '7S', '2S']),
         ("""submission.get_valid_plays([], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6D', '7D', '6H', 'JH', '7S', '2S'],False)""",['0D', '9S', '3S', '3D', '5D', 'AD', '6D', '7D', '7S', '2S']),
        ],

    "score_game":
        [("""submission.score_game([[['5C', '3C', 'JH', 'QS'], ['7H', '8S', '4D', '3D']], [['6H', 'JS', 'JC', '3H'], ['2D', '5S', 'QC', 'KH'], ['AH', '6D', '0S', '4H'], ['2S', '3S', '4C', '4S']], [['9H', '0H', 'KS', 'QD'], ['5D', '8H', '7S', '9S'], ['6S', '0C', '5H', '6C']], [['KC', '8D', 'QH', 'AS'], ['JD', '2H', '0D', '7C'], ['9D', 'KD', 'AC', '9C'], ['7D', '2C', '8C', 'AD']]])""",[(15, False), (5, False), (4, False), (-8, True)]),
         ("""submission.score_game([[['QD', '7D', '5H', '0D'], ['7C', '6D', '2H', 'KS'], ['8S', '3D', '9C', 'KD'], ['4D', '9D', 'KH', '4C']], [['7S', 'JH', '4H', 'QC'], ['2S', 'KC', 'AD', 'AC'], ['JD', '8D', 'QS', '6H'], ['AH', '9H', '9S', '6S']], [['5S', '0S', 'JC', '2D']], [['5D', '8H', '0C', '7H'], ['JS', '6C', '2C', 'AS'], ['3S', '4S', '5C', '0H'], ['3C', 'QH', '3H', '8C']]])""",[(-7, True), (18, False), (0, False), (5, False)]),
         ("""submission.score_game([[['QD', '7D', '5H', '0D'], ['7C', '6D', '2H', 'KS'], ['8S', '3D', '9C', 'KD'], ['4D', '9D', 'KH', '4C'],['7S', 'JH', '4H', 'QC'], ['2S', 'KC', 'AD', 'AC'], ['JD', '8D', 'QS', '6H'], ['AH', '9H', '9S', '6S'],['5S', '0S', 'JC', '2D'],['5D', '8H', '0C', '7H'], ['JS', '6C', '2C', 'AS'], ['3S', '4S', '5C', '0H'], ['3C', 'QH', '3H', '8C']],[],[],[]])""",[(-36, True), (0, False), (0, False), (0, False)]),
        ],

    "play":
        [("""submission.play([[],[],[],[]],['QS'],['JS', '2D', '3H', '5H', '9D', '6H', '7H', 'KH', 'AH', '4C', '7D', '2C', 'QH'],False)""","JS"),
         ("""submission.play([[],[],[],[]],[],['AD', 'KD', 'JD', '0D', '5S', '5S', '9D', '2H', '3H', '5S', '4S', '3S', '2S'],False)""","AS"),
         ],

        }
