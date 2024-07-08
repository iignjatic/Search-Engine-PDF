from graph import * 
from trie import *
import nltk             #za parsiranje po recenicama prepoznavanjem znakova interpunkcije
import pageRank as pageRank
import pickle
import pdfConverter


BRIGHT_GREEN = '\033[92m'
RESET = '\033[0m'

operators = ['AND', 'OR', 'NOT']

def storeGraph(g):
     # koristi binarni mod
    graphFile = open('graphFile', 'wb')
     
    # izvor, destinacija
    pickle.dump(g, graphFile)                    
    graphFile.close()
 

def loadGraph():
    #citanje u binarnom modu
    graphFile = open('graphFile', 'rb')    
    g = pickle.load(graphFile)
    graphFile.close()

    return g

def storeTrie(t):
    trieFile = open('trieFile', 'wb')
    pickle.dump(t, trieFile)                    
    trieFile.close()
 

def loadTrie():
    trieFile = open('trieFile', 'rb')    
    t = pickle.load(trieFile)
    trieFile.close()

    return t


def search(g : Graph, trie, more, user_input):
     #obicna pretraga
            final_results = {}
            for word in user_input.split(" "):
                pages_results = trie.number_of_appearing_word(word.strip().lower())   #vraca strane koje sadrze rezultat sa brojem 
                                                                                #pojavljivanja rezultata
                                                                            
                for key in pages_results.keys():

                    if key in final_results.keys():
                        final_results[key] += 189 + pages_results[key]
                    else:
                        final_results[key] = pages_results[key]    

                    for edget, edges in g.EI.items():
                         if edget == key:
                              for k in edges.keys():
                                   if k in pages_results:
                                    final_results[key] += 189 + pages_results[k]
                                                                                         

            page_rank_dictionary_score = pageRank.page_rank(g)                    #za svaku stranu izracuna skor

            for page, number_of_appearing in final_results.items():
                final_results[page] = number_of_appearing + page_rank_dictionary_score[page]*132490


            list_of_appearing = set(final_results.values())                 #izbacivanje duplikata dobijenih skorova
            list_of_appearing = sorted(list_of_appearing, reverse=True)     #sortiranje u opadajucem redoslijedu

            print_results(user_input.lower(),more,final_results, list_of_appearing, trie, g)


def search_with_operators(g,trie,more,user_input):
    split_input = user_input.split(" ")
    operator = ""

    page_rank_dictionary_score = pageRank.page_rank(g)                    #za svaku stranu izracuna skor
    pages_results = trie.number_of_appearing_word(split_input[0].strip().lower())   #vraca strane koje sadrze rezultat sa brojem 
                                                                          #pojavljivanja rezultata

    split_input.remove(split_input[0])

    for word in split_input:
        if operator == 'OR':
            second_results = trie.number_of_appearing_word(word.strip().lower())   #vraca strane koje sadrze rezultat sa brojem 
                                                                                #pojavljivanja rezultata
                
            for page, number_of_appearing in second_results.items():
                pages_results[page] = number_of_appearing

            operator = ""

        if operator == 'AND':
                    second_results = trie.number_of_appearing_word(word.strip().lower())   #vraca strane koje sadrze rezultat sa brojem 
                                                                                        #pojavljivanja rezultata
                    remove_pages = []
                    for page in pages_results.keys():
                        if page not in second_results.keys():
                            remove_pages.append(page)
                        
        
                    for page in remove_pages:
                         pages_results.pop(page)

                    operator = ""


        if operator == 'NOT':
                    second_results = trie.number_of_appearing_word(word.strip().lower())   
                                                                                        
                        
                    for page, number_of_appearing in second_results.items():
                        if page in pages_results.keys():
                            pages_results.pop(page)
   

                    operator = ""            
             

        if word == 'AND':
            operator = 'AND'
            continue

        if word == 'OR':
            operator = 'OR'
            continue

        if word == 'NOT':
            operator = 'NOT'
            continue

    for page, number_of_appearing in pages_results.items():
         pages_results[page] = number_of_appearing + page_rank_dictionary_score[page]

    list_of_appearing = set(pages_results.values())                 #izbacivanje duplikata dobijenih skorova
    list_of_appearing = sorted(list_of_appearing, reverse=True)     #sortiranje u opadajucem redoslijedu
    print_results(user_input.lower(),more,pages_results, list_of_appearing, trie, g)    



def print_results(user_input, more,result, list_of_appearing, trie, g) :           
    count_results = 1     
    shown_results = 0

    save_to_txt(list_of_appearing ,result, user_input)

    for value in list_of_appearing:
        for page, score in result.items():
            if(round(value) == round(score)):
                with open('txtPages/' + page, 'r', encoding='utf-8') as currentFile:
                    allText = currentFile.read()
                    allText = allText.replace('\n', ' ') 
                    sentences = nltk.sent_tokenize(allText)     #razbijanje na recenice

                    for operator in operators:
                        if operator.lower() in user_input: 
                            user_input = user_input.replace(operator.lower(), "")
                    user_input = user_input.replace("  "," ")        
                    splited_user_input = user_input.split(" ")

                    for sentence in sentences:
                        if any(word in sentence.lower()  for word in splited_user_input):   
                                if shown_results == 10:
                                    
                                    print()
                                    more = input("Kliknite enter za jos rezultata ili x za nazad..")
                                    print()
                                    shown_results = 1                          

                                    if more == 'x':
                                        return 'x'

                                print()
                                print(str(count_results) + ". "+"[Strana: " +page+"]")
                                print()
                                sentence_split = re.split(r'(\W+)', sentence)
                                
                                for chunk in sentence_split:
                                    if not(any(input.lower() in chunk.lower().strip() for input in splited_user_input)):
                                        print(chunk, end = "")
                                    else:
                                        print(BRIGHT_GREEN + chunk + RESET, end = "")
                                    
                                count_results += 1
                                shown_results += 1
                                print()
                                print('_'*200)

                    continue

    if len(result) < 5:

        suggestions = trie.autocomplete(user_input[0:len(user_input)//2])
        if len(suggestions) == 0:
             print("Nazalost nema rezultata ni predloga za ovu pretragu.")
             return
        
        print("Da li ste mislili? ")

        try_suggestion = ""

        for suggestion in suggestions:
             if len(suggestion) > 5:
                print(suggestion)
                try_suggestion = suggestion
                break

        choose = input("Kliknite enter za da ili x za nazad: ")

        if choose == 'x':
            return
        else:
            search(g, trie, more, try_suggestion)


def save_to_txt(list_of_appearing, results, user_input):
    count = 1
    lines = []
    colored_words = []

    for value in list_of_appearing:
        for page, score in results.items():
            if(round(value) == round(score)):
                with open('txtPages/' + page, 'r', encoding='utf-8') as currentFile:
                    allText = currentFile.read()
                    allText = allText.replace('\n', ' ') 
                    sentences = nltk.sent_tokenize(allText)     #razbijanje na recenice

                    for operator in operators:
                        if operator in user_input: 
                            user_input = user_input.replace(operator, "")
                    user_input = user_input.replace("  "," ")        
                    splited_user_input = user_input.split(" ")

                    for sentence in sentences:
                        if any(word in sentence.lower()  for word in splited_user_input):   
                            if count < 11:
                                lines.append(str(count) + ". "+"[Strana: " +page+"]" +"\n")
                            else:
                                break
            
                            sentence_split = re.split(r'(\W+)', sentence)
                            
                            line = ""
                            for chunk in sentence_split:
                                if not(any(input.lower() in chunk.lower().strip() for input in splited_user_input)):
                                    line += chunk + ""
                                else:
                                    line += chunk + ""  
                                    colored_words.append(chunk)
                                
                            lines.append(line+"\n")    
                            count += 1

                            
    with open("rezultatiTXT.txt", 'w', encoding='utf-8') as file:
        file.writelines(lines)
                         
    pdfConverter.txt_to_pdf("rezultatiTXT.txt", "rezultatiPDF.pdf", colored_words)            
