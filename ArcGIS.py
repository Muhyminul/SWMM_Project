from tkinter import *
from tkinter import filedialog
import pandas as pd
import numpy as np
import re
import geopandas as gpd
from shapely.geometry import mapping
import warnings

warnings.filterwarnings('ignore')
file=[]
initial_dir = "C:"
root = Tk()
root.title("ArcGIS Interface")
root.geometry('800x425')

label1 = Label(root, text='Catchment Shape File')
label1.grid(row=1,column=0,sticky=W, padx=5, pady=5)
ent1 = Entry(root, width =90,font=('Helvetica',10))
ent1.grid(row=2, column=0,ipadx=10, ipady=5, padx=10, pady=5)

label2 = Label(root, text='Junction Shape File')
label2.grid(row=3,column=0,sticky=W, padx=5, pady=5)
ent2 = Entry(root, width =90,font=('Helvetica',10))
ent2.grid(row=4, column=0,ipadx=10, ipady=5, padx=10, pady=5)

label3 = Label(root, text='Conduit Shape File')
label3.grid(row=5,column=0,sticky=W, padx=5, pady=5)
ent3 = Entry(root, width =90,font=('Helvetica',10))
ent3.grid(row=6, column=0,ipadx=10, ipady=5, padx=10, pady=5)

label4 = Label(root, text='Input Sample Text File')
label4.grid(row=7,column=0,sticky=W, padx=5, pady=5)
ent4 = Entry(root, width =90,font=('Helvetica',10))
ent4.grid(row=8, column=0,ipadx=10, ipady=5, padx=10, pady=5)

label5 = Label(root, text='Download File Location')
label5.grid(row=9,column=0,sticky=W, padx=5, pady=5)
ent5 = Entry(root, width =90,font=('Helvetica',10))
ent5.grid(row=10, column=0,ipadx=10, ipady=5, padx=10, pady=5)

def browsefunc1():
    filename = filedialog.askopenfilename(initialdir=initial_dir,
                                    defaultextension='.shp',
                                    filetypes=[
                                        ("Text file",".shp")
                                    ])
    ent1.insert(END, filename)
    file.append(filename)

b1 = Button(root, text="Browser", font=('Helvetica',10), command=browsefunc1,
                             width = 10)
b1.grid(row=2, column=6)


def browsefunc2():
    filename = filedialog.askopenfilename(initialdir=initial_dir,
                                    defaultextension='.shp',
                                    filetypes=[
                                        ("Text file",".shp")
                                    ])
    ent2.insert(END, filename)
    file.append(filename)

b2 = Button(root, text="Browser", font=('Helvetica',10), command=browsefunc2,
                             width = 10)
b2.grid(row=4, column=6)

def browsefunc3():
    filename = filedialog.askopenfilename(initialdir=initial_dir,
                                    defaultextension='.shp',
                                    filetypes=[
                                        ("Text file",".shp")
                                    ])
    ent3.insert(END, filename)
    file.append(filename)

b3 = Button(root, text="Browser", font=('Helvetica',10), command=browsefunc3,
                             width = 10)
b3.grid(row=6, column=6)

def browsefunc4():
    filename = filedialog.askopenfilename(initialdir=initial_dir,
                                    defaultextension='.txt',
                                    filetypes=[
                                        ("Text file",".txt")
                                    ])
    ent4.insert(END, filename)
    file.append(filename)

b4 = Button(root, text="Browser", font=('Helvetica',10), command=browsefunc4,
                             width = 10)
b4.grid(row=8, column=6)

def browsefunc5():
    filename = filedialog.asksaveasfile(initialdir=initial_dir,
                                    defaultextension='.txt',
                                    filetypes=[
                                        ("Text file",".txt")
                                              ])
    ent5.insert(END,filename.name)
    file.append(filename.name)

b5 = Button(root, text="Browser", font=('Helvetica',10), command=browsefunc5,
                             width = 10)
b5.grid(row=10, column=6)

def Save_file():
    catchment_file = file[0]
    junction_file = file[1]
    conduit_file = file[2]

    df_1 = gpd.read_file(catchment_file)
    df_1['area'] = df_1['geometry'].area
    df_1['radius'] = np.sqrt(df_1['area'] / np.pi)

    point_shape = gpd.read_file(junction_file)
    from shapely.geometry import Point
    from shapely.strtree import STRtree
    df_1['Center_point'] = df_1['geometry'].centroid
    near_point = []
    tree = STRtree(point_shape['geometry'])
    center_point = df_1.Center_point
    for i in range(len(center_point)):
        near_point.append(tree.nearest(center_point[i]))
        # print(type(tree.nearest(center_point[i])))
    df_1['Near_Point'] = near_point
    df_1

    Subcatchment = []
    X_Coord = []
    Y_Coord = []
    g = [i for i in df_1.Center_point]
    for i in range(len(g)):
        geojson_ob = mapping(g[i])  # for first feature/row
        all_coords = geojson_ob["coordinates"]
        Subcatchment.append('S' + str(i + 1))
        X_Coord.append(int(all_coords[0]))
        Y_Coord.append(int(all_coords[1]))

    near_X_Coord = []
    near_Y_Coord = []
    g = [i for i in df_1.Near_Point]
    # print(g)
    for i in range(len(g)):
        geojson_ob = mapping(g[i])  # for first feature/row
        all_coords = geojson_ob["coordinates"]
        near_X_Coord.append(int(all_coords[0]))
        near_Y_Coord.append(int(all_coords[1]))

    centroid = pd.DataFrame(list(zip(Subcatchment, X_Coord, Y_Coord, near_X_Coord, near_Y_Coord)),
                            columns=[';;Subcatchment', 'X-Coord', 'Y-Coord', 'near_X_Coord', 'near_y_Coord'])
    # -----------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------
    # centroid

    Subcatchment = []
    X_Coord = []
    Y_Coord = []

    g = [i for i in df_1.geometry]
    for i in range(len(g)):
        geojson_ob = mapping(g[i])
        all_coords = geojson_ob["coordinates"]
        coor = all_coords[0]
        for j in range(len(coor) - 1):
            new_coor = coor[j]
            if isinstance(new_coor[0], tuple):
                new_coor=new_coor[0]
                X_Coord.append(int(new_coor[0]))
            else:
                X_Coord.append(int(new_coor[0]))
            Y_Coord.append(int(new_coor[1]))
            Subcatchment.append('S' + str(i + 1))

    polygons = pd.DataFrame(list(zip(Subcatchment, X_Coord, Y_Coord)),
                            columns=[';;Subcatchment', 'X-Coord', 'Y-Coord'])

    polygons = polygons.drop_duplicates()
    # polygons

    df_2 = gpd.read_file(junction_file)
    df_2.head()
    Node = []
    X_Coord = []
    Y_Coord = []
    g = [i for i in df_2.geometry]
    # print(g)
    for i in range(len(g)):
        geojson_ob = mapping(g[i])  # for first feature/row
        all_coords = geojson_ob["coordinates"]
        # print(all_coords)
        Node.append('j' + str(i + 1))
        X_Coord.append(int(all_coords[0]))
        Y_Coord.append(int(all_coords[1]))

    coordinate = pd.DataFrame(list(zip(Node, X_Coord, Y_Coord)),
                              columns=[';;Node', 'X-Coord', 'Y-Coord'])

    # coordinate

    df_3 = gpd.read_file(conduit_file)
    df_3.head()

    Name = []
    x_strt = []
    y_strt = []
    x_end = []
    y_end = []
    Length = []
    id = []
    for i in range(len(df_3)):
        linestring = df_3['geometry'][i]

        (x_s, y_s), *_ = linestring.coords
        *_, (x_e, y_e) = linestring.coords

        id.append(i)
        Name.append('C' + str(i + 1))
        x_strt.append(int(x_s))
        y_strt.append(int(y_s))
        x_end.append(int(x_e))
        y_end.append(int(y_e))

    con_coor = pd.DataFrame(list(zip(id, Name, x_strt, y_strt, x_end, y_end)),
                            columns=['id', ';;Name', 'x_strt', 'y_strt', 'x_end', 'y_end'])

    con_coor['Length'] = df_3.geometry.length

    # con_coor

    from_node = pd.merge(coordinate, con_coor, right_on=['x_strt', 'y_strt'], left_on=['X-Coord', 'Y-Coord'],
                         how='right').rename(columns={';;Node': 'From Node'}).drop(columns=['X-Coord', 'Y-Coord'],
                                                                                   axis=1)
    to_node = pd.merge(coordinate, from_node, right_on=['x_end', 'y_end'], left_on=['X-Coord', 'Y-Coord'],
                       how='right').rename(columns={';;Node': 'To Node'}).drop(columns=['X-Coord', 'Y-Coord'], axis=1)
    coor_df = to_node.drop(columns=['x_strt', 'y_strt', 'x_end', 'y_end', 'id'], axis=1)
    coor_df = coor_df[[';;Name', 'From Node', 'To Node', 'Length']]
    coor_df
    length = len(coor_df[";;Name"])
    Roughness = [0.01]
    Roughness.extend([0.01] * (length - 1))
    coor_df['Roughness'] = Roughness

    InOffset = [0]
    InOffset.extend([0] * (length - 1))
    coor_df['InOffset'] = InOffset

    OutOffset = [0]
    OutOffset.extend([0] * (length - 1))
    coor_df['OutOffset'] = OutOffset

    InitFlow = [0]
    InitFlow.extend([0] * (length - 1))
    coor_df['InitFlow'] = InitFlow

    MaxFlow = [0]
    MaxFlow.extend([0] * (length - 1))
    coor_df['MaxFlow'] = MaxFlow

    # coor_df

    """[TITLE]"""

    """[OPTIONS]"""

    """[EVAPORATION]"""

    lst1 = ['CONSTANT', 'DRY_ONLY']
    lst2 = [0.0, 'NO']
    evapo_df = pd.DataFrame(np.column_stack([lst1, lst2]), columns=[';;Data Source', 'Parameters'])
    evapo_df

    """[RAINGAGES]"""

    # copy from previous file
    # ---------------------------------------------------------------------------------------------------------------------
    sub_to_node = pd.merge(centroid, coordinate, left_on=['near_X_Coord', 'near_y_Coord'],
                           right_on=['X-Coord', 'Y-Coord'], how='left')
    Subcatchmens_df = sub_to_node[[';;Subcatchment', ';;Node']]

    Subcatchmens_df['Area'] = df_1['area']

    Subcatchmens_df['Width'] = df_1['radius']

    SUBCATCHMENTS_df = Subcatchmens_df
    SUBCATCHMENTS_df = SUBCATCHMENTS_df.rename(columns={';;Subcatchment': ';;Name'})
    SUBCATCHMENTS_df = SUBCATCHMENTS_df.rename(columns={';;Node': 'Outlet'})
    sub_len = len(SUBCATCHMENTS_df[';;Name'])

    Rain_Gage = ['Gage1']
    Rain_Gage.extend(['Gage1'] * (sub_len - 1))
    SUBCATCHMENTS_df['Rain Gage'] = Rain_Gage

    # outlet :
    # .......................................................................
    # outlet = ['J1']
    # outlet.extend(['J1'] * (sub_len - 1))
    # SUBCATCHMENTS_df['Outlet'] = outlet
    # outlet value will come from a relational data table

    # area = [4]
    # area.extend([4] * (sub_len - 1))
    # SUBCATCHMENTS_df['Area'] = area

    imperv = [50]
    imperv.extend([50] * (sub_len - 1))
    SUBCATCHMENTS_df['%Imperv'] = imperv

    # width = [400]
    # width.extend([400] * (sub_len - 1))
    # SUBCATCHMENTS_df['Width'] = width

    slope = [.5]
    slope.extend([.5] * (sub_len - 1))
    SUBCATCHMENTS_df['%Slope'] = slope

    curblen = [0]
    curblen.extend([0] * (sub_len - 1))
    SUBCATCHMENTS_df['CurbLen'] = curblen

    snow = ['']
    snow.extend([''] * (sub_len - 1))
    SUBCATCHMENTS_df['SnowPack'] = snow

    SUBCATCHMENTS_df = SUBCATCHMENTS_df.reindex(
        columns=[';;Name', 'Rain Gage', 'Outlet', 'Area', '%Imperv', 'Width', '%Slope', 'CurbLen', 'SnowPack'])










    # ---------------------------------------------------------------------------------------------------------------------

    """[SUBCATCHMENTS]"""

    # SUBCATCHMENTS_df = centroid[[";;Subcatchment"]]
    # SUBCATCHMENTS_df = SUBCATCHMENTS_df.rename(columns={';;Subcatchment': ';;Name'})
    # SUBCATCHMENTS_df
    # sub_len = len(SUBCATCHMENTS_df[';;Name'])
    #
    # Rain_Gage = ['Gage1']
    # Rain_Gage.extend(['Gage1'] * (sub_len - 1))
    # SUBCATCHMENTS_df['Rain Gage'] = Rain_Gage
    #
    # # outlet :
    # # .......................................................................
    # outlet = ['J1']
    # outlet.extend(['J1'] * (sub_len - 1))
    # SUBCATCHMENTS_df['Outlet'] = outlet
    # # outlet value will come from a relational data table
    #
    # area = [4]
    # area.extend([4] * (sub_len - 1))
    # SUBCATCHMENTS_df['Area'] = area
    #
    # imperv = [50]
    # imperv.extend([50] * (sub_len - 1))
    # SUBCATCHMENTS_df['%Imperv'] = imperv
    #
    # width = [400]
    # width.extend([400] * (sub_len - 1))
    # SUBCATCHMENTS_df['Width'] = width
    #
    # slope = [.5]
    # slope.extend([.5] * (sub_len - 1))
    # SUBCATCHMENTS_df['%Slope'] = slope
    #
    # curblen = [0]
    # curblen.extend([0] * (sub_len - 1))
    # SUBCATCHMENTS_df['CurbLen'] = curblen
    #
    # snow = ['']
    # snow.extend([''] * (sub_len - 1))
    # SUBCATCHMENTS_df['SnowPack'] = snow
    #
    # SUBCATCHMENTS_df

    """[SUBAREAS]"""

    Subareas_df = centroid[[";;Subcatchment"]]
    Subareas_df
    sub_len =len(SUBCATCHMENTS_df[';;Name'])

    NImperm = [0.01]
    NImperm.extend(NImperm * (sub_len - 1))
    Subareas_df['N-Imperv'] = NImperm

    Nperm = [0.1]
    Nperm.extend([0.1] * (sub_len - 1))
    Subareas_df['N-Perv'] = Nperm

    SImperm = [0.05]
    SImperm.extend([0.05] * (sub_len - 1))
    Subareas_df['S-Imperv'] = SImperm

    Sperm = [0.05]
    Sperm.extend([0.05] * (sub_len - 1))
    Subareas_df['S-Perv'] = Sperm

    PctZero = [25]
    PctZero.extend([25] * (sub_len - 1))
    Subareas_df['PctZero'] = PctZero

    RouteTo = ['OUTLET']
    RouteTo.extend(['OUTLET'] * (sub_len - 1))
    Subareas_df['RouteTo'] = RouteTo

    PctRouted = [' ']
    PctRouted.extend([' '] * (sub_len - 1))
    Subareas_df['PctRouted'] = PctRouted
    Subareas_df

    """[INFILTRATION]"""

    Infiltration_df = centroid[[";;Subcatchment"]]
    Infiltration_df

    Param1 = [3.5]
    Param1.extend([3.5] * (sub_len - 1))
    Infiltration_df['Param1'] = Param1

    Param2 = [0.5]
    Param2.extend([0.5] * (sub_len - 1))
    Infiltration_df['Param2'] = Param2

    Param3 = [0.25]
    Param3.extend([0.25] * (sub_len - 1))
    Infiltration_df['Param3'] = Param3

    Param4 = [7]
    Param4.extend([7] * (sub_len - 1))
    Infiltration_df['Param4'] = Param4

    Param5 = [0]
    Param5.extend([0] * (sub_len - 1))
    Infiltration_df['Param5'] = Param5

    Infiltration_df

    """[JUNCTIONS]"""

    junction = coordinate.iloc[0:-1]
    junction_df = junction[[";;Node"]].rename(columns={";;Node": ';;Name'})
    junc_len = len(junction_df)
    junction_df

    Elevation = [100]
    Elevation.extend([100] * (junc_len - 1))
    junction_df['Elevation'] = Elevation

    MaxDepth = [4]
    MaxDepth.extend([4] * (junc_len - 1))
    junction_df['MaxDepth'] = MaxDepth

    InitDepth = [0]
    InitDepth.extend([0] * (junc_len - 1))
    junction_df['InitDepth'] = InitDepth

    SurDepth = [0]
    SurDepth.extend([0] * (junc_len - 1))
    junction_df['SurDepth'] = SurDepth

    Aponded = [0]
    Aponded.extend([0] * (junc_len - 1))
    junction_df['Aponded'] = Aponded

    junction_df

    """[OUTFALLS]"""

    outfall = coordinate.tail(1)
    outfall_df = outfall[[";;Node"]].rename(columns={";;Node": ';;Name'})
    outfall_df

    outfall_df['Elevation'] = [85]
    outfall_df['Type'] = ['FREE']
    outfall_df['Stage Data'] = [' ']
    outfall_df['Gated'] = ['NO']
    outfall_df['Route To'] = [' ']

    outfall_df

    """[CONDUITS]"""

    CONDUITS_df = coor_df
    CONDUITS_df

    """[XSECTIONS]"""

    Xsec_df = coor_df[[';;Name']].rename(columns={';;Name': ';;Link'})
    cond_len = len(Xsec_df)
    Xsec_df

    Shape = ['CIRCULAR']
    Shape.extend(['CIRCULAR'] * (cond_len - 1))
    Xsec_df['Shape'] = Shape

    Geom1 = [1]
    Geom1.extend([1] * (cond_len - 1))
    Xsec_df['Geom1'] = Geom1

    Geom2 = [0]
    Geom2.extend([0] * (cond_len - 1))
    Xsec_df['Geom2'] = Geom2

    Geom3 = [0]
    Geom3.extend([0] * (cond_len - 1))
    Xsec_df['Geom3'] = Geom3

    Geom4 = [0]
    Geom4.extend([0] * (cond_len - 1))
    Xsec_df['Geom4'] = Geom4

    Barrels = [1]
    Barrels.extend([1] * (cond_len - 1))
    Xsec_df['Barrels'] = Barrels

    Culvert = [' ']
    Culvert.extend([' '] * (cond_len - 1))
    Xsec_df['Culvert'] = Culvert

    Xsec_df

    """[TIMESERIES]"""

    """[REPORT]"""

    """[TAGS]"""

    """[MAP]"""

    """[COORDINATES]"""

    COORDINATES_df = coordinate
    COORDINATES_df

    """[VERTICES]"""

    """[Polygons]"""

    Polygons_df = polygons
    Polygons_df

    """[SYMBOLS]"""

    """#What i have upto this point is
    1.[Polygons]
    2.[COORDINATES]
    3.[CONDUITS]
    4.[SUBCATCHMENTS]
    """
    load_text_dir = file[3]
    save_dir = file[4]

    with open(load_text_dir) as f:
        first_lines = f.readlines()

    first_lines[1]

    for i in range(len(first_lines)):
        if first_lines[i].startswith('[TITLE]'):
            with open(save_dir, 'w', encoding='utf-8') as output_file:
                for j in range(4):
                    output_file.write(first_lines[i + j])
                    # output_file.write('\n')

        elif first_lines[i].startswith('[OPTIONS]'):
            with open(save_dir, 'a', encoding='utf-8') as output_file:
                for j in range(38):
                    output_file.write(first_lines[i + j])
                    # output_file.write('\n')

    for i in range(len(first_lines)):
        if first_lines[i].startswith('[TITLE]'):
            with open(save_dir, 'w', encoding='utf-8') as output_file:
                for j in range(4):
                    output_file.write(first_lines[i + j])



        elif first_lines[i].startswith('[OPTIONS]'):
            with open(save_dir, 'a', encoding='utf-8') as output_file:
                for j in range(38):
                    output_file.write(first_lines[i + j])


        elif first_lines[i].startswith('[EVAPORATION]'):

            # print(first_lines[i+1])
            # print(first_lines[i+2])

            s = first_lines[i + 1]
            headers = [x for x in re.split("\s{2,}", s) if x]
            headers[-1] = headers[-1].rstrip('\n')
            delim = first_lines[i + 2].split()

            # print(headers)
            # print(len(delim))

            df = pd.DataFrame([delim], columns=headers)
            df = df.append(evapo_df)
            example_string = df.to_string(justify='right', index=False).split('\n')
            with open(save_dir, 'a', encoding='utf-8') as output_file:
                output_file.write(first_lines[i])
                output_file.write('\n')
                for i in range(len(example_string)):
                    output_file.write(example_string[i].lstrip(' '))
                    output_file.write('\n')
                output_file.close()


        elif first_lines[i].startswith('[RAINGAGES]'):

            # print(first_lines[i+1])
            # print(first_lines[i+2])

            s = first_lines[i + 1]
            headers = [x for x in re.split("\s{1,}", s) if x]
            delim = first_lines[i + 2].split()

            # print(len(headers))
            # print(len(delim))

            df = pd.DataFrame([delim], columns=headers)
            example_string = df.to_string(justify='right', index=False).split('\n')
            with open(save_dir, 'a', encoding='utf-8') as output_file:
                output_file.write(first_lines[i])
                output_file.write('\n')
                for i in range(len(example_string)):
                    output_file.write(example_string[i].lstrip(' '))
                    output_file.write('\n')
                output_file.close()

        elif first_lines[i].startswith('[SUBCATCHMENTS]'):

            # print(first_lines[i+1])
            # print(first_lines[i+2])

            s = first_lines[i + 1]
            headers = [x for x in re.split("\s{2,}", s) if x]
            delim = first_lines[i + 2].split()

            # print(len(headers))
            # print(len(delim))

            df = pd.DataFrame([delim], columns=headers)
            df = df.append(SUBCATCHMENTS_df)
            example_string = df.to_string(justify='right', index=False).split('\n')
            with open(save_dir, 'a', encoding='utf-8') as output_file:
                output_file.write(first_lines[i])
                output_file.write('\n')
                for i in range(len(example_string)):
                    output_file.write(example_string[i].lstrip(' '))
                    output_file.write('\n')
                output_file.close()

        elif first_lines[i].startswith('[SUBAREAS]'):

            # print(first_lines[i+1])
            # print(first_lines[i+2])

            s = first_lines[i + 1]
            headers = [x for x in re.split("\s{2,}", s) if x]
            delim = first_lines[i + 2].split()

            # print(len(headers))
            # print(len(delim))

            df = pd.DataFrame([delim], columns=headers)
            df = df.append(Subareas_df)
            example_string = df.to_string(justify='right', index=False).split('\n')
            with open(save_dir, 'a', encoding='utf-8') as output_file:
                output_file.write(first_lines[i])
                output_file.write('\n')
                for i in range(len(example_string)):
                    output_file.write(example_string[i].lstrip(' '))
                    output_file.write('\n')
                output_file.close()

        elif first_lines[i].startswith('[INFILTRATION]'):

            # print(first_lines[i+1])
            # print(first_lines[i+2])

            s = first_lines[i + 1]
            headers = [x for x in re.split("\s{2,}", s) if x]
            delim = first_lines[i + 2].split()

            # print(len(headers))
            # print(len(delim))

            df = pd.DataFrame([delim], columns=headers)
            df = df.append(Infiltration_df)
            example_string = df.to_string(justify='right', index=False).split('\n')
            with open(save_dir, 'a', encoding='utf-8') as output_file:
                output_file.write(first_lines[i])
                output_file.write('\n')
                for i in range(len(example_string)):
                    output_file.write(example_string[i].lstrip(' '))
                    output_file.write('\n')
                output_file.close()

        elif first_lines[i].startswith('[JUNCTIONS]'):

            # print(first_lines[i+1])
            # print(first_lines[i+2])

            s = first_lines[i + 1]
            headers = [x for x in re.split("\s{2,}", s) if x]
            delim = first_lines[i + 2].split()

            # print(len(headers))
            # print(len(delim))

            df = pd.DataFrame([delim], columns=headers)
            df = df.append(junction_df)
            example_string = df.to_string(justify='right', index=False).split('\n')
            with open(save_dir, 'a', encoding='utf-8') as output_file:
                output_file.write(first_lines[i])
                output_file.write('\n')
                for i in range(len(example_string)):
                    output_file.write(example_string[i].lstrip(' '))
                    output_file.write('\n')
                output_file.close()

        elif first_lines[i].startswith('[OUTFALLS]'):

            # print(first_lines[i+1])
            # print(first_lines[i+2])

            s = first_lines[i + 1]
            headers = [x for x in re.split("\s{2,}", s) if x]
            delim = first_lines[i + 2].split()

            # print(len(headers))
            # print(len(delim))

            df = pd.DataFrame([delim], columns=headers)
            df = df.append(outfall_df)
            example_string = df.to_string(justify='right', index=False).split('\n')
            with open(save_dir, 'a', encoding='utf-8') as output_file:
                output_file.write(first_lines[i])
                output_file.write('\n')
                for i in range(len(example_string)):
                    output_file.write(example_string[i].lstrip(' '))
                    output_file.write('\n')
                output_file.close()

        elif first_lines[i].startswith('[CONDUITS]'):

            # print(first_lines[i+1])
            # print(first_lines[i+2])

            s = first_lines[i + 1]
            headers = [x for x in re.split("\s{2,}", s) if x]
            delim = first_lines[i + 2].split()

            # print(len(headers))
            # print(len(delim))

            df = pd.DataFrame([delim], columns=headers)
            df = df.append(CONDUITS_df)

            example_string = df.to_string(justify='right', index=False).split('\n')
            with open(save_dir, 'a', encoding='utf-8') as output_file:
                output_file.write(first_lines[i])
                output_file.write('\n')
                for i in range(len(example_string)):
                    output_file.write(example_string[i].lstrip(' '))
                    output_file.write('\n')
                output_file.close()

        elif first_lines[i].startswith('[XSECTIONS]'):

            # print(first_lines[i+1])
            # print(first_lines[i+2])

            s = first_lines[i + 1]
            headers = [x for x in re.split("\s{2,}", s) if x]
            delim = first_lines[i + 2].split()

            # print(len(headers))
            # print(len(delim))

            df = pd.DataFrame([delim], columns=headers)
            df = df.append(Xsec_df)
            example_string = df.to_string(justify='right', index=False).split('\n')
            with open(save_dir, 'a', encoding='utf-8') as output_file:
                output_file.write(first_lines[i])
                output_file.write('\n')
                for i in range(len(example_string)):
                    output_file.write(example_string[i].lstrip(' '))
                    output_file.write('\n')
                output_file.close()

        elif first_lines[i].startswith('[TIMESERIES]'):

            # print(first_lines[i+1])
            # print(first_lines[i+2])

            s = first_lines[i + 1]
            headers = [x for x in re.split("\s{2,}", s) if x]
            delim = first_lines[i + 2].split()

            # print(len(headers))
            # print(len(delim))

            df = pd.DataFrame([delim], columns=headers)
            example_string = df.to_string(justify='right', index=False).split('\n')
            with open(save_dir, 'a', encoding='utf-8') as output_file:
                output_file.write(first_lines[i])
                output_file.write('\n')
                for i in range(len(example_string)):
                    output_file.write(example_string[i].lstrip(' '))
                    output_file.write('\n')
                output_file.close()

        elif first_lines[i].startswith('[REPORT]'):

            with open(save_dir, 'a', encoding='utf-8') as output_file:
                for j in range(7):
                    output_file.write(first_lines[i + j])

        elif first_lines[i].startswith('[TAGS]'):

            pass

        elif first_lines[i].startswith('[MAP]'):

            pass

        elif first_lines[i].startswith('[COORDINATES]'):

            # print(first_lines[i+1])
            # print(first_lines[i+2])

            s = first_lines[i + 1]
            headers = [x for x in re.split("\s{2,}", s) if x]
            delim = first_lines[i + 2].split()

            # print(len(headers))
            # print(len(delim))

            df = pd.DataFrame([delim], columns=headers)
            df = df.append(coordinate)
            with open(save_dir, 'a', encoding='utf-8') as output_file:
                output_file.write(first_lines[i])
                output_file.write('\n')
                output_file.write('{0:<17} {1:<19} {2:<17}'.format(headers[0], headers[1], headers[2]))
                output_file.write('\n')
                for num, row in df.iterrows():
                    output_file.write('{0:<17} {1:<19} {2:<17}'.format(row[0], row[1], row[2]))
                    output_file.write('\n')
                output_file.close()

        elif first_lines[i].startswith('[VERTICES]'):

            # print(first_lines[i+1])
            # print(first_lines[i+2])

            s = first_lines[i + 1]
            headers = [x for x in re.split("\s{2,}", s) if x]
            delim = first_lines[i + 2].split()

            # print(len(headers))
            # print(len(delim))

            df = pd.DataFrame([delim], columns=headers)
            example_string = df.to_string(justify='right', index=False).split('\n')
            with open(save_dir, 'a', encoding='utf-8') as output_file:
                output_file.write(first_lines[i])
                output_file.write('\n')
                for i in range(len(example_string)):
                    output_file.write(example_string[i].lstrip(' '))
                    output_file.write('\n')
                output_file.close()

        elif first_lines[i].startswith('[Polygons]'):

            # print(first_lines[i+1])
            # print(first_lines[i+2])

            s = first_lines[i + 1]
            headers = [x for x in re.split("\s{2,}", s) if x]
            delim = first_lines[i + 2].split()

            # print(len(headers))
            # print(len(delim))

            df = pd.DataFrame([delim], columns=headers)
            df = df.append(Polygons_df)

            with open(save_dir, 'a', encoding='utf-8') as output_file:
                output_file.write(first_lines[i])
                output_file.write('\n')
                output_file.write('{0:<17} {1:<19} {2:<17}'.format(headers[0], headers[1], headers[2]))
                output_file.write('\n')
                for num, row in df.iterrows():
                    output_file.write('{0:<17} {1:<19} {2:<17}'.format(row[0], row[1], row[2]))
                    output_file.write('\n')
                output_file.close()



        elif first_lines[i].startswith('[SYMBOLS]'):

            # print(first_lines[i+1])
            # print(first_lines[i+2])

            s = first_lines[i + 1]
            headers = [x for x in re.split("\s{2,}", s) if x]
            delim = first_lines[i + 2].split()

            # print(len(headers))
            # print(len(delim))

            df = pd.DataFrame([delim], columns=headers)
            example_string = df.to_string(justify='right', index=False).split('\n')
            with open(save_dir, 'a', encoding='utf-8') as output_file:
                output_file.write(first_lines[i])
                output_file.write('\n')
                for i in range(len(example_string)):
                    output_file.write(example_string[i].lstrip(' '))
                    output_file.write('\n')
                output_file.close()



b6 = Button(root, text="Save Text File", font=('Helvetica',8), command=Save_file,
                             width = 80)
b6.grid(row=12,ipadx=15, ipady=10, padx=15, pady=10)

root.mainloop()