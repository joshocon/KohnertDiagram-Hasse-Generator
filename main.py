'''
Josh O'Connor
University of Kansas
McNair Scholar's Program 2025
'''

from src import Diagram, Graph, DiagramEngine, LaTeXRenderer, Poset
import subprocess


def main():
    #get all Kohnert diagrams from diagrams.txt
    diagrams = []
    with open('diagrams.txt', 'r') as file:
        data = file.readlines()
    
    for line in data:
        raw_cells = line.strip().split(' ')
        cells = [eval(cell) for cell in raw_cells ]
        diagrams.append(cells)
        
    #latex boilerplate
    latex_start = r'''
    \documentclass{article}
    \usepackage{graphicx, geometry, amsmath, amsfonts, tikz, youngtab, cite}
    \geometry{left=2cm, right=2cm}
    \savebox2{%
    \begin{picture}(12,12)
    \put(0,0){\line(1,0){12}}
    \put(0,0){\line(0,1){12}}
    \put(12,0){\line(0,1){12}}
    \put(0,12){\line(1,0){12}}
    \end{picture}}
    \newcommand\cover{\mathrel{\ooalign{$\prec$\cr
    \hidewidth\hbox{$\cdot\mkern0.5mu$}\cr}}}
    \newlength\cellsize
    \setlength\cellsize{12pt} 
    \newcommand\cellify[1]{\def\thearg{#1}\def\nothing{}%
    \ifx\thearg\nothing\vrule width0pt height\cellsize depth0pt%
    \else\hbox to 0pt{\usebox2\hss}\fi%
    \vbox to 12\unitlength{\vss\hbox to 12\unitlength{\hss$#1$\hss}\vss}}
    \newcommand\tableau[1]{\vtop{\let\\=\cr
    \setlength\baselineskip{-12000pt}
    \setlength\lineskiplimit{12000pt}
    \setlength\lineskip{0pt}
    \halign{&\cellify{##}\cr#1\crcr}}}
    \savebox4{% CIRCLE
    \begin{picture}(12,12)
    \put(6,6){\circle{12}}
    \end{picture}}
    \newcommand{\cir}[1]{\def\thearg{#1}\def\nothing{}%
    \ifx\thearg\nothing\vrule width0pt height\cellsize depth0pt%
    \else\hbox to 0pt{\usebox4\hss}\fi%
    \vbox to 12\unitlength{\vss\hbox to 12\unitlength{\hss$#1$\hss}\vss}}
    \newcommand\nocellify[1]{\def\thearg{#1}\def\nothing{}%
    \ifx\thearg\nothing\vrule width0pt height\cellsize depth0pt%
    \else\hbox to 0pt{\hss}\fi%
    \vbox to 12\unitlength{\vss\hbox to 12\unitlength{\hss$#1$\hss}\vss}}
    \newcommand\notableau[1]{\vtop{\let\\=\cr
    \setlength\baselineskip{-12000pt}
    \setlength\lineskiplimit{12000pt}
    \setlength\lineskip{0pt}
    \halign{&\nocellify{##}\cr#1\crcr}}}
    \title{Code Generation of Posets}
    \begin{document}
    \maketitle '''
    latex_hasse_diagrams = ''
    latex_end = '\end{document}'
        
    file = open('main.tex', 'r')
    
    for cells in diagrams:
        graph = Graph()
        engine = DiagramEngine()
        renderer = LaTeXRenderer()
        
        row_num, col_num = engine.get_dimension(cells)
        diagram = Diagram(list(cells), row_num, col_num)  # init diagram
        graph.add_vertex(diagram) #add "root" to graph
        D_0 = graph.get_root_node()
        
        #if the diagram is invalid or not southeast then quit
        if diagram.cells == []:
            print('Error')
        
        elif engine.check_south_east(diagram.cells) == False:
            print('Not Southeast')
        
        #if the diagram is valid, we continue
        else:
            cache = {}  # cache Kohnert diagrams
            move_cells = engine.find_move_cells(diagram)  # find cells eligible for Kohnert move
            for move_pair in move_cells:
                engine.kohnert_move(graph, diagram, move_pair, cache)
            
            #significatly faster to comment out the writing and compiling of latex - the print messages will be enough information for most cases
            renderer.set_node_positions(graph)
            latex_hasse_diagrams += renderer.generate_hasse_diagram(graph, D_0)
            
        
            with open('main.tex', 'w') as f:
                f.write(latex_start + latex_hasse_diagrams + latex_end)
                
            with open('latex_errors.log', 'w') as error_log:
                subprocess.run(['pdflatex', 'main.tex'], stdout=subprocess.DEVNULL, stderr=error_log)
            
                kohnert_poset = Poset(graph)
                kohnert_poset.result()
            
        file.close
        

if __name__ == '__main__':
    main()
