'''
Josh O'Connor
University of Kansas
McNair Scholar's Program 2025
'''

from src import Diagram, Graph, DiagramEngine, LaTeXRenderer, KohnertPoset, SoutheastDiagramGenerator, ProgessBar
import subprocess
import itertools
import ast
    
def main():
    sdg = SoutheastDiagramGenerator()
    #sdg.generate(5) #generates all nxn southeast diagrams and writes it to diagrams.txt
    
    draw_full_poset = False

    diagrams = []
    with open('diagrams.txt', 'r') as file:
        data = file.readlines()
    
    for line in data:
        raw_cells = line.strip().split(' ')
        cells = [ast.literal_eval(cell) for cell in raw_cells ]
        diagrams.append(sdg.normalize_cells(cells))
        
    diagrams.sort(key=len)
    diagrams = list(item for item,_ in itertools.groupby(diagrams))
    
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
    latex_hasse_diagrams = []
    latex_initial_diagrams = []
    kohnert_results = []
    latex_end = r'\end{document}'
    
    progress = ProgessBar(len(diagrams))

    for index, cells in enumerate(diagrams, 1):
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
        
        #elif engine.check_south_east(diagram.cells) == False:
            #print(f'\nNot Southeast: {diagram.cells}')
        
        #if the diagram is valid, we continue
        else:
            cache = {}  # cache Kohnert diagrams
            move_cells = engine.find_move_cells(diagram)  # find cells eligible for Kohnert move
            for move_pair in move_cells:
                engine.kohnert_move(graph, diagram, move_pair, cache)
            
            kohnert_poset = KohnertPoset(graph)
    
            if True:#not kohnert_poset.is_simple(): #if the initial diagram has no possible kohnert moves
                result = kohnert_poset.result()
                test = diagram.test_conjecture()
                    
                with open('output.txt', 'a') as f:
                    f.write(f'{result} ||| Conjecture Result: {test}\n')
                
                kohnert_results.append(f'{result}' + f' ||| Conjecture Result: {test}')
                
                # if draw_full_poset: 
                #     renderer.set_node_positions(graph)
                #     latex_hasse_diagrams.append(renderer.generate_hasse_diagram(graph, D_0, result))
                    
                # if not draw_full_poset:
                #     latex_initial_diagrams.append(renderer.generate_initial_diagrams(D_0, result))
                    
            progress.print_progress(index)
    print() 
    
    with open('output.txt', 'w') as f:
                f.write('\n'.join(kohnert_results))
    
    with open('main.tex', 'w') as f:
                f.write(latex_start + '\n'.join(latex_hasse_diagrams) + '\n'.join(latex_initial_diagrams) + latex_end)
                    
    with open('latex_errors.log', 'w') as error_log:
                subprocess.run(['pdflatex','-interaction=nonstopmode', 'main.tex'], stdout=subprocess.DEVNULL, stderr=error_log)

if __name__ == '__main__':
    main()