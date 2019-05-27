class Const:
    ''' List of buttons in inlinekeyboard '''
    mainInKeyBoard=[
        {'text': u'Office Admin 👨🏻‍💼', 'callback_data': 'department_officeadmin'},
        {'text': u'K Room 🖥️', 'callback_data': 'department_kroom'},
        {'text': u'Sales 🈹', 'callback_data': 'department_sales'},
        {'text': u'k Play 👩‍💻', 'callback_data': 'department_kplay'}
        ]
    peopleKeyBoard=[
        #{'text': u'{name}', 'callback_data': 'people_{department}_{tid}'},
    ]

    ''' List of buttons in inlinekeyboard '''
    approvalInKeyBoard=[
        {'text': u'Done', 'callback_data': 'done'},
        {'text': u'Reject', 'callback_data': 'reject'},
        {'text': u'Reassign', 'callback_data': 'reassign_{dep}_{tid}'}  
        ]
    task_levelInKeyBoard=[
        {'text': u'Urgent', 'callback_data': 'urgent'},
        {'text': u'ASAP', 'callback_data': 'asap'},
        {'text': u'Add More', 'callback_data': 'add more'}  
        ]   

    menu_keyboard = [['set Task'], ['view tasks']]
