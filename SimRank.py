import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os
import copy
import time

class HistAlg:
    def __init__(self):
        self.input_file_name='processed_ibm-5000.txt'
        self.out_file_name='ibm-5000_SimRank.txt'
        self.output_dir='./Results/ibm-5000/'
        self.image_tittle='ibm-5000 Graph Simrank'
        self.file_path=os.path.join('./Input/',self.input_file_name)#For the input file
        self.file_output_path=os.path.join(self.output_dir,self.out_file_name)#For the graph_1_SimRank.txt file
        self.image_out_path=os.path.join('./Graph_images/SimRank/','graph_ibm-5000_simrank.png')#For the Graph image   
        self.file=open(self.file_path)
        self.input_text=[]
        self.node_to_index = {}
        self.G= nx.DiGraph()
        3


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


    #Main code
    def SimRank_calculation(self,Graph,Decay_fact,Num_iter):
        start_time = time.time() #To calculate the time
        Num_nodes= Graph.number_of_nodes()
        self.SRank_matrix=[[0]* Num_nodes for _ in range(Num_nodes)]

        for i in range(Num_nodes):
            self.SRank_matrix[i][i] = 1
        
        for _ in range(Num_iter):
            sim_deepcopy= copy.deepcopy(self.SRank_matrix)
            for u_neigh in Graph.nodes():
                for v_neigh in Graph.nodes():
                    if u_neigh==v_neigh:
                        continue
                    
                    simUV_neigh=0.0

                    u_neighbors=len(list(Graph.predecessors(u_neigh)))
                    v_neighbors=len(list(Graph.predecessors(v_neigh)))

                    if (u_neighbors== 0 or v_neighbors==0):
                        continue  
                    for neigh_u in Graph.predecessors(u_neigh):
                        for neigh_v in Graph.predecessors(v_neigh):
                            indexU = self.node_to_index[neigh_u]
                            indexV = self.node_to_index[neigh_v]
                            simUV_neigh += sim_deepcopy[indexU][indexV]
                        
                    indexU_2 = self.node_to_index[u_neigh]
                    indexV_2 = self.node_to_index[v_neigh]
                    self.SRank_matrix[indexU_2][indexV_2]=(Decay_fact* simUV_neigh/
                                                        (u_neighbors*v_neighbors))


        end_time = time.time()  #stop
        execution_time = end_time - start_time 
        print(f"SimRank execution time for {Num_iter} iterations and Decay factor at: {Decay_fact} : {execution_time:.4f} seconds")

        print(np.array(self.SRank_matrix))    
        return self.SRank_matrix


    #Graph the Nodes
    def Graph_nodes(self):
        self.G.add_edges_from(self.input_text)
        self.node_to_index = {node: i for i, node in enumerate(self.G.nodes())}
        print("Node to index mapping:", self.node_to_index)
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

        #for visualization from here
        #plt.show()

        #export the graph
        #plt.title(self.image_tittle, fontsize=20)
        #plt.savefig(self.image_out_path)


    def Export_ans(self):
        if not os.path.exists(self.output_dir):
            print(f"The folder does not exist in {self.file_output_path} path")
            os.makedirs(self.output_dir)


        with open(self.file_output_path, "w") as ans_file:
            ans_values = np.array(self.SRank_matrix)
            # Usar np.savetxt para escribir la matriz en el archivo
            np.savetxt(ans_file, ans_values, fmt='%d', delimiter=' ')
             

        if os.path.isfile(self.file_output_path):
            print(f"{self.out_file_name} file exported successfully in {self.output_dir} path")
        else:
            print(f"An error occurred exporting the file {self.out_file_name}")


def main():
    Algorithm_obj=HistAlg()

    Algorithm_obj.Load_text_file()

    Algorithm_obj.Graph_nodes()

    Algorithm_obj.SimRank_calculation(Graph=Algorithm_obj.G,Decay_fact=0.7, Num_iter=30)

    #Algorithm_obj.Export_ans()


if __name__=='__main__':
    main()
