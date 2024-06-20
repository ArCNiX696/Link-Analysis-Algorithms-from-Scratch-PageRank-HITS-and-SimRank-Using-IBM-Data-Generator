import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os
import time


class HistAlg:
    def __init__(self):
        self.input_file_name='processed_ibm-5000.txt'
        self.Auth_file_name='ibm-5000_Hits_authority.txt'
        self.Hubs_file_name='ibm-5000_Hits_hub.txt'
        self.image_tittle='ibm-5000 Nodes'
        self.output_dir='./Results/ibm-500/'
        self.file_path=os.path.join('./Input/',self.input_file_name)#For the input file
        self.auth_output_path=os.path.join(self.output_dir,self.Auth_file_name)#For the graph_1_Hits_authority.txt file
        self.hubs_output_path=os.path.join(self.output_dir,self.Hubs_file_name)#For the graph_1_Hits_hub.txt file
        self.image_out_path=os.path.join('./Graph_images/Hits/','ibm-500_nodes.png')#For the Graph image   
        self.file=open(self.file_path)
        self.input_text=[]
        self.G= nx.DiGraph()


    #Load text file function
    def Load_text_file(self):  

        #Open the file and make a list of tuples with the nodes 
        if self.file_path is not None:
                print("File Founded")

                
                for line in  self.file.readlines():
                    splited_line=tuple(line.split('\n')[0].split(','))
                    self.input_text.append(splited_line)

                self.file.close()

        else:
             print("File not Founded , please check if the file is in the  correct path")


    #Main code
    def Hits_calculation(self,Graph,Num_iter):
            start_time = time.time() #To calculate the time
            #Give a value of 1 to every node
            self.Hubs = dict.fromkeys(Graph, 1)
            self.Authorities = dict.fromkeys(Graph, 1)
            
            for _ in range(Num_iter):
                new_hubs = self.Hubs.copy()
                new_authorities = self.Authorities.copy()
                self.Hubs = dict.fromkeys(new_hubs.keys(), 0)
                self.Authorities = dict.fromkeys(new_authorities.keys(), 0)

                for node in self.Authorities:
                    for predecessors in Graph.predecessors(node):
                        self.Authorities[node] += new_hubs[predecessors]

                for node in self.Hubs:
                    for successors in Graph.successors(node):
                        self.Hubs[node] += new_authorities[successors]

                Authorities_total = sum(abs(value) for value in self.Authorities.values())
                Hubs_total = sum(abs(value) for value in self.Hubs.values())


                self.Authorities={key:(self.Authorities[key]/Authorities_total) for key in self.Authorities}

                self.Hubs={key:(self.Hubs[key]/Hubs_total) for key in self.Hubs}


            end_time = time.time()  #stop
            execution_time = end_time - start_time 
            print(f"Hits execution time for {Num_iter} iterations: {execution_time:.4f} seconds")
            
            return self.Authorities,self.Hubs
    
    #Export Authorities
    def Export_ans(self):
        Auth_file=open(self.auth_output_path,"wb")
        Auth_values =[value for _ ,value in self.Authorities.items()]
        Auth_values = np.array(Auth_values)
        np.savetxt(Auth_file, Auth_values, newline=' ', fmt='%.03f')
        
        if os.path.isfile(self.auth_output_path):
             print(f"{self.Auth_file_name} file exported succesfully in {self.output_dir} path")

        else:
             print(f"An error ocurred exporting the file {self.Auth_file_name}")

        Auth_file.close()

        Hubs_file=open(self.hubs_output_path,"wb")
        Hubs_values =[value for _ ,value in self.Hubs.items()]
        Hubs_values = np.array(Hubs_values)
        np.savetxt(Hubs_file, Hubs_values, newline=' ', fmt='%.03f')

        if os.path.isfile(self.hubs_output_path):
             print(f"{self.Hubs_file_name} file exported succesfully in {self.output_dir} path")

        else:
             print(f"An error ocurred exporting the file {self.Hubs_file_name}")

        Hubs_file.close()

        

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

        #for visualization from here
        #plt.show()

        #export the graph
        #plt.title(self.image_tittle, fontsize=20)
        
        #plt.savefig(self.image_out_path)

        

def main():
    Algorithm_obj=HistAlg()

    Algorithm_obj.Load_text_file()

    Algorithm_obj.Graph_nodes()

    Algorithm_obj.Hits_calculation(Graph=Algorithm_obj.G, Num_iter=30)

    #Algorithm_obj.Export_ans()


if __name__=='__main__':
    main()


    






            


              
         
       
