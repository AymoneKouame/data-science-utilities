def ml_model_recommender():
    #Is this supervised or unsupervised?
    model_dd1 = {'yes':'supervised', 'no':'unsupervised'}
    correct_answers = f"{tuple(model_dd1.keys())}".replace("'",'').replace(",",' or').replace("(",':').replace(")",'')

    sup_or_unsup = input(f'''
    Let's get started. Please answer the following questions:

    (1) Does your data include the variable you want to predict? Please answer with: {correct_answers}.''')

    try:
        answer1 = model_dd1[sup_or_unsup.strip()]
    except KeyError:
        print(f'Please answer with one of {correct_answers2}')


    #If supervised, is this regresion or classification
    if sup_or_unsup == 'yes':
        model_dd2 = {'continuous':'regression', 'categorical':'classification or regression', 'time-series': "time-series"}
        model_examples_dd2 = {'continuous':'linear regression, tree-based regression '
                          , 'categorical':'logistic regression, tree-based regression'
                          , 'time-series': "ARIMA, smooth-based, moving average"}

        correct_answers2 = f"{tuple(model_dd2.keys())}".replace("'",'').replace(",",' or').replace(")",':').replace("(",'')
        reg_or_class = input(f'''
    (2) Is the variable you want to predict continuous/numeric or categorical or time-series? Please answer with: {correct_answers2}
     ''')
        try:
            answer2 = model_dd2[reg_or_class.strip()]
            model_examples = model_examples_dd2[reg_or_class]
        except KeyError:
            print(f'Please answer with one of {correct_answers2}')

    elif sup_or_unsup == 'no':
        model_dd3 = {'grouping':'clustering', 'relationship':'association', 'data reduction':'dimensionality reduction'}
        model_examples_dd3 = {'grouping':'kmeans clustering'
                          , 'relationship':'Association rule learning, Principal component analysis'
                          , 'data reduction': "Principal component analysis"}

        correct_answers2 = f"{tuple(model_dd2.keys())}".replace("'",'').replace(",",' or').replace(")",':').replace("(",'')

        unsup_model = input(f'''
    (2) Are you trying to group data points together or identify underlying relationships within your data or reduce your dataset dimensions?
    Please answer with: {correct_answers2}. ''')
        try:
            answer2 = model_dd3[unsup_model.strip()]
            model_examples = model_examples_dd3[unsup_model]
        except KeyError:
            print(f'Please answer with one of {correct_answers2}')


    print(f'''
    Based on your answers, we recommend:

    A(n) {answer1} model using a {answer2} algorithm. 
    Popular examples are: {model_examples} algorithms.''')
