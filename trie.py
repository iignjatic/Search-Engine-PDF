import re
from typing import List, Dict

class TrieNode(object):
    def __init__(self, char: str):
        self.char = char
        self.children = []
        self.word_finished = False
        self.counter = 1
        self.pages = {}


    def add(self, word: str, page_name: str):
        node = self
        for char in word:
            found_in_child = False
            for child in node.children:
                if child.char == char:
                    child.counter += 1
                    node = child
                    found_in_child = True
                    break
            if not found_in_child:
                new_node = TrieNode(char)
                node.children.append(new_node)
                node = new_node
        node.word_finished = True
        if page_name in node.pages:
            node.pages[page_name] += 1
        else:
            node.pages[page_name] = 1


    def number_of_appearing_word(self,prefix: str) -> Dict[str, int]:
        node = self
        if not self.children:
            return {}
        
        for char in prefix:
            char_not_found = True
            for child in node.children:
                if child.char == char:
                    char_not_found = False
                    node = child
                    break
            if char_not_found:
                return {}
        
        return node.pages


    def autocomplete(self, prefix: str) -> List[str]:
        results = []
        node = self
        for char in prefix:
            char_not_found = True
            for child in node.children:
                if child.char == char:
                    char_not_found = False
                    node = child
                    break
            if char_not_found:
                return results
        
        def dfs(node, prefix):
            if node.word_finished:
                results.append(prefix)
            for child in node.children:
                dfs(child, prefix + child.char)

        dfs(node, prefix)
        return results


def form_trie(pages: List[str]) -> TrieNode:
    tr = TrieNode("")
    for page in pages:
        try:
            with open('txtPages/' + page, 'r', encoding='utf-8') as currentFile:
                allLines = currentFile.read()
                words = re.findall(r'\b[a-zA-Z]+\b', allLines.lower())
                for word in words:
                    #page1 = str(int(page[0:len(page)-4])+1)+".txt"
                    tr.add(word, page)
        except FileNotFoundError:
            print(f"File {page} not found.")
    return tr
