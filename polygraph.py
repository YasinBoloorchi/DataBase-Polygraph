# read transactions
transactions_file = open('./transactions.csv')
transactions_data = [transaction.split(',') for transaction in transactions_file.readlines()][0]
transactions_file.close()

print('Transactions -> ',transactions_data)


def get_first_read(transactions):
    for t in transactions:
        if t[0] == 'r':
            return t[1]
    
    return False


def get_last_write(transactions):
    for t in transactions:
        if t[0] == 'w':
            last_write = t[1]
    
    return last_write


def get_trasactions_names(transactions):
    transactions_names = list(set([t.split('(')[0][1::] for t in transactions]))
    transactions_names.sort()
    return transactions_names


def draw_polygraph(transactions_names, first_read, last_write):
    # create an empty graph
    graph = {}
    for t in transactions_names:
        graph[t] = {'childs': []}

    # draw lines from first read to the others
    for t in transactions_names:
        if t == first_read:
            transactions_names_temp = transactions_names.copy()
            transactions_names_temp.remove(t)
            
            for transaction_name in transactions_names:
                if transaction_name != t:
                    graph[t]['childs'].append(transaction_name)

    # draw lines from other nodes to the last write
    for t in transactions_names:
        if t == last_write:
            for transaction_name in transactions_names:
                if transaction_name != t:
                    graph[transaction_name]['childs'].append(t)
    
    # make graph childs set and sorted
    for t in graph:
        childs = list(set(graph[t]['childs']))
        childs.sort()
        graph[t]['childs'] = childs

    return graph


def is_cyclic(node, target ,graph):
    if target not in graph[node]['childs']:
        print('node: ', node, '\tchilds:', graph[node]['childs'], '\ttarget: ', target)
        res = False
        
        for child in graph[node]['childs']:
            if child != node:
                res = is_cyclic(child, target, graph)
        return res

    else:
        return True

    return res


def check_serilizablility(graph):
    for node in graph:
        
        is_cyclic_res = is_cyclic(node, node, graph)

        if is_cyclic_res == True:
            return False

        print('is cyclic: ', is_cyclic_res)
        print('-'*30)
    return True

first_read = get_first_read(transactions_data)
last_write = get_last_write(transactions_data)
print('\nFirs read transaction: ', first_read)
print('Last write transaction: ', last_write)

transactions_names = get_trasactions_names(transactions_data)
print('\ntransactions_names: ', transactions_names)

poly_graph = draw_polygraph(transactions_names, first_read, last_write)
print('\nPoly graph: ', poly_graph, '\n\n')

serilizablity_result = check_serilizablility(poly_graph)

print("\nIs serilizable: ", serilizablity_result)