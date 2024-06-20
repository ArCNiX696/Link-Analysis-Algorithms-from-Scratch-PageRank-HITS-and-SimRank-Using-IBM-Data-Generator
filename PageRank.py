import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import time

class PageRankAlg:
    def __init__(self):
        self.input_file_name='processed_ibm-5000.txt'
        self.output_dir='./Results/ibm-500/'
        self.out_file_name='ibm-500_PageRank.txt'
        self.image_tittle='graph ibm-500 Nodes'
        self.file_path=os.path.join('./Input/',self.input_file_name)#For the input file
        self.Output_path=os.path.join(self.output_dir,self.out_file_name)#path for exporting the file
        self.image_out_path=os.path.join('./Graph_images/PageRank/','graph_ibm-500_PageRank.png')#For the Graph image 
        self.file=open(self.file_path)
        self.input_text=[]
        self.G= nx.DiGraph()
    

    #Load text file function
    def Load_text_file(self):  

        #Open the file and make a list of tuples with the nodes 
        if os.path.isfile(self.file_path):
                print("File Founded")

                for line in  self.file.readlines():
                    splited_line=tuple(line.split('\n')[0].split(','))
                    self.input_text.append(splited_line)

                self.file.close()

        else:
             print("File not Founded , please check if the file is in the  correct path")


    #Graph the Nodes
    def Graph_nodes(self):
        self.G.add_edges_from(self.input_text)
        print(f'The {self.input_file_name} file has: {self.G.number_of_nodes()} Nodes,and {self.G.number_of_edges()} Edges')
        
        plt.figure(figsize=(7,7))
        pos = nx.spring_layout(self.G, seed=42)
        nx.draw_networkx(
            self.G,
            pos=pos,
            with_labels=True,
            node_size=2000,
            node_color="cyan",
            font_size=15,
            font_color="black",
            edge_color="Gray",
            linewidths=5,
            width=2.0,
            alpha=0.8,
        )
        #For visualizing from here
        #plt.show()

        #For exporting the graph image
        #plt.title(self.image_tittle, fontsize=20)
        #plt.savefig(self.image_out_path)

    def PageRank_Calulation(self, Graph, Num_iter, Damping):
        start_time = time.time() #To calculate the time
        Num_nodes = Graph.number_of_nodes()
        teleport = (1 - Damping) / Num_nodes
        self.pagerank = dict.fromkeys(Graph, 1.0 / Num_nodes)

        for _ in range(Num_iter):
            prev_pagerank = self.pagerank.copy()

            for node in self.pagerank:
                sum_rank = 0
                for predecessors in Graph.predecessors(node):
                    outd = Graph.out_degree(predecessors)
                    if outd > 0:
                        sum_rank += prev_pagerank[predecessors] / outd

                self.pagerank[node] = teleport + Damping * sum_rank
        
        end_time = time.time()  #stop
        execution_time = end_time - start_time 
        print(f"PageRank execution time for {Num_iter} iterations: {execution_time:.4f} seconds")

        return self.pagerank

    def Export_ans(self):
        ans_file=open(self.Output_path,"wb")
        ans_values = np.array(list(self.pagerank.values()))
        np.savetxt(ans_file, ans_values, newline=' ', fmt='%.03f')

        if os.path.isfile(self.Output_path):
            print(f"{self.out_file_name} file exported succesfully in {self.output_dir} path")

        else:
             print(f"An error ocurred exporting the file {self.out_file_name}")
            
        ans_file.close()

        


def main():
    Algorithm_obj=PageRankAlg()

    Algorithm_obj.Load_text_file()

    Algorithm_obj.Graph_nodes()

    Algorithm_obj.PageRank_Calulation(Graph=Algorithm_obj.G, Num_iter=30, Damping=0.1)
    
    #Algorithm_obj.Export_ans()


if __name__=='__main__':
    main()


