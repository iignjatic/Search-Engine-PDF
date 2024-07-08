from graph_tools import Graph
import pdfConverter as converter
import os


def creating_graph():
    graph = Graph(directed = True)
    pdf_path = 'Data Structures and Algorithms in Python.pdf'

    #converter.pdf_to_text(pdf_path)        #parsira pdf u txt
   
    files = os.listdir("txtPages")          #izlista sve txt datoteke
    for eachFile in files:
        graph.add_vertex(eachFile)      #dodaje txt u cvor grafa
        with open('txtPages/'+eachFile, 'r', encoding='utf-8') as currentFile:
            allLines = currentFile.readlines()

            for line in allLines:
                if 'page ' in line.lower():  #ako postoje reference
                    index = line.find('page')
                    index += 5
                    number_of_page = ""
                    while(line[index].isdigit()):                 #trazi se broj strane koja je referencirana
                        number_of_page += line[index]
                        index += 1
                    if(number_of_page != ""):
                        number_of_page = str(int(number_of_page)+22)
                        graph.add_edge(eachFile, number_of_page+'.txt')      #dodavanje veza

    return graph                    


 
