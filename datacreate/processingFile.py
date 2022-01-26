import pandas as pd


# edges create
def getEdges(matr):
    edge = {}
    for m in matr.columns:
        for n in matr.index:
            a, b = m, n
            if a > b:  # only add edge once
                x = matr.at[m, n]
                edge[m, n] = float(f"{x}")

    return edge


# return ids to columns name
def addIds(df, first, final):
    data = df.iloc[:, first:final]

    # getting the ids by the number of columns
    arr = []
    for k in range(1, data.shape[1] + 1):
        arr.append(k)

    # replace variable names by number
    for v in range(0, len(arr)):
        data.rename(columns={data.columns[v]: arr[v]}, inplace=True)

    return data


def createNodeTable(data, first, final):
    # get variable names
    names = list(data.columns[first:final])

    # create dataframe
    dfnode = pd.DataFrame(columns={"ID", "Label"})

    # insert names and ids into table
    dfnode["Label"] = names

    arr = []
    for v in range(1, dfnode.shape[0] + 1):
        arr.append(v)

    dfnode["ID"] = arr

    return dfnode


def createEdges(data):
    file = pd.read_csv(data)
    # column insert for column division by comma
    file.insert(2, "3", True)
    # column division
    file = pd.concat([file[["3"]], file["0"].str.split(', ', expand=True)], axis=1)
    # remove caracters
    file[0] = file[0].str.replace("(", "")
    file[1] = file[1].str.replace(")", "")
    # rename and drop column 3
    file.rename(columns={0: "Source", 1: "Target"}, inplace=True)
    file.drop(columns=["3"], inplace=True)
    file.to_csv("edges.csv", index=False)

    return file


# create matrix edges
def dataCreator(file, sheetname, colFirst, colFinal, levelCorr):
    data = pd.read_excel(file, sheet_name=sheetname)
    # create node table
    nodeData = createNodeTable(data, colFirst, colFinal)

    # replace variable names by ids
    data = addIds(data, first=colFirst, final=colFinal)

    # get a correlation matrix
    corr_matrix = data.corr().round(1)
    corr_matrix = corr_matrix[(corr_matrix >= levelCorr)]

    # dictionary of correlations
    dic = getEdges(corr_matrix)

    # dict to df
    items = dic.items()
    data_list = list(items)
    dataframe = pd.DataFrame(data_list, columns={"1", "0"})
    dataframe = dataframe.dropna()

    # format dataframe edges

    dataframe.to_csv("edges.csv", index=False)
    nodeData.to_csv("nodes.csv", index=False)

    return nodeData


# corrlevel -> format: 0.8...
def get_files(path, tabname, firstcolumn, lastcolumn, corrlevel):
    path = path
    node = dataCreator(file=path, sheetname=tabname, colFirst=firstcolumn, colFinal=lastcolumn, levelCorr=corrlevel)
    edges = createEdges("edges.csv")

    return node, edges
