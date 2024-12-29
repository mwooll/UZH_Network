import networkx as nx
import pandas as pd

def create_graph(csv_dir):
    G = nx.Graph()

    for semester in ["HS24", "FS24", "HS23", "FS23"]:
        G = add_semester_to_graph(G, csv_dir, semester)

    store_file = "data/giant_graph.gml"
    nx.write_gml(G, store_file)
    return G
    

def add_semester_to_graph(G, csv_dir, semester):
    path = csv_dir + "/" + semester + "/"
    file_start = path + "VVZ_" + semester 

    G = add_programs(G, file_start + "_study_programs.csv")

    G = add_modules(G, file_start + "_module_components.csv",
                    file_start + "_modules.csv")

    G = add_time_schedules(G, file_start + "_time_schedule.csv")
    return G

def add_programs(G, file_path):
    programs_df = read_file(file_path)

    H = nx.from_pandas_edgelist(programs_df, "Program", "Organization")
    G.update(H)

    for index, program in programs_df.iterrows():
        for part_of in program["Part Of"].split(";"):
            G.add_node(part_of)
            G.add_edge(program["Program"], part_of)
        
    return G

def add_modules(G, comp_path, modules_path):
    modules_df = read_file(modules_path)
    H = nx.from_pandas_edgelist(modules_df, "Name", "Responsible instructor")
    G.update(H)

    # Type,ECTS could easily be added, though not sure if sensible

    components_df = read_file(comp_path)
    for index, module in components_df.iterrows():
        if isinstance(module["Components"], str):
            for component in module["Components"].split(";"):
                G.add_edge(module["Module"], component.split("---")[0])

    return G

def add_time_schedules(G, file_path):
    schedules_df = read_file(file_path)
    H = nx.from_pandas_edgelist(schedules_df, "Event Name", "Instructor")
    I = nx.from_pandas_edgelist(schedules_df, "Event Name", "Component of Module")
    H.update(I)

    G.update(H)
    return G

def read_file(file_name):
    try:
        df = pd.read_csv(file_name, encoding="utf-16")
    except:
        df = pd.read_csv(file_name, encoding="utf-8")

    return df

if __name__ == "__main__":
    G = create_graph("data/csv")
    print("Graph created and stored")
    # print(semesters_in_graph)
    # print(G.nodes())