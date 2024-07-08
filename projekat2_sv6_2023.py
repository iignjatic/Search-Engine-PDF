from search import *
#nltk.download('punkt')

if __name__ == "__main__":
    # g = creating_graph()        
    # trie = form_trie(os.listdir("txtPages/"))
    # storeGraph(g)
    # storeTrie(trie)
    g = loadGraph()            
    trie = loadTrie()

    while True:
        more = ""
        user_input = input("Pretrazite..").strip()
        is_operator = False

        for operator in operators:
            if operator in user_input:
                more = search_with_operators(g,trie,more,user_input)
                is_operator = True
        
        if len(user_input) > 0:
            if is_operator == False and user_input[-1] != '*':
                more = search(g,trie,more,user_input)


            if user_input[-1] == '*':
                autocomplete = trie.autocomplete(user_input[0:len(user_input)-1])
                autocomplete = list(set(autocomplete))

                counter = 0
                for result in autocomplete:
                        if counter == 7:
                            break
                        print(result)
                        counter += 1
        
            
        if more == 'x' :
                break        

