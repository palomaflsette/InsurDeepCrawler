import sys, getopt
import uuid,base64
from anytree import Node, RenderTree, LevelOrderIter, DoubleStyle
from anytree.dotexport import RenderTreeGraph
import requests
from bs4 import BeautifulSoup
from string import printable
from collections import Counter
from html.parser import HTMLParser
import io


url_list = []

#Examinando um arquivo
def unigram_extraction(filename):
        file = open('html-files/'+ filename + '.txt', 'r', encoding="ascii")
        frequency = sorted(Counter(c for l in file for c in l).items())

        print("--------------------------------------------")
        print("A extração de unigramas no arquivo de texto produziu esses resultados.")
        print("--------------------------------------------")
        print(frequency)
        print("--------------------------------------------")


# "Raspa" uma URL e localiza todos os seus links de saída
# Os links são criados como "nós filhos" do "nó pai".
def scrapeUrl(url, rootNode):
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, 'html.parser')

    uuidstring = str(uuid.uuid5(uuid.NAMESPACE_DNS, url))
    filename = base64.b64encode(uuid.UUID(uuidstring).bytes).decode("ascii").rstrip('=\n').replace('/', '_')

    with io.open('html-files/' + filename + '.txt', "wb") as f:
        f.write(soup.encode("ascii"))
        f.close()

    print("Arquivo html salvo!")

    unigram_extraction(filename)

    list_of_nodes = []
    for link in soup.find_all('a', href=True):
        href = link.get('href') # unicode to str
        if (href.startswith( '/' )):
            href = url + href
        elif (href.startswith('http')):
            urlNode = Node(href, parent=rootNode)
            list_of_nodes.append(urlNode)
    return list_of_nodes

# Depth search limitada a partir de um nó raiz.
def depth_limited_search(rootNode, limit=50):
    """[Figure 3.17]"""
    def recursive_dls(rootNode, limit):
        # if problem.goal_test(node.state):
        #     return node
        children = scrapeUrl(rootNode.name, rootNode)

        print("Crawling")
        print("--------------------------------------------")
        print(rootNode.name)
        print("--------------------------------------------")
        print("Depth: ", rootNode.depth)
        print("--------------------------------------------")
        print("Parent: ", rootNode.parent)
        print("--------------------------------------------")

        if limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in children:
                result = recursive_dls(child, limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None

    #Body of depth_limited_search:
    return recursive_dls(rootNode, limit)

def iterative_deepening_search(rootNode, maxDepth):
    """[Figure 3.18]"""
    for depth in range(maxDepth):
        result = depth_limited_search(rootNode, depth)
        if result != 'cutoff':
            return result


def main(argv):
   inputUrl = ''
   inputDepth = 0

   try:
      opts, args = getopt.getopt(argv,"hu:d:",["rootUrl=","depth="])
   except getopt.GetoptError:
      print ('index.py -u <url> -d <depth>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('index.py -u <url> -d <depth>')
         sys.exit()
      elif opt in ("-u", "--rootUrl"):
         inputUrl = arg
      elif opt in ("-d", "--depth"):
         inputDepth = int(arg)
   print ('Input url --> ', inputUrl)
   print ('Depth --> ', inputDepth)

   rootNode = Node(inputUrl)

   iterative_deepening_search(rootNode, inputDepth)

   print("--------------------------------------------")
   print("Finalizando com >>>Iterative Deepening Search<<<<!")
   print("--------------------------------------------")

   print("Estrutura da árvore")
   print("--------------------------------------------")

   print(RenderTree(rootNode, style=DoubleStyle()).by_attr())


   #
   # for pre, fill, node in RenderTree(rootNode):
   #     print("%s%s" % (pre, node.name))
   #
   #
   RenderTreeGraph(rootNode).to_picture("tree.png")


if __name__ == "__main__":
   main(sys.argv[1:])


# udo = Node("Udo")
# marc = Node("Marc", parent=udo)
# lian = Node("Lian", parent=marc)
# dan = Node("Dan", parent=udo)
# jet = Node("Jet", parent=dan)
# jan = Node("Jan", parent=dan)
# joe = Node("Joe", parent=dan)
#
# print(udo)
# Node('/Udo')
# print(joe)
# Node('/Udo/Dan/Joe')
#
# for pre, fill, node in RenderTree(udo):
#     print("%s%s" % (pre, node.name))
