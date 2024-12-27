import networkx as nx
import os
import pandas as pd
from pathlib import Path

def create_module_graph(csv_dir):
    G = nx.Graph()

    semesters_in_graph = []
    # parse the given directory
    for path, dirs, files in os.walk(csv_dir):
        modules_csv = None
        programs_csv = None
        for file in files:
            # search for the right files
            if "modules" in file:
                modules_csv = file
            if "study_programs" in file:
                programs_csv = file

        if modules_csv and programs_csv:
            modules_path = path + "/" + modules_csv
            programs_path = path + "/" + programs_csv
            G = add_semester_to_graph(G, modules_path, programs_path)
            semesters_in_graph.append(path)

    return G, semesters_in_graph
    

def add_semester_to_graph(G, modules_csv, programs_csv):
    programs_df = pd.read_csv(programs_csv, encoding="utf-16")
    programs = programs_df["Program"]
    # part_of = programs_df["Part of"]

    modules_df = pd.read_csv(modules_csv, encoding="utf-16")
    modules = modules_df["Name"]

    G.add_nodes_from(programs)
    G.add_nodes_from(modules)

    modules_txt = modules_csv.replace(".csv", ".txt").replace("/csv/", "/text/")
    text = Path(modules_txt).read_text()

    # a new module always starts with "Page 1", the very first entry is empty
    modules = text.split("Page 1")[1:]

    
        
    return G

    

if __name__ == "__main__":
    G, semesters_in_graph = create_module_graph("data/csv/HS24")
    # print(semesters_in_graph)
    # print(G.nodes())