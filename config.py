TOKEN = 'SECRET_TOCKEN'
PREFIX = '!'


CATEGORIES = {
    'custom': {
        'id': 916606887737303060,
        'info_channel_id': 932001990731497522,
        'create_channels': {
            946123950700773456: {
                'name_pattern': "Канал {}",
                'user_limit': 0,
            },
        }
    },

    'csgo': {
        'id': 881961412879089714,
        'info_channel_id': 932001404854341702,
        'create_channels': {
            932595991964704829: {
                'name_pattern': "Дуо {}",
                'user_limit': 2,
            },
            932596094335082506: {
                'name_pattern': "Трио {}",
                'user_limit': 3,
            },
            932596130905214986: {
                'name_pattern': "Арены {}",
                'user_limit': 3,
            },
        }
    },

    'apex': {
        'id': 602812759117135873,
        'info_channel_id': 932001461569749014,
        'create_channels': {
            932596195673640960: {
                'name_pattern': "Напарники {}",
                'user_limit': 2,
            },
            932596281984045096: {
                'name_pattern': "Соревновательный {}",
                'user_limit': 5,
            },
            932596325093085244: {
                'name_pattern': "Faceit {}",
                'user_limit': 5,
            },
            932596375798046760: {
                'name_pattern': "Запретная зона {}",
                'user_limit': 2,
            },
        }
    },
}


CHANNELS_ID = {
    'new_members': 448125360115154975,
    'raports': 491973951636111378,
    'test': 719591796119961640,
    'main': 448125031751483402,
    'custom': 916723984467394630,
    'score': 930886165618384926,
    'duels': 948657490235621396
}


REACTION_POSTS = {
    'main': {
        'id': 759478163897843712,
        'reactions': {
            '🔫': 759477045062795274,
            '💽': 759476657403854933,
            '🎖️': 881962904017059870,
            '👉': 952202566064803850,
        },
    }
}

ROLES_INFO = {
    492721131900370954: 0,
    480745413402558464: 40 * 60,
    446339392743800852: 120 * 60,
    471374033640882177: 240 * 60,
    480743599781445652: 480 * 60,
    448098549993963520: 720 * 60,
    481469189375262721: 960 * 60,
    448511190402990110: 1200 * 60,
    448120860247851008: 1440 * 60,
    482586466497593373: 1920 * 60,
    482586584932155393: 2400 * 60,
    483671007203426314: 2880 * 60,
    446339198853709824: 3360 * 60,
    471373357321945118: 4080 * 60,
    678682292100792392: 4800 * 60,
    481802232505827329: 6000 * 60,
}